#  Copyright (c) 2023-2026.  OceanDSL (https://oceandsl.uni-kiel.de)
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
from unittest import TestCase

from antlr4 import CommonTokenStream, InputStream
from parameterized import parameterized

from odsllib.code_completion_core import CandidatesCollection, CodeCompletionCore, FollowSetsHolder
from tests.gen.TestExprCore.TestExprCoreLexer import TestExprCoreLexer
from tests.gen.TestExprCore.TestExprCoreParser import TestExprCoreParser

EXAMPLE = "var c = a + b()"
START = {TestExprCoreLexer.VAR, TestExprCoreLexer.LET, TestExprCoreLexer.ID}
OPERATORS = {TestExprCoreLexer.PLUS, TestExprCoreLexer.MINUS, TestExprCoreLexer.MULTIPLY, TestExprCoreLexer.DIVIDE,
             TestExprCoreLexer.OPEN_PAR}
REFERENCE_RULES = {TestExprCoreParser.RULE_variableRef, TestExprCoreParser.RULE_functionRef}


def make_parser(text: str) -> TestExprCoreParser:
    parser = TestExprCoreParser(CommonTokenStream(TestExprCoreLexer(InputStream(text))))
    parser.removeErrorListeners()
    parser.expression()
    return parser


class TestCodeCompletionCoreRegressions(TestCase):

    @parameterized.expand([
        ("separate_instances", True, 0, 8, START, OPERATORS),
        # Each collectCandidates() call returns its own collection (it used to be a class attribute)
        # Input: two engines for 'var c = a + b()', token indexes 0 and 8
        # Expected Result: the start tokens and the operators, the first collection unchanged by the second call

        ("one_instance", False, 0, 4, START, {TestExprCoreLexer.EQUAL}),
        # Repeated calls on one engine return independent collections
        # Input: one engine for 'var c = a + b()', token indexes 0 and 4
        # Expected Result: the start tokens, then only '='

        ("one_instance_reversed", False, 8, 0, OPERATORS, START),
        # The order of the calls does not matter
        # Input: one engine for 'var c = a + b()', token indexes 8 and 0
        # Expected Result: the operators, then the start tokens

        ("separate_instances_same_index", True, 6, 6, {TestExprCoreLexer.ID}, {TestExprCoreLexer.ID}),
        # Two engines asked for the same position return equal but distinct collections
        # Input: two engines for 'var c = a + b()', token index 6 twice
        # Expected Result: only ID in both collections
    ])
    def test_results_are_independent(self, test_name, separate_instances, first_index, second_index,
                                     expected_first, expected_second):
        core = CodeCompletionCore(make_parser(EXAMPLE))
        first = core.collectCandidates(first_index)
        snapshot = dict(first.tokens)
        if separate_instances:
            core = CodeCompletionCore(make_parser(EXAMPLE))
        second = core.collectCandidates(second_index)

        self.assertIsNot(first, second, test_name)
        self.assertEqual(snapshot, first.tokens, f"{test_name}: first collection changed")
        self.assertEqual(expected_first, set(first.tokens), test_name)
        self.assertEqual(expected_second, set(second.tokens), test_name)

    @parameterized.expand([
        ("follow_sets", "sets", False),
        # The follow sets of a state are not shared between holders
        # Input: two new FollowSetsHolder instances, attribute 'sets'
        # Expected Result: two distinct lists

        ("combined_set", "combined", False),
        # The combined follow set is not shared between holders
        # Input: two new FollowSetsHolder instances, attribute 'combined'
        # Expected Result: two distinct interval sets

        ("follow_sets_after_append", "sets", True),
        # Adding to the follow sets of one holder leaves the other one empty
        # Input: two new FollowSetsHolder instances, an entry appended to the first one's 'sets'
        # Expected Result: the second holder's 'sets' stays empty
    ])
    def test_follow_sets_holder_has_no_shared_mutable_defaults(self, test_name, attribute, append_to_first):
        first, second = FollowSetsHolder(), FollowSetsHolder()
        self.assertIsNot(getattr(first, attribute), getattr(second, attribute), test_name)
        if append_to_first:
            getattr(first, attribute).append(object())
            self.assertEqual(0, len(getattr(second, attribute)), test_name)

    @parameterized.expand([
        ("single_identifier", "a", 0),
        # The follow sets are cached per parser class
        # Input: 'a', token index 0
        # Expected Result: the cache holds an entry for TestExprCoreParser

        ("full_example", EXAMPLE, 8),
        # The cache is filled for longer input as well
        # Input: 'var c = a + b()', token index 8
        # Expected Result: the cache holds an entry for TestExprCoreParser

        ("empty_input", "", 0),
        # The cache is filled even for empty input
        # Input: '', token index 0
        # Expected Result: the cache holds an entry for TestExprCoreParser
    ])
    def test_follow_set_cache_is_keyed_by_parser_class(self, test_name, text, token_index):
        CodeCompletionCore(make_parser(text)).collectCandidates(token_index)
        self.assertIn(TestExprCoreParser, CodeCompletionCore.followSetsByATN, test_name)

    @parameterized.expand([
        ("preferred_rules_replace_identifier", REFERENCE_RULES, set(), 6,
         set(), {TestExprCoreLexer.ID}, REFERENCE_RULES),
        # With preferred rules, an identifier position is reported as variableRef/functionRef rule candidates
        # Input: preferred rules variableRef and functionRef, caret on 'a' in 'var c = a + b()'
        # Expected Result: both rules, but no ID token

        ("ignored_token", set(), {TestExprCoreLexer.VAR}, 0,
         {TestExprCoreLexer.LET, TestExprCoreLexer.ID}, {TestExprCoreLexer.VAR}, set()),
        # Ignored tokens are not reported
        # Input: ignored token VAR, caret at the input start
        # Expected Result: LET and ID, but not VAR

        ("all_keywords_ignored", set(), {TestExprCoreLexer.VAR, TestExprCoreLexer.LET}, 0,
         {TestExprCoreLexer.ID}, {TestExprCoreLexer.VAR, TestExprCoreLexer.LET}, set()),
        # Several ignored tokens
        # Input: ignored tokens VAR and LET, caret at the input start
        # Expected Result: only ID

        ("preferred_rules_without_reference", REFERENCE_RULES, set(), 4,
         {TestExprCoreLexer.EQUAL}, set(), set()),
        # Preferred rules do not change positions where no reference is possible
        # Input: preferred rules variableRef and functionRef, caret on '=' in 'var c = a + b()'
        # Expected Result: only '=' and no rule candidates
    ])
    def test_configured_candidates(self, test_name, preferred_rules, ignored_tokens, token_index,
                                   expected_tokens, unexpected_tokens, expected_rules):
        core = CodeCompletionCore(make_parser(EXAMPLE))
        core.preferredRules = preferred_rules
        core.ignoredTokens = ignored_tokens
        candidates = core.collectCandidates(token_index)

        self.assertTrue(expected_tokens <= set(candidates.tokens), f"{test_name}: {set(candidates.tokens)}")
        self.assertFalse(unexpected_tokens & set(candidates.tokens), test_name)
        self.assertEqual(expected_rules, set(candidates.rules), test_name)
        for rule in expected_rules:
            # the path from the start rule to the candidate is recorded
            self.assertEqual(TestExprCoreParser.RULE_expression, candidates.rules[rule].ruleList[0], test_name)

    @parameterized.expand([
        ("debug_and_result", True, True, "collected"),
        # Debug logging used to pass format arguments without placeholders
        # Input: showDebugOutput and showResult, preferred rule variableRef, caret on 'a'
        # Expected Result: candidates are returned and a 'collected' message is logged

        ("debug_only", True, False, "collected"),
        # Debug output without the result summary
        # Input: showDebugOutput only, preferred rule variableRef, caret on 'a'
        # Expected Result: candidates are returned and a 'collected' message is logged

        ("result_only", False, True, "Collected rules"),
        # Only the result summary
        # Input: showResult only, preferred rule variableRef, caret on 'a'
        # Expected Result: candidates are returned and the summary of the collected rules is logged
    ])
    def test_debug_output_does_not_fail(self, test_name, show_debug_output, show_result, expected_message):
        core = CodeCompletionCore(make_parser(EXAMPLE))
        core.showDebugOutput = show_debug_output
        core.showResult = show_result
        core.preferredRules = {TestExprCoreParser.RULE_variableRef}
        with self.assertLogs("odsllib.code_completion_core", level="DEBUG") as logs:
            candidates = core.collectCandidates(6)

        self.assertIsInstance(candidates, CandidatesCollection, test_name)
        self.assertTrue(any(expected_message in r.getMessage() for r in logs.records),
                        f"{test_name}: {[r.getMessage() for r in logs.records]}")

    @parameterized.expand([
        ("module", "codeCompletionCore.CodeCompletionCore", "CodeCompletionCore", CodeCompletionCore),
        # The pre 0.39 module still provides the engine
        # Input: import codeCompletionCore.CodeCompletionCore
        # Expected Result: its CodeCompletionCore is the odsllib class, and a DeprecationWarning is emitted

        ("collection", "codeCompletionCore.CodeCompletionCore", "CandidatesCollection", CandidatesCollection),
        # The candidate collection is available at the old location as well
        # Input: import codeCompletionCore.CodeCompletionCore
        # Expected Result: its CandidatesCollection is the odsllib class, and a DeprecationWarning is emitted

        ("follow_sets_holder", "codeCompletionCore.CodeCompletionCore", "FollowSetsHolder", FollowSetsHolder),
        # The other names are re-exported too
        # Input: import codeCompletionCore.CodeCompletionCore
        # Expected Result: its FollowSetsHolder is the odsllib class, and a DeprecationWarning is emitted
    ])
    def test_legacy_import_location_still_works(self, test_name, module_name, attribute, expected):
        sys.modules.pop(module_name, None)
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            legacy = importlib.import_module(module_name)

        self.assertIs(expected, getattr(legacy, attribute), test_name)
        self.assertTrue(any(issubclass(w.category, DeprecationWarning) for w in caught), test_name)
