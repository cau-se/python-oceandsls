#  Copyright (c) 2023-2026.  OceanDSL (https://oceandsl.uni-kiel.de)
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
"""Symbols of TDD-DSL (test cases, Fortran modules, paths and metrics) on top of :mod:`odsllib.symbol_table`.

The generic symbol table classes are re-exported for compatibility; import them from :mod:`odsllib.symbol_table`.
"""

from __future__ import annotations

__author__ = "sgu"

from typing import List, Optional

from odsllib.symbol_table import (
    DuplicateSymbolError,
    MemberVisibility,
    TypeKind,
    UnitKind,
    UnitPrefix,
    Unit,
    Type,
    SymbolTableOptions,
    classproperty,
    FundamentalUnit,
    FundamentalType,
    get_fundamental_type,
    Symbol,
    P,
    T,
    TypedSymbol,
    UnitSymbol,
    ScopedSymbol,
    VariableSymbol,
    ParameterSymbol,
    ReturnSymbol,
    RoutineSymbol,
    FunctionSymbol,
    SymbolTableInfo,
    SymbolTable,
)

__all__ = [
    "get_all_modules_with_file_sync",
    "TestCaseSymbol",
    "ModuleSymbol",
    "PathSymbol",
    "MetricSymbol",
    "DuplicateSymbolError",
    "MemberVisibility",
    "TypeKind",
    "UnitKind",
    "UnitPrefix",
    "Unit",
    "Type",
    "SymbolTableOptions",
    "classproperty",
    "FundamentalUnit",
    "FundamentalType",
    "get_fundamental_type",
    "Symbol",
    "P",
    "T",
    "TypedSymbol",
    "UnitSymbol",
    "ScopedSymbol",
    "VariableSymbol",
    "ParameterSymbol",
    "ReturnSymbol",
    "RoutineSymbol",
    "FunctionSymbol",
    "SymbolTableInfo",
    "SymbolTable",
]


class TestCaseSymbol(ScopedSymbol):
    """
    A symbol representing a test case from TDD-DSL used for CMake file generation.
    """

    # Symbol name of the test
    __test_name: str
    # System file path to the test file
    __test_file_path: str

    def __init__(self, test_name=None, test_file_path=None):
        """
        A symbol representing a test case from TDD-DSL used for CMake file generation.

        :param test_name: Symbol name of the test
        :param test_file_path: System file path to the test file
        :param sut_name: Symbol name of the sut
        :param sut_file_path: System file path to the sut file
        """
        super().__init__(test_name)
        self.__test_name = test_name
        self.__test_file_path = test_file_path

    def add_include(self, symbol: ModuleSymbol) -> None:
        super().add_include(symbol)

    @property
    def include_files(self) -> List[str]:
        include_files: List[str] = []
        for include in self._include_scopes:
            if include.file:
                include_files.append(include.file)

        return include_files

    @property
    def test_name(self) -> str:
        return self.__test_name

    @test_name.setter
    def test_name(self, test_name: str):
        self.__test_name = test_name

    @property
    def test_file_path(self) -> str:
        return self.__test_file_path

    @test_file_path.setter
    def test_file_path(self, test_file_path: str):
        self.__test_file_path = test_file_path


class ModuleSymbol(ScopedSymbol):
    def __init__(self, name: str = "", file: str = None, include_in: ScopedSymbol = None):
        super().__init__(name)
        self.__childSymbols = []

        # Filename of system file
        self._file: str = file
        self._contains_function: bool = False

        # Inclusions
        self.__included_in: Optional[ScopedSymbol] = include_in
        include_in.add_include(self)

    def parent(self) -> Optional[ScopedSymbol]:
        s_parent: Symbol = super().parent()
        if s_parent:
            return s_parent
        else:
            return self.included_in

    @property
    def included_in(self) -> Optional[ScopedSymbol]:
        return self.__included_in

    @property
    def file(self) -> str:
        return self._file

    @file.setter
    def file(self, file: str):
        self._file = file

    @property
    def contains_function(self) -> bool:
        return self._contains_function

    @contains_function.setter
    def contains_function(self, contains_function: bool):
        self._contains_function = contains_function


class PathSymbol(VariableSymbol):
    pass


class MetricSymbol(VariableSymbol):
    pass


def get_all_modules_with_file_sync(scope: ScopedSymbol, file: str = None, local_only: bool = False,
                                   callers: Optional[List[ScopedSymbol]] = None) -> List[ModuleSymbol]:
    """
    All modules with implementing files in ``scope`` (formerly the method ScopedSymbol.get_all_modules_with_file_sync).

    :param scope: the scope to search
    :param callers: List of visited scopes, that should not be visited again
    :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        and included scopes (recursively).
    :param file: If given only returns symbols from that file.
    :return: A list of all ModuleSymbol with implementing files from this and all nested scopes in the order they were
        defined.
    """
    callers = [] if callers is None else callers
    result: List[ModuleSymbol] = []

    for child in scope.children():
        # Check all ModuleSymbols if basefile is file or if file is None if basefile is defined
        if isinstance(child, ModuleSymbol) and (file is not None and child.file == file
                                                or file is None and child.file is not None):
            result.append(child)

        # Recursively call children scopes, except for scopes that called us
        if isinstance(child, ScopedSymbol) and child not in callers:
            result.extend(get_all_modules_with_file_sync(child, file, True, callers + [scope]))

    # Recursively call parent scopes, except for scopes that called us
    if not local_only:
        if isinstance(scope.parent(), ScopedSymbol) and scope.parent() not in callers:
            local_list = get_all_modules_with_file_sync(scope.parent(), file, local_only, callers + [scope])
            result.extend(local_list)

        # Call scopes that are included
        for include_scope in scope._include_scopes:  # pylint: disable=protected-access
            if isinstance(include_scope, ScopedSymbol) and include_scope not in callers:
                local_list = get_all_modules_with_file_sync(include_scope, file, local_only, callers + [scope])
                result.extend(local_list)

    return result
