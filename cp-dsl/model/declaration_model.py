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
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Coroutine, TypeVar, List, Dict

# Antlr4
from antlr4.tree.Tree import ParseTree

from .symbols import Scope, NamedElement
from .symbols import ScopedSymbol, Symbol, UnitSymbol
from .type_system import NamedType, Type, GenericEnumeralType, EnumeralType
from .unit_model import UnitSpecification
from .arithmetic_model import ArithmeticExpression

#
# Model elements of the DSL
#
# These include
# - user types
# - Parameter Groups
# - Parameter
# - Features Sets
# - Feature
# - Expressions

#
# Declaration Model
#


class DeclarationModel(Scope):

    def __init__(self, name: str = None):
        super().__init__(None)  # DeclarationModel has no parent
        self._name = name
        self._groups = {}
        self._features = {}
        self._types = {}

    def add_new_type(self, type: Type):
        if isinstance(type, NamedType):
            self._types[type.name] = type
        else:
            self._types[type.__hash__] = type

    def resolve_type(self, name: str):
        return self._types.get(name, None)

#
# Types
#


class InlineEnumerationType(GenericEnumeralType):

    def __init__(self) -> None:
        super().__init__()

#
# Parameter Groups
#


class Parameter(NamedElement):

    _type: NamedType
    _unit: UnitSymbol
    _description: str
    _default_value: ArithmeticExpression = None
    _value = None

    def __init__(self, name: str, type: NamedType, unit: UnitSymbol, description: str = None, parent=None) -> None:
        super().__init__(name, parent)
        self._type = type
        self._unit = unit
        self._description = description


class ParameterGroup(NamedElement):

    _description: str
    _parameters: Dict[str, Parameter]

    def __init__(self, name: str, description: str, parent: Scope):
        super().__init__(name, parent)
        self._description = description
        self._parameters = {}

    def resolve_symbol(self, name: str) -> Parameter:
        return self._parameters.get(name, None)

#
# Features
#


class EKind(Enum):
    ALTERNATIVE = 0
    MULTIPLE = 1


class FeatureGroup(Scope):

    _kind: EKind
    _features = {}

    def __init__(self, name: str, parent: Scope):
        super().__init__(parent)


class Feature(NamedElement):

    _is_activated: bool = False  # set if the feature is activated
    _required: bool = False
    _description: str = None
    _requires: List[Feature] = []
    _excludes: List[Feature] = []

    _groups: Dict[str, ParameterGroup] = {}
    _features: Dict[str, FeatureGroup] = {}

    def __init__(self, name: str, description: str, parent: Scope):
        super().__init__(name, parent)
        self._description = description
