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
from model.arithmetic_model import ArithmeticExpression, MultiplicationExpression, StringValue, IntValue, FloatValue
from model.type_system import Enumeral

class ExpressionCalculator():
    logger: GeneratorLogger

    def __init__(self, model: DeclarationModel, logger: GeneratorLogger):
        self.model = model
        self.logger = logger
        self.parameter_stack = []

    def calculate(self, parameter:Parameter):
        expression = parameter.default_value
        if isinstance(expression, ArithmeticExpression):
            result = self.calc_arithmetic_expression(expression)
        elif isinstance(expression, MultiplicationExpression):
            result = self.calc_multiplication_expression(expression)
        elif isinstance(expression, (Enumeral, IntValue, FloatValue, StringValue)):
            result = expression
        else:
            self.logger.error(f"Internal error. Cannot handle {expression} of type {type(expression)}")
            exit(2)

    def calculate_and_overlay(self, parameter:Parameter, entry:SelectorExpression):
        # compute values
        self.logger.error("Calculate and overlay not implemented")
        exit(1)
        # adjust for unit
