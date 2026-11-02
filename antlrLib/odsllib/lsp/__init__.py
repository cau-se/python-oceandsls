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
"""Shared language server infrastructure for the OceanDSL languages."""

from .completion import collect_candidates, keyword_items, matches_prefix, token_label
from .compute_token_index import (
    CaretPosition, TokenPosition, compute_caret_token_position, compute_token_index, compute_token_position,
    find_caret_token, find_context_for_token,
)
from .diagnostic_listener import DiagnosticListener, token_range
from .error_strategy import InputMismatchErrorStrategy
from .parsing import ParseResult, parse_source
from .semantic_tokens import LEGEND, encode_semantic_tokens

__all__ = [
    "CaretPosition", "DiagnosticListener", "InputMismatchErrorStrategy", "LEGEND", "ParseResult", "TokenPosition",
    "collect_candidates", "compute_caret_token_position", "compute_token_index", "compute_token_position",
    "encode_semantic_tokens", "find_caret_token", "find_context_for_token", "keyword_items", "matches_prefix",
    "parse_source", "token_label", "token_range",
]
