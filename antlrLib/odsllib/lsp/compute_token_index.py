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
"""Map an editor caret position onto the ANTLR token stream and parse tree.

LSP positions are 0-based (line and character); ANTLR tokens use 1-based lines and 0-based columns. The helpers in this
module expect a :class:`CaretPosition` in ANTLR coordinates, i.e. ``CaretPosition(lsp.line + 1, lsp.character)``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, List, Optional, Union

from antlr4 import BufferedTokenStream, TerminalNode, Token
from antlr4.ParserRuleContext import ParserRuleContext
from antlr4.tree.Tree import ErrorNodeImpl, ParseTree, TerminalNodeImpl


@dataclass
class CaretPosition:
    """Caret position in ANTLR coordinates (1-based line, 0-based column)."""
    line: int
    column: int


@dataclass
class TokenPosition:
    """Token index under the caret, the enclosing parse tree node and the text in front of the caret."""
    index: int
    context: Optional[Union[ParserRuleContext, TerminalNode]]
    text: str


def _token_end_column(token: Token) -> int:
    """Return the column directly after the last character of a single-line token."""
    return token.column + len(token.text or "")


def _covers(token: Token, caret: CaretPosition) -> bool:
    """True if the caret is inside the token or directly behind its last character (the usual "typing" position)."""
    if token.type == Token.EOF or token.text is None or "\n" in token.text:
        return False
    return token.line == caret.line and token.column <= caret.column <= _token_end_column(token)


def _after(token: Token, caret: CaretPosition) -> bool:
    """True if the token starts at or after the caret."""
    return token.line > caret.line or (token.line == caret.line and token.column >= caret.column)


def find_caret_token(tokens: BufferedTokenStream, caret: CaretPosition, word_token_types: Iterable[int] = ()) -> int:
    """Return the index of the token to use as caret token for code completion.

    * If the caret touches a word-like token (identifier or keyword) on the default channel, that token is returned,
      so completion candidates describe what could stand *instead of* the partially typed word.
    * Otherwise the first default-channel token starting at or after the caret is returned (possibly EOF).

    :param tokens: a token stream that has already been filled (e.g. after parsing)
    :param caret: caret position in ANTLR coordinates
    :param word_token_types: additional token types treated as words (identifiers); literal keyword tokens consisting of
        letters are always treated as words
    """
    tokens.fill()
    word_types = set(word_token_types)
    candidate: Optional[int] = None
    for token in tokens.tokens:
        if token.channel != Token.DEFAULT_CHANNEL:
            continue
        if token.type == Token.EOF:
            return candidate if candidate is not None else token.tokenIndex
        if _covers(token, caret) and (token.type in word_types or _is_word(token.text)):
            # Prefer a word token the caret touches (e.g. 'foo|' or 'fo|o')
            return token.tokenIndex
        if candidate is None and _after(token, caret):
            candidate = token.tokenIndex
    return candidate if candidate is not None else len(tokens.tokens) - 1


def _is_word(text: Optional[str]) -> bool:
    return bool(text) and (text[0].isalpha() or text[0] == "_") and all(c.isalnum() or c in "_%" for c in text)


def caret_prefix(token: Token, caret: CaretPosition) -> str:
    """Return the part of the token text in front of the caret ('' if the caret is not on the token)."""
    if token is None or not _covers(token, caret):
        return ""
    return token.text[: caret.column - token.column]


def find_context_for_token(tree: Optional[ParseTree], token_index: int) -> Optional[ParseTree]:
    """Return the innermost parse tree node whose source interval contains ``token_index`` (None if outside)."""
    if tree is None:
        return None
    if isinstance(tree, TerminalNode):
        return tree if tree.getSymbol().tokenIndex == token_index else None
    interval = tree.getSourceInterval()
    if interval is None or not (interval[0] <= token_index <= interval[1]):
        return None
    for i in range(tree.getChildCount()):
        found = find_context_for_token(tree.getChild(i), token_index)
        if found is not None:
            return found if not isinstance(found, TerminalNode) else tree
    return tree


def compute_caret_token_position(
        tree: Optional[ParseTree], tokens: BufferedTokenStream, caret: CaretPosition,
        word_token_types: Iterable[int] = ()
) -> TokenPosition:
    """Combine :func:`find_caret_token`, :func:`caret_prefix` and :func:`find_context_for_token`."""
    index = find_caret_token(tokens, caret, word_token_types)
    token = tokens.get(index)
    context_index = index
    if token.type == Token.EOF or not _covers(token, caret):
        # The caret is in front of the token (e.g. in whitespace or at the end of the document): it is still inside
        # the structures opened before it (e.g. the current test case or parameter group), so the scope is determined
        # by the previous token on the default channel
        previous = [t.tokenIndex for t in tokens.tokens[:index] if t.channel == Token.DEFAULT_CHANNEL]
        if previous:
            context_index = previous[-1]
    context = find_context_for_token(tree, context_index)
    if context is None and tree is not None and isinstance(tree, ParserRuleContext):
        context = tree
    return TokenPosition(index, context, caret_prefix(token, caret))


# ---------------------------------------------------------------------------------------------------------------------
# Original tree-walking helpers (kept for compatibility with existing DSL code)
# ---------------------------------------------------------------------------------------------------------------------

def compute_token_index_of_terminal_node(terminal_node: TerminalNode, caret_position: CaretPosition) -> Optional[Any]:
    if isinstance(terminal_node, TerminalNodeImpl):
        start = terminal_node.symbol.column
        stop = terminal_node.symbol.column + len(terminal_node.getText())
        if terminal_node.symbol.line == caret_position.line and start <= caret_position.column <= stop:
            return terminal_node.symbol.tokenIndex
    return None


def compute_token_index_of_child_node(parser_rule_context: ParserRuleContext, caret_position: CaretPosition) -> Optional[int]:
    for i in range(parser_rule_context.getChildCount()):
        index = compute_token_index(parser_rule_context.getChild(i), caret_position)
        if index is not None:
            return index
    return None


def compute_token_index(parser_rule_context: ParserRuleContext, caret_position: CaretPosition) -> Optional[int]:
    if isinstance(parser_rule_context, TerminalNode):
        return compute_token_index_of_terminal_node(parser_rule_context, caret_position)
    else:
        return compute_token_index_of_child_node(parser_rule_context, caret_position)


def position_of_token(
        token: Token, text: str, caret_position: CaretPosition, identifier_token_types: List[int],
        parser_rule_context: Union[ParserRuleContext, TerminalNode]
) -> Optional[TokenPosition]:
    if token and text is not None:
        start = token.column
        stop = token.column + len(text)
        if token.line == caret_position.line and start <= caret_position.column <= stop and 0 <= token.tokenIndex:
            index = token.tokenIndex
            if token.type in identifier_token_types:
                index -= 1

            text = text[0: caret_position.column - start] if not isinstance(parser_rule_context, ErrorNodeImpl) else ""
            return TokenPosition(index, parser_rule_context, text)

    return None


def compute_token_position_of_terminal(
        terminal_node: TerminalNode, caret_position: CaretPosition, identifier_token_types: List[int]
) -> Optional[TokenPosition]:
    token: Optional[Token] = terminal_node.symbol if isinstance(terminal_node, TerminalNodeImpl) else None
    text: Optional[str] = terminal_node.getText() if isinstance(terminal_node, TerminalNodeImpl) else None
    return position_of_token(token, text, caret_position, identifier_token_types, terminal_node)


def compute_token_position_of_child_node(
        parser_rule_context: ParserRuleContext, tokens: BufferedTokenStream, caret_position: CaretPosition,
        identifier_token_types: List[int]
) -> Optional[TokenPosition]:
    # Return None if no context exists or caret is outside of context
    if parser_rule_context is None or parser_rule_context.start is None:
        return None

    start_line: int = parser_rule_context.start.line
    start_index: int = parser_rule_context.start.tokenIndex
    # Tokens after a parser error are not part of any context; scan up to the end of the stream
    stop_index: int = len(tokens.tokens)
    # Rule contexts end on the line of their stop token; allow the caret on the following line as well, as the
    # caret is usually behind the last token when completing
    end_line: int = parser_rule_context.stop.line + 1 if parser_rule_context.stop is not None else start_line

    if start_line > caret_position.line or end_line < caret_position.line:
        return None

    # Check nested elements
    for i in range(parser_rule_context.getChildCount()):
        pos = compute_token_position(parser_rule_context.getChild(i), tokens, caret_position, identifier_token_types)
        if pos:
            return pos

    # Check elements in range of context
    for i in range(max(start_index, 0), stop_index):
        pos = position_of_token(
            tokens.tokens[i], tokens.tokens[i].text, caret_position, identifier_token_types, parser_rule_context
        )
        if pos:
            return pos

    return None


def compute_token_position(
        parser_rule_context: ParserRuleContext, tokens: BufferedTokenStream, caret_position: CaretPosition,
        identifier_token_types: Optional[List[int]] = None
) -> Optional[TokenPosition]:
    if identifier_token_types is None:
        identifier_token_types = []
    if isinstance(parser_rule_context, TerminalNode):
        return compute_token_position_of_terminal(parser_rule_context, caret_position, identifier_token_types)
    else:
        return compute_token_position_of_child_node(parser_rule_context, tokens, caret_position, identifier_token_types)
