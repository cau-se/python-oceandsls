"""Calculator Module"""

__author__ = "stu222808"

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

import operator as op

# Relative Imports
from model.declaration_model import DeclarationModel, Parameter, ParameterGroup
from common.logger import GeneratorLogger
from .expression_calculator import ExpressionCalculator

class Calculator():
    '''A calculator for configured values of parameters'''

    def __init__(self, model: DeclarationModel, logger:GeneratorLogger):
        self.model = model
        self.logger = logger

    def calculate_parameter(self, parameter:Parameter):
        if parameter.value == None:
            # 1. calculate the default value
            ExpressionCalculator(self.model).calculate(parameter)
            # 2. calculate all entries over the default value
            for entry in parameter.entries:
                ExpressionCalculator(self.model).calculate_and_overlay(parameter, entry)

    def calculate_group(self, group:ParameterGroup):
        for parameter in group.parameters:
            self.calculate_parameter(parameter)

    def calculate(self):
        for group in self.model.groups:
            self.calculate_group(group)
        for feature in self.model.features:
            self.calculate_feature(feature)
