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

from generator.calculator.expression_calculator import ExpressionCalculator

from common.logger import GeneratorLogger
from common.configuration import CompileFlags

from model.type_system import Enumeral, BaseType, base_types
from model.declaration_model import DeclarationModel, ParameterGroup, Parameter

from model.arithmetic_model import IntValue, StringValue, FloatValue, ArithmeticExpression, MultiplicationExpression, \
    EMultiplicationOperator, EAdditionOperator, ArrayExpression

logger=GeneratorLogger(CompileFlags.STRICT)

class Test(unittest.TestCase):

    def test_calculate(self):
        model = DeclarationModel()

        t1 = ParameterGroup(name="t1", description="test one", parent=model)

        p1 = Parameter(name="p1"m description="parameter one", type=None, unit=None, parent=t1)
        left = FloatValue(None, None, base_types["float"], 5.0)
        expression = ArithmeticExpression(None, None, left=left, right=None, op=EAdditionOperator.ADD)
        p1.default_value = expression
        t1.parameters[p1.name]=p1

        model.groups[t1.name] = t1

        calculator = ExpressionCalculator(model=model, logger=logger)
        calculator.calculate(parameter=p1)

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
