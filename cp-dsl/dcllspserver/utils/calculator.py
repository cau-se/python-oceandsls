"""Declaration Calculator Module"""

__author__ = "stu222808, reiner"

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
from model.model import ParameterSymbol, ArraySymbol, ScopedSymbol, EnumSymbol
from ..gen.python.Declaration.DeclarationParser import DeclarationParser
from model.symbol_table import SymbolTable
from common.logger import GeneratorLogger


class DeclarationCalculator():
    '''A calculator for default values of parameter'''

    def __init__(self, symbol_table: SymbolTable, logger) -> None:
        self._symbol_table = symbol_table
        self._scope = symbol_table
        self.logger = logger

    def calc_parameter(self, parameter_symbol: ParameterSymbol):
        '''calculates a variable or a array and writes its value'''
        # check if the context is a Array or a simple Value
        context = parameter_symbol.context
        if parameter_symbol.is_array:
            # Array
            if context.defaultValue:
                self.calc_arithmetic_expression_array(context, context.defaultValue, parameter_symbol)
                parameter_symbol.is_tree = False
            else:
                parameter_symbol.value = None
                self.logger.relax(context, f"no default value defined for array parameter {parameter_symbol.name}")
        else:
            # simple value
            if context.defaultValue:
                parameter_symbol.value = self.calc_arithmetic_expression(context.defaultValue, parameter_symbol)
                parameter_symbol.is_tree = False
            else:
                parameter_symbol.value = None
                self.logger.relax(context,f"no default value defined for scalar parameter {parameter_symbol.name}")

    def calc_arithmetic_expression_array(
            self,
            var_context: DeclarationParser.ParamAssignStatContext,
            context: DeclarationParser.ArithmeticExpressionContext,
            array_symbol: ArraySymbol
    ):
        '''calculates a array in decl language'''

        # tupleList representation: list[2:4,5] = [range(2,4), range(5)]
        # wanted: list[2,4:8] = [[(4,1),(5,2),(6,3),(7,4),(8,5)],[(4,1),(5,2),(6,3),(7,4),(8,5)],[(4,1),(5,2),(6,3),(7,4),(8,5)]]
        def convertToTupleList(range_list: list, calc_list, vector: list, depth: int) -> None:
            if len(vector) < depth + 1:
                vector.append(0)
            else:
                vector[depth] = 0
            # range_list is empty so there is no given range
            if len(range_list) == 0:
                for i in range(len(calc_list)):
                    vector[depth] = i
                    if isinstance(calc_list[i], list):
                        convertToTupleList(range_list, calc_list[i], vector.copy(), depth + 1)
                    array_symbol.add(vector, calc_list[i])
                return
            index = 0
            if not isinstance(calc_list, list):
                self.logger.relax(context,f"Array value is not a list, proceed to convert it in to one")
                if isinstance(calc_list, str):
                    if calc_list.startswith("'"):
                        calc_list = calc_list.strip("'")
                    else:
                        calc_list = calc_list.strip('"')
                calc_list = [calc_list for _ in range(len(range_list[0]))]
            if len(range_list[0]) < len(calc_list) and isinstance(calc_list, list):
                range_list[0] = range(range_list[0].start, len(calc_list) + range_list[0].start)
            for i in range_list[0]:
                vector[depth] = i
                if isinstance(calc_list[index], list):
                    convertToTupleList(range_list[1:], calc_list[index], vector.copy(), depth + 1)
                else:
                    array_symbol.add(vector, calc_list[index])
                index += 1
            return

        calcList = self.calc_arithmetic_expression(context, array_symbol)

        range_list = []
        for i in varcontext.type_.arrayType().dimensions:
            if i.rangeDimension():
                j = i.rangeDimension()
                range_list.append(range(int(j.lowerBound.text), int(j.upperBound.text) + 1))
            else:
                j = i.sizeDimension()
                size = int(j.size.text) if j.size else 0
                range_list.append(range(size))
        vector = []
        convertToTupleList(range_list, calcList, vector, 0)

    def calc_arithmetic_expression(self, context: DeclarationParser.ArithmeticExpressionContext, parameter_symbol: ParameterSymbol):
        '''calculates a normal arithmetic expression for parameter'''
        if context.getChildCount() == 1:
            # must be a multiplication Expression
            return self.calc_multiplication_expression(context.multiplicationExpression(), parameter_symbol)
        else:
            # has 3 children: left, operator and right
            leftValue = self.calc_multiplication_expression(context.left, parameter_symbol)
            # is enum
            leftValue = leftValue[1] if isinstance(leftValue, tuple) else leftValue
            operator = context.op.getText()
            if operator == "+":
                operator = op.add
            else:
                operator = op.sub
            rightValue = self.calc_arithmetic_expression(context.right, parameter_symbol)
            # is enum
            rightValue = rightValue[1] if isinstance(rightValue, tuple) else rightValue
            return operator(leftValue, rightValue)

    def calc_multiplication_expression(self, context: DeclarationParser.MultiplicationExpressionContext, parameter_symbol: ParameterSymbol):
        '''calculates a multiplication expression'''
        if context.getChildCount() == 1:
            return self.calc_value_expression(context.valueExpression(), parameter_symbol)
        else:
            # has 3 children: left, operator, right
            left_value = self.calc_value_expression(context.left, parameter_symbol)
            left_value = left_value[1] if isinstance(left_value, tuple) else left_value
            operator = context.op.getText()
            right_value = self.calc_multiplication_expression(context.right, parameter_symbol)
            # is enum
            right_value = right_value[1] if isinstance(right_value, tuple) else right_value
            if operator == "*":
                operator = op.mul
            # if int then //
            elif operator == "/":
                if isinstance(left_value, int) and isinstance(right_value, int):
                    operator = op.floordiv
                else:
                    operator = op.truediv
            else:
                operator = op.mod
            return operator(left_value, right_value)

    def calc_value_expression(self, context: DeclarationParser.ValueExpressionContext, parameter_symbol: ParameterSymbol):
        '''calculates a value expression'''
        if context.parenthesisExpression():
            return self.calc_parenthesis_expression(context.parenthesisExpression(), parameter_symbol)
        if context.namedElementReference():
            return self.calc_named_element_reference(context.namedElementReference(), parameter_symbol)
        if context.arrayExpression():
            return self.calc_array_expression(context.arrayExpression(), parameter_symbol)
        if context.literalExpression():
            return self.calc_literal_expression(context.literalExpression())
        self.logger.error(context, "INTERNAL ValueExpressionError: No given Token to proceed in calculation")
        return None

    def calc_parenthesis_expression(self, context: DeclarationParser.ParenthesisExpressionContext, parameter_symbol: ParameterSymbol):
        '''calculates a parenthesis expression (expression = arithmetic expression)'''
        return self.calc_arithmetic_expression(context.expression, parameter_symbol)

    def calc_named_element_reference(self, context: DeclarationParser.NamedElementReferenceContext, parameter_symbol: ParameterSymbol):
        '''resolves a named element reference (Enums, Parameter, etc.) also can handle wrong parser choice to handle true or false'''
        # what is attribute? element is maybe a group
        element_attribute = context.attribute.text if context.attribute else None
        if context.element.text == "true" or context.element.text == "false":
            self.logger.relax(context,f"wrong parsing in variable {parameter_symbol.name} try to compensate to value {context.element.text}")
            if context.element.text == "false":
                parameter_symbol.value = False
            else:
                parameter_symbol.value = True
            return parameter_symbol.value
        element_value = self._scope.resolve_sync(context.element.text)
        if element_value:
            # just return the value here should work due to scoping
            if element_attribute:
                if isinstance(element_value, EnumSymbol):
                    for index, value in element_value.enums:
                        if index == element_attribute:
                            return value
                    self.logger.error(context,f"Enumeral definition could not be found.")
                    return 0
                for i in element_value.children():
                    if i.name == element_attribute:
                        return i.value
            else:
                return element_value.value
        else:
            if isinstance(parameter_symbol.type, EnumSymbol):
                for i, j in parameter_symbol.type.enums:
                    if i == context.element.text:
                        # just return the enums value
                        return i, j
            else:
                for elem in self._symbol_table.get_all_nested_symbols_sync():
                    if isinstance(elem, EnumSymbol):
                        for i, j in elem.enums:
                            if i == context.element.text:
                                self.logger.relax(context,f"EnumType not given for variable {parameter_symbol.name} resolving may result in wrong reference")
                                return i, j
        self.logger.error(context,f"INTERNAL: Named Element {context.element.text} could not be resolved")

    def calc_array_expression(self, context: DeclarationParser.ArrayExpressionContext, parameter_symbol: ParameterSymbol):
        '''calculates a array expression'''
        valueList = []
        for i in context.elements:
            valueList.append(self.calc_arithmetic_expression(i, parameter_symbol))
        return valueList

    def calc_literal_expression(self, context: DeclarationParser.LiteralExpressionContext):
        '''calculates a literal expression'''
        return self.calc_literal(context.value)

    def calc_literal(self, context: DeclarationParser.LiteralContext):
        '''calculates a literal (string, long, double, boolean)'''
        if context.stringValue():
            return context.stringValue().value.text.strip('"')
        if context.longValue():
            return int(context.longValue().value.text)
        if context.doubleValue():
            return float(context.doubleValue().value.text)
        if context.booleanValue():
            if context.booleanValue().value.text == "false":
                return False
            return True

    def calculate(self) -> SymbolTable:
        '''writes the calculated values in the value parameter of every parameter found in symbol_table'''

        def recursion_helper(element):
            if isinstance(element, ParameterSymbol):
                self.calc_parameter(element)
            elif not hasattr(element, "children"):
                pass
            else:
                for i in element.children():
                    if isinstance(i, ScopedSymbol):
                        self._scope = i
                    recursion_helper(i)

        recursion_helper(self._symbol_table)
        return self._symbol_table
