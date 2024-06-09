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
from .symbol_table import TypeKind

#
# units of datatypes
#

class classproperty(property):
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()


class UnitKind(Enum):
    """
    Rough categorization of a unit from SI units.
    """
    Unknown = 0
    Second = 1
    Metre = 2
    # TODO si unit is kilogram | added to FundamentalUnit
    Gram = 3
    Ampere = 4
    Kelvin = 5
    Mole = 6
    Candela = 7
    # TODO add non si units?
    Pascal = 8
    Joule = 9
    ton = 10


class UnitPrefix(Enum):
    """
    Rough categorization of a unit from SI prefixes.
    """
    NoP = 0
    Quetta = 1
    Ronna = 2
    Yotta = 3
    Zetta = 4
    Exa = 5
    Peta = 6
    Tera = 7
    Giga = 8
    Mega = 9
    Kilo = 10
    Hecto = 11
    Deca = 12
    Deci = 13
    Centi = 14
    Mili = 15
    Micro = 16
    Nano = 17
    Pico = 18
    Femto = 19
    Atto = 20
    Zepto = 21
    Yocto = 22
    Ronto = 23
    Quecto = 24


@dataclass
class Unit:
    """
    The root unit. Used for unit symbols
    """
    name: str

    # The super unit of this unit or empty if this is a SI unit such as second.
    # TODO add units
    # TODO add aliases?
    base_types: List[Unit]
    prefix: UnitPrefix
    kind: UnitKind
    # reference: ReferenceKind

class FundamentalUnit(Unit):
    """
    A single class for all fundamental units which are mostly SI units. They are distinguished via the kind field.
    """

    def __init__(self, name: str, base_types=[], unit_prefix=UnitPrefix.NoP, unit_kind=UnitKind.Unknown):
        super().__init__(name=name, base_types=base_types, kind=unit_kind, prefix=unit_prefix)

    @classproperty
    def second_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="second", unit_kind=UnitKind.Second)

    @classproperty
    def metre_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="metre", unit_kind=UnitKind.Metre)

    # TODO si unit is kilogram but unitKind has gram
    @classproperty
    def gram_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="gram", unit_kind=UnitKind.Gram)

    # TODO si unit is kilogram but unitKind has gram
    @classproperty
    def kilogram_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="kilogram", unit_prefix=UnitPrefix.Kilo, unit_kind=UnitKind.Gram)

    @classproperty
    def ampere_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="ampere", unit_kind=UnitKind.Ampere)

    @classproperty
    def kelvin_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Kelvin", unit_kind=UnitKind.Kelvin)

    @classproperty
    def mole_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Mole", unit_kind=UnitKind.Mole)

    @classproperty
    def candela_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Candela", unit_kind=UnitKind.Candela)

    @classproperty
    def pascal_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Pascal", unit_kind=UnitKind.Pascal)

    @classproperty
    def joule_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Joule", unit_kind=UnitKind.Joule)

    # TODO si unit is kilogram. unitKind has gram but could include ton
    @classproperty
    def ton_unit(self) -> FundamentalUnit:
        return FundamentalUnit(name="Ton", unit_prefix=UnitPrefix.Mega, unit_kind=UnitKind.Gram)



class ComposedUnit():
    """The composed Unit Representation of the Declaration-DSL"""
    numerator: FundamentalUnit
    denominator: FundamentalUnit
    exponent: FundamentalUnit
    basicUnit: FundamentalUnit

    def __init__(self, basicUnit: FundamentalUnit = None, numerator: FundamentalUnit = None,
                 denominator: FundamentalUnit = None, exponent: FundamentalUnit = None) -> None:
        self.basicUnit = basicUnit
        self.numerator = numerator
        self.denominator = denominator
        self.exponent = exponent



class UnitSpecification():
    """CP-DSL Declaration UnitSpecification Representation Class"""
    prefix: UnitPrefix

    def __init__(self) -> None:
        self.composedUnitList = []
        self.prefix = None

    def add(self, unit: ComposedUnit):
        self.composedUnitList.append(unit)

    def get_units(self):
        return self.composedUnitList


