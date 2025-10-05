#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
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

from model.declaration_model import DeclarationModel, ParameterGroup, Parameter, Feature, FeatureGroup
from model.arithmetic_model import AbstractExpression, ArithmeticExpression, MultiplicationExpression, IntValue, FloatValue, StringValue
from model.unit_model import UnitSpecification

from cfunits import Unit

from common.logger import GeneratorLogger

class UnitCalculator:

    def __init__(self, model: DeclarationModel, logger:GeneratorLogger):
        self.model = model
        self.logger = logger

    def resolve_unit(self, expression:ArithmeticExpression) -> UnitSpecification:
        left_unit = self.resolve_unit(expression.left)
        right_unit = self.resolve_unit(expression.right)
        return self.conform_units(left_unit, right_unit)

    def resolve_unit(self, expression:AbstractExpression) -> UnitSpecification:
        if isinstance(expression, ArithmeticExpression):
            arithmetic_expression:ArithmeticExpression = expression
            return self.resolve_unit(arithmetic_expression)
        else:
            return None

    def combine_units(self, left_unit: UnitSpecification, right_unit: UnitSpecification) -> UnitSpecification:
        left_unit.units