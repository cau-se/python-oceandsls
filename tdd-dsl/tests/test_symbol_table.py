#  Copyright (c) 2026.  OceanDSL (https://oceandsl.uni-kiel.de)
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
"""Tests of the TDD-DSL symbols on top of odsllib.symbol_table."""

import unittest

from parameterized import parameterized

from odsllib.symbol_table import SymbolTable, SymbolTableOptions
from tddlspserver.symboltable.symbol_table import ModuleSymbol, TestCaseSymbol, get_all_modules_with_file_sync

MATH_AND_IO = [("math", "math.f90"), ("io", None)]  # io has no implementing file


def make_test_case(modules):
    """A test case test_add with the given (name, file) modules."""
    table = SymbolTable("tests", SymbolTableOptions(False))
    test_case = table.add_new_symbol_of_type(TestCaseSymbol, None, "test_add", "test_add.pf")
    symbols = {name: table.add_new_symbol_of_type(ModuleSymbol, test_case, name, file, test_case)
               for name, file in modules}
    return test_case, symbols


class TestSymbolTable(unittest.TestCase):

    @parameterized.expand([
        ("module_with_and_without_file", MATH_AND_IO, ["math.f90"]),
        # Only modules with an implementing file are included
        # Input: the modules math (math.f90) and io (no file)
        # Expected Result: ['math.f90']

        ("no_modules", [], []),
        # A test case without modules
        # Input: no modules
        # Expected Result: no include files

        ("two_files", [("a", "a.f90"), ("b", "b.f90")], ["a.f90", "b.f90"]),
        # The files are included in declaration order
        # Input: the modules a (a.f90) and b (b.f90)
        # Expected Result: ['a.f90', 'b.f90']
    ])
    def test_include_files(self, test_name, modules, expected_files):
        test_case, _ = make_test_case(modules)
        self.assertEqual(expected_files, test_case.include_files, test_name)

    @parameterized.expand([
        ("all_from_test_case", MATH_AND_IO, None, None, ["math"]),
        # Modules with files are found in nested scopes
        # Input: the modules math (math.f90) and io (no file), searched from the test case
        # Expected Result: math

        ("file_filter_match", MATH_AND_IO, None, "math.f90", ["math"]),
        # The search can be restricted to a file
        # Input: file math.f90
        # Expected Result: math

        ("file_filter_no_match", MATH_AND_IO, None, "other.f90", []),
        # No module implements the file
        # Input: file other.f90
        # Expected Result: no modules

        ("from_inside_module", MATH_AND_IO, "math", None, ["math"]),
        # From inside a module, its siblings are found through the parent scope
        # Input: search from the module math
        # Expected Result: math

        ("several_modules_filtered", [("a", "a.f90"), ("b", "b.f90")], None, "b.f90", ["b"]),
        # The filter selects one of several modules
        # Input: the modules a (a.f90) and b (b.f90), file b.f90
        # Expected Result: b

        ("no_modules", [], None, None, []),
        # A test case without modules
        # Input: no modules
        # Expected Result: no modules
    ])
    def test_get_all_modules_with_file(self, test_name, modules, start, file, expected_names):
        test_case, symbols = make_test_case(modules)
        scope = symbols[start] if start else test_case
        result = get_all_modules_with_file_sync(scope) if file is None else get_all_modules_with_file_sync(scope, file)
        self.assertEqual([symbols[name] for name in expected_names], result, test_name)


if __name__ == '__main__':
    unittest.main()
