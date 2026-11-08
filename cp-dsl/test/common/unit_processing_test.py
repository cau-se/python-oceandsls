#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributedBaseType on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

__author__ = "reiner"

import unittest

from parameterized import parameterized

from cpdsl.common.unit_processing import parse_unit, tokenize, split_symbols
from cpdsl.model.unit_model import UnitKind, UnitPrefix, UnitSpecification, SIUnit, DivisionUnit, ExponentUnit, \
    CustomUnit

# SI prefixes except milli, whose symbol is the one of meter and is tested separately
PREFIX_CASES = [
    ("quecto", "q", UnitPrefix.Quecto),
    # The SI prefix Quecto
    # Input: 'q'
    # Expected Result: UnitPrefix.Quecto

    ("ronto", "r", UnitPrefix.Ronto),
    # The SI prefix Ronto
    # Input: 'r'
    # Expected Result: UnitPrefix.Ronto

    ("yocto", "y", UnitPrefix.Yocto),
    # The SI prefix Yocto
    # Input: 'y'
    # Expected Result: UnitPrefix.Yocto

    ("zepto", "z", UnitPrefix.Zepto),
    # The SI prefix Zepto
    # Input: 'z'
    # Expected Result: UnitPrefix.Zepto

    ("atto", "a", UnitPrefix.Atto),
    # The SI prefix Atto
    # Input: 'a'
    # Expected Result: UnitPrefix.Atto

    ("femto", "f", UnitPrefix.Femto),
    # The SI prefix Femto
    # Input: 'f'
    # Expected Result: UnitPrefix.Femto

    ("pico", "p", UnitPrefix.Pico),
    # The SI prefix Pico
    # Input: 'p'
    # Expected Result: UnitPrefix.Pico

    ("nano", "n", UnitPrefix.Nano),
    # The SI prefix Nano
    # Input: 'n'
    # Expected Result: UnitPrefix.Nano

    ("micro", "ü", UnitPrefix.Micro),
    # The SI prefix Micro
    # Input: 'ü'
    # Expected Result: UnitPrefix.Micro

    ("centi", "c", UnitPrefix.Centi),
    # The SI prefix Centi
    # Input: 'c'
    # Expected Result: UnitPrefix.Centi

    ("deci", "d", UnitPrefix.Deci),
    # The SI prefix Deci
    # Input: 'd'
    # Expected Result: UnitPrefix.Deci

    ("deca", "da", UnitPrefix.Deca),
    # The SI prefix Deca
    # Input: 'da'
    # Expected Result: UnitPrefix.Deca

    ("hecto", "h", UnitPrefix.Hecto),
    # The SI prefix Hecto
    # Input: 'h'
    # Expected Result: UnitPrefix.Hecto

    ("kilo", "k", UnitPrefix.Kilo),
    # The SI prefix Kilo
    # Input: 'k'
    # Expected Result: UnitPrefix.Kilo

    ("mega", "M", UnitPrefix.Mega),
    # The SI prefix Mega
    # Input: 'M'
    # Expected Result: UnitPrefix.Mega

    ("giga", "G", UnitPrefix.Giga),
    # The SI prefix Giga
    # Input: 'G'
    # Expected Result: UnitPrefix.Giga

    ("tera", "T", UnitPrefix.Tera),
    # The SI prefix Tera
    # Input: 'T'
    # Expected Result: UnitPrefix.Tera

    ("peta", "P", UnitPrefix.Peta),
    # The SI prefix Peta
    # Input: 'P'
    # Expected Result: UnitPrefix.Peta

    ("exa", "E", UnitPrefix.Exa),
    # The SI prefix Exa
    # Input: 'E'
    # Expected Result: UnitPrefix.Exa

    ("zetta", "Z", UnitPrefix.Zetta),
    # The SI prefix Zetta
    # Input: 'Z'
    # Expected Result: UnitPrefix.Zetta

    ("yotta", "Y", UnitPrefix.Yotta),
    # The SI prefix Yotta
    # Input: 'Y'
    # Expected Result: UnitPrefix.Yotta

    ("ronna", "R", UnitPrefix.Ronna),
    # The SI prefix Ronna
    # Input: 'R'
    # Expected Result: UnitPrefix.Ronna

    ("quetta", "Q", UnitPrefix.Quetta),
    # The SI prefix Quetta
    # Input: 'Q'
    # Expected Result: UnitPrefix.Quetta
]

MILLI_CASE = ("milli", "m", UnitPrefix.Milli)
# The SI prefix Milli
# Input: 'm'
# Expected Result: UnitPrefix.Milli

PREFIX_CASES_WITH_MILLI = PREFIX_CASES + [MILLI_CASE]

KIND_CASES = [
    ("second", "s", UnitKind.Second),
    # The unit kind Second
    # Input: 's'
    # Expected Result: UnitKind.Second

    ("meter", "m", UnitKind.Meter),
    # The unit kind Meter
    # Input: 'm'
    # Expected Result: UnitKind.Meter

    ("gram", "g", UnitKind.Gram),
    # The unit kind Gram
    # Input: 'g'
    # Expected Result: UnitKind.Gram

    ("ampere", "A", UnitKind.Ampere),
    # The unit kind Ampere
    # Input: 'A'
    # Expected Result: UnitKind.Ampere

    ("candela", "cd", UnitKind.Candela),
    # The unit kind Candela
    # Input: 'cd'
    # Expected Result: UnitKind.Candela

    ("joule", "J", UnitKind.Joule),
    # The unit kind Joule
    # Input: 'J'
    # Expected Result: UnitKind.Joule

    ("kelvin", "K", UnitKind.Kelvin),
    # The unit kind Kelvin
    # Input: 'K'
    # Expected Result: UnitKind.Kelvin

    ("mole", "mol", UnitKind.Mole),
    # The unit kind Mole
    # Input: 'mol'
    # Expected Result: UnitKind.Mole

    ("pascal", "Pa", UnitKind.Pascal),
    # The unit kind Pascal
    # Input: 'Pa'
    # Expected Result: UnitKind.Pascal

    ("hour", "h", UnitKind.Hour),
    # Regression: hours were missing, so km/h could not be parsed (h is the hecto prefix otherwise)
    # Input: 'h'
    # Expected Result: UnitKind.Hour

    ("day", "d", UnitKind.Day),
    # Days (d is the deci prefix otherwise)
    # Input: 'd'
    # Expected Result: UnitKind.Day
]

EXPONENTS = [("^2", 2), ("^+2", 2), ("^-2", -2)]


KILOGRAM = SIUnit(UnitPrefix.Kilo, UnitKind.Gram)
MILLIMETER = SIUnit(UnitPrefix.Milli, UnitKind.Meter)
METER = SIUnit(None, UnitKind.Meter)
SECOND = SIUnit(None, UnitKind.Second)


class TestUnitProcessionVisitor(unittest.TestCase):

    @parameterized.expand(KIND_CASES)
    def test_parse_unit_base(self, test_name, symbol, expected_kind):
        spec = parse_unit(symbol)
        self.assertIsInstance(spec, UnitSpecification, test_name)
        self.assertEqual([SIUnit(None, expected_kind)], spec.units, test_name)

    @parameterized.expand(PREFIX_CASES_WITH_MILLI)
    def test_parse_unit_prefix(self, test_name, symbol, expected_prefix):
        spec = parse_unit(f"{symbol}m")
        self.assertIsInstance(spec, UnitSpecification, test_name)
        self.assertEqual([SIUnit(expected_prefix, UnitKind.Meter)], spec.units, test_name)

    @parameterized.expand(PREFIX_CASES_WITH_MILLI)
    def test_parse_unit_prefix_exponent(self, test_name, symbol, expected_prefix):
        # an exponent with and without sign: '^2', '^+2' and '^-2'
        for exponent, expected_exponent in EXPONENTS:
            with self.subTest(exponent=exponent):
                self.assertEqual([ExponentUnit(SIUnit(expected_prefix, UnitKind.Meter), expected_exponent)],
                                 parse_unit(f"{symbol}m{exponent}").units, test_name)

    @parameterized.expand(PREFIX_CASES_WITH_MILLI)
    def test_parse_unit_groups_division(self, test_name, symbol, expected_prefix):
        # Regression: a parenthesized group was processed twice and became an empty unit specification
        self.assertEqual([DivisionUnit(UnitSpecification([SIUnit(expected_prefix, UnitKind.Meter), KILOGRAM]),
                                       SIUnit(None, UnitKind.Kelvin))],
                         parse_unit(f"({symbol}mkg)/K").units, test_name)

    @parameterized.expand([
        ("division_exponent", "kg/mm^2", [("symbol", "kg"), ("operator", "/"), ("symbol", "mm"), ("exponent", 2)]),
        # Symbols, operators and exponents
        # Input: 'kg/mm^2'
        # Expected Result: kg, /, mm, ^2

        ("operator_after_exponent", "m^2/s", [("symbol", "m"), ("exponent", 2), ("operator", "/"), ("symbol", "s")]),
        # Regression: the character after an exponent was skipped
        # Input: 'm^2/s'
        # Expected Result: m, ^2, /, s

        ("symbol_after_exponent", "s^-1K", [("symbol", "s"), ("exponent", -1), ("symbol", "K")]),
        # Regression: the symbol after a negative exponent was skipped
        # Input: 's^-1K'
        # Expected Result: s, ^-1, K

        ("signed_exponent_and_space", "(m s^+2)", [("operator", "("), ("symbol", "m"), ("symbol", "s"),
                                                   ("exponent", 2), ("operator", ")")]),
        # Whitespace separates symbols, a plus sign is allowed
        # Input: '(m s^+2)'
        # Expected Result: (, m, s, ^2, )
    ])
    def test_tokenize(self, test_name, unit_string, expected_tokens):
        self.assertEqual(expected_tokens, tokenize(unit_string), test_name)

    @parameterized.expand([
        ("prefixed_units", "kgmm", [KILOGRAM, MILLIMETER]),
        # A run of symbols is split into prefixed units
        # Input: 'kgmm'
        # Expected Result: kg and mm

        ("milli_mole", "mmol", [SIUnit(UnitPrefix.Milli, UnitKind.Mole)]),
        # A prefix in front of a multi-letter unit
        # Input: 'mmol'
        # Expected Result: millimole

        ("millisecond", "ms", [SIUnit(UnitPrefix.Milli, UnitKind.Second)]),
        # 'm' followed by a unit kind is milli
        # Input: 'ms'
        # Expected Result: millisecond

        ("candela", "cd", [SIUnit(None, UnitKind.Candela)]),
        # Multi-letter units take precedence over a prefix and a unit
        # Input: 'cd'
        # Expected Result: candela, not centi day

        ("hectopascal", "hPa", [SIUnit(UnitPrefix.Hecto, UnitKind.Pascal)]),
        # A prefix in front of Pa
        # Input: 'hPa'
        # Expected Result: hectopascal

        ("unknown", "xyz", None),
        # Letters that are no units
        # Input: 'xyz'
        # Expected Result: None
    ])
    def test_split_symbols(self, test_name, symbols, expected_units):
        self.assertEqual(expected_units, split_symbols(symbols), test_name)

    @parameterized.expand([
        ("division", "kg/mm", None, [DivisionUnit(KILOGRAM, MILLIMETER)]),
        # A division of two units
        # Input: 'kg/mm'
        # Expected Result: kg divided by mm

        ("division_exponent", "kg/mm^2", None, [DivisionUnit(KILOGRAM, ExponentUnit(MILLIMETER, 2))]),
        # The exponent binds stronger than the division
        # Input: 'kg/mm^2'
        # Expected Result: kg divided by mm^2

        ("normalized_exponent", "kgmm^-2", None, [KILOGRAM, ExponentUnit(MILLIMETER, -2)]),
        # A negative exponent instead of a division
        # Input: 'kgmm^-2'
        # Expected Result: kg and mm^-2

        ("negative_exponent", "s^-1", None, [ExponentUnit(SECOND, -1)]),
        # A unit without prefix and a negative exponent
        # Input: 's^-1'
        # Expected Result: s^-1

        ("user_defined", "pebbles", ["pebbles"], [CustomUnit("pebbles")]),
        # A user-defined unit
        # Input: 'pebbles' with the custom unit pebbles
        # Expected Result: the custom unit pebbles

        ("meter_numerator", "m/kg", None, [DivisionUnit(METER, KILOGRAM)]),
        # Regression: 'm' in front of '/' was read as milli (also in configurations)
        # Input: 'm/kg'
        # Expected Result: meter divided by kg

        ("prefixed_numerator", "km/s", None, [DivisionUnit(SIUnit(UnitPrefix.Kilo, UnitKind.Meter), SECOND)]),
        # Regression: km/s became kilo, milli, '/' and a raw second
        # Input: 'km/s'
        # Expected Result: km divided by s

        ("multi_letter_numerator", "mol/s", None, [DivisionUnit(SIUnit(None, UnitKind.Mole), SECOND)]),
        # Regression: the '/' itself was wrapped as SIUnit(None, '/')
        # Input: 'mol/s'
        # Expected Result: mol divided by s

        ("exponent_before_division", "m^2/s", None, [DivisionUnit(ExponentUnit(METER, 2), SECOND)]),
        # Regression: the '/' after an exponent was lost
        # Input: 'm^2/s'
        # Expected Result: m^2 divided by s

        ("hour", "km/h", None, [DivisionUnit(SIUnit(UnitPrefix.Kilo, UnitKind.Meter), SIUnit(None, UnitKind.Hour))]),
        # Regression: hours were not supported (paper example 'speed : 2 km/h')
        # Input: 'km/h'
        # Expected Result: km divided by h

        ("product_with_space", "mmol m^-3", None,
         [SIUnit(UnitPrefix.Milli, UnitKind.Mole), ExponentUnit(METER, -3)]),
        # Whitespace separates the factors of a product
        # Input: 'mmol m^-3'
        # Expected Result: mmol and m^-3

        ("explicit_product", "kg*m/s^2", None, [DivisionUnit(UnitSpecification([KILOGRAM, METER]),
                                                             ExponentUnit(SECOND, 2))]),
        # '*' separates factors; the numerator is the product in front of '/'
        # Input: 'kg*m/s^2'
        # Expected Result: kg m divided by s^2

        ("chained_division", "kg/m/s", None, [DivisionUnit(DivisionUnit(KILOGRAM, METER), SECOND)]),
        # Divisions are left associative
        # Input: 'kg/m/s'
        # Expected Result: (kg / m) / s

        ("group_exponent", "(m/s)^2", None, [ExponentUnit(DivisionUnit(METER, SECOND), 2)]),
        # An exponent applies to a parenthesized group
        # Input: '(m/s)^2'
        # Expected Result: (m / s)^2

        ("user_defined_in_division", "pebbles/s", ["pebbles"], [DivisionUnit(CustomUnit("pebbles"), SECOND)]),
        # Regression: user-defined units were only recognized as the whole unit
        # Input: 'pebbles/s' with the custom unit pebbles
        # Expected Result: pebbles divided by s
    ])
    def test_parse_unit(self, test_name, unit_string, custom_units, expected_units):
        spec = parse_unit(unit_string) if custom_units is None else parse_unit(unit_string, custom_units)
        self.assertIsInstance(spec, UnitSpecification, test_name)
        self.assertEqual(expected_units, spec.units, test_name)

    @parameterized.expand([
        ("unknown_symbol", "xyz", "Unit symbol xyz in xyz not supported", [CustomUnit("xyz")]),
        # Unknown symbols are reported and kept as custom unit
        # Input: 'xyz'
        # Expected Result: an error, the custom unit xyz

        ("missing_exponent", "m^", "Missing exponent after ^ in m^", [METER]),
        # An exponent needs digits
        # Input: 'm^'
        # Expected Result: an error, meter

        ("missing_parenthesis", "(m", "Missing ) in unit (m", [METER]),
        # An open parenthesis needs to be closed
        # Input: '(m'
        # Expected Result: an error, meter

        ("unexpected_parenthesis", "m)", "Unexpected ) in unit m)", [METER]),
        # A closing parenthesis without opening one
        # Input: 'm)'
        # Expected Result: an error, meter
    ])
    def test_parse_unit_errors(self, test_name, unit_string, expected_message, expected_units):
        with self.assertLogs("cpdsl.common.unit_processing", level="ERROR") as logs:
            spec = parse_unit(unit_string)
        self.assertEqual([expected_message], [record.getMessage() for record in logs.records], test_name)
        self.assertEqual(expected_units, spec.units, test_name)


if __name__ == '__main__':
    unittest.main()
