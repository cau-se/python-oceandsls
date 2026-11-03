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
"""Language server behavior of CP-DSL declarations (*.decl) and configurations (*.oconf)."""

import glob
import os
import sys

import pytest
from lsprotocol.types import (
    ClientCapabilities, CompletionItemKind, DiagnosticSeverity, DocumentSymbolParams, InitializeParams, Position,
    TextDocumentIdentifier, TextDocumentItem,
)
from pygls.uris import from_fs_path

from conflspserver.server import confLSPServer
from dcllspserver.server import dclLSPServer, declaration_outline
from odsllib.lsp.testing import run_lsp_session, subprocess_env

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
INPUT = os.path.join(ROOT, "input")

DECLARATION = """model m

types
\tenum Color { red, green, blue }

feature a : "A feature" {
\trequires b
\tgroup ga : "Group of a" {
\t\tdef speed float : meter / second, "speed of a"
\t}
\tsub alternative
\t\tfeature a1 : "first variant"
\t\tfeature a2 : "second variant"
}
feature b : "B feature"
required feature r : "R feature"
feature x : "X feature" {
\texcludes b
}

group g : "General group" {
\tdef p int : meter, "parameter p" = 1
\tdef q float : second = 2
\tdef c Color : "colour"
}
"""


def labels(items):
    return [i.label for i in items]


@pytest.fixture(name="dcl")
def dcl_fixture():
    return dclLSPServer("dcl-test", "0")


@pytest.fixture(name="conf")
def conf_fixture():
    server = confLSPServer("conf-test", "0")
    server.lsp.lsp_initialize(InitializeParams(process_id=None, root_uri=None, capabilities=ClientCapabilities()))
    return server


@pytest.fixture(name="workspace")
def workspace_fixture(tmp_path):
    (tmp_path / "m.decl").write_text(DECLARATION)
    return tmp_path


def conf_uri(workspace, text, name="c.oconf"):
    path = workspace / name
    path.write_text(text)
    return from_fs_path(str(path))


# ---------------------------------------------------------------------------------------------------------------------
# Declarations
# ---------------------------------------------------------------------------------------------------------------------

class TestDeclarationServer:
    @pytest.mark.parametrize("path", sorted(glob.glob(os.path.join(INPUT, "**", "*.decl"), recursive=True)))
    def test_bundled_declarations_have_no_syntax_errors(self, dcl, path):
        with open(path, encoding="utf-8") as f:
            result = dcl.parse(f.read())
        assert result.diagnostics == []

    def test_valid_declaration(self, dcl):
        assert dcl.validate("u", DECLARATION) == []

    def test_unknown_type_and_redefinitions(self, dcl):
        text = DECLARATION.replace("def q float", "def q Unknown") + "group g2 : \"\" {\n\tdef v int : meter\n" \
                                                                      "\tdef v int : meter\n}\n"
        messages = {d.message: d for d in dcl.validate("u", text)}
        assert messages["Unknown type Unknown"].range.start.line == 22
        assert messages["Parameter redefined v"].severity == DiagnosticSeverity.Error
        assert messages["Parameter redefined v"].range.start.line == 27

    def test_unknown_feature_reference(self, dcl):
        diagnostics = dcl.validate("u", DECLARATION.replace("requires b", "requires nope"))
        assert [d.message for d in diagnostics] == ["Feature nope does not exist"]
        assert diagnostics[0].range.start.line == 6

    def test_feature_references_may_point_forward(self, dcl):
        """'requires b' refers to a feature declared later in the file."""
        assert dcl.validate("u", DECLARATION) == []

    def test_no_semantic_errors_on_syntax_errors(self, dcl):
        diagnostics = dcl.validate("u", "model m\ngroup g : \"\" {\n\tdef p int :\n}\n")
        assert diagnostics and all("expecting" in d.message or "input" in d.message for d in diagnostics)

    def test_keyword_completion(self, dcl):
        assert labels(dcl.complete("u", "", Position(line=0, character=0)).items) == ["model"]
        top = set(labels(dcl.complete("u", "model m\n", Position(line=1, character=0)).items))
        assert {"types", "group", "feature", "required"} <= top

    def test_feature_reference_completion(self, dcl):
        dcl.validate("u", DECLARATION)  # last valid version of the document
        text = DECLARATION.replace("requires b", "requires ")
        items = dcl.complete("u", text, Position(line=6, character=10)).items
        assert {"a", "a.a1", "a.a2", "b", "r", "x"} <= set(labels(items))
        documented = {i.label: i for i in items}
        assert documented["b"].documentation.value == "B feature"

    def test_type_completion(self, dcl):
        text = DECLARATION.replace("def q float", "def q ")
        result = set(labels(dcl.complete("u", text, Position(line=22, character=7)).items))
        assert {"int", "float", "string", "boolean", "Color"} <= result

    def test_value_reference_completion(self, dcl):
        text = DECLARATION.replace("def q float : second = 2", "def q float : second = ")
        result = set(labels(dcl.complete("u", text, Position(line=22, character=24)).items))
        assert {"p", "g.p", "ga.speed"} <= result  # local and qualified parameters
        assert {"red", "green", "blue"} <= result  # enumerals

    def test_outline(self, dcl):
        outline = declaration_outline(dcl.parse(DECLARATION).tree)
        assert [s.name for s in outline] == ["Color", "g", "a", "b", "r", "x"]
        group = outline[1]
        assert [c.name for c in group.children] == ["p", "q", "c"]
        feature_a = outline[2]
        assert [c.name for c in feature_a.children] == ["ga", "a1", "a2"]
        assert group.selection_range.start == Position(line=20, character=6)

    def test_document_symbol_handler(self, dcl):
        dcl.lsp.lsp_initialize(InitializeParams(process_id=None, root_uri=None, capabilities=ClientCapabilities()))
        dcl.lsp.workspace.put_text_document(TextDocumentItem(uri="file:///m.decl", language_id="dcl", version=1,
                                                             text=DECLARATION))
        handler = dcl.lsp.fm.features["textDocument/documentSymbol"]
        symbols = handler(DocumentSymbolParams(text_document=TextDocumentIdentifier(uri="file:///m.decl")))
        assert len(symbols) == 6


# ---------------------------------------------------------------------------------------------------------------------
# Configurations
# ---------------------------------------------------------------------------------------------------------------------

class TestConfigurationServer:
    def test_paper_syntax_parses(self, conf):
        """Array selectors with parentheses, units after values and products of parameter references (paper §5.3)."""
        text = ("configuration c : m\n\ngroup g {\n\tlevels(4:5) : [ 1, 2 ]\n\tlevels(1) : 5\n"
                "\tgBaro : 9.81 m/s^2\n\tspeed : 2 km/h\n\tNx : SIZE.sNx*SIZE.nSx*SIZE.nPx\n}\n")
        result = conf.parse(text)
        assert result.diagnostics == []
        nx = result.tree.parameterGroups[0].parameters[4]
        assert nx.value.getChildCount() == 1 and nx.value.multiplicationExpression().right is not None
        assert result.tree.parameterGroups[0].parameters[2].unit.getText() == "m/s^2"

    @pytest.mark.parametrize("path", [
        "testing/features/eval.oconf", "testing/basic/global.oconf", "testing/arrays/array.oconf",
        "UVic/configuration.oconf", "testing/use-declared-array/configuration.oconf",
    ])
    def test_bundled_configurations_are_valid(self, conf, path):
        full = os.path.join(INPUT, path)
        with open(full, encoding="utf-8") as f:
            assert conf.validate(from_fs_path(full), f.read()) == []

    @pytest.mark.parametrize("path", sorted(glob.glob(os.path.join(INPUT, "MITgcm", "tutorial_*.oconf"))))
    def test_mitgcm_tutorials_parse(self, conf, path):
        if path.endswith("tutorial_global_oce_in_p.oconf"):
            pytest.skip("file uses an outdated syntax (no 'configuration' header)")
        with open(path, encoding="utf-8") as f:
            assert conf.parse(f.read()).diagnostics == []

    def test_missing_declaration_model(self, conf, tmp_path):
        uri = conf_uri(tmp_path, "configuration c : unknown\n")
        diagnostics = conf.validate(uri, "configuration c : unknown\n")
        assert len(diagnostics) == 1
        assert "unknown.decl" in diagnostics[0].message
        assert diagnostics[0].range.start == Position(line=0, character=18)

    def test_unknown_elements(self, conf, workspace):
        text = "configuration c : m\n\nactivate a, b, nope\n\ngroup g {\n\tp : 3\n\tmissing : 4\n}\ngroup nogroup {\n}\n"
        diagnostics = conf.validate(conf_uri(workspace, text), text)
        found = {d.message: d.range.start.line for d in diagnostics}
        assert found["Missing feature nope to activate"] == 2
        assert found["Parameter missing does not exist in g"] == 6
        assert found["Missing group nogroup"] == 8

    def test_feature_dependencies(self, conf, workspace):
        text = "configuration c : m\n\nactivate a, x\n"
        diagnostics = conf.validate(conf_uri(workspace, text), text)
        by_message = {d.message: d for d in diagnostics}
        assert by_message["feature a requires b, which is not activated"].severity == DiagnosticSeverity.Error
        assert by_message["required feature r is not activated"].severity == DiagnosticSeverity.Warning
        text = "configuration c : m\n\nactivate a, b, x, r\n"
        assert [d.message for d in conf.validate(conf_uri(workspace, text), text)] == \
               ["feature x excludes b, which is activated"]

    def test_unsaved_declaration_buffer_is_used(self, conf, workspace):
        decl_uri = from_fs_path(str(workspace / "m.decl"))
        conf.lsp.workspace.put_text_document(TextDocumentItem(
            uri=decl_uri, language_id="dcl", version=1, text=DECLARATION.replace("group g :", "group renamed :")))
        text = "configuration c : m\n\nactivate a, b, r\ngroup renamed {\n\tp : 1\n}\n"
        assert conf.validate(conf_uri(workspace, text), text) == []

    def test_declaration_problems_are_summarized(self, conf, workspace):
        (workspace / "m.decl").write_text(DECLARATION.replace("requires b", "requires nope"))
        text = "configuration c : m\n\nactivate b, r\n"
        diagnostics = conf.validate(conf_uri(workspace, text), text)
        assert [d.severity for d in diagnostics] == [DiagnosticSeverity.Warning]
        assert "Feature nope does not exist" in diagnostics[0].message

    def test_feature_completion_with_descriptions(self, conf, workspace):
        text = "configuration c : m\n\nactivate "
        items = conf.complete(conf_uri(workspace, text), text, Position(line=2, character=9)).items
        by_label = {i.label: i for i in items}
        assert {"a", "b", "r", "x"} <= set(by_label)
        assert by_label["a"].documentation.value == "A feature"
        assert by_label["r"].detail == "required feature"

    def test_sub_feature_and_group_completion_in_feature_scope(self, conf, workspace):
        text = "configuration c : m\n\nfeature a {\n\tactivate \n}\n"
        uri = conf_uri(workspace, text)
        assert set(labels(conf.complete(uri, text, Position(line=3, character=10)).items)) >= {"a1", "a2"}
        text = "configuration c : m\n\nfeature a {\n\tgroup \n}\n"
        assert labels(conf.complete(conf_uri(workspace, text), text, Position(line=3, character=7)).items) == ["ga"]

    def test_group_and_parameter_completion(self, conf, workspace):
        text = "configuration c : m\n\ngroup \n"
        items = conf.complete(conf_uri(workspace, text), text, Position(line=2, character=6)).items
        assert labels(items) == ["g"]
        assert items[0].kind == CompletionItemKind.Struct and items[0].documentation.value == "General group"

        text = "configuration c : m\n\ngroup g {\n\t\n}\n"
        items = conf.complete(conf_uri(workspace, text), text, Position(line=3, character=1)).items
        params = {i.label: i for i in items if i.kind == CompletionItemKind.Field}
        assert set(params) == {"p", "q", "c"}
        assert params["p"].detail == "parameter: int" and params["p"].documentation.value == "parameter p"

    def test_prefix_filter(self, conf, workspace):
        text = "configuration c : m\n\ngroup g {\n\tq\n}\n"
        items = conf.complete(conf_uri(workspace, text), text, Position(line=3, character=2)).items
        assert labels(items) == ["q"]


def test_conf_server_stdio_session(workspace):
    text = "configuration c : m\n\nactivate a, b, r\n\ngroup g {\n\tp : 3\n\tzz : 1\n}\n"
    path = workspace / "c.oconf"
    path.write_text(text)
    result = run_lsp_session(
        [sys.executable, "-m", "conflspserver"], from_fs_path(str(path)), text, "oceandsl_conf",
        completion_positions=[(5, 1)], cwd=str(workspace), env=subprocess_env(ROOT),
    )
    assert result.server_name == "pygls-odsl-conf-prototype"
    assert [d.message for d in result.diagnostics] == ["Parameter zz does not exist in g"]
    assert {"p", "q", "c"} <= set(result.completions[(5, 1)])


def test_dcl_server_stdio_session(tmp_path):
    result = run_lsp_session(
        [sys.executable, "-m", "dcllspserver"], "file:///tmp/m.decl", DECLARATION.replace("requires b", "requires nope"),
        "oceandsl_dcl", completion_positions=[(0, 0)], cwd=str(tmp_path), env=subprocess_env(ROOT),
    )
    assert [d.message for d in result.diagnostics] == ["Feature nope does not exist"]
    assert result.completions[(0, 0)] == ["model"]
