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

from __future__ import annotations
import abc

__author__ = "stu222808,sgu,reiner"

from typing import Coroutine, List, Optional, ParamSpec, Set, TypeVar
from model.type_system import Type
from model.unit_model import Unit


# Antlr4
from antlr4.tree.Tree import ParseTree


class DuplicateSymbolError(Exception):
    pass


# TODO should be renamed to ModelObject or SymbolObject or ModelSymbol
# The generic scope interface that manages access to types and data


class Scope:

    parent: Scope

    def __init__(self, parent=None) -> None:
        self.parent = parent

    def resolve_symbol(self, name: str):
        raise NotImplementedError(f"Name {name} not found {self}")


class NamedElement(Scope):

    name: str

    def __init__(self, name: str, parent=None) -> None:
        super().__init__(parent)
        self.name = name


class Symbol:
    """
    The root of the symbol table class hierarchy: a symbol can be any manageable entity (like a block), not only things
    like variables or classes. We are using a class hierarchy here, instead of an enum or similar, to allow for easy
    extension and certain symbols can so provide additional APIs for simpler access to their sub elements, if needed.
    """
    # The name of the scope or empty if anonymous.
    name: str

    # The configuration Trees
    configuration = []

    # Reference to the parse tree which contains this symbol.
    context: Optional[ParseTree]

    @property
    def modifiers(self) -> Set[int]:
        return set()

    __the_parent: Optional[ScopedSymbol] = None

    def __init__(self, name: str = ""):
        self.name = name
        self.context = None
        self.configuration = []

    def parent(self) -> Optional[ScopedSymbol]:
        return self.__the_parent

    def first_sibling(self) -> Symbol:
        if isinstance(self.__the_parent, ScopedSymbol):
            # Expect not to be None
            return self.__the_parent.first_child()

        return self

    def previous_sibling(self) -> Optional[Symbol]:
        """
        :return: the symbol before this symbol in its scope.
        """
        if not isinstance(self.__the_parent, ScopedSymbol):
            return self

        return self.__the_parent.previous_sibling_of(self)

    def next_sibling(self) -> Optional[Symbol]:
        """
        :return: the symbol following this symbol in its scope.
        """
        if not isinstance(self.__the_parent, ScopedSymbol):
            return self

        return self.__the_parent.next_sibling_of(self)

    def last_sibling(self) -> Symbol:
        if isinstance(self.__the_parent, ScopedSymbol):
            # Expect not to be None
            return self.__the_parent.last_child()

        return self

    def next(self) -> Optional[Symbol]:
        """
        :return: the next symbol in definition order, regardless of the scope.
        """
        if isinstance(self.__the_parent, ScopedSymbol):
            return self.__the_parent.next_of(self)

        return None

    def root(self) -> Optional[Symbol]:
        """
        :return: the outermost entity (below the symbol table) that holds us.
        """
        run: Optional[Symbol] = self.__the_parent
        while run is not None:
            if run.parent() is None or isinstance(run.parent(), None):
                return run
            run = run.parent()

        return run

    def symbol_table(self) -> Optional[None]:
        """
        :return: the symbol table we belong too or undefined if we are not yet assigned.
        """
        if isinstance(self, None):
            return self

        run: Optional[Symbol] = self.__the_parent
        while run is not None:
            if isinstance(run, None):
                return run
            run = run.parent()

        return None

    def symbol_path(self) -> List[Symbol]:
        """
        :return: the list of symbols from this one up to root.
        """
        result: List[Symbol] = []

        run: Symbol = self
        while run is not None:
            result.append(run)
            if run.parent() is None:
                break
            run = run.parent()

        return result

    def set_parent(self, parent: Optional[Symbol]) -> None:
        """
        The parent is usually a scoped symbol as only those can have children, but we allow any symbol here for special
        scenarios. This is rather an internal method and should rarely be used by external code.

        :param parent: The new parent to use.
        :return:
        """
        self.__the_parent = parent

    def remove_from_parent(self) -> None:
        if isinstance(self.__the_parent, ScopedSymbol):
            self.__the_parent.remove_symbol(self)
            self.__the_parent = None

    def resolve(self, name: str, t: type = None, type_only: bool = False, local_only: bool = False) -> Optional[Symbol]:
        """
        Synchronously looks up a symbol with a given name, in a bottom-up manner.

        :param name: The name of the symbol to find.
        :param type_only: no subtype
        :param t: parameter type
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :return: the first symbol with a given name, in the order of appearance in this scope or any of the parent
        scopes (conditionally).
        """
        if isinstance(self.__the_parent, ScopedSymbol):
            return self.__the_parent.resolve_sync(name, t, type_only, local_only)

        return None

    def get_parent_of_type(self, t: type) -> Optional[T]:
        """
        :param t: The type of objects to return.
        :return: the next enclosing parent of the given type.
        """
        run = self.__the_parent
        while run is not None:
            if isinstance(run, t):
                return run
            run = run.__the_parent

        return None

    # TODO <anonymous> special string for empty scope names
    def qualified_name(self, separator=".", full=False, include_anonymous=False) -> str:
        """
        Creates a qualified identifier from this symbol and its parent. If `full` is true then all parents are traversed
        in addition to this instance.

        :param separator: The string to be used between the parts.
        :param full: A flag indicating if the full path is to be returned.
        :param include_anonymous: Use a special string for empty scope names.
        :return: the constructed qualified identifier.
        """
        if not include_anonymous and len(self.name) == 0:
            return ""

        result: str = "<anonymous>" if len(self.name) == 0 else self.name
        run = self.__the_parent
        while run:
            if include_anonymous or len(run.name) > 0:
                result = ("<anonymous>" if len(run.name) == 0 else run.name) + separator + result

            if not full or run.__the_parent is None:
                break

            run = run.__the_parent

        return result


P = ParamSpec("P")
T = TypeVar("T", bound=Symbol)


class TypedSymbol(Symbol):
    """
    A symbol with an attached type (variables, fields etc.).
    """

    # Type such as int
    attached_type: Optional[Type]
    # List of keys such as parameter
    attached_type_keys: Optional[List[str]]

    def __init__(self, name: str, attached_type: Type = None, attached_type_keys=None):
        super().__init__(name)

        # Mutable default argument
        if attached_type_keys is None:
            attached_type_keys = []

        self.attached_type = attached_type
        self.attached_type_keys = attached_type_keys


class UnitSymbol(TypedSymbol):
    """
    A symbol with an attached unit (physical units such as second, metre, gram etc.).
    """
    attached_unit: Optional[Unit]
    attached_description: Optional[str]

    def __init__(self, name: str, attached_description: str, attached_keys=None, attached_unit: Unit = None, attached_type: Type = None):
        super().__init__(name, attached_type, attached_keys)
        self.attached_unit = attached_unit
        self.attached_description = attached_description


class ScopedSymbol(Symbol, Scope):
    """
    A symbol with a scope (so it can have child symbols).
    """
    # All child symbols in definition order.
    __child_symbols: List[Symbol]
    # List of scope symbols extending this symbol
    _include_scopes: List[ScopedSymbol]

    def __init__(self, name: str = "", parent: Scope = None):
        super().__init__(name)
        self.parent = parent
        self.__child_symbols = []
        self._include_scopes: Optional[List[ScopedSymbol]] = []

    def direct_scopes(self) -> Coroutine[List[ScopedSymbol]]:
        """
        :return: A promise resolving to all direct child symbols with a scope (e.g. classes in a module).
        """
        return self.get_symbols_of_type(ScopedSymbol)

    def children(self) -> List[Symbol]:
        return self.__child_symbols

    def parent(self) -> Optional[ScopedSymbol]:
        s_parent: Symbol = super().parent()
        if not isinstance(s_parent, None):
            return s_parent
        else:
            return None

    def first_child(self) -> Optional[Symbol]:
        if len(self.children()) > 0:
            return self.children()[0]

        return None

    def last_child(self) -> Optional[Symbol]:
        if len(self.children()) > 0:
            return self.children()[len(self.children()) - 1]

        return None

    def clear(self) -> None:
        self.__child_symbols = []

    def add_include(self, symbol: ScopedSymbol) -> None:
        self._include_scopes.append(symbol)

    @property
    def include_names(self) -> List[str]:
        include_names: List[str] = []
        for include in self._include_scopes:
            if include.name:
                include_names.append(include.name)

        return include_names

    def add_symbol(self, symbol: Symbol) -> None:
        """
        Adds the given symbol to this scope. If it belongs already to a different scope it is removed from that before
        adding it here.

        :param symbol: The symbol to add as a child.
        :return:
        """
        # Filter duplicates by type and name.
        symbol_table = self.symbol_table()
        if symbol_table is None or not symbol_table.options.allow_duplicate_symbols:
            for child in self.children():
                if child is symbol or (type(symbol) == type(child) and child.name == symbol.name) and isinstance(child, type(symbol)):
                    symbol_name = symbol.name if symbol.name else "<anonymous>"
                    scope_name = self.name if self.name else "<anonymous>"
                    msg: str = f"Attempt to add duplicate symbol \"{symbol_name}\" to \"{scope_name}\""

                    raise DuplicateSymbolError(msg)

        self.children().append(symbol)
        symbol.set_parent(self)

    def remove_symbol(self, symbol: Symbol) -> None:
        if symbol in self.children():
            self.children().remove(symbol)
            symbol.set_parent(None)

    def get_nested_symbols_of_type_and_name(self, t: type, name: str = None) -> List[T]:
        """
        Synchronously retrieves child symbols of a given type and name from this symbol.

        :param t: The type of the objects to return.
        :param name: If given only returns symbols with that name.
        :return: A list of all (nested) children of the given type.
        """
        result: List[T] = []

        for child in self.children():
            if isinstance(child, t) and (name is None or child.name == name):
                result.append(child)

            if isinstance(child, ScopedSymbol):
                result.extend(child.get_nested_symbols_of_type_and_name_sync(t, name))

        return result

    def get_nested_symbols_of_type(self, t: type) -> List[T]:
        """
        Synchronously retrieves child symbols of a given type from this symbol.

        :param t: The type of the objects to return.
        :return: A list of all (nested) children of the given type.
        """
        result: List[T] = []

        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            if isinstance(child, ScopedSymbol):
                result.extend(child.get_nested_symbols_of_type_sync(t))

        return result

    def get_all_nested_symbols(self, name: str = None) -> List[Symbol]:
        """
        :param name: If given only returns symbols with that name.
        :return: A list of all symbols from this and all nested scopes in the order they were defined.
        """
        result: List[Symbol] = []

        for child in self.children():
            if name is None or child.name == name:
                result.append(child)

            if isinstance(child, ScopedSymbol):
                result.extend(child.get_all_nested_symbols_sync(name))

        return result

    def get_symbols_of_type_and_name(self, t: type, name: str = None, local_only=True, callers: List[T] = []) -> List[T]:
        """
        Synchronously returns symbols of the type and optionally the name, if given.

        :param callers: List of visited scopes, that should not be visited again
        :param t: The type of the objects to return.
        :param name: If given only returns symbols with that name.
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol (recursively) and included scopes.
        :return: A promise resolving to direct children of a given type.
        """
        result: List[T] = []
        for child in self.children():
            if isinstance(child, t) and (name is None or child.name == name):
                result.append(child)

        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                result.extend(self.parent().get_symbols_of_type_and_name_sync(t, name, local_only, callers + [self]))

            # Call scopes that are included
            for include_scope in self._include_scopes:
                if isinstance(include_scope, ScopedSymbol) and include_scope not in callers:
                    result.extend(include_scope.get_symbols_of_type_and_name_sync(t, name, local_only, callers + [self]))

        return result

    def get_symbols_of_type(self, t: type, local_only: bool = True, callers: List[T] = []) -> List[T]:
        """
        :param callers: List of visited scopes, that should not be visited again
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively).
        :param t: The type of the objects to return.
        :return: A promise resolving to direct children of a given type.
        """
        result: List[T] = []
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                result.extend(self.parent().get_symbols_of_type_sync(t, local_only, callers + [self]))

            # Call scopes that are included
            for include_scope in self._include_scopes:
                if isinstance(include_scope, ScopedSymbol) and include_scope not in callers:
                    result.extend(include_scope.get_symbols_of_type_sync(t, local_only, callers + [self]))

        return result

    # TODO: add optional position dependency (only symbols defined before a given caret pos are viable).
    def get_all_symbols(self, t: type, local_only: bool = False, callers: List[T] = []) -> List[T]:
        """
        :param callers: List of visited scopes, that should not be visited again
        :param t: The type of the objects to return.
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively) and scopes that are included.
        :return: A list with all symbols of the the given type, accessible from this scope (if local_only is false),
        within the owning symbol table.
        """
        result: List[T] = []

        # Special handling for namespaces, which act like grouping symbols in this scope, so we show them as available
        # in this scope.
        for child in self.children():
            if isinstance(child, t):
                result.append(child)

            # Recursively call children scopes, except for scopes that called us
            if isinstance(child, ScopedSymbol) and child not in callers:
                result.extend(child.get_all_symbols_sync(t, True, callers + [self]))

        # Recursively call parent scopes, except for scopes that called us
        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                local_list: List[T] = self.parent().get_all_symbols_sync(t, local_only, callers + [self])
                result.extend(local_list)

            # Call scopes that are included
            for include_scope in self._include_scopes:
                if isinstance(include_scope, ScopedSymbol) and include_scope not in callers:
                    local_list: List[T] = include_scope.get_all_symbols_sync(t, local_only, callers + [self])
                    result.extend(local_list)

        return result

    def resolve(self, name: str, t: type = None, type_only: bool = False, local_only: bool = False, callers: List[T] = []) -> Optional[Symbol]:
        """
        :param name: The name of the symbol to resolve.
        :param type_only: no subtype
        :param t: parameter type
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively) or scopes that are included.
        :param callers: List of visited scopes, that should not be visited again
        :return: the first symbol with a given name, in the order of appearance in this scope or any of the parent
        scopes (conditionally) or any scope included.
        """
        # TODO this is broken
        # Nothing found locally. the parent continues.
        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                return self.parent().resolve_sync(name, t, type_only, local_only, callers + [self])

            # Call scopes that are included
            for include_scope in self._include_scopes:
                if isinstance(include_scope, ScopedSymbol) and include_scope not in callers:
                    return include_scope.resolve_sync(name, t, type_only, local_only, callers + [self])

        return None

    def get_typed_symbols(self, local_only: bool=True, callers: List[T]=[]) -> List[TypedSymbol]:
        """
        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively) and scopes that are included.
        :param callers: List of visited scopes, that should not be visited again
        :return: all accessible symbols that have a type assigned.
        """
        result: List[TypedSymbol]=[]

        for child in self.children():
            if isinstance(child, TypedSymbol):
                result.append(child)

        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                local_list=self.parent().get_typed_symbols(local_only, callers + [self])
                result.extend(local_list)

            # Call scopes that are included
            for include_scope in self._include_scopes:
                if isinstance(include_scope, ScopedSymbol) and include_scope not in callers:
                    local_list=include_scope.get_typed_symbols(local_only, callers + [self])
                    result.extend(local_list)

        return result

    def get_typed_symbol_names(self, local_only: bool=True, callers: List[T]=[]) -> List[str]:
        """
        The names of all accessible symbols with a type.

        :param local_only: If true only child symbols are returned, otherwise also symbols from the parent of this symbol
        (recursively) and scopes that are included.
        :param callers: List of visited scopes, that should not be visited again
        :return: A list of names.
        :param callers:
        """
        result: List[str]=[]
        for child in self.children():
            if isinstance(child, TypedSymbol):
                result.append(child.name)

        if not local_only:
            # Call parent scope
            if isinstance(self.parent(), ScopedSymbol) and self.parent() not in callers:
                local_list=self.parent().get_typed_symbol_names(local_only, callers + [self])
                result.extend(local_list)

            # Call scopes that are included
            for include_scope in self._include_scopes:
                if isinstance(include_scope, ScopedSymbol) and include_scope not in callers:
                    local_list=include_scope.get_typed_symbol_names(local_only, callers + [self])
                    result.extend(local_list)

        return result

    def symbol_from_path(self, path: str, separator=".") -> Optional[Symbol]:
        """
        :param path: The path consisting of symbol names separator by `separator`.
        :param separator: The character to separate path segments.
        :return: the symbol located at the given path through the symbol hierarchy.
        """
        elements=path.split(separator)
        index=0
        if elements[0] == self.name or len(elements[0]) == 0:
            index += 1

        result: Symbol=self
        while index < len(elements):
            if not isinstance(result, ScopedSymbol):
                return None

            child: Optional[Symbol]=next(
                filter(lambda candidate: candidate.name == elements[index], result.children()), None
            )
            if child is None:
                return None

            result=child
            index += 1

        return result

    def index_of_child(self, child: Symbol) -> int:
        """
        :param child: The child to search for.
        :return: the index of the given child symbol in the child list or -1 if it couldn't be found.
        """
        # two pass org
        # return lambda child,self.children() : self.children().index(child) if child in self.children() else -1
        try:
            return self.children().index(child)
        except ValueError:
            return -1

    def next_sibling_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the sibling symbol after the given child symbol, if one exists.
        """
        index=self.index_of_child(child)
        if index == -1 or index >= len(self.children()) - 1:
            return None

        return self.children()[index + 1]

    def previous_sibling_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the sibling symbol before the given child symbol, if one exists.
        """
        index=self.index_of_child(child)
        if index < 1:
            return None

        return self.children()[index - 1]

    def next_of(self, child: Symbol) -> Optional[Symbol]:
        """
        :param child: The reference node.
        :return: the next symbol in definition order, regardless of the scope.
        """
        if not isinstance(child.parent(), ScopedSymbol):
            return None

        if child.parent() is not self:
            return child.parent().nextOf(child)

        if isinstance(child, ScopedSymbol) and len(child.children()) > 0:
            return child.children()[0]

        sibling=self.next_sibling_of(child)
        if sibling is not None:
            return sibling

        return self.parent().next_of(self)
