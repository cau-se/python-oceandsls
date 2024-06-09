  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
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
from typing import List, Optional
from utils import classproperty

#
# Type system
#

class TypeKind(Enum):
    """
    Primitive types.
    """
    Unknown = 0
    Integer = 1
    Float = 2
    Number = 3
    String = 4
    Char = 5
    Boolean = 6
    Class = 7
    Interface = 8
    Array = 9
    Map = 10
    Enum = 11
    Alias = 12

@dataclass
class Type:
    """
    The root type. Used for typed symbols and type aliases.
    """
    name: str

    # The super type of this type or empty if this is a fundamental type.
    # Also used as the target type for type aliases.
    base_types: Optional[List[Type]]
    kind: Optional[TypeKind]
    # reference: Optional[ReferenceKind]


class FundamentalType(Type):
    """
    A single class for all fundamental types. They are distinguished via the kind field.
    """

    # , reference_kind=ReferenceKind.Irrelevant
    def __init__(self, name: str, base_types=[], type_kind=TypeKind.Unknown):
        # , reference=reference_kind
        super().__init__(name=name, base_types=base_types, kind=type_kind)

    @classproperty
    def integer_type(self) -> FundamentalType:
        return FundamentalType(name="integer", type_kind=TypeKind.Integer)

    @classproperty
    def real_type(self) -> FundamentalType:
        return FundamentalType(name="real", type_kind=TypeKind.Float)

    @classproperty
    def float_type(self) -> FundamentalType:
        return FundamentalType(name="float", type_kind=TypeKind.Float)

    @classproperty
    def string_type(self) -> FundamentalType:
        return FundamentalType(name="string", type_kind=TypeKind.String)

    @classproperty
    def bool_type(self) -> FundamentalType:
        return FundamentalType(name="bool", type_kind=TypeKind.Boolean)


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

