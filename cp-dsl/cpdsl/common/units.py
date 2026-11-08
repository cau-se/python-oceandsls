#  Copyright (c) 2026.  OceanDSL (https://oceandsl.uni-kiel.de)
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
"""Conversion of the CP-DSL unit model (cpdsl.model.unit_model) into units of odsllib.units (cfunits, UDUNITS-2).

Prefixes and unit kinds are written as UDUNITS-2 names (``kilotonne``), not as symbols, because symbols are
ambiguous in UDUNITS-2: ``kt`` is the knot, not a kilotonne. Quoted custom units of declarations become custom units
of :class:`~odsllib.units.CompositeUnit`; the empty custom unit ``""``, which declarations use for values without
unit, is dimensionless.
"""

from typing import Optional

from odsllib.units import CompositeUnit, UnitError

from cpdsl.model.unit_model import Unit, UnitKind, UnitPrefix, SIUnit, CustomUnit, DivisionUnit, ExponentUnit, \
    UnitSpecification

PREFIX_NAMES = {
    UnitPrefix.NoP: "", UnitPrefix.Quetta: "quetta", UnitPrefix.Ronna: "ronna", UnitPrefix.Yotta: "yotta",
    UnitPrefix.Zetta: "zetta", UnitPrefix.Exa: "exa", UnitPrefix.Peta: "peta", UnitPrefix.Tera: "tera",
    UnitPrefix.Giga: "giga", UnitPrefix.Mega: "mega", UnitPrefix.Kilo: "kilo", UnitPrefix.Hecto: "hecto",
    UnitPrefix.Deca: "deka", UnitPrefix.Deci: "deci", UnitPrefix.Centi: "centi", UnitPrefix.Milli: "milli",
    UnitPrefix.Micro: "micro", UnitPrefix.Nano: "nano", UnitPrefix.Pico: "pico", UnitPrefix.Femto: "femto",
    UnitPrefix.Atto: "atto", UnitPrefix.Zepto: "zepto", UnitPrefix.Yocto: "yocto", UnitPrefix.Ronto: "ronto",
    UnitPrefix.Quecto: "quecto",
}

KIND_NAMES = {
    UnitKind.Second: "second", UnitKind.Meter: "meter", UnitKind.Gram: "gram", UnitKind.Ampere: "ampere",
    UnitKind.Kelvin: "kelvin", UnitKind.Mole: "mole", UnitKind.Candela: "candela", UnitKind.Pascal: "pascal",
    UnitKind.Joule: "joule", UnitKind.ton: "tonne", UnitKind.Hour: "hour", UnitKind.Day: "day",
}


def to_composite_unit(unit: Optional[Unit]) -> Optional[CompositeUnit]:
    """The unit of odsllib.units for a unit of the CP-DSL unit model, None for no unit.

    :raises UnitError: for unit kinds that have no UDUNITS-2 name (UnitKind.Unknown)
    """
    if unit is None:
        return None
    if isinstance(unit, SIUnit):
        name = KIND_NAMES.get(unit.kind)
        if name is None:
            raise UnitError(f"unknown unit kind {unit.kind}")
        return CompositeUnit.of(PREFIX_NAMES[unit.prefix or UnitPrefix.NoP] + name)
    if isinstance(unit, CustomUnit):
        return CompositeUnit() if unit.name == "" else CompositeUnit.custom_unit(unit.name)
    if isinstance(unit, DivisionUnit):
        return to_composite_unit(unit.numerator) / to_composite_unit(unit.denominator)
    if isinstance(unit, ExponentUnit):
        return to_composite_unit(unit.unit) ** unit.exponent
    if isinstance(unit, UnitSpecification):
        result = CompositeUnit()
        for part in unit.units:
            result = result * to_composite_unit(part)
        return result
    raise UnitError(f"unsupported unit {unit!r}")
