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

from generator.visitors.test_utils import AbstractTestGeneratorDeclarationVisitor


class TestBaseGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    @parameterized.expand([
        ("model_name", "model eval", "eval", []),
        # The model statement sets the name of the model
        # Input: 'model eval'
        # Expected Result: the model eval without types

        ("name_with_digit", "model m2", "m2", []),
        # Model names may contain digits
        # Input: 'model m2'
        # Expected Result: the model m2

        ("surrounding_whitespace", " model   spaced  ", "spaced", []),
        # Whitespace is ignored
        # Input: ' model   spaced  '
        # Expected Result: the model spaced

        ("model_with_types", "model eval\n types\n enum Color { red, green }", "eval", ["Color"]),
        # The name is set for models with declarations as well
        # Input: the model eval with the enumeration type Color
        # Expected Result: the model eval with the type Color
    ])
    def test_visitDeclarationModel(self, test_name, code, expected_name, expected_types):
        model = self.parse_code(code)
        self.assertEqual(expected_name, model.name, test_name)
        self.assertEqual(expected_types, list(model.types), test_name)


if __name__ == '__main__':
    unittest.main()
