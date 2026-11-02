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
"""End-to-end test of the base server over stdio."""

import os
import sys

from odsllib.lsp.testing import run_lsp_session, subprocess_env

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_stdio_session():
    result = run_lsp_session(
        [sys.executable, "-m", "tests.expr_server"], "file:///tmp/e2e.expr", "var c = a +", "expr",
        completion_positions=[(0, 10), (0, 11)], cwd=ROOT, env=subprocess_env(ROOT),
    )
    assert result.server_name == "expr-e2e-server"
    assert len(result.diagnostics) == 1  # missing operand after '+'
    assert {"+", "-", "*", "/", "("} <= set(result.completions[(0, 10)])  # operators at the "+"
    assert result.completions[(0, 11)] == []  # only an identifier may follow "+"
    assert result.semantic_tokens[:5] == [0, 6, 1, 4, 0]
