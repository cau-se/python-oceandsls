#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software

"""Symbol based completion of TDD-DSL: paths and metrics are suggested by their values.

The scope lookup and the collection of the visible symbols are shared (:mod:`odsllib.lsp.symbols`).
"""

from typing import List, Type

from odsllib.lsp.compute_token_index import TokenPosition
from odsllib.lsp.symbols import filter_symbols as filter_symbol_names, get_scope, suggest_symbols as suggest
from odsllib.symbol_table import RoutineSymbol, Symbol, SymbolTable, VariableSymbol
from ..symboltable.symbol_table import MetricSymbol, ModuleSymbol, PathSymbol

__all__ = ["get_scope", "suggest_symbols", "filter_symbols"]


def suggest_symbols(symbol_table: SymbolTable, position: TokenPosition, symbol_type: Type = VariableSymbol,
                    descending_sort=False) -> List[str]:
    """Completion candidates of a symbol type at ``position`` (metric values sorted, descending if requested)."""
    return suggest(symbol_table, position, symbol_type,
                   lambda text, symbols, kind: filter_symbols(text, symbols, kind, descending_sort))


def filter_symbols(text: str, symbols: List[Symbol], symbol_type: Type = VariableSymbol,
                   descending_sort=False) -> List[str]:
    """Paths and metrics by value, variables, modules and routines by the names starting with ``text``."""
    if issubclass(symbol_type, PathSymbol):
        return [symbol.value for symbol in symbols]
    if issubclass(symbol_type, MetricSymbol):
        values = sorted((symbol.value for symbol in symbols), reverse=descending_sort)
        return [str(value) for value in values]
    if issubclass(symbol_type, (VariableSymbol, ModuleSymbol, RoutineSymbol)):
        return filter_symbol_names(text, symbols)
    return []
