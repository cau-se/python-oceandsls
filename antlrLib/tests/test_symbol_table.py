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
from unittest import TestCase

from parameterized import parameterized

from odsllib.symbol_table import (
    DuplicateSymbolError, FundamentalType, FundamentalUnit, FunctionSymbol, RoutineSymbol, ScopedSymbol, SymbolTable,
    SymbolTableOptions, Type, TypeKind, UnitKind, VariableSymbol, get_fundamental_type,
)


class TestSymbolTable(TestCase):

    def setUp(self):
        """A table with a module that has a variable and a routine with a local variable."""
        self.table = SymbolTable("main", SymbolTableOptions(False))
        self.module = self.table.add_new_symbol_of_type(ScopedSymbol, None, "module")
        self.table.add_new_symbol_of_type(VariableSymbol, self.module, "global_var", 1)
        self.routine = self.table.add_new_symbol_of_type(RoutineSymbol, self.module, "init")
        self.table.add_new_symbol_of_type(VariableSymbol, self.routine, "local_var", 2)

    def scope(self, name):
        return {"table": self.table, "module": self.module, "routine": self.routine}[name]

    @parameterized.expand([
        ("table", ["module"], None, False, True),
        # The table holds the top level symbols, but is no parent scope of them
        # Input: the symbol table
        # Expected Result: the module, whose parent scope is None; the table has no parent and is its own table

        ("module", ["global_var", "init"], None, True, True),
        # A scope at the top level
        # Input: the module
        # Expected Result: its variable and routine, which have the module as parent; the module has no parent
        # scope, but belongs to the table

        ("routine", ["local_var"], "module", True, False),
        # Symbols are added to the scope they are created in
        # Input: the routine
        # Expected Result: its local variable, which has the routine as parent; the module is the routine's parent
    ])
    def test_symbols_are_added_to_their_scopes(self, test_name, expected_children, expected_parent,
                                               children_have_scope_as_parent, check_symbol_table):
        scope = self.scope(test_name)

        self.assertEqual(expected_children, [s.name for s in scope.children()], test_name)
        self.assertEqual(children_have_scope_as_parent,
                         all(child.parent() is scope for child in scope.children()), test_name)
        self.assertIs(self.scope(expected_parent) if expected_parent else None, scope.parent(), test_name)
        if check_symbol_table:
            self.assertIs(self.table, scope.symbol_table(), test_name)

    @parameterized.expand([
        ("duplicate_rejected", False, "global_var", DuplicateSymbolError, 2),
        # Duplicate symbols are rejected unless the table allows them
        # Input: a second 'global_var' in the module of a table without allow_duplicate_symbols
        # Expected Result: DuplicateSymbolError, the module keeps its two children

        ("duplicate_allowed", True, "global_var", None, 3),
        # A table can allow duplicates
        # Input: a second 'global_var' in the module of a table with allow_duplicate_symbols
        # Expected Result: the symbol is added

        ("new_name", False, "other_var", None, 3),
        # A new name is always added
        # Input: 'other_var' in the module of a table without allow_duplicate_symbols
        # Expected Result: the symbol is added
    ])
    def test_duplicate_symbols(self, test_name, allow_duplicates, name, expected_error, expected_children):
        self.table.options = SymbolTableOptions(allow_duplicates)
        if expected_error:
            with self.assertRaises(expected_error, msg=test_name):
                self.table.add_new_symbol_of_type(VariableSymbol, self.module, name)
        else:
            self.table.add_new_symbol_of_type(VariableSymbol, self.module, name)
        self.assertEqual(expected_children, len(self.module.children()), test_name)

    @parameterized.expand([
        ("local_variable", "routine", "local_var", None, False, 2),
        # A local symbol
        # Input: 'local_var' resolved in the routine
        # Expected Result: the variable with the value 2

        ("variable_of_parent", "routine", "global_var", None, False, 1),
        # Names resolve through parent scopes
        # Input: 'global_var' resolved in the routine
        # Expected Result: the module's variable with the value 1

        ("local_only", "routine", "global_var", None, True, None),
        # A local search does not look into parent scopes
        # Input: 'global_var' resolved in the routine with local_only
        # Expected Result: nothing

        ("not_in_child_scopes", "module", "local_var", None, False, None),
        # Child scopes are not searched
        # Input: 'local_var' resolved in the module
        # Expected Result: nothing

        ("by_type", "routine", "init", RoutineSymbol, False, "routine"),
        # The type of the symbol can be required
        # Input: 'init' resolved in the routine as RoutineSymbol
        # Expected Result: the routine itself

        ("wrong_type", "routine", "init", VariableSymbol, False, None),
        # A symbol of another type is not found
        # Input: 'init' resolved in the routine as VariableSymbol
        # Expected Result: nothing
    ])
    def test_resolve(self, test_name, scope, name, symbol_type, local_only, expected):
        symbol = self.scope(scope).resolve_sync(name, symbol_type, local_only=local_only)
        if expected is None:
            self.assertIsNone(symbol, test_name)
        elif isinstance(expected, str):
            self.assertIs(self.scope(expected), symbol, test_name)
        else:
            self.assertEqual(expected, symbol.value, test_name)

    @parameterized.expand([
        ("nested_in_table", "table", "nested", ["global_var", "local_var"]),
        # All nested symbols of a type
        # Input: the variables nested in the table
        # Expected Result: both variables

        ("all_visible_from_routine", "routine", "all", ["global_var", "local_var"]),
        # All symbols visible from a scope (its own and those of its parents)
        # Input: the variables visible from the routine
        # Expected Result: both variables

        ("local_only", "routine", "local", ["local_var"]),
        # Only the symbols of the scope itself
        # Input: the variables of the routine with local_only
        # Expected Result: only the local variable

        ("asynchronous", "routine", "async", ["global_var", "local_var"]),
        # The asynchronous variant collects the same symbols
        # Input: the variables visible from the routine, collected asynchronously
        # Expected Result: both variables

        ("routines", "module", "routines", ["init"]),
        # Symbols of another type
        # Input: the routines of the module
        # Expected Result: the routine 'init'
    ])
    def test_symbols_are_collected_by_type(self, test_name, scope, how, expected_names):
        scope = self.scope(scope)
        collect = {
            "nested": lambda: scope.get_nested_symbols_of_type_sync(VariableSymbol),
            "all": lambda: scope.get_all_symbols_sync(VariableSymbol),
            "local": lambda: scope.get_all_symbols_sync(VariableSymbol, local_only=True),
            "async": lambda: asyncio.run(scope.get_all_symbols(VariableSymbol)),
            "routines": lambda: scope.get_all_symbols_sync(RoutineSymbol),
        }[how]
        first = collect()

        self.assertEqual(expected_names, sorted(s.name for s in first), test_name)
        # repeated calls give the same result (the visited scopes are no longer a shared default argument)
        self.assertEqual([s.name for s in first], [s.name for s in collect()], test_name)

    @parameterized.expand([
        ("dependency_symbol", "sqrt", False, FundamentalType.real_type),
        # Dependencies are searched
        # Input: 'sqrt', defined in a dependency of the table
        # Expected Result: the function with the return type real

        ("dependency_symbol_local_only", "sqrt", True, None),
        # A local search does not look into dependencies
        # Input: 'sqrt' with local_only
        # Expected Result: nothing

        ("own_symbol", "module", True, "module"),
        # The table's own symbols are found first
        # Input: 'module' with local_only
        # Expected Result: the module

        ("unknown", "cbrt", False, None),
        # A name that is defined nowhere
        # Input: 'cbrt'
        # Expected Result: nothing
    ])
    def test_dependencies_are_searched(self, test_name, name, local_only, expected):
        library = SymbolTable("library", SymbolTableOptions(False))
        library.add_new_symbol_of_type(FunctionSymbol, None, "sqrt", FundamentalType.real_type)
        self.table.add_dependencies(library)
        symbol = self.table.resolve_sync(name, local_only=local_only)

        self.assertEqual((1, 1), (self.table.info().dependency_count, self.table.info().symbol_count), test_name)
        if expected is None:
            self.assertIsNone(symbol, test_name)
        elif isinstance(expected, str):
            self.assertIs(self.scope(expected), symbol, test_name)
        else:
            self.assertEqual(expected, symbol.return_type, test_name)


class TestFundamentalTypes(TestCase):

    @parameterized.expand([
        ("integer_any_case", "Integer", FundamentalType.integer_type),
        # Fundamental types are found by name, case-insensitively
        # Input: 'Integer'
        # Expected Result: the fundamental integer type

        ("real", "real", FundamentalType.real_type),
        # The real type
        # Input: 'real'
        # Expected Result: the fundamental real type (kind Float)

        ("string", "STRING", FundamentalType.string_type),
        # The string type
        # Input: 'STRING'
        # Expected Result: the fundamental string type

        ("unknown", "matrix", Type(name="matrix", base_types=None, kind=None)),
        # An unknown name becomes a new type
        # Input: 'matrix'
        # Expected Result: a type 'matrix' without base types and kind

        ("empty", "", None),
        # No name
        # Input: ''
        # Expected Result: None
    ])
    def test_fundamental_types_are_found_by_name(self, test_name, name, expected):
        self.assertEqual(expected, get_fundamental_type(name), test_name)

    @parameterized.expand([
        ("integer_type", FundamentalType.integer_type, TypeKind.Integer),
        # The kind distinguishes the fundamental types
        # Input: FundamentalType.integer_type
        # Expected Result: kind Integer

        ("real_type", FundamentalType.real_type, TypeKind.Float),
        # Real numbers are floats
        # Input: FundamentalType.real_type
        # Expected Result: kind Float

        ("second_unit", FundamentalUnit.second_unit, UnitKind.Second),
        # Units are distinguished by their kind as well
        # Input: FundamentalUnit.second_unit
        # Expected Result: kind Second
    ])
    def test_kinds(self, test_name, fundamental, expected_kind):
        self.assertEqual(expected_kind, fundamental.kind, test_name)

    @parameterized.expand([
        ("types", FundamentalType("a"), FundamentalType("b")),
        # The base types of fundamental types are not one shared list
        # Input: two new fundamental types, a base type added to the first
        # Expected Result: the second has no base types

        ("units", FundamentalUnit("a"), FundamentalUnit("b")),
        # The base types of fundamental units are not one shared list
        # Input: two new fundamental units, a base type added to the first
        # Expected Result: the second has no base types

        ("type_and_unit", FundamentalType("a"), FundamentalUnit("b")),
        # Types and units do not share their base types either
        # Input: a new fundamental type and unit, a base type added to the type
        # Expected Result: the unit has no base types
    ])
    def test_instances_do_not_share_their_base_types(self, test_name, first, second):
        first.base_types.append(FundamentalType.integer_type)
        self.assertEqual([], second.base_types, test_name)
