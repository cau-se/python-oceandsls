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
"""Start the TDD-DSL language server as a process and talk LSP over stdio."""

import os
import sys
import tempfile
import unittest

from parameterized import parameterized

from odsllib.lsp.testing import run_lsp_session, subprocess_env

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALID = "suite su:\ntest t1:\n    srcpath: 'src'\n    var:\n        x: real = 1D0\n    assert Equal:\n" \
        "        in:\n            x\n        out:\n            1D0\n"
INVALID = VALID + "    test t1:\n"


class TestStdio(unittest.TestCase):

    @parameterized.expand([
        ("syntax_error", INVALID, [(7, 12), (2, 4)], 1, {(7, 12): {"x"}, (2, 4): {"srcpath"}}),
        # 'test t1:' inside the assertion is a syntax error; the missing source path an information
        # Input: a test case followed by a misplaced 'test t1:', completions in the assertion and the header
        # Expected Result: an error first, the variable x and the keyword srcpath are proposed

        ("valid_document", VALID, [(7, 12)], 3, {(7, 12): {"x"}}),
        # A valid document only gets the information about the missing source path
        # Input: a valid test case whose source path does not exist, completion in the assertion
        # Expected Result: an information, the variable x is proposed

        ("empty_document", "", [(0, 0)], 1, {(0, 0): {"suite"}}),
        # An empty document lacks the required suite
        # Input: an empty document, completion at its start
        # Expected Result: an error, the keyword suite is proposed
    ])
    def test_stdio_session(self, test_name, text, positions, first_severity, expected_completions):
        with tempfile.TemporaryDirectory() as directory:
            result = run_lsp_session(
                [sys.executable, "-m", "tddlspserver"], "file:///tmp/e2e.tdd", text, "oceandsl_tdd",
                completion_positions=positions, cwd=directory, env=subprocess_env(ROOT),
            )

        self.assertEqual("pygls-odsl-tdd-prototype", result.server_name, test_name)
        severities = sorted(d.severity for d in result.diagnostics)
        self.assertEqual(first_severity, severities[0], test_name)
        for position, labels in expected_completions.items():
            self.assertLessEqual(labels, set(result.completions[position]), f"{test_name}: {position}")
        if text:
            self.assertTrue(result.semantic_tokens, test_name)


if __name__ == '__main__':
    unittest.main()
