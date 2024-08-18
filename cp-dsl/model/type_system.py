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
from typing import List, Optional, Dict
from .utils import classproperty

#
# Type system
#

base_type_names = ["byte", "ubyte", "short", "ushort", "int", "unit", "long", "ulong", "single", "float", "double", "boolean", "string"]


@dataclass
class Type:
    pass


@dataclass
class NamedType(Type):
    """
    The root type. Used for typed symbols and type aliases.
    """
    name: str


@dataclass
class BaseType(NamedType):
    pass


base_types = {}

for name in base_type_names:
    base_types[name] = BaseType(name)


@dataclass
class Enumeral:
    name: str
    value: int


class GenericEnumeralType(Type):

    _enumerals: Dict[str,Enumeral]

    def __init__(self) -> None:
        self._enumerals = {}

class InternalEnumeralType(GenericEnumeralType):
    pass

class EnumeralType(GenericEnumeralType, NamedType):

    def __init__(self, name: str = "", enumerals={}):
        super().__init__()
        self.name = name
        self._enumerals = enumerals


class RangeType(NamedType):
    '''
    a class for ranges in cp-dsl
    '''

    def __init__(self, name, type: NamedType, minimum, maximum):
        super().__init__(name)
        self.type = type
        self.minimum = minimum
        self.maximum = maximum


class Dimension:

    def __init__(self, lower: int, upper: int) -> None:
        self.lower = lower
        self.upper = upper

    def get_size(self):
        return self.upper - self.lower


class ArrayType(Type):

    _type: NamedType
    _dimensions: List[Dimension]

    def __init__(self, type: NamedType, dimensions: List[Dimension]):
        self._type = type
        self._dimensions = dimensions


def get_fundamental_type(type: str = "") -> Type | FundamentalType:
    """
    Return FundamentalType of type or, if non-existent, new Type of type
    :param type: Type name to return
    :return: FundamentalType of type or, if non-existent, new Type of type
    """
    for key in FundamentalType.__dict__.keys():
        if type:
            if key == type.lower() + "_type":
                return getattr(FundamentalType, key)

            return Type(name=type.lower(), base_types=None, kind=None)
        else:
            return None
