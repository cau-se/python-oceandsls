#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
"""Language server for CP-DSL declaration models (``*.decl``).

Declaration models declare the features, parameter groups, parameters and types of one ocean model
(Jung et al., "Domain-specific languages for ocean modeling", Section 5). The server reports syntax errors and the
problems found by the generator's declaration visitor (unknown types and features, redefinitions, ...), completes
keywords, feature references (``requires``/``excludes``), types and value references, and provides an outline.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from antlr4 import FileStream
from lsprotocol.types import (
    CompletionItem, Diagnostic, DidSaveTextDocumentParams, DocumentSymbol, DocumentSymbolParams, Position, Range,
    SymbolKind, TEXT_DOCUMENT_DOCUMENT_SYMBOL,
)

from cpdsl.model.declaration_model import DeclarationModel
from cpdsl.lsp_support import (
    all_groups, build_declaration_model, enumeral_items, feature_items, messages_to_diagnostics,
    new_logger, parameter_items, type_items,
)
from odsllib.code_completion_core import CandidatesCollection
from odsllib.lsp.compute_token_index import TokenPosition
from odsllib.lsp.parsing import ParseResult
from odsllib.lsp.server import AntlrLanguageServer

from .gen.python.Declaration.DeclarationLexer import DeclarationLexer
from .gen.python.Declaration.DeclarationParser import DeclarationParser

logger = logging.getLogger(__name__)


class dclLSPServer(AntlrLanguageServer):
    CONFIGURATION_SECTION = 'ODslDCLServer'

    lexer_class = DeclarationLexer
    parser_class = DeclarationParser
    start_rule = "declarationModel"
    preferred_rules = {DeclarationParser.RULE_featureReference, DeclarationParser.RULE_typeReference,
                       DeclarationParser.RULE_namedElementReference}
    word_token_types = {DeclarationParser.ID}
    trigger_characters = [",", "."]
    number_tokens = {"ELONG", "EDOUBLE", "INT"}

    def __init__(self, *args):
        super().__init__(*args)
        self.input_path: Optional[str] = None
        # Model of the last version of each document without syntax errors; used for completion while typing
        self.last_valid_models: Dict[str, DeclarationModel] = {}
        self.feature(TEXT_DOCUMENT_DOCUMENT_SYMBOL)(lambda params: self.document_symbols(params))

    # Diagnostics -------------------------------------------------------------------------------------------------

    def semantic_diagnostics(self, result: ParseResult, uri: str) -> List[Diagnostic]:
        if result.has_errors:
            return []  # semantic checks on incomplete parse trees would only produce follow-up errors
        model_logger = new_logger()
        self.last_valid_models[uri] = build_declaration_model(result.tree, model_logger)
        return messages_to_diagnostics(model_logger.messages, self.diagnostic_source)

    # Completion ---------------------------------------------------------------------------------------------------

    def symbol_completions(
            self, result: ParseResult, position: TokenPosition, candidates: CandidatesCollection, uri: str
    ) -> List[CompletionItem]:
        if result.has_errors and uri in self.last_valid_models:
            # While typing the document is usually incomplete; the last valid version knows all declarations
            model = self.last_valid_models[uri]
        else:
            model = build_declaration_model(result.tree, new_logger())
        items: List[CompletionItem] = []
        rules = candidates.rules
        if DeclarationParser.RULE_featureReference in rules:
            items.extend(feature_items(model.features.values(), qualified=True))
        if DeclarationParser.RULE_typeReference in rules:
            items.extend(type_items(model))
        if DeclarationParser.RULE_namedElementReference in rules:
            group = self._enclosing_group(position.context, model)
            if group is not None:
                items.extend(parameter_items(group.parameters.values()))
            for name, g in all_groups(model):
                items.extend(parameter_items(g.parameters.values(), prefix=f"{name}."))
            items.extend(enumeral_items(model))
        return items

    @staticmethod
    def _enclosing_group(ctx, model):
        while ctx is not None and not isinstance(ctx, DeclarationParser.ParameterGroupDeclarationContext):
            ctx = ctx.parentCtx
        if ctx is None or getattr(ctx, "name", None) is None:
            return None
        return dict(all_groups(model)).get(ctx.name.text)

    # Outline ------------------------------------------------------------------------------------------------------

    def document_symbols(self, params: DocumentSymbolParams) -> List[DocumentSymbol]:
        result = self.parse(self.workspace.get_text_document(params.text_document.uri).source)
        return declaration_outline(result.tree)

    def document_saved(self, uri: str, result: ParseResult) -> None:
        """Declaration models are used by the configuration generator; nothing is generated on save."""


def _symbol(name_token, ctx, kind: SymbolKind, detail: Optional[str] = None, children=None) -> Optional[DocumentSymbol]:
    if name_token is None or ctx is None or ctx.start is None:
        return None
    stop = ctx.stop if ctx.stop is not None else ctx.start
    full = Range(start=Position(line=ctx.start.line - 1, character=ctx.start.column),
                 end=Position(line=stop.line - 1, character=stop.column + len(stop.text or " ")))
    name = Range(start=Position(line=name_token.line - 1, character=name_token.column),
                 end=Position(line=name_token.line - 1, character=name_token.column + len(name_token.text)))
    return DocumentSymbol(name=name_token.text, kind=kind, range=full, selection_range=name, detail=detail,
                          children=[c for c in (children or []) if c is not None])


def _group_symbol(ctx) -> Optional[DocumentSymbol]:
    parameters = [_symbol(p.name, p, SymbolKind.Field) for p in getattr(ctx, "parameterDeclarations", [])]
    return _symbol(getattr(ctx, "name", None), ctx, SymbolKind.Struct, "group", parameters)


def _feature_symbol(ctx) -> Optional[DocumentSymbol]:
    children = [_group_symbol(g) for g in getattr(ctx, "parameterGroupDeclarations", [])]
    for feature_group in getattr(ctx, "featureGroupDeclarations", []):
        children.extend(_feature_symbol(f) for f in getattr(feature_group, "featureDeclarations", []))
    return _symbol(getattr(ctx, "name", None), ctx, SymbolKind.Module, "feature", children)


def declaration_outline(tree) -> List[DocumentSymbol]:
    """Hierarchical document symbols: types, parameter groups with parameters and features."""
    if tree is None:
        return []
    symbols = []
    for declared in tree.types:
        inner = declared.getChild(0)
        symbols.append(_symbol(getattr(inner, "name", None), inner, SymbolKind.Enum
                               if isinstance(inner, DeclarationParser.EnumerationTypeContext) else SymbolKind.Class,
                               "type"))
    symbols.extend(_group_symbol(g) for g in tree.parameterGroupDeclarations)
    symbols.extend(_feature_symbol(f) for f in tree.featureDeclarations)
    return [s for s in symbols if s is not None]


dcl_server = dclLSPServer('pygls-odsl-dcl-prototype', 'v0.4')


def did_save(server: dclLSPServer, params: Optional[DidSaveTextDocumentParams]):
    """Handle a saved document (LSP) or check ``server.input_path`` (CLI, ``params`` is None)."""
    if params is not None:
        server.on_did_save(params)
        return
    source = str(FileStream(server.input_path, encoding="utf-8"))
    for diagnostic in server.validate(server.input_path, source):
        logger.error("%s:%d:%d: %s", server.input_path, diagnostic.range.start.line + 1,
                     diagnostic.range.start.character + 1, diagnostic.message)
