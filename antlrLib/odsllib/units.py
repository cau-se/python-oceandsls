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
"""Units of measurement for the OceanDSL languages, checked and converted with cfunits (UDUNITS-2).

A :class:`CompositeUnit` combines a unit that UDUNITS-2 knows (``udunits``, e.g. ``'mmol.m-3'``) with custom units
(``custom``, e.g. ``pebble`` or a substance in a biogeochemical model). cfunits 3.3 cannot define new units, so the
custom units are kept beside the UDUNITS-2 part: two units are equivalent if their UDUNITS-2 parts are equivalent and
their custom units are identical, and conversions only scale the UDUNITS-2 part. Once cfunits supports
``Units.new_unit`` (NCAS-CMS/cfunits#59), custom units can become UDUNITS-2 units (see ``merge_PR59.txt``).

cfunits is an optional dependency (``pip install odsllib[units]``) that also needs the UDUNITS-2 C library. Without
it, :func:`units_available` is False, validity and equivalence are unknown (None) and only identical units can be
converted, so the language servers keep working without unit checks.
"""

from __future__ import annotations

import logging
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, Optional, Tuple, Union

_log = logging.getLogger(__name__)

_UNSET = object()
_cfunits_module = _UNSET
_unavailable_reason: Optional[str] = None


class UnitError(ValueError):
    """A unit is invalid, or a value cannot be converted between two units."""


def _cfunits():
    """The cfunits module, None if it or the UDUNITS-2 library is not installed (loaded once)."""
    global _cfunits_module, _unavailable_reason  # pylint: disable=global-statement
    if _cfunits_module is _UNSET:
        try:
            import cfunits  # pylint: disable=import-outside-toplevel
            _cfunits_module = cfunits
        except (ImportError, OSError) as error:  # OSError: FileNotFoundError if the UDUNITS-2 library is missing
            _cfunits_module = None
            _unavailable_reason = f"unit checks are disabled: {error}"
            _log.info("%s", _unavailable_reason)
    return _cfunits_module


def units_available() -> bool:
    """Whether cfunits and the UDUNITS-2 library are installed, i.e. whether units can be checked and converted."""
    return _cfunits() is not None


def unavailable_reason() -> Optional[str]:
    """Why units cannot be checked, None if they can."""
    _cfunits()
    return _unavailable_reason


CustomUnits = Tuple[Tuple[str, int], ...]


def _custom_units(custom: Union[None, Dict[str, int], Iterable[Tuple[str, int]]]) -> CustomUnits:
    """Sorted (name, exponent) pairs without zero exponents."""
    counter: Counter = Counter()
    for name, exponent in (custom.items() if isinstance(custom, dict) else (custom or ())):
        counter[name] += exponent
    return tuple(sorted((name, exponent) for name, exponent in counter.items() if exponent != 0))


def _product(left: str, right: str) -> str:
    if left == "1":
        return right
    if right == "1":
        return left
    return f"({left}).({right})"


def _power(unit: str, exponent: int) -> str:
    if exponent == 0 or unit == "1":
        return "1"
    if exponent == 1:
        return unit
    return f"({unit})^{exponent}"


@dataclass(frozen=True)
class CompositeUnit:
    """A UDUNITS-2 unit combined with custom units.

    :param udunits: the UDUNITS-2 part in UDUNITS-2 syntax (no spaces around operators), ``'1'`` if dimensionless
    :param custom: the custom units as sorted (name, exponent) pairs, use :meth:`of` to create them from a dict
    """
    udunits: str = "1"
    custom: CustomUnits = ()

    @classmethod
    def of(cls, udunits: str = "1",
           custom: Union[None, Dict[str, int], Iterable[Tuple[str, int]]] = None) -> CompositeUnit:
        """A unit of a UDUNITS-2 part and custom units given as dict or pairs, e.g. ``of('m-2', {'pebble': 1})``."""
        return cls(udunits.strip() or "1", _custom_units(custom))

    @classmethod
    def custom_unit(cls, name: str) -> CompositeUnit:
        """A custom unit, e.g. ``custom_unit('pebble')``."""
        return cls("1", ((name, 1),))

    def __mul__(self, other: CompositeUnit) -> CompositeUnit:
        return CompositeUnit(_product(self.udunits, other.udunits), _custom_units(self.custom + other.custom))

    def __truediv__(self, other: CompositeUnit) -> CompositeUnit:
        return self * other ** -1

    def __pow__(self, exponent: int) -> CompositeUnit:
        return CompositeUnit(_power(self.udunits, exponent),
                             _custom_units((name, power * exponent) for name, power in self.custom))

    def __str__(self) -> str:
        parts = [] if self.udunits == "1" else [self.udunits]
        parts += [name if exponent == 1 else f"{name}^{exponent}" for name, exponent in self.custom]
        return " ".join(parts) or "1"

    def _udunits_units(self):
        """The cfunits Units of the UDUNITS-2 part, None if cfunits is not available."""
        cfunits = _cfunits()
        return None if cfunits is None else cfunits.Units(self.udunits)

    def is_valid(self) -> Optional[bool]:
        """Whether UDUNITS-2 knows the UDUNITS-2 part, None if that cannot be checked."""
        units = self._udunits_units()
        return None if units is None else bool(units.isvalid)

    def equivalent(self, other: CompositeUnit) -> Optional[bool]:
        """Whether values can be converted between the units, None if that cannot be checked."""
        if self.custom != other.custom:
            return False
        if self.udunits == other.udunits:
            return True
        this, that = self._udunits_units(), other._udunits_units()  # pylint: disable=protected-access
        if this is None:
            return None
        return bool(this.isvalid and that.isvalid and this.equivalent(that))

    def convert(self, value: float, to: CompositeUnit) -> float:
        """Convert a value of this unit to another unit.

        :raises UnitError: if the units are not equivalent or the conversion cannot be checked
        """
        if self == to:
            return value
        equivalent = self.equivalent(to)
        if equivalent is None:
            raise UnitError(f"cannot convert from {self} to {to}: {unavailable_reason()}")
        if not equivalent:
            raise UnitError(f"cannot convert from {self} to {to}: the units are not equivalent")
        cfunits = _cfunits()
        return float(cfunits.Units.conform(value, cfunits.Units(self.udunits), cfunits.Units(to.udunits)))


DIMENSIONLESS = CompositeUnit()
