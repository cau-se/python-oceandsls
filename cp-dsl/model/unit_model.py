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
from typing import List

from .utils import classproperty

#
# units of datatypes
#


class UnitKind(Enum):
    """
    Rough categorization of a unit from SI units.
    """
    Unknown = 0
    Second = 1
    Meter = 2
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
    Quetta = 30
    Ronna = 27
    Yotta = 24
    Zetta = 21
    Exa = 18
    Peta = 15
    Tera = 12
    Giga = 9
    Mega = 6
    Kilo = 3
    Hecto = 2
    Deca = 1
    Deci = -1
    Centi = -2
    Milli = -3
    Micro = -6
    Nano = -9
    Pico = -12
    Femto = -15
    Atto = -18
    Zepto = -21
    Yocto = -24
    Ronto = -27
    Quecto = -30


class Unit:
    pass


@dataclass
class SIUnit(Unit):
    prefix: UnitPrefix
    kind: UnitKind


@dataclass
class CustomUnit(Unit):
    name: str


@dataclass
class DivisionUnit(Unit):
    numerator: Unit
    denominator: Unit


@dataclass
class ExponentUnit(Unit):
    unit: Unit
    exponent: int


@dataclass
class UnitSpecification(Unit):
    units: List[Unit]
