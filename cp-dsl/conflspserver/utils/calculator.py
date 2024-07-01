"""Declaration Calculator Module"""

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
from model.symbol_table import DeclarationModel
from model.model import ParameterSymbol, ArraySymbol, ScopedSymbol
from ..gen.python.Configuration.ConfigurationParser import ConfigurationParser
from dcllspserver.utils.calculator import DeclarationCalculator

class ConfigurationCalculator(DeclarationCalculator):
    '''A calculator for configured values of parameters'''

    def __init__(self, symbol_table: DeclarationModel, configuration_list: list, logger):
        super().__init__(symbol_table, logger)
        self.configuration_list = configuration_list

    def calculate(self) -> DeclarationModel:
        '''writes the calculated values into value parameters of every (in order) configured parameter'''
        for elem, index in self.configuration_list:
            if isinstance(elem, ScopedSymbol):
                self._scope = elem
            else:
                self._scope = elem.parent()
            self.calc_variable(elem, index)
        return self._symbol_table

    def calc_variable(self, parameter_symbol: ParameterSymbol, index: int):
        '''calculates a parameter or an array'''
        context = parameter_symbol.configuration[index]
        # check if the context is a Array or a simple Value
        if parameter_symbol.is_array:
            # Array
            self.calc_arithmetic_expression_array(context, context.value, parameter_symbol)
        else:
            # simple Value
            parameter_symbol.value = self.calc_arithmetic_expression(context.value, parameter_symbol)
            parameter_symbol.is_tree = False

    def calc_arithmetic_expression_array(self,
        var_context: ConfigurationParser.ParameterAssignmentContext,
        context: ConfigurationParser.ArithmeticExpressionContext,
        array_symbol: ArraySymbol):
        '''calculates a array configuration'''

        # tupleList representation: list[2:4,5] = [range(2,4), range(5)]
        # wanted: list[2,4:8] = [[(4,1),(5,2),(6,3),(7,4),(8,5)],[(4,1),(5,2),(6,3),(7,4),(8,5)],[(4,1),(5,2),(6,3),(7,4),(8,5)]]
        def convert_to_tuple_list(range_list: list, calc_list, vector: list, depth: int) -> list:
            if len(vector) < depth + 1:
                vector.append(0)
            else:
                vector[depth] = 0
            # range_list is empty so there is no given range
            if len(range_list) == 0:
                for i in range(len(calc_list)):
                    vector[depth] = i
                    if isinstance(calc_list[i], list):
                        convert_to_tuple_list(range_list, calc_list[i], vector.copy(), depth + 1)
                    array_symbol.add(vector, calc_list[i])
                return
            index = 0
            if not isinstance(calc_list, list):
                print("Warning: Array Value is not a list, proceed to convert it in to one", array_symbol.name, "=", calc_list)
                if isinstance(calc_list, str):
                    if calc_list.startswith("'"):
                        calc_list = calc_list.strip("'")
                    else:
                        calc_list = calc_list.strip('"')
                calc_list = [calc_list for _ in range(len(range_list[0]))]
                print("Converted to:", calc_list)
            if len(range_list[0]) < len(calc_list) and isinstance(calc_list, list):
                range_list[0] = range(range_list[0].start, len(calc_list) + range_list[0].start)
            for i in range_list[0]:
                vector[depth] = i
                if not len(calc_list) == 0:
                    if isinstance(calc_list[index], list):
                        convert_to_tuple_list(range_list[1:], calc_list[index], vector.copy(), depth + 1)
                    else:
                        array_symbol.add(vector, calc_list[index])
                    index += 1
                else:
                    print("WARNING: didn't give enough values to ranged nd-array", array_symbol.name)
            return

        calc_list = self.calc_arithmetic_expression(context, array_symbol)

        range_list = []
        for i in var_context.selectors:
            if i.rangeSelector():
                j: ConfigurationParser.RangeSelectorContext = i.rangeSelector()
                range_list.append(range(int(j.lowerBound.text), int(j.upperBound.text) + 1))
            else:
                j: ConfigurationParser.ElementSelectorContext = i.elementSelector()
                element = int(j.element.text)
                range_list.append(range(element, element + 1))
        vector = []
        convert_to_tuple_list(range_list, calc_list, vector, 0)
