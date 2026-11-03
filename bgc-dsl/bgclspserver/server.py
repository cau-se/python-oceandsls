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
"""Language server of the BGC-DSL (biogeochemical models).

Provides syntax diagnostics, content assist (keywords and declared substances, parameters, diagnostics,
compartments and connections) and semantic highlighting via :class:`odsllib.lsp.server.AntlrLanguageServer`.
"""

from __future__ import annotations

import logging
from typing import List, Optional

from antlr4 import FileStream
from lsprotocol.types import CompletionItem, CompletionItemKind, DidSaveTextDocumentParams

from odsllib.code_completion_core import CandidatesCollection
from odsllib.lsp.compute_token_index import TokenPosition
from odsllib.lsp.parsing import ParseResult
from odsllib.lsp.server import AntlrLanguageServer

from .cst.symbol_table_visitor import SymbolTableVisitor
from .gen.python.BgcDsl.BgcDslLexer import BgcDslLexer
from .gen.python.BgcDsl.BgcDslParser import BgcDslParser
from odsllib.symbol_table import VariableSymbol
from odsllib.lsp.symbols import suggest_symbols

logger = logging.getLogger(__name__)


class bgcLSPServer(AntlrLanguageServer):
    CONFIGURATION_SECTION = 'ODslBGCServer'

    lexer_class = BgcDslLexer
    parser_class = BgcDslParser
    start_rule = "bgcModel"
    # References to declared elements in expressions
    preferred_rules = {BgcDslParser.RULE_qualifiedName}
    word_token_types = {BgcDslParser.ID}
    trigger_characters = [","]

    def __init__(self, *args):
        super().__init__(*args)
        self.input_path: Optional[str] = None
        self.parse_tree: Optional[BgcDslParser.BgcModelContext] = None

    def symbol_completions(
            self, result: ParseResult, position: TokenPosition, candidates: CandidatesCollection, uri: str
    ) -> List[CompletionItem]:
        if BgcDslParser.RULE_qualifiedName not in candidates.rules or result.tree is None:
            return []
        symbol_table = SymbolTableVisitor('completions').visit(result.tree)
        names = suggest_symbols(symbol_table, position, VariableSymbol)
        # Connections are registered as "<name> from <source> to <target>" and cannot be referenced by that label
        return [CompletionItem(label=name, kind=CompletionItemKind.Variable) for name in names if " " not in name]

    def document_saved(self, uri: str, result: ParseResult) -> None:
        self.parse_tree = result.tree
        # TODO code generator for BGC models


bgc_server = bgcLSPServer('pygls-odsl-bgc-prototype', 'v0.4')


def did_save(server: bgcLSPServer, params: Optional[DidSaveTextDocumentParams]):
    """Handle a saved document (LSP) or check ``server.input_path`` (CLI, ``params`` is None)."""
    if params is not None:
        server.on_did_save(params)
        return
    result = server.parse(str(FileStream(server.input_path, encoding="utf-8")))
    for diagnostic in result.diagnostics:
        logger.error("%s:%d:%d: %s", server.input_path, diagnostic.range.start.line + 1,
                     diagnostic.range.start.character + 1, diagnostic.message)
    server.parse_tree = result.tree
