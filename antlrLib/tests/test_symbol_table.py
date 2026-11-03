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
"""Tests of the shared symbol table (odsllib.symbol_table)."""

import asyncio

import pytest

from odsllib.symbol_table import (
    DuplicateSymbolError, FundamentalType, FundamentalUnit, FunctionSymbol, RoutineSymbol, ScopedSymbol, SymbolTable,
    SymbolTableOptions, Type, TypeKind, VariableSymbol, get_fundamental_type,
)


@pytest.fixture(name="table")
def table_fixture():
    """A table with a module that has a variable and a routine with a local variable."""
    table = SymbolTable("main", SymbolTableOptions(False))
    module = table.add_new_symbol_of_type(ScopedSymbol, None, "module")
    table.add_new_symbol_of_type(VariableSymbol, module, "global_var", 1)
    routine = table.add_new_symbol_of_type(RoutineSymbol, module, "init")
    table.add_new_symbol_of_type(VariableSymbol, routine, "local_var", 2)
    return table


def routine_of(table) -> RoutineSymbol:
    return table.resolve_sync("module").resolve_sync("init")


def test_symbols_are_added_to_their_scopes(table):
    module = table.resolve_sync("module")
    routine = routine_of(table)
    assert isinstance(routine, RoutineSymbol)
    assert [s.name for s in module.children()] == ["global_var", "init"]
    assert [s.name for s in routine.children()] == ["local_var"]
    assert routine.children()[0].parent() is routine
    # the symbol table is the root, but not a parent scope of its children
    assert module.parent() is None and module.symbol_table() is table
    assert table.info().symbol_count == 1


def test_duplicate_symbols_are_rejected_unless_allowed(table):
    with pytest.raises(DuplicateSymbolError):
        table.add_new_symbol_of_type(VariableSymbol, table.resolve_sync("module"), "global_var")
    tolerant = SymbolTable("tolerant", SymbolTableOptions(True))
    tolerant.add_new_symbol_of_type(VariableSymbol, None, "x")
    tolerant.add_new_symbol_of_type(VariableSymbol, None, "x")
    assert len(tolerant.children()) == 2


def test_names_resolve_through_parent_scopes(table):
    routine = routine_of(table)
    assert routine.resolve_sync("local_var").value == 2
    assert routine.resolve_sync("global_var").value == 1
    assert routine.resolve_sync("global_var", local_only=True) is None
    assert table.resolve_sync("module").resolve_sync("local_var") is None
    assert routine.resolve_sync("init", RoutineSymbol) is routine
    assert routine.resolve_sync("init", VariableSymbol) is None


def test_symbols_are_collected_by_type(table):
    routine = routine_of(table)
    assert sorted(s.name for s in table.get_nested_symbols_of_type_sync(VariableSymbol)) == ["global_var", "local_var"]
    assert sorted(s.name for s in routine.get_all_symbols_sync(VariableSymbol)) == ["global_var", "local_var"]
    assert [s.name for s in routine.get_all_symbols_sync(VariableSymbol, local_only=True)] == ["local_var"]
    # repeated calls give the same result (the visited scopes are no longer a shared default argument)
    assert routine.get_all_symbols_sync(VariableSymbol) == routine.get_all_symbols_sync(VariableSymbol)
    assert sorted(s.name for s in asyncio.run(routine.get_all_symbols(VariableSymbol))) == ["global_var", "local_var"]


def test_dependencies_are_searched(table):
    library = SymbolTable("library", SymbolTableOptions(False))
    library.add_new_symbol_of_type(FunctionSymbol, None, "sqrt", FundamentalType.real_type)
    table.add_dependencies(library)
    assert table.resolve_sync("sqrt").return_type == FundamentalType.real_type
    assert table.resolve_sync("sqrt", local_only=True) is None
    assert table.info().dependency_count == 1


def test_fundamental_types_are_found_by_name():
    assert get_fundamental_type("Integer") == FundamentalType.integer_type
    assert get_fundamental_type("real").kind == TypeKind.Float
    assert get_fundamental_type("matrix") == Type(name="matrix", base_types=None, kind=None)
    assert get_fundamental_type("") is None


def test_fundamental_instances_do_not_share_their_base_types():
    first, second = FundamentalType("a"), FundamentalType("b")
    first.base_types.append(FundamentalType.integer_type)
    assert second.base_types == []
    assert FundamentalUnit("u").base_types == []
