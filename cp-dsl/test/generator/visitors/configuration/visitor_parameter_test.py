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

from cpdsl.model.declaration_model import DeclarationModel, ParameterGroup, Parameter, SelectorExpression

from generator.visitors.test_utils import AbstractTestGeneratorConfigurationVisitor, describe_expression

DECLARATION = """
        model eval
            group my_group : "my group" {
                def scalar int : meter , "scalar description" = 5
                def array int[5] : meter , "array description" = [ 2,4,6,8 ]
                def dyn_array int[] : meter , "dyn_array description"
                def dyn2_array int[,] : meter , "dyn2_array description"
            }
        """
ARRAY_DEFAULT = ("array", [("int", 2), ("int", 4), ("int", 6), ("int", 8)])


def describe_entry(entry):
    """A selector expression as ('select', selectors, expression), other entries as their expression."""
    if isinstance(entry, SelectorExpression):
        return ("select", entry.selectors, describe_expression(entry.expression))
    return describe_expression(entry)


class TestParameterGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    def create_declaration_model(self):
        model = self.parse_declaration_code(DECLARATION)
        self.assertEqual("eval", model.name, "Name not set")
        return model

    @parameterized.expand([
        ("scalar_twice", "scalar : 7\nscalar : 8", "scalar", ("int", 5), [("int", 7), ("int", 8)]),
        # Each configuration of a parameter is an entry, the declared default value is kept
        # Input: 'scalar : 7' and 'scalar : 8'
        # Expected Result: the default value 5 and the entries 7 and 8

        ("scalar_expression", "scalar : 2 + 3", "scalar", ("int", 5), [("+", ("int", 2), ("int", 3))]),
        # A configured expression
        # Input: 'scalar : 2 + 3'
        # Expected Result: the entry 2 + 3

        ("array", "array: [ 3,5,7,9,11 ]", "array", ARRAY_DEFAULT,
         [("array", [("int", 3), ("int", 5), ("int", 7), ("int", 9), ("int", 11)])]),
        # A complete array
        # Input: 'array: [ 3,5,7,9,11 ]'
        # Expected Result: the default value [2,4,6,8] and the array entry [3,5,7,9,11]

        ("array_selectors", "array[0]: 3\narray[1,3]: [ 5,7,9 ]\narray[4]: 11", "array", ARRAY_DEFAULT,
         [("select", [[0]], ("int", 3)), ("select", [[1], [3]], ("array", [("int", 5), ("int", 7), ("int", 9)])),
          ("select", [[4]], ("int", 11))]),
        # Parts of an array selected by index
        # Input: 'array[0]: 3', 'array[1,3]: [ 5,7,9 ]' and 'array[4]: 11'
        # Expected Result: three selector entries with their selectors and values

        ("selector_expression", "array[2]: 4 * 2", "array", ARRAY_DEFAULT, [("select", [[2]], ("*", ("int", 4),
                                                                                              ("int", 2)))]),
        # A selected element with an expression
        # Input: 'array[2]: 4 * 2'
        # Expected Result: a selector entry for index 2 with 4 * 2

        ("dynamic_array", "dyn_array: [ 1 ]", "dyn_array", None, [("array", [("int", 1)])]),
        # An array of open size
        # Input: 'dyn_array: [ 1 ]'
        # Expected Result: no default value, the array entry [1]

        ("two_dimensional_selector", "dyn2_array[0,1]: 5", "dyn2_array", None, [("select", [[0], [1]], ("int", 5))]),
        # A selector of a two-dimensional array
        # Input: 'dyn2_array[0,1]: 5'
        # Expected Result: a selector entry for 0, 1 with the value 5
    ])
    def test_visit_parameter(self, test_name, configuration, name, expected_default, expected_entries):
        model: DeclarationModel = self.parse_code(f"""
                configuration test : eval

                group my_group {{
                    {configuration}
                }}
                """, self.create_declaration_model())

        self.assertEqual("eval", model.name, test_name)
        self.assertEqual("test", model.configuration_name, test_name)
        group: ParameterGroup = model.groups['my_group']
        self.assertIsInstance(group, ParameterGroup, test_name)
        parameter: Parameter = group.parameters[name]
        self.assertIsInstance(parameter, Parameter, test_name)
        self.assertEqual(expected_default, describe_expression(parameter.default_value), test_name)
        self.assertEqual(expected_entries, [describe_entry(entry) for entry in parameter.entries], test_name)
        for other in group.parameters.values():
            if other is not parameter:
                self.assertEqual([], other.entries, f"{test_name}: {other.name}")


if __name__ == '__main__':
    unittest.main()
