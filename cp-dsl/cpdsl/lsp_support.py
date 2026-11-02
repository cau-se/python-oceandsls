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
"""Helpers shared by the CP-DSL language servers (declaration and configuration).

The servers reuse the generator's visitors to build the :class:`~cpdsl.model.declaration_model.DeclarationModel`,
so editors report the same problems as the generator.
"""

from __future__ import annotations

import logging
from typing import Iterable, List, Optional, Tuple

from antlr4 import ParserRuleContext
from lsprotocol.types import (
    CompletionItem, CompletionItemKind, Diagnostic, DiagnosticSeverity, MarkupContent, MarkupKind, Position, Range,
)

from cpdsl.common.configuration import CompileFlags
from cpdsl.common.logger import GeneratorLogger
from cpdsl.model.declaration_model import DeclarationModel, Feature, Parameter, ParameterGroup
from cpdsl.model.type_system import base_type_names

logger = logging.getLogger(__name__)


def context_range(ctx: Optional[ParserRuleContext]) -> Range:
    """LSP range covering a parser rule context (first line only for multi-line contexts)."""
    if ctx is None or getattr(ctx, "start", None) is None:
        return Range(start=Position(line=0, character=0), end=Position(line=0, character=1))
    start, stop = ctx.start, ctx.stop if getattr(ctx, "stop", None) is not None else ctx.start
    begin = Position(line=start.line - 1, character=start.column)
    if stop.line == start.line and stop.tokenIndex >= start.tokenIndex:
        end = Position(line=stop.line - 1, character=stop.column + len(stop.text or " "))
    else:
        end = Position(line=start.line - 1, character=start.column + len(start.text or " "))
    return Range(start=begin, end=end)


def messages_to_diagnostics(messages: Iterable[Tuple[str, object, str]], source: str) -> List[Diagnostic]:
    """Convert :attr:`GeneratorLogger.messages` into LSP diagnostics."""
    diagnostics = []
    for severity, ctx, message in messages:
        diagnostics.append(Diagnostic(
            range=context_range(ctx if isinstance(ctx, ParserRuleContext) else None), message=message, source=source,
            severity=DiagnosticSeverity.Error if severity == "error" else DiagnosticSeverity.Warning,
        ))
    return diagnostics


def new_logger() -> GeneratorLogger:
    """A generator logger collecting all problems as errors (nothing is printed to stdout)."""
    return GeneratorLogger(CompileFlags.STRICT)


def build_declaration_model(tree, model_logger: GeneratorLogger) -> DeclarationModel:
    """Build a declaration model from a parse tree. Partial models are returned if the visitor fails."""
    from cpdsl.generator.visitors.declaration_visitor import GeneratorDeclarationVisitor
    model = DeclarationModel()
    if tree is not None:
        try:
            GeneratorDeclarationVisitor(model, model_logger).visit(tree)
        except Exception as e:  # keep what has been collected so far, but make the failure visible
            logger.debug("Building the declaration model failed", exc_info=True)
            model_logger.messages.append(
                ("error", tree, f"internal error while analysing the declaration model: {type(e).__name__}: {e}"))
    return model


# ---------------------------------------------------------------------------------------------------------------------
# Completion items
# ---------------------------------------------------------------------------------------------------------------------

def _doc(text: Optional[str]) -> Optional[MarkupContent]:
    text = (text or "").strip('"\'')
    return MarkupContent(kind=MarkupKind.PlainText, value=text) if text else None


def sub_features(feature: Feature) -> List[Feature]:
    return [f for feature_set in feature.feature_sets for f in feature_set.features.values()]


def feature_items(features: Iterable[Feature], qualified: bool = False, prefix: str = "") -> List[CompletionItem]:
    """Completion items for features; with ``qualified`` sub-features are offered as ``parent.child``."""
    items = []
    for feature in features:
        name = f"{prefix}{feature.name}"
        items.append(CompletionItem(label=name, kind=CompletionItemKind.Module, documentation=_doc(feature.description),
                                    detail="required feature" if feature.required else "feature"))
        if qualified:
            items.extend(feature_items(sub_features(feature), True, f"{name}."))
    return items


def group_items(groups: Iterable[ParameterGroup]) -> List[CompletionItem]:
    return [CompletionItem(label=g.name, kind=CompletionItemKind.Struct, detail="parameter group",
                           documentation=_doc(g.description)) for g in groups]


def parameter_items(parameters: Iterable[Parameter], prefix: str = "") -> List[CompletionItem]:
    items = []
    for p in parameters:
        type_name = getattr(p.type, "name", None)
        items.append(CompletionItem(label=f"{prefix}{p.name}", kind=CompletionItemKind.Field,
                                    detail=f"parameter: {type_name}" if type_name else "parameter",
                                    documentation=_doc(p.description)))
    return items


def type_items(model: DeclarationModel) -> List[CompletionItem]:
    items = [CompletionItem(label=name, kind=CompletionItemKind.TypeParameter, detail="base type")
             for name in base_type_names]
    items.extend(CompletionItem(label=name, kind=CompletionItemKind.Enum if hasattr(t, "enumerals") else
                                CompletionItemKind.TypeParameter, detail="declared type")
                 for name, t in model.types.items())
    return items


def enumeral_items(model: DeclarationModel) -> List[CompletionItem]:
    items = []
    for type_name, t in model.types.items():
        for name in (getattr(t, "enumerals", None) or {}):
            items.append(CompletionItem(label=str(name), kind=CompletionItemKind.EnumMember, detail=type_name))
    return items


def all_groups(model: DeclarationModel) -> List[Tuple[str, ParameterGroup]]:
    """All parameter groups with qualified names (feature groups as 'feature.group' is not supported by the DSL,
    therefore only their plain names are returned)."""
    groups = [(name, g) for name, g in model.groups.items()]

    def walk(feature: Feature):
        for name, g in feature.groups.items():
            groups.append((name, g))
        for sub in sub_features(feature):
            walk(sub)
    for f in model.features.values():
        walk(f)
    return groups
