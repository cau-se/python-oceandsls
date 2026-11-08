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
"""Language server for CP-DSL configurations (``*.oconf``).

A configuration refers to the declaration model of an ocean model (``configuration <name> : <model>``), which is read
from ``<model>.decl`` next to the configuration (an open, unsaved editor buffer of that file takes precedence). The
server reports syntax errors, references to undeclared features, parameter groups and parameters (using the
generator's configuration visitor), violated feature dependencies (``requires``/``excludes``), and required features
that are not activated (Jung et al., "Domain-specific languages for ocean modeling", Sections 5.1-5.3). Content assist
offers keywords and the declared features, groups and parameters with their descriptions.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional, Tuple

from antlr4 import FileStream
from lsprotocol.types import CompletionItem, Diagnostic, DiagnosticSeverity, DidSaveTextDocumentParams
from pygls.uris import from_fs_path, to_fs_path

from cpdsl.lsp_support import (
    all_groups, build_declaration_model, context_range, enumeral_items, feature_items, group_items,
    messages_to_diagnostics, new_logger, parameter_items, sub_features,
)
from cpdsl.model.declaration_model import DeclarationModel, Feature
from odsllib.code_completion_core import CandidatesCollection
from odsllib.lsp.compute_token_index import TokenPosition
from odsllib.lsp.diagnostic_listener import token_range
from odsllib.lsp.parsing import ParseResult, parse_source
from odsllib.lsp.server import AntlrLanguageServer
from dcllspserver.gen.python.Declaration.DeclarationLexer import DeclarationLexer
from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from .gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from .gen.python.Configuration.ConfigurationParser import ConfigurationParser

logger = logging.getLogger(__name__)

DECLARATION_SUFFIX = ".decl"


class confLSPServer(AntlrLanguageServer):
    CONFIGURATION_SECTION = 'ODslCONFServer'

    lexer_class = ConfigurationLexer
    parser_class = ConfigurationParser
    start_rule = "configurationModel"
    preferred_rules = {ConfigurationParser.RULE_featureActivation, ConfigurationParser.RULE_qualifiedName,
                       ConfigurationParser.RULE_namedElementReference}
    word_token_types = {ConfigurationParser.ID}
    trigger_characters = [",", "."]
    number_tokens = {"ELONG", "EDOUBLE", "INT"}

    def __init__(self, *args):
        super().__init__(*args)
        self.input_path: Optional[str] = None
        #: Syntax and semantic problems of the declaration model loaded last
        self.declaration_problems: List[Diagnostic] = []

    # Declaration model ----------------------------------------------------------------------------------------------

    def declaration_path(self, uri: str, tree) -> Optional[str]:
        if tree is None or tree.declarationModel is None:
            return None
        path = to_fs_path(uri) if uri.startswith("file:") else uri
        return os.path.join(os.path.dirname(path), tree.declarationModel.text + DECLARATION_SUFFIX)

    def load_declaration_model(self, uri: str, tree) -> Tuple[Optional[DeclarationModel], Optional[str]]:
        """Return the declaration model referenced by a configuration and the path it was expected at."""
        path = self.declaration_path(uri, tree)
        if path is None:
            return None, None
        source = None
        try:  # prefer an open (possibly unsaved) editor buffer
            document = self.workspace.text_documents.get(from_fs_path(path))
            source = document.source if document is not None else None
        except RuntimeError:  # workspace not initialized (CLI)
            pass
        if source is None:
            if not os.path.isfile(path):
                return None, path
            with open(path, encoding="utf-8") as f:
                source = f.read()
        result = parse_source(source, DeclarationLexer, DeclarationParser, "declarationModel")
        model_logger = new_logger()
        model = build_declaration_model(result.tree, model_logger)
        self.declaration_problems = list(result.diagnostics) + messages_to_diagnostics(
            model_logger.messages, self.diagnostic_source)
        return model, path

    # Diagnostics -------------------------------------------------------------------------------------------------

    def semantic_diagnostics(self, result: ParseResult, uri: str) -> List[Diagnostic]:
        tree = result.tree
        if result.has_errors or tree is None:
            return []
        model, path = self.load_declaration_model(uri, tree)
        if model is None:
            if path is None:
                return []
            token = tree.declarationModel
            return [Diagnostic(range=token_range(token, token.line, token.column), severity=DiagnosticSeverity.Error,
                               source=self.diagnostic_source,
                               message=f"declaration model '{token.text}' not found: expected {os.path.basename(path)} "
                                       f"next to this configuration")]

        from cpdsl.generator.visitors.configuration_visitor import GeneratorConfigurationVisitor
        from cpdsl.generator.calculator.unit_calculator import UnitCalculator
        diagnostics: List[Diagnostic] = []
        if self.declaration_problems:
            token = tree.declarationModel
            diagnostics.append(Diagnostic(
                range=token_range(token, token.line, token.column), severity=DiagnosticSeverity.Warning,
                source=self.diagnostic_source,
                message=f"declaration model {os.path.basename(path)} has {len(self.declaration_problems)} problem(s), "
                        f"e.g. line {self.declaration_problems[0].range.start.line + 1}: "
                        f"{self.declaration_problems[0].message}"))
        model_logger = new_logger()
        try:
            GeneratorConfigurationVisitor(model, model_logger).visit(tree)
            # configured values must be given in units compatible with the declared units
            UnitCalculator(model_logger).check_model(model)
        except Exception:
            logger.exception("Configuration visitor failed for %s", uri)
        diagnostics.extend(messages_to_diagnostics(model_logger.messages, self.diagnostic_source))
        diagnostics.extend(self.feature_dependency_diagnostics(tree, model))
        return diagnostics

    def feature_dependency_diagnostics(self, tree, model: DeclarationModel) -> List[Diagnostic]:
        """Check requires/excludes of activated features and required features (paper, Section 5.2)."""
        locations: Dict[str, object] = {}
        self._collect_activation_locations(tree, locations)
        diagnostics: List[Diagnostic] = []

        def report(feature_name: str, message: str, severity=DiagnosticSeverity.Error):
            ctx = locations.get(feature_name)
            rng = context_range(ctx) if ctx is not None else token_range(tree.name, tree.name.line, tree.name.column)
            diagnostics.append(Diagnostic(range=rng, message=message, severity=severity,
                                          source=self.diagnostic_source))

        def check(features: List[Feature], parent_activated: bool):
            for feature in features:
                if feature.is_activated:
                    for required in feature.requires:
                        if not required.is_activated:
                            report(feature.name, f"feature {feature.name} requires {required.name}, which is not "
                                                 f"activated")
                    for excluded in feature.excludes:
                        if excluded.is_activated:
                            report(feature.name, f"feature {feature.name} excludes {excluded.name}, which is "
                                                 f"activated")
                elif feature.required and parent_activated:
                    report(feature.name, f"required feature {feature.name} is not activated",
                           DiagnosticSeverity.Warning)
                check(sub_features(feature), feature.is_activated)

        check(list(model.features.values()), True)
        return diagnostics

    def _collect_activation_locations(self, ctx, locations: Dict[str, object]) -> None:
        for activation in getattr(ctx, "featureActivations", []):
            if activation.declaration is not None:
                locations.setdefault(activation.declaration.text, activation)
        for configuration in getattr(ctx, "featureConfigurations", []):
            if configuration.declaration is not None:
                locations.setdefault(configuration.declaration.text, configuration)
            self._collect_activation_locations(configuration, locations)

    # Completion ---------------------------------------------------------------------------------------------------

    def symbol_completions(
            self, result: ParseResult, position: TokenPosition, candidates: CandidatesCollection, uri: str
    ) -> List[CompletionItem]:
        model, _ = self.load_declaration_model(uri, result.tree)
        if model is None:
            return []
        scope, group = self._scope_at(position.context, model)
        features = list(model.features.values()) if scope is model else sub_features(scope)
        groups = list(model.groups.values()) if scope is model else list(scope.groups.values())

        items: List[CompletionItem] = []
        previous = self._previous_token_text(result, position.index)
        if previous == "feature" or ConfigurationParser.RULE_featureActivation in candidates.rules:
            items.extend(feature_items(features))
        if previous == "group":
            items.extend(group_items(groups))
        if ConfigurationParser.RULE_qualifiedName in candidates.rules and group is not None:
            items.extend(parameter_items(group.parameters.values()))
        if ConfigurationParser.RULE_namedElementReference in candidates.rules:
            if group is not None:
                items.extend(parameter_items(group.parameters.values()))
            for name, g in all_groups(model):
                items.extend(parameter_items(g.parameters.values(), prefix=f"{name}."))
            items.extend(enumeral_items(model))
        return items

    @staticmethod
    def _previous_token_text(result: ParseResult, index: int) -> Optional[str]:
        for token in reversed(result.tokens.tokens[:index]):
            if token.channel == 0:
                return token.text
        return None

    @staticmethod
    def _scope_at(ctx, model: DeclarationModel):
        """Return the feature (or model) and parameter group enclosing a parse tree node."""
        path: List[str] = []
        group_name: Optional[str] = None
        node = ctx
        while node is not None:
            if isinstance(node, ConfigurationParser.FeatureConfigurationContext) and node.declaration is not None:
                path.insert(0, node.declaration.text)
            elif isinstance(node, ConfigurationParser.ParameterGroupContext) and group_name is None \
                    and node.declaration is not None:
                group_name = node.declaration.text
            node = node.parentCtx
        scope = model
        for name in path:
            feature = scope.resolve_feature(name)
            if feature is None:
                break
            scope = feature
        group = scope.resolve_parameter_group(group_name) if group_name else None
        return scope, group

    def document_saved(self, uri: str, result: ParseResult) -> None:
        """Code generation is provided by the generator CLI (python -m cpdsl.generator)."""


conf_server = confLSPServer('pygls-odsl-conf-prototype', 'v0.4')


def did_save(server: confLSPServer, params: Optional[DidSaveTextDocumentParams]):
    """Handle a saved document (LSP) or check ``server.input_path`` (CLI, ``params`` is None)."""
    if params is not None:
        server.on_did_save(params)
        return
    source = str(FileStream(server.input_path, encoding="utf-8"))
    for diagnostic in server.validate(server.input_path, source):
        logger.error("%s:%d:%d: %s", server.input_path, diagnostic.range.start.line + 1,
                     diagnostic.range.start.character + 1, diagnostic.message)
