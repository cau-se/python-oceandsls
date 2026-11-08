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
"""Candidates of the c3 engine for 'var c = a + b()' (the antlr4-c3 example), at different caret positions."""

from unittest import TestCase

from antlr4 import CommonTokenStream, DiagnosticErrorListener, InputStream
from parameterized import parameterized

from odsllib.code_completion_core import CodeCompletionCore
from tests.gen.TestExprCore.TestExprCoreLexer import TestExprCoreLexer
from tests.gen.TestExprCore.TestExprCoreParser import TestExprCoreParser

EXAMPLE = "var c = a + b()"
ASSIGNMENT_FOLLOW = [TestExprCoreLexer.ID, TestExprCoreLexer.EQUAL]
OPERATORS = {TestExprCoreLexer.PLUS, TestExprCoreLexer.MINUS, TestExprCoreLexer.MULTIPLY, TestExprCoreLexer.DIVIDE,
             TestExprCoreLexer.OPEN_PAR}


def make_core(text: str) -> CodeCompletionCore:
    """Parse ``text`` with the rule 'expression' and return a c3 engine for the parser."""
    parser = TestExprCoreParser(CommonTokenStream(TestExprCoreLexer(InputStream(text))))
    parser.addErrorListener(DiagnosticErrorListener)
    parser.expression()
    return CodeCompletionCore(parser)


class TestCodeCompletionCore(TestCase):

    @parameterized.expand([
        ("input_start", EXAMPLE, 0,
         {TestExprCoreLexer.VAR, TestExprCoreLexer.LET, TestExprCoreLexer.ID},
         {TestExprCoreLexer.VAR: ASSIGNMENT_FOLLOW, TestExprCoreLexer.LET: ASSIGNMENT_FOLLOW,
          TestExprCoreLexer.ID: []}),
        # At the input start
        # Input: 'var c = a + b()', caret token index 0 ('var')
        # Expected Result: VAR and LET (each followed by ID and '=') and ID (an expression)

        ("first_whitespace", EXAMPLE, 1, {TestExprCoreLexer.ID}, {}),
        # On the first whitespace (a real implementation would check where in the whitespace the caret is)
        # Input: 'var c = a + b()', caret token index 1 (the space after 'var')
        # Expected Result: only ID (the variable name)

        ("variable_name", EXAMPLE, 2, {TestExprCoreLexer.ID}, {}),
        # On the variable name
        # Input: 'var c = a + b()', caret token index 2 ('c')
        # Expected Result: only ID

        ("equal_sign", EXAMPLE, 4, {TestExprCoreLexer.EQUAL}, {}),
        # On the equal sign (whitespace positions are ignored from now on)
        # Input: 'var c = a + b()', caret token index 4 ('=')
        # Expected Result: only '='

        ("variable_reference", EXAMPLE, 6, {TestExprCoreLexer.ID}, {}),
        # On the variable reference: without preferred rules, references are reported as ID
        # Input: 'var c = a + b()', caret token index 6 ('a')
        # Expected Result: only ID

        ("plus_operator", EXAMPLE, 8, OPERATORS, {}),
        # On the '+' operator: operators are candidates, as the engine is not told to leave them out
        # Input: 'var c = a + b()', caret token index 8 ('+')
        # Expected Result: '+', '-', '*', '/' and '(' (a function call)
    ])
    def test_collect_candidates(self, test_name, text, token_index, expected_tokens, expected_following):
        candidates = make_core(text).collectCandidates(token_index)

        self.assertEqual(expected_tokens, set(candidates.tokens), test_name)
        for token, following in expected_following.items():
            self.assertEqual(following, candidates.tokens.get(token), f"{test_name}: tokens following {token}")
