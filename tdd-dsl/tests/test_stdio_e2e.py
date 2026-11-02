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

from odsllib.lsp.testing import run_lsp_session, subprocess_env

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEXT = "suite su:\ntest t1:\n    srcpath: 'src'\n    var:\n        x: real = 1D0\n    assert Equal:\n" \
       "        in:\n            x\n        out:\n            1D0\n    test t1:\n"


def test_stdio_session(tmp_path):
    env = subprocess_env(ROOT)
    result = run_lsp_session(
        [sys.executable, "-m", "tddlspserver"], "file:///tmp/e2e.tdd", TEXT, "oceandsl_tdd",
        completion_positions=[(7, 12), (2, 4)], cwd=str(tmp_path), env=env,
    )
    assert result.server_name == "pygls-odsl-tdd-prototype"
    # 'test t1:' inside the assertion is a syntax error; the missing source path an information
    severities = sorted(d.severity for d in result.diagnostics)
    assert severities[0] == 1 and len(result.diagnostics) >= 1
    assert "x" in result.completions[(7, 12)]
    assert "srcpath" in result.completions[(2, 4)]
    assert result.semantic_tokens
