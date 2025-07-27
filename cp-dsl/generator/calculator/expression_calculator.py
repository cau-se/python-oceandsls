#  Copyright (c) 2025  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from common.logger import GeneratorLogger
from model.declaration_model import DeclarationModel, Parameter, SelectorExpression
from model.arithmetic_model import AbstractExpression, ArithmeticExpression, MultiplicationExpression, \
    AbstractTypedValue, StringValue, IntValue, FloatValue, EAdditionOperator, EMultiplicationOperator
from model.type_system import Enumeral

class ExpressionCalculator():
    logger: GeneratorLogger

    def __init__(self, model: DeclarationModel, logger: GeneratorLogger):
        self.model = model
        self.logger = logger
        self.parameter_stack = []

    def calculate(self, parameter:Parameter):
        expression = parameter.default_value
        return self.calculate_expression(expression)

    def calculate_and_overlay(self, parameter:Parameter, entry:SelectorExpression):
        # compute values
        self.logger.error("Calculate and overlay not implemented")
        exit(1)
        # adjust for unit

    def calculate_expression(self, expression:AbstractExpression) -> AbstractTypedValue:
        if isinstance(expression, ArithmeticExpression):
            result = self.calc_arithmetic_expression(expression)
        elif isinstance(expression, MultiplicationExpression):
            result = self.calc_multiplication_expression(expression)
        elif isinstance(expression, (Enumeral, IntValue, FloatValue, StringValue)):
            result = expression
        else:
            self.logger.error(f"Internal error. Cannot handle {expression} of type {type(expression)}")
            exit(2)
        return result

    def calc_arithmetic_expression(self, expression: ArithmeticExpression) -> AbstractTypedValue:
        left = self.calculate_expression(expression.left)
        right = self.calculate_expression(expression.right)
        if expression.op == EAdditionOperator.ADD:
            result = left.value + right.value
        elif expression.op == EAdditionOperator.SUB:
            result = left.value - right.value
        else:
            self.logger.error(f"Illegal operation {expression.op}")
            exit(1)

        result_unit = None
        result_type = None

        if isinstance(result, float):
            return FloatValue(ctx=None, unit=result_unit, type=result_type, value=result)
        elif isinstance(result, int):
            return IntValue(ctx=None, unit=result_unit, type=result_type, value=result)
        else:
            self.logger.error(f"Arithmetic operation on none numerical values {left.value} and {right.value}")
            exit(1)

    def calc_multiplication_expression(self, expression: MultiplicationExpression) -> AbstractTypedValue:
        left = self.calculate_expression(expression.left)
        right = self.calculate_expression(expression.right)
        if expression.op == EMultiplicationOperator.MULT:
            result = left.value * right.value
        elif expression.op == EMultiplicationOperator.DIV:
            result = left.value / right.value
        elif expression.op == EMultiplicationOperator.MOD:
            result = left.value % right.value
        else:
            self.logger.error(f"Illegal operation {expression.op}")
            exit(1)

        result_unit = None
        result_type = None

        if isinstance(result, float):
            return FloatValue(ctx=None, unit=result_unit, type=result_type, value=result)
        elif isinstance(result, int):
            return IntValue(ctx=None, unit=result_unit, type=result_type, value=result)
        else:
            self.logger.error(f"Multiplication operation on none numerical values {left.value} and {right.value}")
            exit(1)