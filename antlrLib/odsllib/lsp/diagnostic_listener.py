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
"""ANTLR error listener collecting LSP diagnostics."""

from __future__ import annotations

import logging
from typing import List, Optional

from antlr4.Recognizer import Recognizer
from antlr4.Token import Token
from antlr4.error.ErrorListener import ErrorListener
from antlr4.error.Errors import RecognitionException
from lsprotocol.types import Diagnostic, DiagnosticSeverity, Position, Range

logger = logging.getLogger(__name__)


def token_range(token: Optional[Token], line: int, column: int) -> Range:
    """Return the LSP range of a token (or a one character range at ``line``/``column`` if there is no token).

    ``line`` is 1-based as reported by ANTLR, the returned range is 0-based as required by LSP.
    """
    length = 1
    if token is not None and token.type != Token.EOF and token.text:
        # Multi-line tokens are cut at the first line break
        length = max(1, len(token.text.split("\n", 1)[0]))
    start = Position(line=max(line - 1, 0), character=max(column, 0))
    return Range(start=start, end=Position(line=start.line, character=start.character + length))


class DiagnosticListener(ErrorListener):
    """Collects lexer and parser errors as LSP :class:`Diagnostic` objects."""

    # Enables logging of syntax errors
    show_debug_output: bool = False

    def __init__(self, source: Optional[str] = None):
        super().__init__()
        self.source = source
        self.diagnostics: List[Diagnostic] = []
        self._symbol: Optional[str] = None
        self._state: Optional[int] = None

    @property
    def symbol(self) -> Optional[str]:
        """Text of the last offending symbol."""
        return self._symbol

    @property
    def state(self) -> Optional[int]:
        """Parser state of the last reported error."""
        return self._state

    def reset(self):
        """Reset the listener's state."""
        self.diagnostics = []
        self._symbol = None
        self._state = None

    def syntaxError(
            self, recognizer: Recognizer, offendingSymbol: Optional[Token], line: int, column: int, msg: str,
            e: Optional[RecognitionException] = None
    ):
        self._state = recognizer.state if recognizer is not None else None
        self._symbol = offendingSymbol.text if offendingSymbol is not None else None
        self.diagnostics.append(
            Diagnostic(
                range=token_range(offendingSymbol, line, column),
                message=msg,
                severity=DiagnosticSeverity.Error,
                source=self.source,
            )
        )

        if self.show_debug_output and logger.isEnabledFor(logging.DEBUG):
            logger.debug("ERROR: when parsing line %d column %d: %s", line, column, msg)
