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
"""Language server behavior of the BGC-DSL."""

import os
import sys

import pytest
from lsprotocol.types import CompletionItemKind, DiagnosticSeverity, Position

from bgclspserver.server import bgcLSPServer, did_save
from odsllib.lsp.testing import run_lsp_session, subprocess_env

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT = os.path.join(ROOT, "input")

MODEL = """model bgc

substances
    float N ::
    float P ::

parameters
    float growth :: = 0.5

compartment Phy {
    states N P

    update N = growth * N
    update P = assimilation.P
}

compartment Ki {
    states N

    update N = 0
}

connection assimilation(N, P) from Phy to Ki {
    N = Phy.N + Ki.N
    P = Phy.P + 1
}
"""


@pytest.fixture
def server():
    return bgcLSPServer("bgc-test", "0")


@pytest.mark.parametrize("name", ["example.bgc", "example1.bgc", "example2.bgc"])
def test_examples_have_no_diagnostics(server, name):
    with open(os.path.join(INPUT, name), encoding="utf-8") as f:
        assert server.validate("file:///" + name, f.read()) == []


def test_connection_requires_from(server):
    text = MODEL.replace("from Phy to Ki", "Phy to Ki")
    diagnostics = server.validate("u", text)
    assert diagnostics and diagnostics[0].severity == DiagnosticSeverity.Error
    assert diagnostics[0].range.start.line == 22


def test_keyword_completion_at_start(server):
    assert [i.label for i in server.complete("u", "", Position(line=0, character=0)).items] == ["model"]


def test_type_completion_in_substances(server):
    text = "model mymodel\n\nsubstances\n    "
    labels = {i.label for i in server.complete("u", text, Position(line=3, character=4)).items}
    assert {"int", "float", "double", "string"} <= labels


def test_reference_completion_offers_declared_names(server):
    position = Position(line=12, character=24)  # 'update N = growth * |N'
    items = server.complete("u", MODEL, position).items
    variables = {i.label for i in items if i.kind == CompletionItemKind.Variable}
    assert {"N", "P", "growth", "Phy", "Ki"} <= variables
    assert not any(" " in label for label in variables)


def test_reference_completion_filters_prefix(server):
    text = MODEL.replace("update N = growth * N", "update N = gr")
    items = server.complete("u", text, Position(line=12, character=17)).items
    assert [i.label for i in items] == ["growth"]


def test_cli_check(tmp_path, caplog):
    path = tmp_path / "broken.bgc"
    path.write_text(MODEL.replace("states N P", "states"))
    server = bgcLSPServer("bgc-cli", "0")
    server.input_path = str(path)
    with caplog.at_level("ERROR"):
        did_save(server, None)
    assert any("broken.bgc:13:" in r.getMessage() for r in caplog.records), [r.getMessage() for r in caplog.records]


def test_stdio_session(tmp_path):
    result = run_lsp_session(
        [sys.executable, "-m", "bgclspserver"], "file:///tmp/m.bgc", MODEL, "oceandsl_bgc",
        completion_positions=[(12, 24)], cwd=str(tmp_path), env=subprocess_env(ROOT),
    )
    assert result.server_name == "pygls-odsl-bgc-prototype"
    assert result.diagnostics == []
    assert "growth" in result.completions[(12, 24)]
    assert result.semantic_tokens
