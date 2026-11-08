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

from cpdsl.model.unit_model import UnitSpecification, UnitKind, UnitPrefix, SIUnit, ExponentUnit

from generator.visitors.test_utils import AbstractTestGeneratorConfigurationVisitor, describe_expression

DECLARATION = """
        model eval
            group my_group : "description" {
                def param int : meter / kilo gram
            }
        """


class TestUnitGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    @parameterized.expand([
        ("division", "4 m/kg", ("int", 4), UnitSpecification),
        # A configured value with a unit
        # Input: 'param: 4 m/kg' for the parameter declared with meter / kilo gram
        # Expected Result: the value 4 with a unit specification

        ("float_with_unit", "2.5 m/kg", ("float", 2.5), UnitSpecification),
        # A float value with a unit
        # Input: 'param: 2.5 m/kg'
        # Expected Result: the value 2.5 with a unit specification

        ("without_unit", "4", ("int", 4), None),
        # A configured value without unit
        # Input: 'param: 4'
        # Expected Result: the value 4 without unit

        ("prefixed_unit", "4 kg", ("int", 4), UnitSpecification(units=[SIUnit(UnitPrefix.Kilo, UnitKind.Gram)])),
        # A unit with prefix
        # Input: 'param: 4 kg'
        # Expected Result: the value 4 in kg

        ("exponent", "3 s^-1", ("int", 3),
         UnitSpecification(units=[ExponentUnit(SIUnit(None, UnitKind.Second), -1)])),
        # A unit with exponent
        # Input: 'param: 3 s^-1'
        # Expected Result: the value 3 in s^-1
    ])
    def test_visit_unitSpecification(self, test_name, value, expected_value, expected_unit):
        model = self.parse_declaration_code(DECLARATION)
        self.assertEqual("eval", model.name, test_name)

        model = self.parse_code(f"""
                configuration test : eval

                group my_group {{
                    param: {value}
                }}

                """, model)

        entries = model.groups["my_group"].parameters["param"].entries
        self.assertEqual([expected_value], [describe_expression(entry) for entry in entries], test_name)
        if isinstance(expected_unit, type):
            self.assertIsInstance(entries[0].unit, expected_unit, test_name)
        else:
            self.assertEqual(expected_unit, entries[0].unit, test_name)


if __name__ == '__main__':
    unittest.main()
