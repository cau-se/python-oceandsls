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

from common.unit_processing import parse_unit, tokenize, resolve, process_tokens
from model.unit_model import UnitKind, UnitPrefix, UnitSpecification, SIUnit, DivisionUnit, ExponentUnit

from test_utils import AbstractTestGeneratorConfigurationVisitor

prefix = { 'q': UnitPrefix.Quecto,
            'r': UnitPrefix.Ronto,
            'y': UnitPrefix.Yocto,
            'z': UnitPrefix.Zepto,
            'a': UnitPrefix.Atto,
            'f': UnitPrefix.Femto,
            'p': UnitPrefix.Pico,
            'n': UnitPrefix.Nano,
            'ü': UnitPrefix.Micro,
            'm': UnitPrefix.Milli,
            'c': UnitPrefix.Centi,
            'd': UnitPrefix.Deci,
            'da': UnitPrefix.Deca,
            'h': UnitPrefix.Hecto,
            'k': UnitPrefix.Kilo,
            'M': UnitPrefix.Mega,
            'G': UnitPrefix.Giga,
            'T': UnitPrefix.Tera,
            'P': UnitPrefix.Peta,
            'E': UnitPrefix.Exa,
            'Z': UnitPrefix.Zetta,
            'Y': UnitPrefix.Yotta,
            'R': UnitPrefix.Ronna,
            'Q': UnitPrefix.Quetta
        }

kind = { 's': UnitKind.Second,
        'm': UnitKind.Meter,
        'g': UnitKind.Gram,
        'A': UnitKind.Ampere,
        'cd': UnitKind.Candela,
        'J': UnitKind.Joule,
        'K': UnitKind.Kelvin,
        'mol': UnitKind.Mole,
        'Pa': UnitKind.Pascal
        }

class TestGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    def test_tokenize_kind(self):
        for e in [ 's', 'g', 'A', 'cd', 'J', 'K', 'mol', 'Pa']:
            spec = tokenize(e)
            self.assertEqual(len(spec), 1, "Wrong number of tokens")
            self.assertEqual(spec[0], kind[e], "Wrong unit kind")

        spec = tokenize('m')
        self.assertEqual(len(spec), 1, "Wrong number of tokens")
        self.assertEqual(spec[0], UnitKind.Meter, "Wrong unit kind")

    def test_tokenize_prefix(self):
        for p in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            spec = tokenize(p)
            self.assertEqual(len(spec), 1, "Wrong number of tokens")
            self.assertEqual(spec[0], prefix[p], "Wrong unit prefix")

    def test_tokenize_prefix_kind(self):
        for p in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            unit_string = f"{p}m"
            spec = tokenize(unit_string)
            self.assertEqual(len(spec), 2, "Wrong number of tokens")
            self.assertEqual(spec[0], prefix[p], "Wrong unit prefix")
            self.assertEqual(spec[1], kind['m'], "Wrong unit kind")

        unit_string = f"mm"
        spec = tokenize(unit_string)
        self.assertEqual(len(spec), 2, "Wrong number of tokens")
        self.assertEqual(spec[0], [prefix['m'], kind['m']], "Wrong unit prefix")
        self.assertEqual(spec[1], kind['m'], "Wrong unit kind")

    def test_tokenize_prefix_kind_exponent(self):
        for p in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            unit_string = f"{p}m^2"
            spec = tokenize(unit_string)
            self.assertEqual(len(spec), 3, "Wrong number of tokens")
            self.assertEqual(spec[0], prefix[p], "Wrong unit prefix")
            self.assertEqual(spec[1], [prefix['m'], kind['m']], "Wrong unit kind")
            self.assertEqual(spec[2], 2, "Wrong exponent")

        unit_string = f"mm^2"
        spec = tokenize(unit_string)
        self.assertEqual(len(spec), 3, "Wrong number of tokens")
        self.assertEqual(spec[0], [prefix['m'], kind['m']], "Wrong unit prefix")
        self.assertEqual(spec[1], [prefix['m'], kind['m']], "Wrong unit kind")
        self.assertEqual(spec[2], 2, "Wrong exponent")

        for p in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            unit_string = f"{p}m^+2"
            spec = tokenize(unit_string)
            self.assertEqual(len(spec), 3, "Wrong number of tokens")
            self.assertEqual(spec[0], prefix[p], "Wrong unit prefix")
            self.assertEqual(spec[1], [prefix['m'], kind['m']], "Wrong unit kind")
            self.assertEqual(spec[2], 2, "Wrong exponent")

        for p in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            unit_string = f"{p}m^-2"
            spec = tokenize(unit_string)
            self.assertEqual(len(spec), 3, "Wrong number of tokens")
            self.assertEqual(spec[0], prefix[p], "Wrong unit prefix")
            self.assertEqual(spec[1], [prefix['m'], kind['m']], "Wrong unit kind")
            self.assertEqual(spec[2], -2, "Wrong exponent")

    def test_tokenize_groups_division(self):
        for p in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            unit_string = f"({p}mkg)/K"
            spec = tokenize(unit_string)
            self.assertEqual(len(spec), 8, "Wrong number of tokens")
            self.assertEqual(spec[0], '(')
            self.assertEqual(spec[1], prefix[p], "Wrong unit prefix")
            self.assertEqual(spec[2], [prefix['m'], kind['m']], "Wrong unit kind")
            self.assertEqual(spec[3], prefix['k'], "Wrong unit prefix, kilo expected")
            self.assertEqual(spec[4], kind['g'])
            self.assertEqual(spec[5], ')')
            self.assertEqual(spec[6], '/')
            self.assertEqual(spec[7], kind['K'])

    def test_resolve_groups_division(self):
        for p in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'm', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            unit_string = f"({p}mkg)/K"
            spec = resolve(tokenize(unit_string))
            self.assertEqual(len(spec), 8, "Wrong number of tokens")
            self.assertEqual(spec[0], '(')
            self.assertEqual(spec[1], prefix[p], "Wrong unit prefix")
            self.assertEqual(spec[2], kind['m'], "Wrong unit kind")
            self.assertEqual(spec[3], prefix['k'], "Wrong unit prefix, kilo expected")
            self.assertEqual(spec[4], kind['g'])
            self.assertEqual(spec[5], ')')
            self.assertEqual(spec[6], '/')
            self.assertEqual(spec[7], kind['K'])

    def test_parse_unit_base(self):
        for e in [ 's', 'm', 'g', 'A', 'cd', 'J', 'K', 'mol', 'Pa']:
            spec = parse_unit(e)
            self.assertIsInstance(spec, UnitSpecification, "Wrong class for UnitSpecification")
            unit = spec.units[0]
            self.assertIsInstance(unit, SIUnit, "Wrong class for SIUnit")
            self.assertEqual(unit.kind, kind[e], "Wrong unit kind")

    def test_parse_unit_prefix(self):
        i = 0
        for p in ['q', 'r', 'y', 'z', 'a', 'f', 'p', 'n', 'ü', 'm', 'c', 'd', 'da', 'h', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y', 'R', 'Q' ]:
            unit_string = f"{p}m"
            spec = parse_unit(unit_string)
            self.assertIsInstance(spec, UnitSpecification, "Wrong class for UnitSpecification")
            unit = spec.units[0]
            self.assertIsInstance(unit, SIUnit, "Wrong class for SIUnit")
            self.assertEqual(unit.kind, UnitKind.Meter, "Wrong unit kind")
            self.assertEqual(unit.prefix, prefix[p] , "Wrong unit prefix")

    def test_tokenize_unit_division(self):
        spec = tokenize("kg/mm")
        self.assertEqual(len(spec), 5)
        self.assertEqual(spec[0], UnitPrefix.Kilo)
        self.assertEqual(spec[1], UnitKind.Gram)
        self.assertEqual(spec[2], "/")
        self.assertEqual(spec[3], [UnitPrefix.Milli, UnitKind.Meter])
        self.assertEqual(spec[4], UnitKind.Meter)

    def test_resolve_unit_division(self):
        spec = resolve(tokenize("kg/mm"))
        self.assertEqual(len(spec), 5)
        self.assertEqual(spec[0], UnitPrefix.Kilo)
        self.assertEqual(spec[1], UnitKind.Gram)
        self.assertEqual(spec[2], "/")
        self.assertEqual(spec[3], UnitPrefix.Milli)
        self.assertEqual(spec[4], UnitKind.Meter)

    def test_process_tokens_unit_division(self):
        spec = process_tokens(resolve(tokenize("kg/mm")))
        self.assertEqual(len(spec), 3)
        self.assertEqual(spec[0], SIUnit(UnitPrefix.Kilo, UnitKind.Gram))
        self.assertEqual(spec[1], "/")
        self.assertEqual(spec[2], SIUnit(UnitPrefix.Milli, UnitKind.Meter))

    def test_parse_unit_division(self):
        spec = parse_unit("kg/mm")
        self.assertIsInstance(spec, UnitSpecification)
        self.assertEqual(len(spec.units), 1)
        unit:DivisionUnit = spec.units[0]
        self.assertIsInstance(unit, DivisionUnit)
        numerator:SIUnit = unit.numerator
        self.assertIsInstance(numerator, SIUnit)
        self.assertEqual(numerator.prefix, UnitPrefix.Kilo)
        self.assertEqual(numerator.kind, UnitKind.Gram)
        denominator:SIUnit = unit.denominator
        self.assertIsInstance(denominator, SIUnit)
        self.assertEqual(denominator.prefix, UnitPrefix.Milli)
        self.assertEqual(denominator.kind, UnitKind.Meter)


    def test_parse_unit_division_exponent(self):
        spec = parse_unit("kg/mm^2")
        self.assertIsInstance(spec, UnitSpecification, "Wrong class for UnitSpecification")
        self.assertEqual(len(spec.units), 1)
        unit:DivisionUnit = spec.units[0]
        self.assertIsInstance(unit, DivisionUnit)
        numerator:SIUnit = unit.numerator
        self.assertIsInstance(numerator, SIUnit)
        self.assertEqual(numerator.prefix, UnitPrefix.Kilo)
        self.assertEqual(numerator.kind, UnitKind.Gram)
        denominator:ExponentUnit = unit.denominator
        e_u:SIUnit = denominator.unit
        e_e:int = denominator.exponent
        self.assertEqual(e_u.prefix, UnitPrefix.Milli)
        self.assertEqual(e_u.kind, UnitKind.Meter)
        self.assertEqual(e_e, 2)

    def test_parse_unit_normalized_exponent(self):
        spec = parse_unit("kgmm^-2")
        self.assertIsInstance(spec, UnitSpecification, "Wrong class for UnitSpecification")
        self.assertEqual(len(spec.units), 2)

        unit_1 = spec.units[0]
        self.assertIsInstance(unit_1, SIUnit)
        self.assertEqual(unit_1.prefix, UnitPrefix.Kilo)
        self.assertEqual(unit_1.kind, UnitKind.Gram)

        unit_2:ExponentUnit = spec.units[1]
        self.assertIsInstance(unit_2, ExponentUnit)
        self.assertIsInstance(unit_2.unit, SIUnit)
        self.assertEqual(unit_2.unit.prefix, UnitPrefix.Milli)
        self.assertEqual(unit_2.unit.kind, UnitKind.Meter)
        self.assertEqual(unit_2.exponent, -2)

if __name__ == '__main__':
    unittest.main()
