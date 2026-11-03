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
"""Language server of the TDD-DSL.

Features (cf. Gundlach et al., "Facilitating Test-Driven Development via Domain-Specific Languages in Computational
Science Software Engineering"):

* syntax diagnostics and high-level checks of the test specification (unique test case and variable names,
  existence of the source path),
* content assist: DSL keywords, variables/functions/routines of the test case and the system under test (SUT, parsed
  with fxtran), modules, and source paths,
* generation of pFUnit, Fortran and CMake files when a test specification is saved (also available via the CLI),
* recommendation of SUTs to test based on complexity metrics (``recommendSUT`` command).
"""

from __future__ import annotations

import os
from logging import getLogger
from typing import Dict, List, Optional, Tuple

from antlr4 import FileStream, InputStream
from lsprotocol.types import (
    CompletionItem, CompletionItemKind, Diagnostic, DiagnosticSeverity, DidSaveTextDocumentParams, MessageType,
)
from pygls.workspace import Document

from odsllib.code_completion_core import CandidatesCollection
from odsllib.lsp.compute_token_index import TokenPosition
from odsllib.lsp.diagnostic_listener import token_range
from odsllib.lsp.parsing import ParseResult
from odsllib.lsp.server import AntlrLanguageServer

from .cst.calculate_complexity_visitor import ComplexityMetricVisitor
from .cst.cmake_file_generator_visitor import CMakeFileGeneratorVisitor
from .cst.f90_file_generator_visitor import F90FileGeneratorVisitor
from .cst.pf_file_generator_visitor import PFFileGeneratorVisitor
from .cst.symbol_table_visitor import SymbolTableVisitor
from .gen.python.TestSuite.TestSuiteLexer import TestSuiteLexer
from .gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from odsllib.symbol_table import RoutineSymbol, VariableSymbol
from .symboltable.symbol_table import MetricSymbol, ModuleSymbol
from .utils.suggest_variables import suggest_symbols

LOG = getLogger(__name__)


class TDDLSPServer(AntlrLanguageServer):
    CMD_RECOMMEND_SUT_BLOCKING = "recommendSUT"

    CONFIGURATION_SECTION = "ODsl-TDD-DSL-Server"

    # Number of SuT to return for metric calculation
    N_SHOW_METRICS = 3

    # Write metric tables to a file instead of showing the top entries (enabled by the CLI option --debug)
    SHOW_DEBUG_OUTPUT: bool = False
    DEBUG_OUTPUT_SEPERATOR: str = "\t"
    DEBUG_HEADER: str = DEBUG_OUTPUT_SEPERATOR.join([
        "Scope", "Source", "Cyclomatic Complexity", "Depth", "LOC", "Parameters", "Conditionals", "Loops",
        "Branches", "Variables", "Returns", "Calls", "Decision Points", "Halstead Complexity", "(d)Operators ηT",
        "(d)Operands ηD", "(t)Operators NT", "(t)Operands ND", "Operator ratio nNT", "Operands ratio nND",
        "Vocabulary (ηT + ηD)", "Program Length (NT + ND)", "Calculated Length", "Volume", "Difficulty", "Effort",
        "Time to program", "delivered bugs", "Test Score", "Testability Difficulty", "Testability Index",
        "Normalized Testability Difficulty", "Aggregated Testability Difficulty", "Test Index",
        "Normalized Test Score", "Aggregated Test Score", "Test Factor"
    ])

    LOG = LOG

    lexer_class = TestSuiteLexer
    parser_class = TestSuiteParser
    start_rule = "testSuite"
    preferred_rules = {TestSuiteParser.RULE_reference, TestSuiteParser.RULE_srcPath, TestSuiteParser.RULE_testModule}
    # Identifiers and the quoted source path are completed as a whole
    word_token_types = {TestSuiteParser.ID, TestSuiteParser.STRING}
    trigger_characters = [",", "/"]

    def __init__(self, *args):
        super().__init__(*args)
        self.files: Dict[str, Tuple[float, str, str]] = {}  # Generated files
        self.fxtran_path = "fxtran"  # Default Fxtran system file path can be overwritten
        self.sort_metric: Optional[str] = None  # Recommendation metric option
        self.descending_sort = False
        self.input_path: Optional[str] = None
        self.parse_tree: Optional[TestSuiteParser.TestSuiteContext] = None
        # Root of relative source paths and generated files
        self.work_path: str = os.getcwd()
        self.command(self.CMD_RECOMMEND_SUT_BLOCKING)(lambda *args: recommend_software_under_test(self, *args))

    # -----------------------------------------------------------------------------------------------------------------
    # Diagnostics
    # -----------------------------------------------------------------------------------------------------------------

    def validate(self, uri: str, source: str) -> List[Diagnostic]:
        diagnostics = super().validate(uri, source)
        self.parse_tree = self.parse_results[uri].tree
        return diagnostics

    def semantic_diagnostics(self, result: ParseResult, uri: str) -> List[Diagnostic]:
        diagnostics: List[Diagnostic] = []
        if result.tree is None:
            return diagnostics

        def error(token, message, severity=DiagnosticSeverity.Error):
            diagnostics.append(Diagnostic(range=token_range(token, token.line, token.column), message=message,
                                          severity=severity, source=self.diagnostic_source))

        test_names = set()
        for case in result.tree.cases:
            if case.name is None:
                continue
            # Test case names identify the tests in the generated setup files and must be unique
            if case.name.text in test_names:
                error(case.name, f"duplicate test case '{case.name.text}'")
            test_names.add(case.name.text)

            if case.vars_ is not None:
                var_names = set()
                for var in case.vars_.vars_:
                    decl = var.decl
                    if decl is None or decl.name is None:
                        continue
                    name = decl.name.getText()
                    if name in var_names:
                        error(decl.name.start, f"duplicate variable '{name}' in test case '{case.name.text}'")
                    var_names.add(name)

            if case.srcpath is not None and case.srcpath.path is not None:
                src_path = case.srcpath.path.text.strip("'")
                if src_path and not os.path.isdir(os.path.join(self.work_path, src_path)):
                    error(case.srcpath.path, f"source path '{src_path}' does not exist; new modules will be created "
                                             f"there", DiagnosticSeverity.Information)
        return diagnostics

    # -----------------------------------------------------------------------------------------------------------------
    # Completion
    # -----------------------------------------------------------------------------------------------------------------

    def symbol_completions(
            self, result: ParseResult, position: TokenPosition, candidates: CandidatesCollection, uri: str
    ) -> List[CompletionItem]:
        if result.tree is None:
            return []
        items: List[CompletionItem] = []
        rules = candidates.rules
        if TestSuiteParser.RULE_srcPath in rules:
            items.extend(self.path_completions(position.text))
        if TestSuiteParser.RULE_reference in rules or TestSuiteParser.RULE_testModule in rules:
            symbol_table = SymbolTableVisitor("completions", self.work_path, self.fxtran_path).visit(result.tree)
            if TestSuiteParser.RULE_reference in rules:
                for symbol_type, kind in ((VariableSymbol, CompletionItemKind.Variable),
                                          (RoutineSymbol, CompletionItemKind.Function)):
                    # FunctionSymbol is derived from RoutineSymbol
                    names = suggest_symbols(symbol_table=symbol_table, position=position, symbol_type=symbol_type,
                                            descending_sort=self.descending_sort)
                    items.extend(CompletionItem(label=name, kind=kind) for name in names)
            if TestSuiteParser.RULE_testModule in rules:
                names = suggest_symbols(symbol_table=symbol_table, position=position, symbol_type=ModuleSymbol,
                                        descending_sort=self.descending_sort)
                items.extend(CompletionItem(label=name, kind=CompletionItemKind.Module) for name in names)
        return items

    def path_completions(self, typed: str) -> List[CompletionItem]:
        """Complete the directory part of a quoted source path relative to :attr:`work_path`."""
        typed = typed[1:] if typed.startswith("'") else typed
        base, _, partial = typed.rpartition("/")
        directory = os.path.join(self.work_path, base)
        items: List[CompletionItem] = []
        try:
            entries = sorted(os.scandir(directory), key=lambda e: e.name)
        except OSError:
            return items
        for entry in entries:
            if entry.is_dir() and not entry.name.startswith(".") and entry.name.startswith(partial):
                path = f"{base}/{entry.name}" if base else entry.name
                items.append(CompletionItem(label=entry.name, kind=CompletionItemKind.Folder, detail=path,
                                            filter_text=f"'{path}", insert_text=entry.name))
        return items

    # -----------------------------------------------------------------------------------------------------------------
    # Generation
    # -----------------------------------------------------------------------------------------------------------------

    def document_saved(self, uri: str, result: ParseResult) -> None:
        document: Document = self.workspace.get_text_document(uri)
        generate(self, result.tree, os.path.abspath(document.path))


tdd_server = TDDLSPServer("pygls-odsl-tdd-prototype", "v0.8")


def generate(server: TDDLSPServer, parse_tree: Optional[TestSuiteParser.TestSuiteContext], file_path: str) -> None:
    """Generate pFUnit, Fortran and CMake files for a parsed test suite."""
    if parse_tree is None:
        return
    work_path = server.work_path
    # Get symboltable for f90 generator
    symbol_table = SymbolTableVisitor("variables", work_path, server.fxtran_path).visit(parse_tree)

    rel_file_path: str = os.path.relpath(file_path, work_path)  # Get relative input path for file generation
    # Generate pf files
    server.files = PFFileGeneratorVisitor(
        work_path=work_path, files=server.files, symbol_table=symbol_table, rel_file_path=rel_file_path
    ).visit(parse_tree)
    # Generate F90 files
    server.files = F90FileGeneratorVisitor(
        work_path=work_path, files=server.files, symbol_table=symbol_table, rel_file_path=rel_file_path
    ).visit(parse_tree)
    # Generate CMake files
    server.files = CMakeFileGeneratorVisitor(
        work_path=work_path, files=server.files, symbol_table=symbol_table
    ).visit(parse_tree)


def did_save(server: TDDLSPServer, params: Optional[DidSaveTextDocumentParams]):
    """Generate files for a saved document (LSP) or for ``server.input_path`` (CLI, ``params`` is None)."""
    if params is not None:
        server.on_did_save(params)
        return

    result = parse_stream(FileStream(server.input_path, encoding="utf-8"), server)
    for diagnostic in result.diagnostics:
        LOG.error("%s:%d:%d: %s", server.input_path, diagnostic.range.start.line + 1,
                  diagnostic.range.start.character + 1, diagnostic.message)
    server.parse_tree = result.tree
    generate(server, result.tree, os.path.abspath(server.input_path))


def parse_stream(stream: InputStream, server: TDDLSPServer = tdd_server) -> ParseResult:
    """Parse a stream and return the parse result."""
    return server.parse(str(stream))


def recommend_software_under_test(server: TDDLSPServer, *args):
    """Calculates the complexity of Software Under Test (SuT) in the input path and returns SuTs test recommendations.

    Called with arguments from the LSP client (uses the last parsed test specification) and without arguments from the
    CLI (analyses ``server.input_path``).
    """
    sort_metric = server.sort_metric or "Test Index"

    # Initialize a visitor to calculate complexity metrics
    complexity_visitor = ComplexityMetricVisitor(
        name="recommend",
        source_root_directory=server.work_path,
        fxtran_command_path=server.fxtran_path,
        sorting_metric=sort_metric,
        debug_mode=server.SHOW_DEBUG_OUTPUT,
        debug_separator=server.DEBUG_OUTPUT_SEPERATOR
    )

    # Generate a symbol table based on cli or client call
    if args:
        if server.parse_tree is None:
            server.show_message("Open a TDD-DSL file before requesting recommendations.", MessageType.Warning)
            return None
        symbol_table = complexity_visitor.visit(server.parse_tree)
    else:
        symbol_table = complexity_visitor.calculate_metrics_for(server.input_path)

    # Suggest metrics based on the generated symbol table
    recommended_metrics = suggest_symbols(symbol_table, position=None, symbol_type=MetricSymbol,
                                          descending_sort=server.descending_sort)

    # Write output to file if passed to llm analysis or debug enabled
    if server.SHOW_DEBUG_OUTPUT or not args:
        recommended_metrics.insert(0, server.DEBUG_HEADER)
        file_path = os.path.join(server.work_path, filter_escape_chars(sort_metric))
        debug_file_write(file_path, "\n".join(recommended_metrics))
        return file_path

    server.show_message(f"Recommendations for Software Under Test (SuT) based on {sort_metric}...")
    # Show the top N metrics as determined by the configuration
    for metric in recommended_metrics[:server.N_SHOW_METRICS]:
        server.show_message(metric)
    return recommended_metrics[:server.N_SHOW_METRICS]


def filter_escape_chars(input_string: str) -> str:
    """Removes characters to be escaped for Bash."""
    escape_chars = r'\"\'$`!&*?;|<>()[\]{} '
    return input_string.translate(str.maketrans('', '', escape_chars))


def debug_file_write(file_path: str, content: str):
    """Writes debugging information to a file."""
    LOG.debug("Log metric to file %s", file_path)
    with open(file_path, mode="w", encoding="utf-8") as f:
        f.write(content)


def stripTerminals(elements: List[str], terminal: str = "'") -> List[str]:
    """Strip string terminals from list elements."""
    return [e.strip(terminal) for e in elements]
