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
"""Tests of the conversion of the CP-DSL unit model into units of odsllib.units (cpdsl.common.units)."""

import unittest

from parameterized import parameterized

from odsllib.units import CompositeUnit, UnitError, units_available

from cpdsl.common.units import to_composite_unit
from cpdsl.model.unit_model import UnitKind, UnitPrefix, SIUnit, CustomUnit, DivisionUnit, ExponentUnit, \
    UnitSpecification

METER = SIUnit(None, UnitKind.Meter)
SECOND = SIUnit(None, UnitKind.Second)
REQUIRES_CFUNITS = unittest.skipUnless(units_available(), "cfunits or the UDUNITS-2 library is not installed")


class TestToCompositeUnit(unittest.TestCase):

    @parameterized.expand([
        ("no_unit", None, None),
        # A value or parameter without unit
        # Input: None
        # Expected Result: None

        ("si_unit", METER, CompositeUnit.of("meter")),
        # SI units are written as UDUNITS-2 names
        # Input: meter without prefix
        # Expected Result: meter

        ("no_prefix", SIUnit(UnitPrefix.NoP, UnitKind.Second), CompositeUnit.of("second")),
        # The prefix NoP is no prefix
        # Input: second with the prefix NoP
        # Expected Result: second

        ("prefix", SIUnit(UnitPrefix.Kilo, UnitKind.Gram), CompositeUnit.of("kilogram")),
        # Prefix names precede the unit name
        # Input: kilo gram
        # Expected Result: kilogram

        ("tonne", SIUnit(UnitPrefix.Kilo, UnitKind.ton), CompositeUnit.of("kilotonne")),
        # ton is the metric tonne; names avoid the symbol kt, which is the knot in UDUNITS-2
        # Input: kilo ton
        # Expected Result: kilotonne

        ("deca", SIUnit(UnitPrefix.Deca, UnitKind.Meter), CompositeUnit.of("dekameter")),
        # UDUNITS-2 spells the prefix deka
        # Input: deca meter
        # Expected Result: dekameter

        ("dimensionless_custom_unit", CustomUnit(""), CompositeUnit()),
        # Declarations use the empty custom unit for values without unit
        # Input: the custom unit ""
        # Expected Result: dimensionless

        ("custom_unit", CustomUnit("pebble"), CompositeUnit.custom_unit("pebble")),
        # Other custom units stay custom units
        # Input: the custom unit "pebble"
        # Expected Result: the custom unit pebble

        ("division", DivisionUnit(SIUnit(UnitPrefix.Kilo, UnitKind.Meter), SIUnit(None, UnitKind.Hour)),
         CompositeUnit.of("kilometer") / CompositeUnit.of("hour")),
        # A division
        # Input: kilometer divided by hour
        # Expected Result: kilometer / hour

        ("exponent", ExponentUnit(METER, -3), CompositeUnit.of("meter") ** -3),
        # A power
        # Input: meter to the power of -3
        # Expected Result: meter ** -3

        ("product_with_custom_unit", UnitSpecification([CustomUnit("pebble"), ExponentUnit(METER, -2)]),
         CompositeUnit.custom_unit("pebble") * CompositeUnit.of("meter") ** -2),
        # A product of a custom unit and an SI unit
        # Input: pebble and meter^-2
        # Expected Result: pebble * meter ** -2

        ("empty_specification", UnitSpecification([]), CompositeUnit()),
        # An empty unit specification
        # Input: no units
        # Expected Result: dimensionless
    ])
    def test_to_composite_unit(self, test_name, unit, expected):
        self.assertEqual(expected, to_composite_unit(unit), test_name)

    @parameterized.expand([
        ("unknown_kind", SIUnit(None, UnitKind.Unknown), "unknown unit kind"),
        # Unit kinds without UDUNITS-2 name
        # Input: the unit kind Unknown
        # Expected Result: UnitError

        ("unknown_kind_in_division", DivisionUnit(METER, SIUnit(UnitPrefix.Kilo, UnitKind.Unknown)),
         "unknown unit kind"),
        # Also inside composed units
        # Input: meter divided by an unknown unit kind
        # Expected Result: UnitError

        ("no_unit_model", "m", "unsupported unit"),
        # Strings are no units of the unit model
        # Input: the string 'm'
        # Expected Result: UnitError
    ])
    def test_to_composite_unit_errors(self, test_name, unit, expected_message):
        with self.assertRaises(UnitError) as context:
            to_composite_unit(unit)
        self.assertIn(expected_message, str(context.exception), test_name)

    @parameterized.expand([
        ("all_si_units", [SIUnit(None, kind) for kind in UnitKind if kind is not UnitKind.Unknown], True),
        # UDUNITS-2 knows the names of all unit kinds
        # Input: every unit kind except Unknown
        # Expected Result: valid

        ("all_supported_prefixes", [SIUnit(prefix, UnitKind.Meter) for prefix in UnitPrefix if prefix not in (
            UnitPrefix.Quetta, UnitPrefix.Ronna, UnitPrefix.Ronto, UnitPrefix.Quecto)], True),
        # UDUNITS-2 knows the names of the prefixes
        # Input: meter with every prefix except the four of 2022
        # Expected Result: valid

        ("prefixes_of_2022", [SIUnit(prefix, UnitKind.Meter) for prefix in (
            UnitPrefix.Quetta, UnitPrefix.Ronna, UnitPrefix.Ronto, UnitPrefix.Quecto)], False),
        # UDUNITS-2 2.2 does not know the prefixes quetta, ronna, ronto and quecto
        # Input: meter with these prefixes
        # Expected Result: invalid
    ])
    @REQUIRES_CFUNITS
    def test_udunits_names(self, test_name, units, expected_valid):
        for unit in units:
            self.assertEqual(expected_valid, to_composite_unit(unit).is_valid(), f"{test_name}: {unit}")

    @parameterized.expand([
        ("kilotonne", SIUnit(UnitPrefix.Kilo, UnitKind.ton), CompositeUnit.of("kg"), 1.0, 1e6),
        # A kilotonne is 10^6 kg
        # Input: 1 kilo ton in kg
        # Expected Result: 1000000

        ("day", SIUnit(None, UnitKind.Day), CompositeUnit.of("s"), 1.0, 86400.0),
        # A day has 86400 seconds
        # Input: 1 day in s
        # Expected Result: 86400

        ("speed", DivisionUnit(SIUnit(UnitPrefix.Kilo, UnitKind.Meter), SIUnit(None, UnitKind.Hour)),
         CompositeUnit.of("m/s"), 3.6, 1.0),
        # A composed unit
        # Input: 3.6 kilometer per hour in m/s
        # Expected Result: 1
    ])
    @REQUIRES_CFUNITS
    def test_conversion(self, test_name, unit, to, value, expected):
        self.assertAlmostEqual(expected, to_composite_unit(unit).convert(value, to), msg=test_name)


if __name__ == '__main__':
    unittest.main()
