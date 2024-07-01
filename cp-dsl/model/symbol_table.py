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

__author__ = "stu222808,sgu,reiner"

# Utils import
import asyncio
from enum import Enum
from dataclasses import dataclass
from typing import Coroutine, List, Optional, ParamSpec, Set, TypeVar
from model.type_system import Type, NamedType

# Antlr4
from antlr4.tree.Tree import ParseTree

from model.type_system import Type
from model.units import Unit

class DuplicateSymbolError(Exception):
    pass

import abc

# TODO should be renamed to ModelObject or SymbolObject or ModelSymbol
# The generic scope interface that manages access to types and data
class Scope:

    parent:Scope

    def __init__(self, parent = None) -> None:
        self.parent = parent

    def resolve_symbol(self, name:str):
        raise NotImplementedError(f"Name {name} not found {self}")

#
# Declaration Model
#
class DeclarationModel(Scope):

    def __init__(self):
        super().__init__()
        self._groups = {}
        self._features = {}
        self._types = {}

    def add_new_type(self, type:Type):
        if isinstance(type,NamedType):
            self._types[type.name] = type
        else:
            self._types[type.__hash__] = type

    def resolve_type(self, name:str):
        return self._types.get(name, None)



