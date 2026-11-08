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
"""Tests of the unit checks and conversions of configured values (cpdsl.generator.calculator.unit_calculator)."""

import unittest
from unittest.mock import patch

from parameterized import parameterized

from odsllib.units import units_available

from cpdsl.common.configuration import CompileFlags
from cpdsl.common.logger import GeneratorLogger
from cpdsl.generator.calculator.calculator import Calculator
from cpdsl.generator.calculator.unit_calculator import UnitCalculator, unit_of
from cpdsl.model.arithmetic_model import FloatValue, IntValue, StringValue
from cpdsl.model.declaration_model import DeclarationModel, Parameter
from cpdsl.model.type_system import base_types
from cpdsl.model.unit_model import UnitKind, UnitPrefix, SIUnit, CustomUnit, DivisionUnit

from generator.visitors.test_utils import AbstractTestGeneratorConfigurationVisitor

METER = SIUnit(None, UnitKind.Meter)
KILOMETER = SIUnit(UnitPrefix.Kilo, UnitKind.Meter)
SECOND = SIUnit(None, UnitKind.Second)
PEBBLE = CustomUnit("pebble")
REQUIRES_CFUNITS = unittest.skipUnless(units_available(), "cfunits or the UDUNITS-2 library is not installed")

DECLARATION = """
        model eval
            group g : "group" {
                def length float : meter = 1.0
                def speed float : meter / second = 1.0
                def count int : "pebble" = 0
                def plain float : "" = 0.0
            }
        """


def parameter(unit, name="p"):
    return Parameter(name, base_types["float"], unit, "", None)


def without_cfunits():
    """Patch odsllib.units as if cfunits were not installed."""
    return patch.multiple("odsllib.units", _cfunits=lambda: None, _unavailable_reason="cfunits is not installed")


class TestUnitCalculator(unittest.TestCase):

    def setUp(self):
        self.logger = GeneratorLogger(CompileFlags.STRICT)
        self.calculator = UnitCalculator(self.logger)

    def errors(self):
        return [message for severity, _, message in self.logger.messages if severity == "error"]

    @parameterized.expand([
        ("explicit_unit", FloatValue(None, KILOMETER, base_types["double"], 1.0), KILOMETER),
        # The unit written with a value
        # Input: 1.0 km
        # Expected Result: km

        ("no_unit", IntValue(None, None, base_types["long"], 1), None),
        # A value without unit
        # Input: 1
        # Expected Result: None

        ("reference", parameter(SECOND), SECOND),
        # A reference to a parameter has the unit of the parameter
        # Input: a parameter in s
        # Expected Result: s
    ])
    def test_unit_of(self, test_name, expression, expected):
        self.assertEqual(expected, unit_of(expression), test_name)

    @parameterized.expand([
        ("same_unit", METER, METER, True, []),
        # A value in the declared unit
        # Input: m for a parameter in m
        # Expected Result: compatible, no error

        ("no_value_unit", METER, None, True, []),
        # Values without unit are in the declared unit
        # Input: no unit for a parameter in m
        # Expected Result: compatible

        ("no_declared_unit", None, SECOND, True, []),
        # Parameters without unit accept every unit
        # Input: s for a parameter without unit
        # Expected Result: compatible

        ("same_custom_unit", PEBBLE, PEBBLE, True, []),
        # Identical custom units need no cfunits
        # Input: pebble for a parameter in pebble
        # Expected Result: compatible

        ("other_custom_unit", PEBBLE, CustomUnit("coin"), False,
         ["Unit coin of the value is not compatible with unit pebble of parameter p"]),
        # Different custom units are never compatible
        # Input: coin for a parameter in pebble
        # Expected Result: an error

        ("unknown_kind", METER, SIUnit(None, UnitKind.Unknown), True,
         ["Invalid unit: unknown unit kind UnitKind.Unknown"]),
        # Units without UDUNITS-2 name are reported and not checked further
        # Input: an unknown unit kind for a parameter in m
        # Expected Result: an error about the invalid unit
    ])
    def test_check(self, test_name, target, source, expected, expected_errors):
        self.assertEqual(expected, self.calculator.check(target, source, parameter(target)), test_name)
        self.assertEqual(expected_errors, self.errors(), test_name)

    @parameterized.expand([
        ("prefixed_unit", METER, KILOMETER, True, []),
        # A prefixed unit is compatible
        # Input: km for a parameter in m
        # Expected Result: compatible

        ("other_dimension", METER, SECOND, False,
         ["Unit second of the value is not compatible with unit meter of parameter p"]),
        # A unit of another dimension
        # Input: s for a parameter in m
        # Expected Result: an error naming both units and the parameter

        ("composed_unit", DivisionUnit(METER, SECOND), DivisionUnit(KILOMETER, SIUnit(None, UnitKind.Hour)), True, []),
        # Composed units are compared by their dimension
        # Input: km/h for a parameter in m/s
        # Expected Result: compatible

        ("prefix_unknown_to_udunits", METER, SIUnit(UnitPrefix.Quetta, UnitKind.Meter), False,
         ["Unit quettameter is not known to UDUNITS-2"]),
        # UDUNITS-2 2.2 does not know the prefixes of 2022
        # Input: quetta meter for a parameter in m
        # Expected Result: an error about the unknown unit
    ])
    @REQUIRES_CFUNITS
    def test_check_with_cfunits(self, test_name, target, source, expected, expected_errors):
        self.assertEqual(expected, self.calculator.check(target, source, parameter(target)), test_name)
        self.assertEqual(expected_errors, self.errors(), test_name)

    @parameterized.expand([
        ("other_unit", METER, KILOMETER),
        # Without cfunits other units cannot be compared and are accepted
        # Input: km for a parameter in m
        # Expected Result: compatible, no error

        ("other_dimension", METER, SECOND),
        # Even other dimensions cannot be detected
        # Input: s for a parameter in m
        # Expected Result: compatible, no error

        ("twice", DivisionUnit(METER, SECOND), METER),
        # The skipped check is reported once
        # Input: m for a parameter in m/s, checked twice
        # Expected Result: compatible, one information
    ])
    def test_check_without_cfunits(self, test_name, target, source):
        with without_cfunits(), self.assertLogs("cpc", level="INFO") as logs:
            self.assertTrue(self.calculator.check(target, source, parameter(target)), test_name)
            self.assertTrue(self.calculator.check(target, source, parameter(target)), test_name)
        self.assertEqual([], self.errors(), test_name)
        self.assertEqual(["INFO:cpc:cfunits is not installed"], logs.output, test_name)

    @parameterized.expand([
        ("same_unit", FloatValue(None, METER, base_types["double"], 2.5), METER, METER, 2.5),
        # No conversion in the declared unit
        # Input: 2.5 m for a parameter in m
        # Expected Result: 2.5

        ("no_unit", IntValue(None, None, base_types["long"], 3), None, METER, 3),
        # Values without unit are not converted
        # Input: 3 for a parameter in m
        # Expected Result: 3

        ("not_numeric", StringValue(None, None, base_types["string"], "text"), KILOMETER, METER, "text"),
        # Only numbers are converted
        # Input: 'text' with the unit km for a parameter in m
        # Expected Result: 'text'
    ])
    def test_convert_unchanged(self, test_name, value, source, target, expected):
        result = self.calculator.convert(value, source, target, parameter(target))
        self.assertIs(value, result, test_name)
        self.assertEqual(expected, result.value, test_name)

    @parameterized.expand([
        ("prefixed_unit", IntValue(None, KILOMETER, base_types["long"], 4), KILOMETER, METER, 4000.0, []),
        # A value in km for a parameter in m is converted to a float in m
        # Input: 4 km for a parameter in m
        # Expected Result: 4000.0 m

        ("speed", FloatValue(None, None, base_types["double"], 36.0),
         DivisionUnit(KILOMETER, SIUnit(None, UnitKind.Hour)), DivisionUnit(METER, SECOND), 10.0, []),
        # A composed unit
        # Input: 36 km/h for a parameter in m/s
        # Expected Result: 10.0 m/s

        ("other_dimension", FloatValue(None, SECOND, base_types["double"], 2.0), SECOND, METER, 2.0, []),
        # Incompatible units are not converted; check() reports them
        # Input: 2 s for a parameter in m
        # Expected Result: no error from the conversion, the value 2.0
    ])
    @REQUIRES_CFUNITS
    def test_convert(self, test_name, value, source, target, expected, expected_errors):
        result = self.calculator.convert(value, source, target, parameter(target))
        self.assertAlmostEqual(expected, result.value, msg=test_name)
        self.assertEqual(target if expected != value.value else value.unit, result.unit, test_name)
        self.assertEqual(expected_errors, self.errors(), test_name)

    @parameterized.expand([
        ("prefixed_unit", KILOMETER, METER,
         "Value of parameter p not converted: cannot convert from kilometer to meter: cfunits is not installed"),
        # Without cfunits a value in another unit cannot be converted, which is reported
        # Input: 4 km for a parameter in m
        # Expected Result: an error, the value is kept

        ("composed_unit", DivisionUnit(KILOMETER, SIUnit(None, UnitKind.Hour)), DivisionUnit(METER, SECOND),
         "Value of parameter p not converted: cannot convert from (kilometer).((hour)^-1) to (meter).((second)^-1): "
         "cfunits is not installed"),
        # The same for composed units
        # Input: 4 km/h for a parameter in m/s
        # Expected Result: an error, the value is kept

        ("custom_units", PEBBLE, CustomUnit("coin"), None),
        # Different custom units are known to be incompatible and left to check()
        # Input: 4 pebble for a parameter in coin
        # Expected Result: no error, the value is kept
    ])
    def test_convert_without_cfunits(self, test_name, source, target, expected_error):
        value = IntValue(None, source, base_types["long"], 4)
        with without_cfunits():
            result = self.calculator.convert(value, source, target, parameter(target))
        self.assertIs(value, result, test_name)
        self.assertEqual([expected_error] if expected_error else [], self.errors(), test_name)


class TestConfiguredUnits(AbstractTestGeneratorConfigurationVisitor):

    def setUp(self):
        self.logger = GeneratorLogger(CompileFlags.STRICT)
        self.model: DeclarationModel = self.parse_declaration_code(DECLARATION)

    def configure(self, configuration):
        self.parse_code(f"configuration test : eval\ngroup g {{\n{configuration}\n}}\n", self.model)
        return self.model

    def errors(self):
        return [message for severity, _, message in self.logger.messages if severity == "error"]

    @parameterized.expand([
        ("plain_value", "length: 4", [], ("length", 4)),
        # A value without unit is in the declared unit
        # Input: 'length: 4' for a parameter in meter
        # Expected Result: no error, the value 4

        ("custom_unit", "count: 3", [], ("count", 3)),
        # Custom units
        # Input: 'count: 3' for a parameter in "pebble"
        # Expected Result: no error, the value 3

        ("default_value", "", [], ("speed", 1.0)),
        # Without configuration the default value applies
        # Input: no configured value for speed
        # Expected Result: no error, the default value 1.0
    ])
    def test_configured_units(self, test_name, configuration, expected_errors, expected_value):
        self.check_configuration(test_name, configuration, expected_errors, expected_value)

    def check_configuration(self, test_name, configuration, expected_errors, expected_value):
        model = self.configure(configuration)
        checker = UnitCalculator(self.logger)
        self.assertEqual(not expected_errors, checker.check_model(model), test_name)
        self.assertEqual(expected_errors, self.errors(), test_name)
        Calculator(model, self.logger).calculate()
        name, value = expected_value
        self.assertAlmostEqual(value, model.groups["g"].parameters[name].value.value, msg=test_name)

    @parameterized.expand([
        ("converted", "length: 4 km", [], ("length", 4000.0)),
        # Regression: units of configured values were not checked; values in other units are converted
        # Input: 'length: 4 km' for a parameter in meter
        # Expected Result: no error, the value 4000.0

        ("composed_unit", "speed: 36 km/h", [], ("speed", 10.0)),
        # A composed unit
        # Input: 'speed: 36 km/h' for a parameter in meter / second
        # Expected Result: no error, the value 10.0

        ("incompatible", "length: 4 s", ["Unit second of the value is not compatible with unit meter of parameter "
                                         "length"], ("length", 4)),
        # A unit of another dimension
        # Input: 'length: 4 s' for a parameter in meter
        # Expected Result: an error, the value is not converted

        ("dimensionless_parameter", "plain: 2 m", ["Unit meter of the value is not compatible with unit 1 of "
                                                   "parameter plain"], ("plain", 2)),
        # Parameters with the empty unit are dimensionless
        # Input: 'plain: 2 m' for a parameter in ""
        # Expected Result: an error
    ])
    @REQUIRES_CFUNITS
    def test_configured_units_with_cfunits(self, test_name, configuration, expected_errors, expected_value):
        self.check_configuration(test_name, configuration, expected_errors, expected_value)


if __name__ == '__main__':
    unittest.main()
