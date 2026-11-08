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
"""End-to-end test of the base server over stdio."""

import os
import sys
from unittest import TestCase

from parameterized import parameterized

from odsllib.lsp.testing import run_lsp_session, subprocess_env

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OPERATORS = ["(", "*", "+", "-", "/"]


class TestStdioSession(TestCase):

    @parameterized.expand([
        ("missing_operand", "var c = a +", {(0, 10): OPERATORS, (0, 11): []}, 1, [0, 6, 1, 4, 0, 0, 4, 1, 4, 0]),
        # An incomplete expression
        # Input: 'var c = a +', completion on the '+' and behind it
        # Expected Result: one diagnostic (missing operand), the operators at the '+', nothing behind it (only an
        # identifier may follow) and semantic tokens for '=' and '+'

        ("complete_assignment", "var c = a ", {(0, 0): [], (0, 10): OPERATORS}, 0, [0, 6, 1, 4, 0]),
        # A complete assignment followed by a space
        # Input: 'var c = a ', completion at the start and behind the space
        # Expected Result: no diagnostics, no keyword candidates at the start (VAR and LET have no literal names), the
        # operators behind the space and a semantic token for '='

        ("syntax_error", "let x = )", {(0, 8): []}, 1, [0, 6, 1, 4, 0, 0, 2, 1, 4, 0]),
        # A closing parenthesis instead of an operand
        # Input: 'let x = )', completion on the ')'
        # Expected Result: one diagnostic, no candidates and semantic tokens for '=' and ')'
    ])
    def test_stdio_session(self, test_name, text, expected_completions, expected_diagnostics,
                           expected_semantic_tokens):
        result = run_lsp_session(
            [sys.executable, "-m", "tests.expr_server"], "file:///tmp/e2e.expr", text, "expr",
            completion_positions=list(expected_completions), cwd=ROOT, env=subprocess_env(ROOT),
        )

        self.assertEqual("expr-e2e-server", result.server_name, test_name)
        self.assertEqual(expected_diagnostics, len(result.diagnostics), test_name)
        for position, labels in expected_completions.items():
            self.assertEqual(labels, sorted(result.completions[position]), f"{test_name}: completion at {position}")
        self.assertEqual(expected_semantic_tokens, result.semantic_tokens, test_name)
