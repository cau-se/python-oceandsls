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

from odsllib.symbol_table import SymbolTable, SymbolTableOptions
from tddlspserver.symboltable.symbol_table import ModuleSymbol, TestCaseSymbol, get_all_modules_with_file_sync


def test_modules_with_files_are_found_in_nested_scopes():
    table = SymbolTable("tests", SymbolTableOptions(False))
    test_case = table.add_new_symbol_of_type(TestCaseSymbol, None, "test_add", "test_add.pf")
    with_file = table.add_new_symbol_of_type(ModuleSymbol, test_case, "math", "math.f90", test_case)
    table.add_new_symbol_of_type(ModuleSymbol, test_case, "io", None, test_case)  # no implementing file

    assert test_case.include_files == ["math.f90"]
    assert get_all_modules_with_file_sync(test_case) == [with_file]
    assert get_all_modules_with_file_sync(test_case, "math.f90") == [with_file]
    assert get_all_modules_with_file_sync(test_case, "other.f90") == []
    # from inside a module, its siblings are found through the parent scope
    assert get_all_modules_with_file_sync(with_file) == [with_file]
