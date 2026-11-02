#  Copyright (c) 2025.  OceanDSL (https://oceandsl.uni-kiel.de)
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

from cpdsl.generator.calculator.expression_calculator import ExpressionCalculator

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.configuration import CompileFlags

from cpdsl.model.type_system import Enumeral, BaseType, base_types
from cpdsl.model.declaration_model import DeclarationModel, ParameterGroup, Parameter

from cpdsl.model.arithmetic_model import IntValue, StringValue, FloatValue, ArithmeticExpression, MultiplicationExpression, \
    EMultiplicationOperator, EAdditionOperator, ArrayExpression

logger=GeneratorLogger(CompileFlags.STRICT)

class Test(unittest.TestCase):

    def test_calculate(self):
        model = DeclarationModel()

        t1 = ParameterGroup(name="t1", description="test one", parent=model)

        p1 = Parameter(name="p1", description="parameter one", type=None, unit=None, parent=t1)
        left = FloatValue(None, None, base_types["float"], 5.0)
        expression = ArithmeticExpression(None, None, left=left, right=None, op=EAdditionOperator.ADD)
        p1.default_value = expression
        t1.parameters[p1.name]=p1

        model.groups[t1.name] = t1

        calculator = ExpressionCalculator(model=model, logger=logger)
        result = calculator.calculate(parameter=p1)
        self.assertEqual(result.value, 5.0)

    def test_calculate_operations(self):
        model = DeclarationModel()
        calculator = ExpressionCalculator(model=model, logger=logger)
        two = IntValue(None, None, base_types["int"], 2)
        three = IntValue(None, None, base_types["int"], 3)
        half = FloatValue(None, None, base_types["float"], 0.5)
        # 2 + 3 * 0.5 = 3.5 (float), 3 - 2 = 1 (int), 3 % 2 = 1
        product = MultiplicationExpression(None, None, left=three, right=half, op=EMultiplicationOperator.MULT)
        self.assertEqual(calculator.calculate_expression(
            ArithmeticExpression(None, None, left=two, right=product, op=EAdditionOperator.ADD)).value, 3.5)
        difference = calculator.calculate_expression(
            ArithmeticExpression(None, None, left=three, right=two, op=EAdditionOperator.SUB))
        self.assertIsInstance(difference, IntValue)
        self.assertEqual(difference.value, 1)
        self.assertEqual(calculator.calculate_expression(
            MultiplicationExpression(None, None, left=three, right=two, op=EMultiplicationOperator.MOD)).value, 1)

    # one side expression with a value
    def test_calc_arithmetic_expression_value(self):
        pass

    # both side expression with values
    def test_calc_arithmetic_expression_expression(self):
        pass

    # both side expression with nested values
    def test_calc_arithmetic_expression_complex(self):
        pass

    # one side expression with value
    def test_calc_multiplication_expression_value(self):
        pass

    # two side expression with value
    def test_calc_multiplication_expression_expression(self):
        pass

    # two side with parenthesis
    def test_calc_arithmetic_expression_parenthesis(self):
        pass

    # parenthesis
    def test_calc_parenthesis(self):
        pass

    # values
    def test_calc_value(self):
        pass

    # exponent
    def test_calc_exponent(self):
        pass

    # function
    def test_calc_function(self):
        pass

    # enumeration
    def test_calc_enumeration(self):
        pass

if __name__ == '__main__':
    unittest.main()
