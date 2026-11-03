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
"""Token based semantic highlighting (``textDocument/semanticTokens/full``)."""

from __future__ import annotations

from typing import FrozenSet, Iterable, List, Optional, Set

from antlr4 import BufferedTokenStream, Parser, Token
from lsprotocol.types import SemanticTokensLegend

TOKEN_TYPES: List[str] = ["keyword", "string", "number", "comment", "operator"]
LEGEND = SemanticTokensLegend(token_types=TOKEN_TYPES, token_modifiers=[])

DEFAULT_STRING_TOKENS: FrozenSet[str] = frozenset({"STRING"})
DEFAULT_NUMBER_TOKENS: FrozenSet[str] = frozenset({"INT", "NUM", "DP", "ELONG", "EDOUBLE", "FLOAT", "NUMBER", "DOUBLE"})
DEFAULT_COMMENT_TOKENS: FrozenSet[str] = frozenset(
    {"COMMENT", "SL_COMMENT", "ML_COMMENT", "LINE_COMMENT", "TDD_COMMENT"})


def classify(parser: Parser, token: Token, string_tokens: Set[str], number_tokens: Set[str],
             comment_tokens: Set[str]) -> Optional[int]:
    """Return the index into :data:`TOKEN_TYPES` for a token or None if it is not highlighted."""
    if token.type < 0:
        return None
    symbolic = parser.symbolicNames[token.type] if token.type < len(parser.symbolicNames) else None
    literal = parser.literalNames[token.type] if token.type < len(parser.literalNames) else None
    if symbolic in comment_tokens:
        return TOKEN_TYPES.index("comment")
    if symbolic in string_tokens:
        return TOKEN_TYPES.index("string")
    if symbolic in number_tokens:
        return TOKEN_TYPES.index("number")
    if literal and literal != "<INVALID>":
        text = literal[1:-1]
        if text[:1].isalpha():
            return TOKEN_TYPES.index("keyword")
        return TOKEN_TYPES.index("operator")
    return None


def encode_semantic_tokens(
        parser: Parser, tokens: BufferedTokenStream, string_tokens: Iterable[str] = DEFAULT_STRING_TOKENS,
        number_tokens: Iterable[str] = DEFAULT_NUMBER_TOKENS, comment_tokens: Iterable[str] = DEFAULT_COMMENT_TOKENS,
) -> List[int]:
    """Encode all classified tokens (including hidden channel tokens such as comments) in LSP's relative format."""
    tokens.fill()
    string_tokens, number_tokens, comment_tokens = set(string_tokens), set(number_tokens), set(comment_tokens)
    data: List[int] = []
    last_line, last_start = 0, 0
    for token in tokens.tokens:
        kind = classify(parser, token, string_tokens, number_tokens, comment_tokens)
        if kind is None or not token.text:
            continue
        line, column = token.line - 1, token.column
        # LSP tokens must not span multiple lines: emit one entry per line
        for part in token.text.split("\n"):
            length = len(part.rstrip("\r"))
            if length > 0:
                delta_line = line - last_line
                delta_start = column - last_start if delta_line == 0 else column
                data.extend([delta_line, delta_start, length, kind, 0])
                last_line, last_start = line, column
            line, column = line + 1, 0
    return data
