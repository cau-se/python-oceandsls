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

from parameterized import parameterized

from cpdsl.generator.calculator.expression_calculator import ExpressionCalculator

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.configuration import CompileFlags

from cpdsl.model.type_system import base_types, Enumeral
from cpdsl.model.declaration_model import DeclarationModel, ParameterGroup, Parameter

from cpdsl.model.arithmetic_model import IntValue, FloatValue, StringValue, BooleanValue, ArrayExpression, \
    ArithmeticExpression, MultiplicationExpression, EMultiplicationOperator, EAdditionOperator

logger = GeneratorLogger(CompileFlags.STRICT)


def integer(value):
    return IntValue(None, None, base_types["int"], value)


def real(value):
    return FloatValue(None, None, base_types["float"], value)


def string(value):
    return StringValue(None, None, base_types["string"], value)


def add(left, right=None, op=EAdditionOperator.ADD):
    return ArithmeticExpression(None, None, left=left, right=right, op=op)


def sub(left, right):
    return add(left, right, EAdditionOperator.SUB)


def mul(left, right=None, op=EMultiplicationOperator.MULT):
    return MultiplicationExpression(None, None, left=left, right=right, op=op)


class Test(unittest.TestCase):

    @parameterized.expand([
        ("float_value", add(real(5.0)), FloatValue, 5.0),
        # The default value of a parameter is calculated
        # Input: parameter p1 with the default value 5.0 (an addition without right side)
        # Expected Result: the float 5.0

        ("int_value", add(integer(7)), IntValue, 7),
        # An integer default value
        # Input: parameter p1 with the default value 7
        # Expected Result: the integer 7

        ("expression", add(integer(2), mul(integer(3), integer(4))), IntValue, 14),
        # A default value expression
        # Input: parameter p1 with the default value 2 + 3 * 4
        # Expected Result: the integer 14
    ])
    def test_calculate(self, test_name, default_value, expected_type, expected_value):
        model = DeclarationModel()
        t1 = ParameterGroup(name="t1", description="test one", parent=model)
        p1 = Parameter(name="p1", description="parameter one", type=None, unit=None, parent=t1)
        p1.default_value = default_value
        t1.parameters[p1.name] = p1
        model.groups[t1.name] = t1

        result = ExpressionCalculator(model=model, logger=logger).calculate(parameter=p1)

        self.assertIsInstance(result, expected_type, test_name)
        self.assertEqual(expected_value, result.value, test_name)

    @parameterized.expand([
        ("int_value", integer(2), IntValue, 2),
        # Values are returned as they are
        # Input: the integer 2
        # Expected Result: the integer 2

        ("float_value", real(0.5), FloatValue, 0.5),
        # A float value
        # Input: the float 0.5
        # Expected Result: the float 0.5

        ("string_value", string("text"), StringValue, "text"),
        # A string value
        # Input: the string 'text'
        # Expected Result: the string 'text'

        ("boolean_value", BooleanValue(None, None, base_types["boolean"], True), BooleanValue, True),
        # A boolean value
        # Input: True
        # Expected Result: True

        ("enumeral", Enumeral(name="red", value=1), Enumeral, 1),
        # Enumerals are values as well
        # Input: the enumeral red with the value 1
        # Expected Result: the enumeral red

        ("addition_one_side", add(integer(2)), IntValue, 2),
        # An addition without right side is its left value
        # Input: 2 as arithmetic expression without operator
        # Expected Result: the integer 2

        ("addition", add(integer(2), integer(3)), IntValue, 5),
        # Addition of two values
        # Input: 2 + 3
        # Expected Result: the integer 5

        ("subtraction", sub(integer(3), integer(2)), IntValue, 1),
        # Subtraction of two values keeps the integer type
        # Input: 3 - 2
        # Expected Result: the integer 1

        ("nested_addition", add(integer(2), mul(integer(3), real(0.5))), FloatValue, 3.5),
        # A nested product turns the sum into a float
        # Input: 2 + 3 * 0.5
        # Expected Result: the float 3.5

        ("multiplication_one_side", mul(real(1.5)), FloatValue, 1.5),
        # A multiplication without right side is its left value
        # Input: 1.5 as multiplication expression without operator
        # Expected Result: the float 1.5

        ("multiplication", mul(integer(3), integer(2)), IntValue, 6),
        # Multiplication of two values
        # Input: 3 * 2
        # Expected Result: the integer 6

        ("division", mul(integer(3), integer(2), EMultiplicationOperator.DIV), FloatValue, 1.5),
        # Division always gives a float
        # Input: 3 / 2
        # Expected Result: the float 1.5

        ("modulo", mul(integer(3), integer(2), EMultiplicationOperator.MOD), IntValue, 1),
        # The remainder of a division
        # Input: 3 % 2
        # Expected Result: the integer 1

        ("parenthesis", mul(add(integer(2), integer(3)), integer(2)), IntValue, 10),
        # A parenthesized sum as factor
        # Input: (2 + 3) * 2
        # Expected Result: the integer 10

        ("parenthesis_on_both_sides", sub(mul(integer(4), integer(2)), add(integer(1), integer(2))), IntValue, 5),
        # Nested expressions on both sides
        # Input: (4 * 2) - (1 + 2)
        # Expected Result: the integer 5
    ])
    def test_calculate_expression(self, test_name, expression, expected_type, expected_value):
        calculator = ExpressionCalculator(model=DeclarationModel(), logger=logger)

        result = calculator.calculate_expression(expression)

        self.assertIsInstance(result, expected_type, test_name)
        self.assertEqual(expected_value, result.value, test_name)

    @parameterized.expand([
        ("unsupported_expression", ArrayExpression(None, None, elements=[integer(1)]), 2),
        # Expressions other than arithmetic expressions and values are an internal error
        # Input: an array expression
        # Expected Result: exit code 2

        ("string_addition", add(string("a"), string("b")), 1),
        # Arithmetic needs numbers
        # Input: 'a' + 'b'
        # Expected Result: exit code 1

        ("string_multiplication", mul(string("a"), integer(2)), 1),
        # Multiplication needs numbers
        # Input: 'a' * 2
        # Expected Result: exit code 1

        ("illegal_addition_operator", add(integer(1), integer(2), op=None), 1),
        # An addition needs + or -
        # Input: 1 and 2 without operator
        # Expected Result: exit code 1

        ("illegal_multiplication_operator", mul(integer(1), integer(2), op=None), 1),
        # A multiplication needs *, / or %
        # Input: 1 and 2 without operator
        # Expected Result: exit code 1
    ])
    def test_calculate_expression_errors(self, test_name, expression, expected_code):
        error_logger = GeneratorLogger(CompileFlags.STRICT)
        calculator = ExpressionCalculator(model=DeclarationModel(), logger=error_logger)

        with self.assertLogs(level="ERROR"):
            with self.assertRaises(SystemExit) as context:
                calculator.calculate_expression(expression)

        self.assertEqual(expected_code, context.exception.code, test_name)
        self.assertEqual(1, error_logger.error_count, test_name)


if __name__ == '__main__':
    unittest.main()
