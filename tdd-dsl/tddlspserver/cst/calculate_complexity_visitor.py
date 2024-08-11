"""Visitor extracting system file information from the cst"""

__author__ = "sgu"

import logging
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

# Standard library imports
from logging import getLogger
from os.path import join, relpath
from shutil import rmtree
from typing import Callable, Generic

# Antlr4
from antlr4.tree.Tree import ParseTree

# Package imports
from ..fxca.util.fxtran_utils import get_files, write_decorate_src_xml
from ..gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from ..gen.python.TestSuite.TestSuiteVisitor import TestSuiteVisitor
from ..utils.calculate_complexity import calculate_metrics
from ..symboltable.symbol_table import MetricSymbol, SymbolTable, SymbolTableOptions, P, T, TestCaseSymbol

# Debug Log
LOGGER = getLogger(__name__)


class ComplexityMetricVisitor(TestSuiteVisitor, Generic[T]):
    # Class constants
    TEMP_DIR_NAME = "tmp"
    XML_FILE_PATTERN = "*.[fF]90.xml"
    SINGLE_QUOTE = "'"

    def __init__(self, name: str = "", source_root_directory: str = "tdd-dsl/output",
                 fxtran_command_path: str = "fxtran", sorting_metric=None,
                 debug_mode: bool = False, debug_separator: str = "\n"):
        super().__init__()
        self.sorting_metric = sorting_metric
        self.fxtran_command_path = fxtran_command_path  # Updated variable name
        self._symbol_table = SymbolTable(name, SymbolTableOptions(False))
        self._current_scope = None
        self._source_root_directory = source_root_directory
        self._source_path = ""
        self._debug_mode = debug_mode
        self._debug_separator = debug_separator

    @property
    def work_path(self) -> str:
        return self._source_root_directory

    # Visit a parse tree produced by TestSuiteParser#testSuite.
    def visitTestSuite(self, ctx: TestSuiteParser.TestSuiteContext):
        self.visitChildren(ctx)
        return self._symbol_table

    # Visit a parse tree produced by TestSuiteParser#testCase.
    def visitTestCase(self, ctx: TestSuiteParser.TestCaseContext):
        return self.withScope(ctx, TestCaseSymbol, lambda: self.visitChildren(ctx), ctx.ID().getText())

    # Process the source path provided by the user or default to the working path
    def visitSrcPath(self, ctx: TestSuiteParser.SrcPathContext):
        # Extract and clean the user-provided path
        user_path = ctx.path.text.strip(self.SINGLE_QUOTE) if ctx.path else ''
        # Return symbol table for client call via TestSuite
        self.calculate_metrics_for(user_path)

    def calculate_metrics_for(self, user_path):
        # Update the source directory based on the user input
        self._source_path = join(self._source_root_directory, user_path)
        # Create a temporary directory for XML files
        temp_xml_path = join(self._source_path, self.TEMP_DIR_NAME)
        write_decorate_src_xml(self._source_path, temp_xml_path, fxtran_path=self.fxtran_command_path)  # Updated variable name
        # Retrieve Fortran XML files from the temporary directory
        xml_files = get_files(temp_xml_path, self.XML_FILE_PATTERN)
        for path, filename in xml_files:
            src_filename = filename.rsplit(".", 1)[0]
            rel_path = relpath(path, temp_xml_path)
            # Construct the source path using the relative path
            src_path = join(self._source_path, rel_path, src_filename) if rel_path != "." else join(self._source_path, src_filename)

            # Calculate metrics for the current XML file
            scope_elements = calculate_metrics(
                xml_path=join(path, filename),
                src=src_path,
                sort_metric=self.sorting_metric,
                debug=self._debug_mode,
                debug_separator=self._debug_separator
            )

            # Add the calculated metrics to the symbol table
            for scope_name, scope in scope_elements.items():
                if scope.is_testable:
                    self._symbol_table.add_new_symbol_of_type(MetricSymbol, self._current_scope, scope_name, scope)
        # Clean up temporary XML files after processing
        self._remove_temp_files(temp_xml_path)
        # Return symboltable for cli call
        return self._symbol_table

    def _remove_temp_files(self, temp_xml_path: str):
        """Remove the temporary XML files directory."""
        try:
            rmtree(temp_xml_path)
        except OSError as e:
            LOGGER.error("Error deleting temporary XML directory: %s - %s.", e.filename, e.strerror)

    def withScope(self, tree: ParseTree, symbol_type: type, action: Callable, *args: P.args or None, **kwargs: P.kwargs or None) -> T:
        """
        Visit a scoped symbol and recursively visit all symbols inside with the scoped symbol as scope.
        :param tree: Context of the scoped symbol
        :param symbol_type: Type of the symbol
        :param action: Lambda function to add child symbols to the symbol table
        :param args: Arguments for the symbol type
        :param kwargs: Named arguments for the symbol type
        :return: Current scope
        """
        scope = self._symbol_table.add_new_symbol_of_type(symbol_type, self._current_scope, *args, **kwargs)
        scope.context = tree
        self._current_scope = scope
        try:
            return action()
        finally:
            self._current_scope = scope.parent()
