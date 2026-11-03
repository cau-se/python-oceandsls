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
"""Symbol based completion: the symbols of a :class:`~odsllib.symbol_table.SymbolTable` visible at the caret.

``suggest_symbols()`` collects the symbols of a type in the scope of the caret and filters their names by the text in
front of the caret. A DSL can pass its own ``filter_function`` to present other symbols (e.g. their values).
"""

import asyncio
import threading
from typing import Callable, List, Optional, ParamSpec, Tuple, Type

from antlr4 import ParserRuleContext

from odsllib.lsp.compute_token_index import TokenPosition
from odsllib.symbol_table import ScopedSymbol, Symbol, SymbolTable, VariableSymbol

__all__ = ["run_async", "get_scope", "get_all_symbols_of_type", "collect_symbols", "filter_symbols", "suggest_symbols"]

P = ParamSpec("P")

#: ``filter_function(text, symbols, symbol_type)`` returns the completion candidates
FilterFunction = Callable[[str, List[Symbol], type], List[str]]


class _RunThread(threading.Thread):
    """Runs a coroutine function in its own event loop (used while another event loop is running)."""

    def __init__(self, func, *args: P.args, **kwargs: P.kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.result = None

    def run(self):
        self.result = asyncio.run(self.func(*self.args, **self.kwargs))


def run_async(func, *args: P.args, **kwargs: P.kwargs):
    """Run the coroutine function ``func`` and return its result, also from inside a running event loop."""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:  # no running event loop
        loop = None
    if loop and loop.is_running():
        thread = _RunThread(func, *args, **kwargs)
        thread.start()
        thread.join()
        return thread.result
    return asyncio.run(func(*args, **kwargs))


def get_scope(context: Optional[ParserRuleContext], symbol_table: SymbolTable) -> Optional[Symbol]:
    """Return the symbol of the innermost parse tree node (``context`` or one of its parents) that has one."""
    while context is not None:
        scope = run_async(symbol_table.symbol_with_context, context)
        if scope is not None:
            return scope
        context = context.parentCtx
    return None


def get_all_symbols_of_type(scope: ScopedSymbol, symbol_type: type) -> List[Symbol]:
    """Symbols of a type in ``scope`` and its parent scopes, also across parents that are no scopes."""
    symbols: List[Symbol] = run_async(scope.get_symbols_of_type, symbol_type, False)
    parent = scope.parent()
    broken_chain = False
    while parent is not None and not isinstance(parent, ScopedSymbol):
        parent = parent.parent()
        broken_chain = True
    if parent is not None and broken_chain:
        symbols.extend(get_all_symbols_of_type(parent, symbol_type))
    return symbols


def collect_symbols(symbol_table: SymbolTable, position: Optional[TokenPosition],
                    symbol_type: type = VariableSymbol) -> Tuple[List[Symbol], str]:
    """Return the symbols of a type visible at ``position`` and the text in front of the caret.

    Without a position all symbols of the type in the table are returned.
    """
    if not position:
        return run_async(symbol_table.get_nested_symbols_of_type, symbol_type), ""
    scope = get_scope(position.context, symbol_table)
    if isinstance(scope, ScopedSymbol):  # local scope
        symbols = get_all_symbols_of_type(scope, symbol_type)
    else:  # global scope
        symbols = run_async(symbol_table.get_symbols_of_type, symbol_type, False)
    return symbols, position.text


def filter_symbols(text: str, symbols: List[Symbol], symbol_type: Optional[type] = None) -> List[str]:
    """Names of the symbols that start with ``text`` (case-insensitive); all names for an empty text."""
    del symbol_type  # same signature as the filter functions of the DSLs
    names = [symbol.name for symbol in symbols]
    if not text.strip():
        return names
    return [name for name in names if name.lower().startswith(text.lower())]


def suggest_symbols(symbol_table: SymbolTable, position: Optional[TokenPosition], symbol_type: Type = VariableSymbol,
                    filter_function: Optional[FilterFunction] = None) -> List[str]:
    """Completion candidates: the symbols of ``symbol_type`` visible at ``position``, filtered by the typed text."""
    symbols, text = collect_symbols(symbol_table, position, symbol_type)
    return (filter_function or filter_symbols)(text, symbols, symbol_type)
