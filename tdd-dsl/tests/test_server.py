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
"""Language server behavior of the TDD-DSL (diagnostics, content assist, highlighting and generation)."""

import os

import pytest
from lsprotocol.types import (
    ClientCapabilities, CompletionItemKind, DiagnosticSeverity, DidSaveTextDocumentParams, InitializeParams, Position,
    TextDocumentIdentifier, TextDocumentItem,
)

from odsllib.lsp.semantic_tokens import TOKEN_TYPES
from tddlspserver.server import TDDLSPServer, did_save

DATA = os.path.join(os.path.dirname(__file__), "data")
URI = "file:///work/suite.tdd"


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return f.read()


@pytest.fixture(name="server")
def server_fixture(tmp_path):
    srv = TDDLSPServer("tdd-test", "0")
    srv.work_path = str(tmp_path)
    srv.fxtran_path = "fxtran-not-installed"
    srv.lsp.lsp_initialize(InitializeParams(process_id=None, root_uri=None, capabilities=ClientCapabilities()))
    srv.published = []
    srv.publish_diagnostics = lambda uri, diagnostics, *a, **k: srv.published.append((uri, diagnostics))
    srv.show_message = lambda *a, **k: None
    return srv


def labels(server, text, line, character):
    return [i.label for i in server.complete(URI, text, Position(line=line, character=character)).items]


def suite(body: str, src: str = "src") -> str:
    return f"suite su:\ntest t1:\n    srcpath: '{src}'\n{body}"


# ---------------------------------------------------------------------------------------------------------------------
# Diagnostics
# ---------------------------------------------------------------------------------------------------------------------

class TestDiagnostics:
    def test_valid_paper_example_has_only_source_path_information(self, server):
        diagnostics = server.validate(URI, read("paper_listing1.tdd"))
        assert [d.severity for d in diagnostics] == [DiagnosticSeverity.Information]
        assert "does not exist" in diagnostics[0].message

    def test_existing_source_path_is_accepted(self, server, tmp_path):
        (tmp_path / "src").mkdir()
        assert server.validate(URI, suite("")) == []

    def test_syntax_error_position(self, server, tmp_path):
        (tmp_path / "src").mkdir()
        diagnostics = server.validate(URI, suite("    assert Foo:\n"))
        assert diagnostics[0].severity == DiagnosticSeverity.Error
        assert diagnostics[0].range.start == Position(line=3, character=11)
        assert diagnostics[0].range.end == Position(line=3, character=14)

    def test_duplicate_test_cases_are_reported(self, server, tmp_path):
        (tmp_path / "src").mkdir()
        text = suite("") + "test t1:\n    srcpath: 'src'\n"
        diagnostics = server.validate(URI, text)
        assert [d.message for d in diagnostics] == ["duplicate test case 't1'"]
        assert diagnostics[0].range.start == Position(line=3, character=5)

    def test_duplicate_variables_are_reported(self, server, tmp_path):
        (tmp_path / "src").mkdir()
        diagnostics = server.validate(URI, suite("    var:\n        x: real = 1D0\n        x: real = 2D0\n"))
        assert [d.message for d in diagnostics] == ["duplicate variable 'x' in test case 't1'"]
        assert diagnostics[0].range.start == Position(line=5, character=8)

    def test_did_save_publishes_and_generates(self, server, tmp_path):
        (tmp_path / "src").mkdir()
        path = tmp_path / "suite.tdd"
        text = read("paper_listing1.tdd").replace("'tdd-dsl/input/tdd_dev/UVic_example_opem'", "'src'")
        path.write_text(text)
        uri = path.as_uri()
        server.lsp.workspace.put_text_document(TextDocumentItem(uri=uri, language_id="tdd", version=1, text=text))

        server.on_did_save(DidSaveTextDocumentParams(text_document=TextDocumentIdentifier(uri=uri)))

        assert server.published[-1] == (uri, [])
        pf_file = tmp_path / "src" / "tests" / "test_fT_ME.pf"
        assert pf_file.is_file()
        pf = pf_file.read_text()
        assert "@assertEqual( 0D0, fT_ME ( xIntercept ), message='fails x-Intercept at 14.89D0', tolerance=1D-12)" in pf
        assert "use cfo_example" in pf
        # A Fortran template for the not yet implemented SUT and the CMake setup are generated as well
        assert "FUNCTION fT_ME" in (tmp_path / "src" / "cfo_example.f90").read_text()
        assert (tmp_path / "src" / "CMakeLists.txt").is_file()
        assert (tmp_path / "src" / "tests" / "CMakeLists.txt").is_file()


# ---------------------------------------------------------------------------------------------------------------------
# Content assist
# ---------------------------------------------------------------------------------------------------------------------

class TestCompletion:
    def test_start_of_document(self, server):
        assert labels(server, "", 0, 0) == ["suite"]

    def test_after_suite_header(self, server):
        assert labels(server, "suite su:\n", 1, 0) == ["test"]

    def test_test_case_header(self, server):
        assert set(labels(server, "suite su:\ntest t1:\n", 2, 4)) == {"srcpath", "overwrite"}

    def test_test_case_sections(self, server):
        assert set(labels(server, suite("    "), 3, 4)) >= {"var", "modules", "assert", "test"}

    def test_overwrite_flags(self, server):
        assert set(labels(server, "suite su:\ntest t1:\n    overwrite: ", 2, 15)) == {"pf", "cmake", "f90"}

    def test_assertion_directives(self, server):
        result = labels(server, suite("    assert "), 3, 11)
        assert {"Equal", "NotEqual", "LessThan", "True", "IsNaN"} <= set(result)

    def test_test_variables_in_assertion(self, server):
        text = read("paper_listing1.tdd")
        result = server.complete(URI, text, Position(line=12, character=12)).items
        variables = {i.label for i in result if i.kind == CompletionItemKind.Variable}
        assert variables == {"dp", "xIntercept", "yIntercept"}
        assert "call" in {i.label for i in result}

    def test_typed_prefix_filters_case_insensitive(self, server):
        text = read("paper_listing1.tdd").replace("fT_ME(xIntercept), K", "XI")
        assert labels(server, text, 12, 14) == ["xIntercept"]

    def test_source_path_directories(self, server, tmp_path):
        (tmp_path / "models" / "uvic").mkdir(parents=True)
        (tmp_path / "models" / "mitgcm").mkdir()
        (tmp_path / "models" / ".hidden").mkdir()
        (tmp_path / "models" / "file.f90").write_text("")
        text = "suite su:\ntest t1:\n    srcpath: 'models/'\n"
        assert labels(server, text, 2, 21) == ["mitgcm", "uvic"]
        assert labels(server, "suite su:\ntest t1:\n    srcpath: 'models/u'\n", 2, 22) == ["uvic"]

    def test_modules(self, server):
        text = suite("    modules:\n        mod_a\n        ")
        assert "mod_a" in labels(server, text, 5, 8)


def test_semantic_tokens_classify_keywords_strings_and_numbers(server):
    data = server.semantic_tokens("suite su:\ntest t1:\n    srcpath: 'src'\n    var:\n        x: real = 1D0\n").data
    entries = [data[i:i + 5] for i in range(0, len(data), 5)]
    kinds = [TOKEN_TYPES[e[3]] for e in entries]
    assert kinds[0] == "keyword"  # suite
    assert "string" in kinds  # 'src'
    assert "number" in kinds  # 1D0


def test_cli_generation(tmp_path):
    """``tdd_dsl -f suite.tdd`` generates the pFUnit files without an LSP client."""
    (tmp_path / "src").mkdir()
    path = tmp_path / "suite.tdd"
    path.write_text(suite("    assert True:\n        in:\n            1 == 1\n        out:\n            1\n")
                    .replace("1 == 1", "1"))
    srv = TDDLSPServer("tdd-cli-test", "0")
    srv.work_path = str(tmp_path)
    srv.input_path = str(path)
    did_save(srv, None)
    assert (tmp_path / "src" / "tests" / "t1.pf").is_file()  # named after the test case


def test_duplicate_test_case_does_not_break_completion(server):
    """The symbol table used to raise DuplicateSymbolError, which disabled all symbol completions."""
    text = suite("    var:\n        x: real = 1D0\n    assert Equal:\n        in:\n            x\n        out:\n"
                 "            1D0\n") + "test t1:\n    srcpath: 'src'\n"
    assert "x" in labels(server, text, 7, 12)
