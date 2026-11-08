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

from cpdsl.common.unit_processing import parse_unit, tokenize, resolve, process_tokens
from cpdsl.model.unit_model import UnitKind, UnitPrefix, UnitSpecification, SIUnit, DivisionUnit, ExponentUnit, \
    CustomUnit

MILLI_METER = [UnitPrefix.Milli, UnitKind.Meter]  # 'm' is milli or meter: the tokenizer keeps both readings

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
]

EXPONENTS = [("^2", 2), ("^+2", 2), ("^-2", -2)]


class TestUnitProcessionVisitor(unittest.TestCase):

    @parameterized.expand(KIND_CASES)
    def test_tokenize_kind(self, test_name, symbol, expected_kind):
        self.assertEqual([expected_kind], tokenize(symbol), test_name)

    @parameterized.expand(PREFIX_CASES)
    def test_tokenize_prefix(self, test_name, symbol, expected_prefix):
        self.assertEqual([expected_prefix], tokenize(symbol), test_name)

    @parameterized.expand(PREFIX_CASES)
    def test_tokenize_prefix_kind(self, test_name, symbol, expected_prefix):
        self.assertEqual([expected_prefix, UnitKind.Meter], tokenize(f"{symbol}m"), test_name)

    @parameterized.expand(PREFIX_CASES)
    def test_tokenize_prefix_kind_exponent(self, test_name, symbol, expected_prefix):
        # an exponent with and without sign: '^2', '^+2' and '^-2'
        for exponent, expected_exponent in EXPONENTS:
            with self.subTest(exponent=exponent):
                self.assertEqual([expected_prefix, MILLI_METER, expected_exponent],
                                 tokenize(f"{symbol}m{exponent}"), test_name)

    @parameterized.expand(PREFIX_CASES)
    def test_tokenize_groups_division(self, test_name, symbol, expected_prefix):
        self.assertEqual(["(", expected_prefix, MILLI_METER, UnitPrefix.Kilo, UnitKind.Gram, ")", "/", UnitKind.Kelvin],
                         tokenize(f"({symbol}mkg)/K"), test_name)

    @parameterized.expand(PREFIX_CASES_WITH_MILLI)
    def test_resolve_groups_division(self, test_name, symbol, expected_prefix):
        self.assertEqual(["(", expected_prefix, UnitKind.Meter, UnitPrefix.Kilo, UnitKind.Gram, ")", "/",
                          UnitKind.Kelvin], resolve(tokenize(f"({symbol}mkg)/K")), test_name)

    @parameterized.expand(PREFIX_CASES_WITH_MILLI)
    def test_parse_unit_prefix(self, test_name, symbol, expected_prefix):
        spec = parse_unit(f"{symbol}m")
        self.assertIsInstance(spec, UnitSpecification, test_name)
        self.assertEqual([SIUnit(expected_prefix, UnitKind.Meter)], spec.units, test_name)

    @parameterized.expand(KIND_CASES)
    def test_parse_unit_base(self, test_name, symbol, expected_kind):
        spec = parse_unit(symbol)
        self.assertIsInstance(spec, UnitSpecification, test_name)
        self.assertEqual([SIUnit(None, expected_kind)], spec.units, test_name)

    @parameterized.expand([
        ("millimeter", "mm", [MILLI_METER, UnitKind.Meter]),
        # The first 'm' may be milli or meter, the last one is a meter
        # Input: 'mm'
        # Expected Result: both readings for the first 'm', meter for the second

        ("millimeter_exponent", "mm^2", [MILLI_METER, MILLI_METER, 2]),
        # Before an exponent both 'm' keep both readings
        # Input: 'mm^2'
        # Expected Result: both readings for both 'm', the exponent 2

        ("division", "kg/mm", [UnitPrefix.Kilo, UnitKind.Gram, "/", MILLI_METER, UnitKind.Meter]),
        # A division
        # Input: 'kg/mm'
        # Expected Result: kilo, gram, '/', both readings of 'm', meter

        ("kind_division", "mol/s", [UnitKind.Mole, "/", UnitKind.Second]),
        # A division of unit kinds
        # Input: 'mol/s'
        # Expected Result: mole, '/', second
    ])
    def test_tokenize(self, test_name, unit_string, expected_tokens):
        self.assertEqual(expected_tokens, tokenize(unit_string), test_name)

    @parameterized.expand([
        ("division", "kg/mm", [UnitPrefix.Kilo, UnitKind.Gram, "/", UnitPrefix.Milli, UnitKind.Meter]),
        # Resolving decides the readings of 'm'
        # Input: 'kg/mm'
        # Expected Result: kilo, gram, '/', milli, meter

        ("millimeter", "mm", [UnitPrefix.Milli, UnitKind.Meter]),
        # A prefix followed by a kind
        # Input: 'mm'
        # Expected Result: milli, meter

        ("kilometer_exponent", "km^2", [UnitPrefix.Kilo, UnitKind.Meter, 2]),
        # Before an exponent 'm' after a prefix is a meter
        # Input: 'km^2'
        # Expected Result: kilo, meter, 2

        ("meter", "m", [UnitKind.Meter]),
        # A single 'm' is a meter
        # Input: 'm'
        # Expected Result: meter
    ])
    def test_resolve(self, test_name, unit_string, expected_tokens):
        self.assertEqual(expected_tokens, resolve(tokenize(unit_string)), test_name)

    @parameterized.expand([
        ("division", "kg/mm", [SIUnit(UnitPrefix.Kilo, UnitKind.Gram), "/", SIUnit(UnitPrefix.Milli, UnitKind.Meter)]),
        # Prefixes and kinds are combined to SI units
        # Input: 'kg/mm'
        # Expected Result: kg, '/', mm

        ("millimeter", "mm", [SIUnit(UnitPrefix.Milli, UnitKind.Meter)]),
        # A unit with prefix
        # Input: 'mm'
        # Expected Result: mm

        ("kilometer_exponent", "km^2", [ExponentUnit(SIUnit(UnitPrefix.Kilo, UnitKind.Meter), 2)]),
        # An exponent applies to the unit before it
        # Input: 'km^2'
        # Expected Result: km to the power of 2

        ("pascal", "Pa", [SIUnit(None, UnitKind.Pascal)]),
        # A unit without prefix
        # Input: 'Pa'
        # Expected Result: Pa
    ])
    def test_process_tokens(self, test_name, unit_string, expected_units):
        self.assertEqual(expected_units, process_tokens(resolve(tokenize(unit_string))), test_name)

    @parameterized.expand([
        ("division", "kg/mm", None,
         [DivisionUnit(SIUnit(UnitPrefix.Kilo, UnitKind.Gram), SIUnit(UnitPrefix.Milli, UnitKind.Meter))]),
        # A division of two units
        # Input: 'kg/mm'
        # Expected Result: kg divided by mm

        ("division_exponent", "kg/mm^2", None,
         [DivisionUnit(SIUnit(UnitPrefix.Kilo, UnitKind.Gram),
                       ExponentUnit(SIUnit(UnitPrefix.Milli, UnitKind.Meter), 2))]),
        # The exponent binds stronger than the division
        # Input: 'kg/mm^2'
        # Expected Result: kg divided by mm^2

        ("normalized_exponent", "kgmm^-2", None,
         [SIUnit(UnitPrefix.Kilo, UnitKind.Gram), ExponentUnit(SIUnit(UnitPrefix.Milli, UnitKind.Meter), -2)]),
        # A negative exponent instead of a division
        # Input: 'kgmm^-2'
        # Expected Result: kg and mm^-2

        ("negative_exponent", "s^-1", None, [ExponentUnit(SIUnit(None, UnitKind.Second), -1)]),
        # A unit without prefix and a negative exponent
        # Input: 's^-1'
        # Expected Result: s^-1

        ("user_defined", "pebbles", ["pebbles"], [CustomUnit("pebbles")]),
        # A user-defined unit
        # Input: 'pebbles' with the custom unit pebbles
        # Expected Result: the custom unit pebbles
    ])
    def test_parse_unit(self, test_name, unit_string, custom_units, expected_units):
        spec = parse_unit(unit_string) if custom_units is None else parse_unit(unit_string, custom_units)
        self.assertIsInstance(spec, UnitSpecification, test_name)
        self.assertEqual(expected_units, spec.units, test_name)


if __name__ == '__main__':
    unittest.main()
