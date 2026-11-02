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
"""Parse a document with a fresh ANTLR lexer/parser pair and collect syntax diagnostics."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Type

from antlr4 import CommonTokenStream, InputStream, Lexer, Parser, Token
from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.error.ErrorStrategy import ErrorStrategy
from lsprotocol.types import Diagnostic, DiagnosticSeverity

from .diagnostic_listener import DiagnosticListener, token_range
from .error_strategy import InputMismatchErrorStrategy


@dataclass
class ParseResult:
    """Everything produced by parsing one document."""
    source: str
    lexer: Lexer
    tokens: CommonTokenStream
    parser: Parser
    tree: Optional[ParserRuleContext]
    diagnostics: List[Diagnostic] = field(default_factory=list)

    @property
    def has_errors(self) -> bool:
        return any(d.severity in (None, DiagnosticSeverity.Error) for d in self.diagnostics)


def parse_source(
        source: str,
        lexer_class: Type[Lexer],
        parser_class: Type[Parser],
        start_rule: str,
        error_strategy_factory: Optional[Callable[[], ErrorStrategy]] = InputMismatchErrorStrategy,
        diagnostic_source: Optional[str] = None,
        require_eof: bool = True,
) -> ParseResult:
    """Parse ``source`` starting with ``start_rule`` using a fresh lexer and parser.

    A fresh lexer/parser pair is used for every call, so concurrent LSP requests never share parser state.

    :param require_eof: report input that was not consumed by the start rule. Most grammars do not end their start rule
        with ``EOF``; without this check trailing garbage would be silently ignored.
    """
    listener = DiagnosticListener(diagnostic_source)

    lexer = lexer_class(InputStream(source))
    lexer.removeErrorListeners()
    lexer.addErrorListener(listener)

    tokens = CommonTokenStream(lexer)
    parser = parser_class(tokens)
    parser.removeErrorListeners()
    parser.addErrorListener(listener)
    if error_strategy_factory is not None:
        parser._errHandler = error_strategy_factory()

    tree: Optional[ParserRuleContext] = getattr(parser, start_rule)()
    tokens.fill()

    diagnostics = list(listener.diagnostics)
    if require_eof:
        next_token: Token = tokens.LT(1)
        if next_token is not None and next_token.type != Token.EOF and not diagnostics:
            diagnostics.append(
                Diagnostic(
                    range=token_range(next_token, next_token.line, next_token.column),
                    message=f"unexpected input '{next_token.text}': the parser stopped before the end of the file",
                    severity=DiagnosticSeverity.Error,
                    source=diagnostic_source,
                )
            )

    return ParseResult(source, lexer, tokens, parser, tree, diagnostics)
