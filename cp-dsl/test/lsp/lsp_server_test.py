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

import os
import pathlib
import sys
import tempfile
import unittest

from lsprotocol.types import (
    ClientCapabilities, CompletionItemKind, DiagnosticSeverity, DocumentSymbolParams, InitializeParams, Position,
    TextDocumentIdentifier, TextDocumentItem,
)
from parameterized import parameterized
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
ERROR = DiagnosticSeverity.Error
WARNING = DiagnosticSeverity.Warning
PAPER_SYNTAX = ("configuration c : m\n\ngroup g {\n\tlevels(4:5) : [ 1, 2 ]\n\tlevels(1) : 5\n"
                "\tgBaro : 9.81 m/s^2\n\tspeed : 2 km/h\n\tNx : SIZE.sNx*SIZE.nSx*SIZE.nPx\n}\n")


def labels(items):
    return [i.label for i in items]


def compare(test, test_name, comparison, expected, actual):
    """Compare labels: 'equal' (same list), 'set' (same set) or 'superset' (at least the expected labels)."""
    if comparison == "equal":
        test.assertEqual(expected, actual, test_name)
    elif comparison == "set":
        test.assertEqual(set(expected), set(actual), test_name)
    else:
        test.assertLessEqual(set(expected), set(actual), test_name)


def diagnostics_of(diagnostics):
    return [(d.message, d.severity, d.range.start.line) for d in diagnostics]


# ---------------------------------------------------------------------------------------------------------------------
# Declarations
# ---------------------------------------------------------------------------------------------------------------------

class TestDeclarationServer(unittest.TestCase):

    def setUp(self):
        self.dcl = dclLSPServer("dcl-test", "0")

    @parameterized.expand([
        ("mitgcm_mitgcm", "MITgcm/mitgcm.decl"),
        # A bundled declaration model
        # Input: input/MITgcm/mitgcm.decl
        # Expected Result: no syntax errors

        ("uvic_uvic", "UVic/uvic.decl"),
        # A bundled declaration model
        # Input: input/UVic/uvic.decl
        # Expected Result: no syntax errors

        ("testing_arrays_array", "testing/arrays/array.decl"),
        # A bundled declaration model
        # Input: input/testing/arrays/array.decl
        # Expected Result: no syntax errors

        ("testing_basic_eval", "testing/basic/eval.decl"),
        # A bundled declaration model
        # Input: input/testing/basic/eval.decl
        # Expected Result: no syntax errors

        ("testing_conditions_conditions", "testing/conditions/conditions.decl"),
        # A bundled declaration model
        # Input: input/testing/conditions/conditions.decl
        # Expected Result: no syntax errors

        ("testing_eval_array", "testing/eval/array.decl"),
        # A bundled declaration model
        # Input: input/testing/eval/array.decl
        # Expected Result: no syntax errors

        ("testing_eval_eval", "testing/eval/eval.decl"),
        # A bundled declaration model
        # Input: input/testing/eval/eval.decl
        # Expected Result: no syntax errors

        ("testing_features_eval", "testing/features/eval.decl"),
        # A bundled declaration model
        # Input: input/testing/features/eval.decl
        # Expected Result: no syntax errors

        ("testing_good_cases_only_good_cases", "testing/good-cases-only/good-cases.decl"),
        # A bundled declaration model
        # Input: input/testing/good-cases-only/good-cases.decl
        # Expected Result: no syntax errors

        ("testing_use_declared_array_use_default", "testing/use-declared-array/use_default.decl"),
        # A bundled declaration model
        # Input: input/testing/use-declared-array/use_default.decl
        # Expected Result: no syntax errors
    ])
    def test_bundled_declarations_have_no_syntax_errors(self, test_name, path):
        with open(os.path.join(INPUT, path), encoding="utf-8") as f:
            result = self.dcl.parse(f.read())
        self.assertEqual([], result.diagnostics, test_name)

    @parameterized.expand([
        ("valid_declaration", DECLARATION, []),
        # A valid declaration; 'requires b' refers to a feature declared later in the file
        # Input: the declaration model m
        # Expected Result: no diagnostics

        ("unknown_type_and_redefinition", DECLARATION.replace("def q float", "def q Unknown")
         + "group g2 : \"\" {\n\tdef v int : meter\n\tdef v int : meter\n}\n",
         [("Unknown type Unknown", ERROR, 22), ("Parameter redefined v", ERROR, 27)]),
        # Unknown types and redefined parameters are errors
        # Input: 'def q Unknown' and a group g2 that defines v twice
        # Expected Result: errors at the type in line 23 and the second v in line 28

        ("unknown_required_feature", DECLARATION.replace("requires b", "requires nope"),
         [("Feature nope does not exist", ERROR, 6)]),
        # A required feature must exist
        # Input: 'requires nope'
        # Expected Result: an error in line 7

        ("unknown_excluded_feature", DECLARATION.replace("excludes b", "excludes zz"),
         [("Feature zz does not exist", ERROR, 17)]),
        # An excluded feature must exist
        # Input: 'excludes zz'
        # Expected Result: an error in line 18

        ("unknown_enumeration_type", DECLARATION.replace("def c Color", "def c Colour"),
         [("Unknown type Colour", ERROR, 23)]),
        # A misspelled declared type
        # Input: 'def c Colour'
        # Expected Result: an error in line 24
    ])
    def test_validate(self, test_name, text, expected):
        self.assertEqual(expected, diagnostics_of(self.dcl.validate("u", text)), test_name)

    @parameterized.expand([
        ("missing_unit", "model m\ngroup g : \"\" {\n\tdef p int :\n}\n"),
        # A parameter without unit is a syntax error, no semantic errors are reported
        # Input: 'def p int :' without unit
        # Expected Result: only syntax errors

        ("missing_group_description", "model m\ngroup g {\n}\n"),
        # A group without description
        # Input: 'group g {'
        # Expected Result: only syntax errors

        ("missing_model_name", "model\n"),
        # A model without name
        # Input: 'model'
        # Expected Result: only the syntax error about the missing name
    ])
    def test_no_semantic_errors_on_syntax_errors(self, test_name, text):
        diagnostics = self.dcl.validate("u", text)
        self.assertTrue(diagnostics, test_name)
        for d in diagnostics:
            self.assertTrue(any(part in d.message for part in ("expecting", "input", "missing")),
                            f"{test_name}: {d.message}")

    @parameterized.expand([
        ("start_of_document", None, "", 0, 0, "equal", ["model"]),
        # A declaration starts with the model
        # Input: empty document, position 0:0
        # Expected Result: exactly 'model'

        ("top_level", None, "model m\n", 1, 0, "superset", ["types", "group", "feature", "required"]),
        # The top-level declarations
        # Input: 'model m', position 1:0
        # Expected Result: at least types, group, feature and required

        ("feature_reference", DECLARATION, DECLARATION.replace("requires b", "requires "), 6, 10, "superset",
         ["a", "a.a1", "a.a2", "b", "r", "x"]),
        # Features and qualified sub-features of the last valid version of the document are proposed
        # Input: 'requires ' after validating the declaration
        # Expected Result: at least a, a.a1, a.a2, b, r and x

        ("type", None, DECLARATION.replace("def q float", "def q "), 22, 7, "superset",
         ["int", "float", "string", "boolean", "Color"]),
        # Base types and declared types
        # Input: 'def q ', position 22:7
        # Expected Result: at least int, float, string, boolean and Color

        ("value_reference", None, DECLARATION.replace("def q float : second = 2", "def q float : second = "), 22, 24,
         "superset", ["p", "g.p", "ga.speed", "red", "green", "blue"]),
        # Local and qualified parameters and enumerals as values
        # Input: 'def q float : second = ', position 22:24
        # Expected Result: at least p, g.p, ga.speed, red, green and blue
    ])
    def test_completion(self, test_name, validated, text, line, character, comparison, expected):
        if validated is not None:
            self.dcl.validate("u", validated)  # last valid version of the document
        actual = labels(self.dcl.complete("u", text, Position(line=line, character=character)).items)
        compare(self, test_name, comparison, expected, actual)

    @parameterized.expand([
        ("feature", "b", "B feature"),
        # Feature proposals are documented with their description
        # Input: 'requires ' after validating the declaration, the proposal b
        # Expected Result: 'B feature'

        ("feature_with_body", "a", "A feature"),
        # A feature with body
        # Input: the proposal a
        # Expected Result: 'A feature'

        ("sub_feature", "a.a2", "second variant"),
        # A qualified sub-feature
        # Input: the proposal a.a2
        # Expected Result: 'second variant'
    ])
    def test_feature_reference_documentation(self, test_name, label, expected_documentation):
        self.dcl.validate("u", DECLARATION)
        items = self.dcl.complete("u", DECLARATION.replace("requires b", "requires "),
                                  Position(line=6, character=10)).items
        documented = {i.label: i for i in items}
        self.assertEqual(expected_documentation, documented[label].documentation.value, test_name)

    @parameterized.expand([
        ("top_level", [], ["Color", "g", "a", "b", "r", "x"], (3, 6)),
        # Types, groups and features are top-level symbols
        # Input: the declaration model m
        # Expected Result: Color, g, a, b, r and x, the first selected at 4:7

        ("group", [1], ["p", "q", "c"], (20, 6)),
        # The parameters of a group
        # Input: the group g
        # Expected Result: p, q and c, the group selected at 21:7

        ("feature", [2], ["ga", "a1", "a2"], (5, 8)),
        # Groups and sub-features of a feature
        # Input: the feature a
        # Expected Result: ga, a1 and a2, the feature selected at 6:9

        ("group_of_feature", [2, 0], ["speed"], (7, 7)),
        # The parameters of a group of a feature
        # Input: the group ga of the feature a
        # Expected Result: speed, the group selected at 8:8
    ])
    def test_outline(self, test_name, path, expected_names, expected_start):
        symbols = declaration_outline(self.dcl.parse(DECLARATION).tree)
        symbol = None
        for index in path:
            symbol = symbols[index]
            symbols = symbol.children
        self.assertEqual(expected_names, [s.name for s in symbols], test_name)
        start = (symbol or symbols[0]).selection_range.start
        self.assertEqual(Position(line=expected_start[0], character=expected_start[1]), start, test_name)

    @parameterized.expand([
        ("declaration", DECLARATION, 6),
        # The document symbol handler returns the outline
        # Input: the declaration model m
        # Expected Result: six top-level symbols

        ("model_only", "model m\n", 0),
        # A model without declarations
        # Input: 'model m'
        # Expected Result: no symbols

        ("additional_group", DECLARATION + "group g2 : \"\" {\n\tdef v int : meter\n}\n", 7),
        # Another group
        # Input: the declaration model m with the group g2
        # Expected Result: seven top-level symbols
    ])
    def test_document_symbol_handler(self, test_name, text, expected_count):
        self.dcl.lsp.lsp_initialize(InitializeParams(process_id=None, root_uri=None, capabilities=ClientCapabilities()))
        self.dcl.lsp.workspace.put_text_document(TextDocumentItem(uri="file:///m.decl", language_id="dcl", version=1,
                                                                  text=text))
        handler = self.dcl.lsp.fm.features["textDocument/documentSymbol"]
        symbols = handler(DocumentSymbolParams(text_document=TextDocumentIdentifier(uri="file:///m.decl")))
        self.assertEqual(expected_count, len(symbols), test_name)


# ---------------------------------------------------------------------------------------------------------------------
# Configurations
# ---------------------------------------------------------------------------------------------------------------------

class TestConfigurationServer(unittest.TestCase):

    def setUp(self):
        self.conf = confLSPServer("conf-test", "0")
        self.conf.lsp.lsp_initialize(InitializeParams(process_id=None, root_uri=None,
                                                      capabilities=ClientCapabilities()))
        directory = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.addCleanup(directory.cleanup)
        self.workspace = pathlib.Path(directory.name)
        (self.workspace / "m.decl").write_text(DECLARATION, encoding="utf-8")

    def conf_uri(self, text, name="c.oconf"):
        path = self.workspace / name
        path.write_text(text, encoding="utf-8")
        return from_fs_path(str(path))

    @parameterized.expand([
        ("product_of_references", lambda groups: groups[0].parameters[4].value.multiplicationExpression().right
         is not None and groups[0].parameters[4].value.getChildCount() == 1),
        # Products of parameter references (paper section 5.3)
        # Input: 'Nx : SIZE.sNx*SIZE.nSx*SIZE.nPx'
        # Expected Result: one multiplication expression with a right side

        ("unit_after_value", lambda groups: groups[0].parameters[2].unit.getText() == "m/s^2"),
        # Units after values
        # Input: 'gBaro : 9.81 m/s^2'
        # Expected Result: the unit m/s^2

        ("unit_with_prefix", lambda groups: groups[0].parameters[3].unit.getText() == "km/h"),
        # A unit with prefix
        # Input: 'speed : 2 km/h'
        # Expected Result: the unit km/h

        ("array_selectors", lambda groups: [p.getText().split(":")[0] for p in groups[0].parameters[:2]]
         == ["levels(4", "levels(1)"]),
        # Array selectors with parentheses
        # Input: 'levels(4:5) : [ 1, 2 ]' and 'levels(1) : 5'
        # Expected Result: the selectors (4:5) and (1)
    ])
    def test_paper_syntax_parses(self, test_name, check):
        result = self.conf.parse(PAPER_SYNTAX)
        self.assertEqual([], result.diagnostics, test_name)
        self.assertTrue(check(result.tree.parameterGroups), test_name)

    @parameterized.expand([
        ("features", "testing/features/eval.oconf"),
        # A configuration activating features
        # Input: input/testing/features/eval.oconf
        # Expected Result: no diagnostics

        ("basic", "testing/basic/global.oconf"),
        # A basic configuration
        # Input: input/testing/basic/global.oconf
        # Expected Result: no diagnostics

        ("arrays", "testing/arrays/array.oconf"),
        # A configuration of arrays
        # Input: input/testing/arrays/array.oconf
        # Expected Result: no diagnostics

        ("uvic", "UVic/configuration.oconf"),
        # The UVic configuration
        # Input: input/UVic/configuration.oconf
        # Expected Result: no diagnostics

        ("use_declared_array", "testing/use-declared-array/configuration.oconf"),
        # A configuration using a declared array
        # Input: input/testing/use-declared-array/configuration.oconf
        # Expected Result: no diagnostics
    ])
    def test_bundled_configurations_are_valid(self, test_name, path):
        full = os.path.join(INPUT, path)
        with open(full, encoding="utf-8") as f:
            self.assertEqual([], self.conf.validate(from_fs_path(full), f.read()), test_name)

    @parameterized.expand([
        ("advection_in_gyre", "MITgcm/tutorial_advection_in_gyre.oconf", False),
        # The configuration of the MITgcm tutorial advection in gyre
        # Input: input/MITgcm/tutorial_advection_in_gyre.oconf
        # Expected Result: no syntax errors

        ("baroclinic_gyre", "MITgcm/tutorial_baroclinic_gyre.oconf", False),
        # The configuration of the MITgcm tutorial baroclinic gyre
        # Input: input/MITgcm/tutorial_baroclinic_gyre.oconf
        # Expected Result: no syntax errors

        ("barotropic_gyre", "MITgcm/tutorial_barotropic_gyre.oconf", False),
        # The configuration of the MITgcm tutorial barotropic gyre
        # Input: input/MITgcm/tutorial_barotropic_gyre.oconf
        # Expected Result: no syntax errors

        ("cfc_offline", "MITgcm/tutorial_cfc_offline.oconf", False),
        # The configuration of the MITgcm tutorial cfc offline
        # Input: input/MITgcm/tutorial_cfc_offline.oconf
        # Expected Result: no syntax errors

        ("deep_convection", "MITgcm/tutorial_deep_convection.oconf", False),
        # The configuration of the MITgcm tutorial deep convection
        # Input: input/MITgcm/tutorial_deep_convection.oconf
        # Expected Result: no syntax errors

        ("global_oce_biogeo", "MITgcm/tutorial_global_oce_biogeo.oconf", False),
        # The configuration of the MITgcm tutorial global oce biogeo
        # Input: input/MITgcm/tutorial_global_oce_biogeo.oconf
        # Expected Result: no syntax errors

        ("global_oce_in_p", "MITgcm/tutorial_global_oce_in_p.oconf", True),
        # The configuration of the MITgcm tutorial global oce in p uses an outdated syntax (no 'configuration' header)
        # Input: input/MITgcm/tutorial_global_oce_in_p.oconf
        # Expected Result: skipped

        ("global_oce_latlon", "MITgcm/tutorial_global_oce_latlon.oconf", False),
        # The configuration of the MITgcm tutorial global oce latlon
        # Input: input/MITgcm/tutorial_global_oce_latlon.oconf
        # Expected Result: no syntax errors

        ("held_suarez_cs", "MITgcm/tutorial_held_suarez_cs.oconf", False),
        # The configuration of the MITgcm tutorial held suarez cs
        # Input: input/MITgcm/tutorial_held_suarez_cs.oconf
        # Expected Result: no syntax errors

        ("plume_on_slope", "MITgcm/tutorial_plume_on_slope.oconf", False),
        # The configuration of the MITgcm tutorial plume on slope
        # Input: input/MITgcm/tutorial_plume_on_slope.oconf
        # Expected Result: no syntax errors

        ("reentrant_channel", "MITgcm/tutorial_reentrant_channel.oconf", False),
        # The configuration of the MITgcm tutorial reentrant channel
        # Input: input/MITgcm/tutorial_reentrant_channel.oconf
        # Expected Result: no syntax errors

        ("rotating_tank", "MITgcm/tutorial_rotating_tank.oconf", False),
        # The configuration of the MITgcm tutorial rotating tank
        # Input: input/MITgcm/tutorial_rotating_tank.oconf
        # Expected Result: no syntax errors
    ])
    def test_mitgcm_tutorials_parse(self, test_name, path, outdated):
        if outdated:
            self.skipTest("file uses an outdated syntax (no 'configuration' header)")
        with open(os.path.join(INPUT, path), encoding="utf-8") as f:
            self.assertEqual([], self.conf.parse(f.read()).diagnostics, test_name)

    @parameterized.expand([
        ("unknown_elements", "configuration c : m\n\nactivate a, b, nope\n\ngroup g {\n\tp : 3\n\tmissing : 4\n}\n"
                             "group nogroup {\n}\n",
         [("Missing feature nope to activate", ERROR, 2), ("Parameter missing does not exist in g", ERROR, 6),
          ("Missing group nogroup", ERROR, 8), ("required feature r is not activated", WARNING, 0)]),
        # Unknown features, parameters and groups are errors
        # Input: 'activate a, b, nope', the unknown parameter missing and the unknown group nogroup
        # Expected Result: errors in lines 3, 7 and 9, a warning that r is not activated

        ("missing_requirement", "configuration c : m\n\nactivate a, x\n",
         [("feature a requires b, which is not activated", ERROR, 2),
          ("required feature r is not activated", WARNING, 0)]),
        # Requirements of activated features must be activated
        # Input: 'activate a, x'
        # Expected Result: an error that a requires b, a warning that r is not activated

        ("exclusion", "configuration c : m\n\nactivate a, b, x, r\n",
         [("feature x excludes b, which is activated", ERROR, 2)]),
        # Excluded features must not be activated
        # Input: 'activate a, b, x, r'
        # Expected Result: an error that x excludes b

        ("missing_required_feature", "configuration c : m\n\nactivate b\n",
         [("required feature r is not activated", WARNING, 0)]),
        # Required features should be activated
        # Input: 'activate b'
        # Expected Result: a warning that r is not activated

        ("valid", "configuration c : m\n\nactivate a, b, r\n", []),
        # A valid configuration
        # Input: 'activate a, b, r'
        # Expected Result: no diagnostics
    ])
    def test_validate(self, test_name, text, expected):
        self.assertEqual(expected, diagnostics_of(self.conf.validate(self.conf_uri(text), text)), test_name)

    @parameterized.expand([
        ("missing_declaration_model", "configuration c : unknown\n",
         "declaration model 'unknown' not found: expected unknown.decl next to this configuration", (0, 18)),
        # The declaration model is expected next to the configuration
        # Input: 'configuration c : unknown' without unknown.decl
        # Expected Result: one error at the model name

        ("other_model_name", "configuration c : ocean\n",
         "declaration model 'ocean' not found: expected ocean.decl next to this configuration", (0, 18)),
        # Another missing model
        # Input: 'configuration c : ocean' without ocean.decl
        # Expected Result: one error naming ocean.decl

        ("other_configuration_name", "configuration longer_name : unknown\n",
         "declaration model 'unknown' not found: expected unknown.decl next to this configuration", (0, 28)),
        # The error marks the model name
        # Input: 'configuration longer_name : unknown'
        # Expected Result: one error at the model name in column 29
    ])
    def test_missing_declaration_model(self, test_name, text, expected_message, expected_start):
        diagnostics = self.conf.validate(self.conf_uri(text), text)
        self.assertEqual([expected_message], [d.message for d in diagnostics], test_name)
        self.assertEqual(Position(line=expected_start[0], character=expected_start[1]), diagnostics[0].range.start,
                         test_name)

    @parameterized.expand([
        ("unsaved_declaration_buffer", DECLARATION.replace("group g :", "group renamed :"), None,
         "configuration c : m\n\nactivate a, b, r\ngroup renamed {\n\tp : 1\n}\n", []),
        # An open, unsaved declaration is used instead of the file
        # Input: the declaration buffer with the group renamed, a configuration of renamed
        # Expected Result: no diagnostics

        ("declaration_problems_are_summarized", None, DECLARATION.replace("requires b", "requires nope"),
         "configuration c : m\n\nactivate b, r\n", [(WARNING, "Feature nope does not exist")]),
        # Problems of the declaration are summarized as a warning
        # Input: a declaration file with 'requires nope'
        # Expected Result: one warning mentioning the problem

        ("problems_of_unsaved_buffer", DECLARATION.replace("requires b", "requires nope"), None,
         "configuration c : m\n\nactivate b, r\n", [(WARNING, "Feature nope does not exist")]),
        # Problems of the open declaration are summarized as well
        # Input: a declaration buffer with 'requires nope'
        # Expected Result: one warning mentioning the problem
    ])
    def test_declaration_source(self, test_name, buffer, file, text, expected):
        if buffer is not None:
            self.conf.lsp.workspace.put_text_document(TextDocumentItem(
                uri=from_fs_path(str(self.workspace / "m.decl")), language_id="dcl", version=1, text=buffer))
        if file is not None:
            (self.workspace / "m.decl").write_text(file, encoding="utf-8")

        diagnostics = self.conf.validate(self.conf_uri(text), text)

        self.assertEqual([severity for severity, _ in expected], [d.severity for d in diagnostics], test_name)
        for (_, part), diagnostic in zip(expected, diagnostics):
            self.assertIn(part, diagnostic.message, test_name)

    @parameterized.expand([
        ("features", "configuration c : m\n\nactivate ", 2, 9, None, "superset", ["a", "b", "r", "x"]),
        # The features of the declaration can be activated
        # Input: 'activate ', position 2:9
        # Expected Result: at least a, b, r and x

        ("sub_features", "configuration c : m\n\nfeature a {\n\tactivate \n}\n", 3, 10, None, "superset",
         ["a1", "a2"]),
        # Sub-features in the scope of a feature
        # Input: 'activate ' in 'feature a { }', position 3:10
        # Expected Result: at least a1 and a2

        ("group_of_feature", "configuration c : m\n\nfeature a {\n\tgroup \n}\n", 3, 7, None, "equal", ["ga"]),
        # The groups of a feature
        # Input: 'group ' in 'feature a { }', position 3:7
        # Expected Result: exactly ga

        ("group", "configuration c : m\n\ngroup \n", 2, 6, None, "equal", ["g"]),
        # The top-level groups
        # Input: 'group ', position 2:6
        # Expected Result: exactly g

        ("parameters", "configuration c : m\n\ngroup g {\n\t\n}\n", 3, 1, CompletionItemKind.Field, "set",
         ["p", "q", "c"]),
        # The parameters of a group
        # Input: an empty line in 'group g { }', position 3:1
        # Expected Result: the fields p, q and c

        ("prefix_filter", "configuration c : m\n\ngroup g {\n\tq\n}\n", 3, 2, None, "equal", ["q"]),
        # A typed prefix filters the proposals
        # Input: 'q' in 'group g { }', position 3:2
        # Expected Result: exactly q

        ("feature_prefix", "configuration c : m\n\nactivate b", 2, 10, None, "equal", ["b"]),
        # A typed prefix filters the features
        # Input: 'activate b', position 2:10
        # Expected Result: exactly b
    ])
    def test_completion(self, test_name, text, line, character, kind, comparison, expected):
        items = self.conf.complete(self.conf_uri(text), text, Position(line=line, character=character)).items
        compare(self, test_name, comparison, expected, labels(i for i in items if kind is None or i.kind == kind))

    @parameterized.expand([
        ("feature_documentation", "configuration c : m\n\nactivate ", 2, 9, "a",
         (CompletionItemKind.Module, "feature", "A feature")),
        # Feature proposals carry their description
        # Input: 'activate ', the proposal a
        # Expected Result: a module 'feature' documented with 'A feature'

        ("required_feature_detail", "configuration c : m\n\nactivate ", 2, 9, "r",
         (CompletionItemKind.Module, "required feature", "R feature")),
        # Required features are marked
        # Input: 'activate ', the proposal r
        # Expected Result: a module 'required feature' documented with 'R feature'

        ("group_documentation", "configuration c : m\n\ngroup \n", 2, 6, "g",
         (CompletionItemKind.Struct, "parameter group", "General group")),
        # Group proposals are structs with their description
        # Input: 'group ', the proposal g
        # Expected Result: a struct 'parameter group' documented with 'General group'

        ("parameter_documentation", "configuration c : m\n\ngroup g {\n\t\n}\n", 3, 1, "p",
         (CompletionItemKind.Field, "parameter: int", "parameter p")),
        # Parameter proposals show their type and description
        # Input: an empty line in 'group g { }', the proposal p
        # Expected Result: a field 'parameter: int' documented with 'parameter p'

        ("parameter_without_description", "configuration c : m\n\ngroup g {\n\t\n}\n", 3, 1, "q",
         (CompletionItemKind.Field, "parameter: float", None)),
        # A parameter without description
        # Input: an empty line in 'group g { }', the proposal q
        # Expected Result: a field 'parameter: float' without documentation
    ])
    def test_completion_details(self, test_name, text, line, character, label, expected):
        items = self.conf.complete(self.conf_uri(text), text, Position(line=line, character=character)).items
        item = {i.label: i for i in items}[label]
        documentation = item.documentation.value if item.documentation else None
        self.assertEqual(expected, (item.kind, item.detail, documentation), test_name)


# ---------------------------------------------------------------------------------------------------------------------
# Language servers as processes
# ---------------------------------------------------------------------------------------------------------------------

class TestStdioSessions(unittest.TestCase):

    @parameterized.expand([
        ("configuration_with_unknown_parameter", "conflspserver", "oceandsl_conf", "c.oconf",
         "configuration c : m\n\nactivate a, b, r\n\ngroup g {\n\tp : 3\n\tzz : 1\n}\n", (5, 1),
         ["Parameter zz does not exist in g"], ["p", "q", "c"]),
        # The configuration server runs as a process and talks LSP over stdio
        # Input: a configuration with the unknown parameter zz, completion in the group g
        # Expected Result: one error about zz, the parameters p, q and c are proposed

        ("valid_configuration", "conflspserver", "oceandsl_conf", "c.oconf",
         "configuration c : m\n\nactivate a, b, r\n\ngroup g {\n\tp : 3\n\t\n}\n", (6, 1), [], ["p", "q", "c"]),
        # A valid configuration
        # Input: a configuration of p, completion in the group g
        # Expected Result: no diagnostics, the parameters p, q and c are proposed

        ("declaration_with_unknown_feature", "dcllspserver", "oceandsl_dcl", "m2.decl",
         DECLARATION.replace("requires b", "requires nope"), (0, 0), ["Feature nope does not exist"], ["model"]),
        # The declaration server runs as a process and talks LSP over stdio
        # Input: a declaration with 'requires nope', completion at the start
        # Expected Result: one error about nope, the keyword model is proposed

        ("valid_declaration", "dcllspserver", "oceandsl_dcl", "m2.decl", DECLARATION, (0, 0), [], ["model"]),
        # A valid declaration
        # Input: the declaration model m, completion at the start
        # Expected Result: no diagnostics, the keyword model is proposed
    ])
    def test_stdio_session(self, test_name, module, language, file_name, text, position, expected_messages,
                           expected_labels):
        with tempfile.TemporaryDirectory() as directory:
            workspace = pathlib.Path(directory)
            (workspace / "m.decl").write_text(DECLARATION, encoding="utf-8")
            path = workspace / file_name
            path.write_text(text, encoding="utf-8")
            result = run_lsp_session(
                [sys.executable, "-m", module], from_fs_path(str(path)), text, language,
                completion_positions=[position], cwd=directory, env=subprocess_env(ROOT),
            )

        self.assertEqual(expected_messages, [d.message for d in result.diagnostics], test_name)
        if module == "conflspserver":
            self.assertEqual("pygls-odsl-conf-prototype", result.server_name, test_name)
            self.assertLessEqual(set(expected_labels), set(result.completions[position]), test_name)
        else:
            self.assertEqual(expected_labels, result.completions[position], test_name)


if __name__ == '__main__':
    unittest.main()
