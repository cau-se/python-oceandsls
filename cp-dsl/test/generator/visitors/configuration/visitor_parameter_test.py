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

from model.declaration_model import DeclarationModel, ParameterGroup, Parameter, SelectorExpression
from model.arithmetic_model import IntValue, ArrayExpression

from test_utils import AbstractTestGeneratorConfigurationVisitor

class TestGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    def create_declaration_model(self):
        model = self.parse_declaration_code("""
                model eval
                    group my_group : "my group" {
                        def scalar int : meter , "scalar description" = 5
                        def array int[5] : meter , "array description" = [ 2,4,6,8 ]
                        def dyn_array int[] : meter , "dyn_array description"
                        def dyn2_array int[,] : meter , "dyn2_array description"
                    }
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        return model

    def test_visit_parameter_group(self):
        model:DeclarationModel = self.parse_code("""
                configuration test : eval

                group my_group {
                    scalar : 7
                    scalar : 8
                }
                """, self.create_declaration_model())

        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")

        group:ParameterGroup = model.groups['my_group']
        self.assertIsInstance(group, ParameterGroup, "Missing parameter group 'my_group'")
        parameter:Parameter = group.parameters['scalar']
        self.assertIsInstance(parameter, Parameter, "Missing parameter scalar")
        default_value = parameter.default_value
        self.assertIsInstance(default_value, IntValue, "Wrong value type for declaration")
        self.assertEqual(default_value.value, 5, "Wrong declaration value")
        expression = parameter.entries[0]
        self.assertIsInstance(expression, IntValue, "Wrong value type for configuration (1)")
        self.assertEqual(expression.value, 7, "Wrong configuration value (1)")
        expression = parameter.entries[1]
        self.assertIsInstance(expression, IntValue, "Wrong value type for configuration (2)")
        self.assertEqual(expression.value, 8, "Wrong configuration value (2)")

    def test_visit_parameter_array(self):
        model:DeclarationModel = self.parse_code("""
                configuration test : eval

                group my_group {
                    array: [ 3,5,7,9,11 ]
                }
                """, self.create_declaration_model())

        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")

        my_group:ParameterGroup = model.groups['my_group']

        self.assertIsInstance(my_group, ParameterGroup, "Parameter group 'my_group' is missing")

        array:Parameter = my_group.parameters['array']

        self.assertIsInstance(array, Parameter, "Parameter 'array' is missing")
        self.assertIsInstance(array.default_value, ArrayExpression, "Wrong default value")
        self.assertEqual(len(array.entries), 1, "Wrong number of entries")

        array_value:ArrayExpression = array.entries[0]
        self.assertIsInstance(array_value, ArrayExpression, "Wrong expression type")
        self.assertEqual(len(array_value.elements), 5, "Wrong number of entries")

        self.assertEqual(array_value.elements[0].value, 3, "Wrong 1st value")
        self.assertEqual(array_value.elements[1].value, 5, "Wrong 2nd value")
        self.assertEqual(array_value.elements[2].value, 7, "Wrong 3rd value")
        self.assertEqual(array_value.elements[3].value, 9, "Wrong 4th value")
        self.assertEqual(array_value.elements[4].value, 11, "Wrong 5th value")

    def test_visit_parameter_array_multiple(self):
        model:DeclarationModel = self.parse_code("""
                configuration test : eval

                group my_group {
                    array[0]: 3
                    array[1,3]: [ 5,7,9 ]
                    array[4]: 11
                }
                """, self.create_declaration_model())

        self.assertEqual(model.name, "eval", "Name not set after configuration")
        self.assertEqual(model.configuration_name, "test", "Configuration name not set")

        my_group:ParameterGroup = model.groups['my_group']

        self.assertIsInstance(my_group, ParameterGroup, "Parameter group 'my_group' is missing")

        array:Parameter = my_group.parameters['array']

        self.assertIsInstance(array, Parameter, "Parameter 'array' is missing")
        self.assertIsInstance(array.default_value, ArrayExpression, "Wrong default value")
        self.assertEqual(len(array.entries), 3, "Wrong number of entries")

        array_value:SelectorExpression = array.entries[0]
        self.assertIsInstance(array_value, SelectorExpression, "Wrong expression type (1)")
        value = array_value.expression
        self.assertIsInstance(value, IntValue, "Wrong expression type")
        self.assertEqual(value.value, 3, "Wrong 1st value")

        array_value:ArrayExpression = array.entries[1]
        self.assertIsInstance(array_value, SelectorExpression, "Wrong expression type (2)")
        value:ArrayExpression = array_value.expression
        self.assertIsInstance(value, ArrayExpression, "Wrong expression type")
        self.assertEqual(len(value.elements), 3, "Wrong number of entries")

        self.assertEqual(value.elements[0].value, 5, "Wrong 2nd value")
        self.assertEqual(value.elements[1].value, 7, "Wrong 3rd value")
        self.assertEqual(value.elements[2].value, 9, "Wrong 4th value")

if __name__ == '__main__':
    unittest.main()
