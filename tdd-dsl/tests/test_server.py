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
import pathlib
import tempfile
import unittest

from lsprotocol.types import (
    ClientCapabilities, CompletionItemKind, DiagnosticSeverity, DidSaveTextDocumentParams, InitializeParams, Position,
    TextDocumentIdentifier, TextDocumentItem,
)
from parameterized import parameterized

from odsllib.lsp.semantic_tokens import TOKEN_TYPES
from tddlspserver.server import TDDLSPServer, did_save

DATA = os.path.join(os.path.dirname(__file__), "data")
URI = "file:///work/suite.tdd"


def read(name):
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return f.read()


def suite(body: str, src: str = "src") -> str:
    return f"suite su:\ntest t1:\n    srcpath: '{src}'\n{body}"


LISTING1 = read("paper_listing1.tdd")
LISTING1_SRC = LISTING1.replace("'tdd-dsl/input/tdd_dev/UVic_example_opem'", "'src'")
ASSERT_TRUE = suite("    assert True:\n        in:\n            1\n        out:\n            1\n")
TWO_CASES = ASSERT_TRUE + "test t2:\n    srcpath: 'src'\n    assert False:\n        in:\n            0\n" \
                          "        out:\n            0\n"
WITH_MODULE = suite("    modules:\n        mod_a\n    assert True:\n        in:\n            1\n        out:\n"
                    "            1\n")
DUPLICATE_CASE = suite("    var:\n        x: real = 1D0\n    assert Equal:\n        in:\n            x\n        out:\n"
                       "            1D0\n") + "test t1:\n    srcpath: 'src'\n"
CMAKE_FILES = ["src/CMakeLists.txt", "src/build_with_cmake_and_run.x", "src/tests/CMakeLists.txt"]


class TestServer(unittest.TestCase):
    """Base class with a TDD-DSL language server working in a temporary directory."""

    def setUp(self):
        directory = tempfile.TemporaryDirectory()  # pylint: disable=consider-using-with
        self.addCleanup(directory.cleanup)
        self.tmp_path = pathlib.Path(directory.name)

        self.server = TDDLSPServer("tdd-test", "0")
        self.server.work_path = str(self.tmp_path)
        self.server.fxtran_path = "fxtran-not-installed"
        self.server.lsp.lsp_initialize(InitializeParams(process_id=None, root_uri=None,
                                                        capabilities=ClientCapabilities()))
        self.server.published = []
        self.server.publish_diagnostics = lambda uri, diagnostics, *a, **k: self.server.published.append(
            (uri, diagnostics))
        self.server.show_message = lambda *a, **k: None

    def make_dirs(self, *directories: str):
        for directory in directories:
            (self.tmp_path / directory).mkdir(parents=True, exist_ok=True)

    def generated_files(self):
        return sorted(f.relative_to(self.tmp_path).as_posix() for f in self.tmp_path.rglob("*") if f.is_file())


class TestDiagnostics(TestServer):

    @parameterized.expand([
        ("paper_example_without_source_path", LISTING1, [],
         [(DiagnosticSeverity.Information, "source path 'tdd-dsl/input/tdd_dev/UVic_example_opem' does not exist; "
                                           "new modules will be created there", (3, 13), (3, 54))]),
        # A valid paper example whose source path is missing only gets an information
        # Input: paper Listing 1, its source path does not exist
        # Expected Result: one information that the source path does not exist

        ("missing_source_path", suite(""), [],
         [(DiagnosticSeverity.Information, "source path 'src' does not exist; new modules will be created there",
           (2, 13), (2, 18))]),
        # The information marks the source path
        # Input: a test case with the source path 'src' that does not exist
        # Expected Result: an information at 'src'

        ("existing_source_path", suite(""), ["src"], []),
        # An existing source path is accepted
        # Input: a test case with the existing source path 'src'
        # Expected Result: no diagnostics

        ("syntax_error", suite("    assert Foo:\n"), ["src"],
         [(DiagnosticSeverity.Error, "no viable alternative at input 'assert Foo'", (3, 11), (3, 14))]),
        # A syntax error is reported at the offending token
        # Input: 'assert Foo:'
        # Expected Result: an error at 'Foo'

        ("duplicate_test_cases", suite("") + "test t1:\n    srcpath: 'src'\n", ["src"],
         [(DiagnosticSeverity.Error, "duplicate test case 't1'", (3, 5), (3, 7))]),
        # Test case names are unique
        # Input: two test cases named t1
        # Expected Result: an error at the name of the second test case

        ("duplicate_variables", suite("    var:\n        x: real = 1D0\n        x: real = 2D0\n"), ["src"],
         [(DiagnosticSeverity.Error, "duplicate variable 'x' in test case 't1'", (5, 8), (5, 9))]),
        # Variable names are unique within a test case
        # Input: the variable x declared twice
        # Expected Result: an error at the second declaration

        ("distinct_variables", suite("    var:\n        x: real = 1D0\n        y: real = 2D0\n"), ["src"], []),
        # Different variables are accepted
        # Input: the variables x and y
        # Expected Result: no diagnostics
    ])
    def test_validate(self, test_name, text, directories, expected):
        self.make_dirs(*directories)

        diagnostics = self.server.validate(URI, text)

        self.assertEqual(expected, [(d.severity, d.message, (d.range.start.line, d.range.start.character),
                                     (d.range.end.line, d.range.end.character)) for d in diagnostics], test_name)


class TestGeneration(TestServer):

    @parameterized.expand([
        ("paper_example_on_save", "save", LISTING1_SRC, ["src/cfo_example.f90", "src/tests/test_fT_ME.pf"],
         {"src/tests/test_fT_ME.pf": ["@assertEqual( 0D0, fT_ME ( xIntercept ), message='fails x-Intercept at "
                                      "14.89D0', tolerance=1D-12)", "use cfo_example"],
          "src/cfo_example.f90": ["FUNCTION fT_ME"]}),
        # Saving publishes the diagnostics and generates the pFUnit test, the SUT template and the CMake setup
        # Input: paper Listing 1 with the existing source path 'src', saved in the client
        # Expected Result: no diagnostics, test_fT_ME.pf with the assertion, cfo_example.f90 with FUNCTION fT_ME

        ("assert_true_on_save", "save", ASSERT_TRUE, ["src/tests/t1.pf"], {"src/tests/t1.pf": ["@assertTrue( 1, 1)"]}),
        # The pFUnit file is named after the test case
        # Input: test case t1 with 'assert True', saved in the client
        # Expected Result: t1.pf with @assertTrue

        ("two_test_cases_on_save", "save", TWO_CASES, ["src/tests/t1.pf", "src/tests/t2.pf"],
         {"src/tests/t2.pf": ["@assertFalse"]}),
        # Each test case gets its own pFUnit file
        # Input: test cases t1 and t2, saved in the client
        # Expected Result: t1.pf and t2.pf

        ("paper_example_cli", "cli", LISTING1_SRC, ["src/cfo_example.f90", "src/tests/test_fT_ME.pf"],
         {"src/tests/test_fT_ME.pf": ["use cfo_example"]}),
        # 'tdd_dsl -f suite.tdd' generates the files without an LSP client
        # Input: paper Listing 1 given as input file
        # Expected Result: test_fT_ME.pf, cfo_example.f90 and the CMake setup

        ("assert_true_cli", "cli", ASSERT_TRUE, ["src/tests/t1.pf"], {"src/tests/t1.pf": ["SUBROUTINE t1()"]}),
        # The pFUnit file is named after the test case
        # Input: test case t1 with 'assert True' given as input file
        # Expected Result: t1.pf with the test subroutine t1

        ("module_template_cli", "cli", WITH_MODULE, ["src/mod_a.f90", "src/tests/t1.pf"],
         {"src/tests/t1.pf": ["use mod_a"], "src/mod_a.f90": ["MODULE mod_a"]}),
        # A Fortran template is generated for a module under test that does not exist
        # Input: test case t1 using the module mod_a given as input file
        # Expected Result: mod_a.f90 with MODULE mod_a, t1.pf uses mod_a
    ])
    def test_generation(self, test_name, mode, text, expected_files, expected_contents):
        self.make_dirs("src")
        path = self.tmp_path / "suite.tdd"
        path.write_text(text, encoding="utf-8")

        if mode == "save":
            uri = path.as_uri()
            self.server.lsp.workspace.put_text_document(TextDocumentItem(uri=uri, language_id="tdd", version=1,
                                                                         text=text))
            self.server.on_did_save(DidSaveTextDocumentParams(text_document=TextDocumentIdentifier(uri=uri)))
            self.assertEqual((uri, []), self.server.published[-1], test_name)
        else:
            cli_server = TDDLSPServer("tdd-cli-test", "0")
            cli_server.work_path = str(self.tmp_path)
            cli_server.input_path = str(path)
            did_save(cli_server, None)

        self.assertEqual(sorted(CMAKE_FILES + expected_files + ["suite.tdd"]), self.generated_files(), test_name)
        for file_name, parts in expected_contents.items():
            content = (self.tmp_path / file_name).read_text(encoding="utf-8")
            for part in parts:
                self.assertIn(part, content, f"{test_name}: {file_name}")


class TestCompletion(TestServer):

    def labels(self, text, line, character, kind=None):
        items = self.server.complete(URI, text, Position(line=line, character=character)).items
        return [i.label for i in items if kind is None or i.kind == kind]

    @parameterized.expand([
        ("start_of_document", "", 0, 0, "equal", ["suite"]),
        # An empty document starts with a suite
        # Input: empty document, position 0:0
        # Expected Result: exactly 'suite'

        ("after_suite_header", "suite su:\n", 1, 0, "equal", ["test"]),
        # A suite contains test cases
        # Input: 'suite su:', position 1:0
        # Expected Result: exactly 'test'

        ("test_case_header", "suite su:\ntest t1:\n", 2, 4, "set", {"srcpath", "overwrite"}),
        # A test case starts with its source path or overwrite flags
        # Input: test case header, position 2:4
        # Expected Result: 'srcpath' and 'overwrite'

        ("test_case_sections", suite("    "), 3, 4, "superset", {"var", "modules", "assert", "test"}),
        # The sections of a test case
        # Input: a test case after its source path, position 3:4
        # Expected Result: at least 'var', 'modules', 'assert' and 'test'

        ("overwrite_flags", "suite su:\ntest t1:\n    overwrite: ", 2, 15, "set", {"pf", "cmake", "f90"}),
        # The files that may be overwritten
        # Input: 'overwrite: ', position 2:15
        # Expected Result: 'pf', 'cmake' and 'f90'

        ("assertion_directives", suite("    assert "), 3, 11, "superset",
         {"Equal", "NotEqual", "LessThan", "True", "IsNaN"}),
        # The pFUnit assertion directives
        # Input: 'assert ', position 3:11
        # Expected Result: at least 'Equal', 'NotEqual', 'LessThan', 'True' and 'IsNaN'

        ("call_in_assertion", LISTING1, 12, 12, "superset", {"call"}),
        # Keywords of the assertion input
        # Input: paper Listing 1, position 12:12 in an assertion
        # Expected Result: at least 'call'

        ("typed_prefix_filters_case_insensitive", LISTING1.replace("fT_ME(xIntercept), K", "XI"), 12, 14, "equal",
         ["xIntercept"]),
        # A typed prefix filters the proposals case-insensitively
        # Input: 'XI' typed in the assertion, position 12:14
        # Expected Result: exactly 'xIntercept'

        ("modules", suite("    modules:\n        mod_a\n        "), 5, 8, "superset", {"mod_a"}),
        # Declared modules are proposed
        # Input: a module section with mod_a, position 5:8
        # Expected Result: at least 'mod_a'

        ("duplicate_test_case_does_not_break_completion", DUPLICATE_CASE, 7, 12, "superset", {"x"}),
        # The symbol table used to raise DuplicateSymbolError, which disabled all symbol completions
        # Input: a test case with the variable x and a second test case t1, position 7:12 in the assertion
        # Expected Result: at least 'x'
    ])
    def test_completion(self, test_name, text, line, character, comparison, expected):
        labels = self.labels(text, line, character)
        if comparison == "equal":
            self.assertEqual(expected, labels, test_name)
        elif comparison == "set":
            self.assertEqual(expected, set(labels), test_name)
        else:
            self.assertLessEqual(expected, set(labels), test_name)

    @parameterized.expand([
        ("test_variables", LISTING1, 12, 12, CompletionItemKind.Variable, {"dp", "xIntercept", "yIntercept"}),
        # The variables of the test case are proposed in an assertion
        # Input: paper Listing 1, position 12:12 in an assertion
        # Expected Result: the variables dp, xIntercept and yIntercept

        ("suite_keyword", "", 0, 0, CompletionItemKind.Keyword, {"suite"}),
        # Keywords are proposed as keywords
        # Input: empty document, position 0:0
        # Expected Result: the keyword 'suite'

        ("operators_in_assertion", LISTING1, 12, 12, CompletionItemKind.Operator, {"-", "(", "+"}),
        # Operators are proposed in an assertion
        # Input: paper Listing 1, position 12:12 in an assertion
        # Expected Result: the operators '-', '(' and '+'
    ])
    def test_completion_kinds(self, test_name, text, line, character, kind, expected):
        self.assertEqual(expected, set(self.labels(text, line, character, kind)), test_name)

    @parameterized.expand([
        ("directories", "models/", 21, ["mitgcm", "uvic"]),
        # The directories in the source path are proposed, without hidden directories and files
        # Input: 'models/' with uvic, mitgcm, .hidden and file.f90
        # Expected Result: 'mitgcm' and 'uvic'

        ("prefix", "models/u", 22, ["uvic"]),
        # A typed prefix filters the directories
        # Input: 'models/u'
        # Expected Result: 'uvic'

        ("work_path", "", 14, ["models"]),
        # An empty source path proposes the directories of the work path
        # Input: ''
        # Expected Result: 'models'

        ("no_match", "models/x", 22, []),
        # No directory matches
        # Input: 'models/x'
        # Expected Result: no proposals
    ])
    def test_source_path_directories(self, test_name, srcpath, character, expected):
        self.make_dirs("models/uvic", "models/mitgcm", "models/.hidden")
        (self.tmp_path / "models" / "file.f90").write_text("", encoding="utf-8")

        text = f"suite su:\ntest t1:\n    srcpath: '{srcpath}'\n"
        self.assertEqual(expected, self.labels(text, 2, character, CompletionItemKind.Folder), test_name)


class TestSemanticTokens(TestServer):

    @parameterized.expand([
        ("keywords_strings_and_numbers", "suite su:\ntest t1:\n    srcpath: 'src'\n    var:\n        x: real = 1D0\n",
         ["keyword", "operator", "keyword", "operator", "keyword", "operator", "string", "keyword", "operator",
          "operator", "operator", "number"]),
        # Keywords, strings and numbers are classified
        # Input: a test case with the source path 'src' and the variable x = 1D0
        # Expected Result: 'suite' is a keyword, 'src' a string and 1D0 a number

        ("suite_header", "suite su:\n", ["keyword", "operator"]),
        # The suite header
        # Input: 'suite su:'
        # Expected Result: the keyword 'suite' and the operator ':'

        ("overwrite_flags", "suite su:\ntest t1:\n    overwrite: pf\n",
         ["keyword", "operator", "keyword", "operator", "keyword", "operator", "keyword"]),
        # Overwrite flags are keywords
        # Input: 'overwrite: pf'
        # Expected Result: 'pf' is a keyword
    ])
    def test_semantic_tokens(self, test_name, text, expected_kinds):
        data = self.server.semantic_tokens(text).data
        kinds = [TOKEN_TYPES[data[i + 3]] for i in range(0, len(data), 5)]
        self.assertEqual(expected_kinds, kinds, test_name)


if __name__ == '__main__':
    unittest.main()
