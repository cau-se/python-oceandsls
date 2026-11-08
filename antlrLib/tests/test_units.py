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
"""Tests of the units of the OceanDSL languages (odsllib.units)."""

import unittest
from unittest.mock import patch

from parameterized import parameterized

import odsllib.units as units_module
from odsllib.units import CompositeUnit, UnitError, units_available, unavailable_reason

M = CompositeUnit.of("m")
KM = CompositeUnit.of("km")
S = CompositeUnit.of("s")
PEBBLE = CompositeUnit.custom_unit("pebble")
COIN = CompositeUnit.custom_unit("coin")
REQUIRES_CFUNITS = unittest.skipUnless(units_available(), "cfunits or the UDUNITS-2 library is not installed")


def without_cfunits():
    """Patch odsllib.units as if cfunits were not installed."""
    return patch.multiple("odsllib.units", _cfunits=lambda: None, _unavailable_reason="cfunits is not installed")


class TestCompositeUnit(unittest.TestCase):

    @parameterized.expand([
        ("udunits_only", CompositeUnit.of("m.s-1"), "m.s-1", (), "m.s-1"),
        # A unit that UDUNITS-2 knows
        # Input: of('m.s-1')
        # Expected Result: the UDUNITS-2 part m.s-1, no custom units

        ("dimensionless", CompositeUnit.of(""), "1", (), "1"),
        # An empty UDUNITS-2 part is dimensionless
        # Input: of('')
        # Expected Result: the UDUNITS-2 part 1

        ("custom_only", PEBBLE, "1", (("pebble", 1),), "pebble"),
        # A custom unit
        # Input: custom_unit('pebble')
        # Expected Result: no UDUNITS-2 part, the custom unit pebble

        ("mixed", CompositeUnit.of("m-2", {"pebble": 1, "coin": -1, "gone": 0}), "m-2",
         (("coin", -1), ("pebble", 1)), "m-2 coin^-1 pebble"),
        # Custom units are sorted and zero exponents dropped
        # Input: of('m-2', {'pebble': 1, 'coin': -1, 'gone': 0})
        # Expected Result: m-2 with coin^-1 and pebble
    ])
    def test_of(self, test_name, unit, expected_udunits, expected_custom, expected_text):
        self.assertEqual((expected_udunits, expected_custom, expected_text), (unit.udunits, unit.custom, str(unit)),
                         test_name)

    @parameterized.expand([
        ("product", M * S, CompositeUnit("(m).(s)")),
        # Products keep both UDUNITS-2 parts in parentheses
        # Input: m * s
        # Expected Result: (m).(s)

        ("quotient", M / S, CompositeUnit("(m).((s)^-1)")),
        # A quotient is a product with a negative power
        # Input: m / s
        # Expected Result: (m).((s)^-1)

        ("power", KM ** 2, CompositeUnit("(km)^2")),
        # A power
        # Input: km ** 2
        # Expected Result: (km)^2

        ("dimensionless_factor", CompositeUnit() * M, M),
        # Dimensionless factors are dropped
        # Input: 1 * m
        # Expected Result: m

        ("custom_product", PEBBLE * M / PEBBLE, M),
        # Custom units cancel out
        # Input: pebble * m / pebble
        # Expected Result: m

        ("custom_power", (PEBBLE / COIN) ** 2, CompositeUnit("1", (("coin", -2), ("pebble", 2)))),
        # Powers of custom units
        # Input: (pebble / coin) ** 2
        # Expected Result: coin^-2 pebble^2

        ("power_zero", (M * PEBBLE) ** 0, CompositeUnit()),
        # The power zero is dimensionless
        # Input: (m * pebble) ** 0
        # Expected Result: 1
    ])
    def test_arithmetic(self, test_name, unit, expected):
        self.assertEqual(expected, unit, test_name)

    @parameterized.expand([
        ("identical", M, CompositeUnit.of("m"), True),
        # Identical units are equivalent without cfunits
        # Input: m and m
        # Expected Result: True

        ("different_custom_units", PEBBLE, COIN, False),
        # Different custom units are never equivalent
        # Input: pebble and coin
        # Expected Result: False

        ("same_custom_other_udunits", M * PEBBLE, KM * COIN, False),
        # The custom units decide first
        # Input: m pebble and km coin
        # Expected Result: False

        ("needs_udunits", M, KM, None),
        # Other UDUNITS-2 parts cannot be compared without cfunits
        # Input: m and km
        # Expected Result: None (unknown)
    ])
    def test_equivalent_without_cfunits(self, test_name, unit, other, expected):
        with without_cfunits():
            self.assertEqual(expected, unit.equivalent(other), test_name)
            self.assertIsNone(unit.is_valid(), test_name)

    @parameterized.expand([
        ("identical", 2.5, M, M, 2.5, None),
        # Identical units need no conversion
        # Input: 2.5 m to m
        # Expected Result: 2.5

        ("other_unit", 1.0, KM, M, None, "cfunits is not installed"),
        # Without cfunits other units cannot be converted
        # Input: 1 km to m
        # Expected Result: UnitError naming the reason

        ("other_custom_unit", 1.0, PEBBLE, COIN, None, "not equivalent"),
        # Different custom units are known to be incompatible
        # Input: 1 pebble to coin
        # Expected Result: UnitError, not equivalent
    ])
    def test_convert_without_cfunits(self, test_name, value, unit, to, expected, expected_error):
        with without_cfunits():
            if expected_error:
                with self.assertRaises(UnitError) as context:
                    unit.convert(value, to)
                self.assertIn(expected_error, str(context.exception), test_name)
            else:
                self.assertEqual(expected, unit.convert(value, to), test_name)

    @parameterized.expand([
        ("missing_library", "cfunits requires UNIDATA UDUNITS-2", False),
        # The UDUNITS-2 library is missing
        # Input: importing cfunits raises FileNotFoundError
        # Expected Result: units are not available, the reason names the error

        ("not_installed", "No module named 'cfunits'", False),
        # cfunits is not installed
        # Input: importing cfunits raises ModuleNotFoundError
        # Expected Result: units are not available, the reason names the error

        ("installed", None, True),
        # cfunits can be imported
        # Input: importing cfunits succeeds
        # Expected Result: units are available, no reason
    ])
    def test_loading(self, test_name, error, expected_available):
        def fake_import(name, *args, **kwargs):
            if name == "cfunits":
                if error is None:
                    return object()
                raise (FileNotFoundError if "UDUNITS" in error else ModuleNotFoundError)(error)
            return original_import(name, *args, **kwargs)

        original_import = __import__
        with patch.multiple("odsllib.units", _cfunits_module=units_module._UNSET,  # pylint: disable=protected-access
                            _unavailable_reason=None), patch("builtins.__import__", fake_import):
            self.assertEqual(expected_available, units_available(), test_name)
            reason = unavailable_reason()
            if error is None:
                self.assertIsNone(reason, test_name)
            else:
                self.assertIn(error, reason, test_name)


@REQUIRES_CFUNITS
class TestCompositeUnitWithCfunits(unittest.TestCase):

    @parameterized.expand([
        ("valid", CompositeUnit.of("mmol.m-3"), True),
        # A unit that UDUNITS-2 knows
        # Input: mmol.m-3
        # Expected Result: valid

        ("invalid", CompositeUnit.of("milli mole / (meter ** 3)"), False),
        # Spaces around operators are no UDUNITS-2 syntax
        # Input: 'milli mole / (meter ** 3)'
        # Expected Result: invalid

        ("custom_only", PEBBLE, True),
        # Custom units are kept beside the (dimensionless) UDUNITS-2 part
        # Input: pebble
        # Expected Result: valid
    ])
    def test_is_valid(self, test_name, unit, expected):
        self.assertEqual(expected, unit.is_valid(), test_name)

    @parameterized.expand([
        ("prefix", KM, M, True),
        # Prefixed units are equivalent
        # Input: km and m
        # Expected Result: True

        ("composed", M / S, CompositeUnit.of("km.h-1"), True),
        # Composed units are compared by their dimension
        # Input: m / s and km.h-1
        # Expected Result: True

        ("other_dimension", M, S, False),
        # Different dimensions
        # Input: m and s
        # Expected Result: False

        ("custom_with_udunits", KM * PEBBLE, M * PEBBLE, True),
        # Same custom units and equivalent UDUNITS-2 parts
        # Input: km pebble and m pebble
        # Expected Result: True

        ("invalid", CompositeUnit.of("nonsense"), M, False),
        # Invalid units are equivalent to nothing
        # Input: nonsense and m
        # Expected Result: False
    ])
    def test_equivalent(self, test_name, unit, other, expected):
        self.assertEqual(expected, unit.equivalent(other), test_name)

    @parameterized.expand([
        ("prefix", 2.0, KM, M, 2000.0),
        # A prefixed unit
        # Input: 2 km to m
        # Expected Result: 2000

        ("speed", 2.0, CompositeUnit.of("km/h"), M / S, 2 / 3.6),
        # A composed unit
        # Input: 2 km/h to m/s
        # Expected Result: 0.5556

        ("offset", 0.0, CompositeUnit.of("degC"), CompositeUnit.of("K"), 273.15),
        # A unit with offset
        # Input: 0 degC to K
        # Expected Result: 273.15

        ("custom_scaled", 1.0, KM * PEBBLE, M * PEBBLE, 1000.0),
        # Only the UDUNITS-2 part is scaled
        # Input: 1 km pebble to m pebble
        # Expected Result: 1000
    ])
    def test_convert(self, test_name, value, unit, to, expected):
        self.assertAlmostEqual(expected, unit.convert(value, to), msg=test_name)

    @parameterized.expand([
        ("other_dimension", M, S),
        # Different dimensions cannot be converted
        # Input: m to s
        # Expected Result: UnitError

        ("other_custom_unit", PEBBLE, COIN),
        # Different custom units cannot be converted
        # Input: pebble to coin
        # Expected Result: UnitError

        ("invalid", CompositeUnit.of("nonsense"), M),
        # Invalid units cannot be converted
        # Input: nonsense to m
        # Expected Result: UnitError
    ])
    def test_convert_errors(self, test_name, unit, to):
        with self.assertRaises(UnitError, msg=test_name):
            unit.convert(1.0, to)


if __name__ == '__main__':
    unittest.main()
