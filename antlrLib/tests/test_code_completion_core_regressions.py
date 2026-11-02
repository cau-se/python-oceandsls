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
"""Regression tests for the c3 engine port."""

import importlib
import sys
import warnings

import pytest
from antlr4 import CommonTokenStream, InputStream

from odsllib.code_completion_core import CandidatesCollection, CodeCompletionCore, FollowSetsHolder
from tests.gen.TestExprCore.TestExprCoreLexer import TestExprCoreLexer
from tests.gen.TestExprCore.TestExprCoreParser import TestExprCoreParser


def make_parser(text: str) -> TestExprCoreParser:
    parser = TestExprCoreParser(CommonTokenStream(TestExprCoreLexer(InputStream(text))))
    parser.removeErrorListeners()
    parser.expression()
    return parser


def test_results_are_not_shared_between_instances():
    """Each collectCandidates() call returns its own collection (the collection used to be a class attribute)."""
    first = CodeCompletionCore(make_parser("var c = a + b()")).collectCandidates(0)
    snapshot = dict(first.tokens)
    second = CodeCompletionCore(make_parser("var c = a + b()")).collectCandidates(8)

    assert first is not second
    assert first.tokens == snapshot
    assert TestExprCoreLexer.VAR in first.tokens
    assert TestExprCoreLexer.PLUS in second.tokens
    assert TestExprCoreLexer.VAR not in second.tokens


def test_repeated_calls_on_one_instance_return_independent_results():
    core = CodeCompletionCore(make_parser("var c = a + b()"))
    first = core.collectCandidates(0)
    second = core.collectCandidates(4)
    assert set(first.tokens) == {TestExprCoreLexer.VAR, TestExprCoreLexer.LET, TestExprCoreLexer.ID}
    assert set(second.tokens) == {TestExprCoreLexer.EQUAL}


def test_follow_sets_holder_has_no_shared_mutable_defaults():
    a, b = FollowSetsHolder(), FollowSetsHolder()
    assert a.combined is not b.combined
    assert a.sets is not b.sets


def test_follow_set_cache_is_keyed_by_parser_class():
    CodeCompletionCore(make_parser("a")).collectCandidates(0)
    assert TestExprCoreParser in CodeCompletionCore.followSetsByATN


def test_preferred_rules_replace_tokens():
    """With preferred rules, an identifier position is reported as variableRef/functionRef rule candidates."""
    core = CodeCompletionCore(make_parser("var c = a + b()"))
    core.preferredRules = {TestExprCoreParser.RULE_variableRef, TestExprCoreParser.RULE_functionRef}
    candidates = core.collectCandidates(6)

    assert TestExprCoreParser.RULE_variableRef in candidates.rules
    assert TestExprCoreParser.RULE_functionRef in candidates.rules
    assert TestExprCoreLexer.ID not in candidates.tokens
    # The path from the start rule to the candidate is recorded
    assert candidates.rules[TestExprCoreParser.RULE_variableRef].ruleList[0] == TestExprCoreParser.RULE_expression


def test_ignored_tokens_are_not_reported():
    core = CodeCompletionCore(make_parser("var c = a + b()"))
    core.ignoredTokens = {TestExprCoreLexer.VAR}
    candidates = core.collectCandidates(0)
    assert TestExprCoreLexer.VAR not in candidates.tokens
    assert TestExprCoreLexer.LET in candidates.tokens


def test_debug_output_does_not_fail(caplog):
    """Debug logging used to pass format arguments without placeholders."""
    core = CodeCompletionCore(make_parser("var c = a + b()"))
    core.showDebugOutput = True
    core.showResult = True
    core.preferredRules = {TestExprCoreParser.RULE_variableRef}
    with caplog.at_level("DEBUG", logger="odsllib.code_completion_core"):
        candidates = core.collectCandidates(6)
    assert isinstance(candidates, CandidatesCollection)
    assert any("collected" in r.getMessage() for r in caplog.records)


def test_legacy_import_location_still_works():
    sys.modules.pop("codeCompletionCore.CodeCompletionCore", None)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        legacy = importlib.import_module("codeCompletionCore.CodeCompletionCore")
    assert legacy.CodeCompletionCore is CodeCompletionCore
    assert any(issubclass(w.category, DeprecationWarning) for w in caught)
