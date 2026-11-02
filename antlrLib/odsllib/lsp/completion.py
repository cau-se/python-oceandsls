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
"""Grammar-driven code completion based on :class:`odsllib.code_completion_core.CodeCompletionCore`."""

from __future__ import annotations

from typing import Iterable, List, Optional, Set

from antlr4 import Parser, Token
from lsprotocol.types import CompletionItem, CompletionItemKind

from ..code_completion_core import CandidatesCollection, CodeCompletionCore


def collect_candidates(
        parser: Parser, caret_token_index: int, preferred_rules: Iterable[int] = (), ignored_tokens: Iterable[int] = (),
        context=None,
) -> CandidatesCollection:
    """Run the c3 engine on ``parser`` (whose token stream must already be filled) for the given caret token."""
    core = CodeCompletionCore(parser)
    core.ignoredTokens = {Token.EPSILON, *ignored_tokens}
    core.preferredRules = set(preferred_rules)
    return core.collectCandidates(caret_token_index, context)


def token_label(parser: Parser, token_type: int) -> Optional[str]:
    """Return the text to insert for a literal token type (``'suite'`` -> ``suite``) or None for symbolic tokens."""
    if token_type < 0 or token_type >= len(parser.literalNames):
        return None
    literal = parser.literalNames[token_type]
    if not literal or literal == "<INVALID>" or len(literal) < 2:
        return None
    return literal[1:-1].replace("\\'", "'")


def keyword_items(
        parser: Parser, candidates: CandidatesCollection, prefix: str = "", with_following: bool = True
) -> List[CompletionItem]:
    """Convert candidate literal tokens into keyword completion items.

    :param with_following: append the fixed tokens which always follow a candidate (e.g. ``suite`` -> ``suite :``)
        to the item's detail, so clients can show what will be expected next
    """
    items: List[CompletionItem] = []
    seen: Set[str] = set()
    for token_type, following in sorted(candidates.tokens.items()):
        label = token_label(parser, token_type)
        if not label or label in seen or not matches_prefix(label, prefix):
            continue
        seen.add(label)
        detail = None
        if with_following and following:
            follow = [token_label(parser, t) for t in following]
            if all(follow):
                detail = " ".join([label, *follow])
        kind = CompletionItemKind.Keyword if label[0].isalpha() else CompletionItemKind.Operator
        items.append(CompletionItem(label=label, kind=kind, detail=detail))
    return items


def matches_prefix(label: str, prefix: str) -> bool:
    """Case-insensitive prefix filter used for all completion items."""
    return not prefix or label.lower().startswith(prefix.lower())
