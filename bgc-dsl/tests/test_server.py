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

import logging
import os
import sys
import tempfile
import unittest

from lsprotocol.types import CompletionItemKind, DiagnosticSeverity, Position
from parameterized import parameterized

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
WITHOUT_FROM = MODEL.replace("from Phy to Ki", "Phy to Ki")
WITHOUT_STATES = MODEL.replace("states N P", "states")
DECLARED_NAMES = {"N", "P", "growth", "Phy", "Ki"}


def read(name):
    with open(os.path.join(INPUT, name), encoding="utf-8") as f:
        return f.read()


class TestServer(unittest.TestCase):

    def setUp(self):
        self.server = bgcLSPServer("bgc-test", "0")

    def labels(self, text, line, character, kind=None):
        items = self.server.complete("u", text, Position(line=line, character=character)).items
        return [i.label for i in items if kind is None or i.kind == kind]

    @parameterized.expand([
        ("example", read("example.bgc"), []),
        # The example model is valid
        # Input: input/example.bgc
        # Expected Result: no diagnostics

        ("example1", read("example1.bgc"), []),
        # The example model 1 is valid
        # Input: input/example1.bgc
        # Expected Result: no diagnostics

        ("example2", read("example2.bgc"), []),
        # The example model 2 is valid
        # Input: input/example2.bgc
        # Expected Result: no diagnostics

        ("connection_requires_from", WITHOUT_FROM, [(DiagnosticSeverity.Error, "missing 'from' at 'Phy'", 22, 30)]),
        # A connection names its source compartment after 'from'
        # Input: 'connection assimilation(N, P) Phy to Ki'
        # Expected Result: an error at 'Phy' in line 23

        ("states_require_names", WITHOUT_STATES, [(DiagnosticSeverity.Error, "extraneous input 'update' expecting ID",
                                                   12, 4)]),
        # A states declaration lists the states
        # Input: 'states' without names
        # Expected Result: an error at the following 'update'

        ("model_requires_name", MODEL.replace("model bgc", "model"),
         [(DiagnosticSeverity.Error, "missing ID at 'substances'", 2, 0)]),
        # The model has a name
        # Input: 'model' without name
        # Expected Result: an error at 'substances'

        ("compartment_requires_body", MODEL.replace("compartment Ki {", "compartment Ki"),
         [(DiagnosticSeverity.Error, "expecting {'extends', '{'}", 17, 4)]),
        # A compartment has a body
        # Input: 'compartment Ki' without '{'
        # Expected Result: an error at the first statement of the compartment
    ])
    def test_validate(self, test_name, text, expected):
        diagnostics = self.server.validate("file:///" + test_name, text)
        self.assertEqual(expected, [(d.severity, d.message, d.range.start.line, d.range.start.character)
                                    for d in diagnostics], test_name)

    @parameterized.expand([
        ("keyword_at_start", "", 0, 0, None, "equal", ["model"]),
        # A model starts with the keyword model
        # Input: empty document, position 0:0
        # Expected Result: exactly 'model'

        ("types_in_substances", "model mymodel\n\nsubstances\n    ", 3, 4, None, "superset",
         {"int", "float", "double", "string"}),
        # Substances are declared with a type
        # Input: an empty substances section, position 3:4
        # Expected Result: at least int, float, double and string

        ("declared_names", MODEL, 12, 24, CompletionItemKind.Variable, "superset", DECLARED_NAMES),
        # References offer the declared substances, parameters and compartments
        # Input: 'update N = growth * |N', position 12:24
        # Expected Result: at least N, P, growth, Phy and Ki as variables

        ("filtered_by_prefix", MODEL.replace("update N = growth * N", "update N = gr"), 12, 17, None, "equal",
         ["growth"]),
        # A typed prefix filters the references
        # Input: 'update N = gr', position 12:17
        # Expected Result: exactly 'growth'

        ("filtered_by_capital_prefix", MODEL.replace("update N = growth * N", "update N = P"), 12, 16, None,
         "equal", ["P", "Phy"]),
        # A prefix matches several names
        # Input: 'update N = P', position 12:16
        # Expected Result: exactly 'P' and 'Phy'

        ("functions_in_expression", MODEL, 12, 24, CompletionItemKind.Keyword, "superset", {"exp", "inverse", "max"}),
        # Expressions offer the built-in functions
        # Input: 'update N = growth * |N', position 12:24
        # Expected Result: at least exp, inverse and max as keywords
    ])
    def test_completion(self, test_name, text, line, character, kind, comparison, expected):
        labels = self.labels(text, line, character, kind)
        if comparison == "equal":
            self.assertEqual(expected, labels, test_name)
        else:
            self.assertLessEqual(expected, set(labels), test_name)

    @parameterized.expand([
        ("declared_names_have_no_spaces", MODEL, 12, 24),
        # Connections are stored as 'name from A to B', but only plain names are offered
        # Input: 'update N = growth * |N', position 12:24
        # Expected Result: no proposal contains a space

        ("connection_body", MODEL, 23, 8),
        # The same holds inside a connection
        # Input: position 23:8 in the connection body
        # Expected Result: no proposal contains a space

        ("filtered", MODEL.replace("update N = growth * N", "update N = P"), 12, 16),
        # And for filtered proposals
        # Input: 'update N = P', position 12:16
        # Expected Result: no proposal contains a space
    ])
    def test_completion_offers_plain_names(self, test_name, text, line, character):
        variables = self.labels(text, line, character, CompletionItemKind.Variable)
        self.assertTrue(variables, test_name)
        self.assertFalse([label for label in variables if " " in label], test_name)

    @parameterized.expand([
        ("missing_states", WITHOUT_STATES, ["broken.bgc:13:5: extraneous input 'update' expecting ID"]),
        # The command line check logs syntax errors with file, line and column
        # Input: a model whose states declaration lacks the names
        # Expected Result: an error at 13:5

        ("missing_from", WITHOUT_FROM, ["broken.bgc:23:31: missing 'from' at 'Phy'"]),
        # Another syntax error
        # Input: a model whose connection lacks 'from'
        # Expected Result: an error at 23:31

        ("valid_model", MODEL, []),
        # A valid model
        # Input: the valid model
        # Expected Result: no errors
    ])
    def test_cli_check(self, test_name, text, expected_messages):
        with tempfile.TemporaryDirectory() as directory:
            path = os.path.join(directory, "broken.bgc")
            with open(path, "w", encoding="utf-8") as f:
                f.write(text)
            server = bgcLSPServer("bgc-cli", "0")
            server.input_path = path

            with self.assertLogs(level="DEBUG") as logs:
                logging.getLogger(__name__).debug("check %s", path)  # a valid model logs nothing
                did_save(server, None)

        errors = [r.getMessage() for r in logs.records if r.levelname == "ERROR"]
        self.assertEqual(len(expected_messages), len(errors), f"{test_name}: {errors}")
        for expected, message in zip(expected_messages, errors):
            self.assertTrue(message.endswith(expected), f"{test_name}: {message}")

    @parameterized.expand([
        ("valid_model", MODEL, (12, 24), [], {"growth"}),
        # The server runs as a process and talks LSP over stdio
        # Input: the valid model, completion at 'update N = growth * |N'
        # Expected Result: no diagnostics, growth is proposed

        ("syntax_error", WITHOUT_FROM, (12, 24), [DiagnosticSeverity.Error], {"growth"}),
        # Diagnostics are published
        # Input: a model whose connection lacks 'from'
        # Expected Result: one error, completion still works

        ("empty_document", "", (0, 0), None, {"model"}),
        # An empty document
        # Input: an empty document, completion at its start
        # Expected Result: the keyword model is proposed
    ])
    def test_stdio_session(self, test_name, text, position, expected_severities, expected_labels):
        with tempfile.TemporaryDirectory() as directory:
            result = run_lsp_session(
                [sys.executable, "-m", "bgclspserver"], "file:///tmp/m.bgc", text, "oceandsl_bgc",
                completion_positions=[position], cwd=directory, env=subprocess_env(ROOT),
            )

        self.assertEqual("pygls-odsl-bgc-prototype", result.server_name, test_name)
        if expected_severities is not None:
            self.assertEqual(expected_severities, [d.severity for d in result.diagnostics], test_name)
        self.assertLessEqual(expected_labels, set(result.completions[position]), test_name)
        if text:
            self.assertTrue(result.semantic_tokens, test_name)


if __name__ == '__main__':
    unittest.main()
