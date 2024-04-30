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
from symboltable.symbol_table import SymbolTable, VariableSymbol, ArraySymbol, ScopedSymbol, EnumSymbol
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser
from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser
from symboltable.symbol_table import ArraySymbol, SymbolTable


class DeclarationCalculator():
    '''A calculator for default values of parameter'''

    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table
        self._scope = symbol_table

    def calc_variable(self, variable_symbol: VariableSymbol):
        '''calculates a variable or a array and writes its value'''
        # check if the context is a Array or a simple Value
        context = variable_symbol.context
        if variable_symbol.is_array:
            # Array
            if context.defaultValue:
                self.calc_arithmetic_expression_array(context, context.defaultValue, variable_symbol)
                variable_symbol.is_tree = False
            else:
                variable_symbol.val = None
                print("WARNING: no default value defined for Array", variable_symbol.name)
        else:
            # simple Value
            if context.defaultValue:
                variable_symbol.val = self.calc_arithmetic_expression(context.defaultValue, variable_symbol)
                variable_symbol.is_tree = False
            else:
                variable_symbol.val = None
                print("WARNING: no default value defined for Variable", variable_symbol.name)

    def calc_arithmetic_expression_array(self, varctx: DeclarationParser.ParamAssignStatContext,
                                      ctx: DeclarationParser.ArithmeticExpressionContext, array_symbol: ArraySymbol):
        '''calculates a array in decl language'''

        # tupleList representation: list[2:4,5] = [range(2,4), range(5)]
        # wanted: list[2,4:8] = [[(4,1),(5,2),(6,3),(7,4),(8,5)],[(4,1),(5,2),(6,3),(7,4),(8,5)],[(4,1),(5,2),(6,3),(7,4),(8,5)]]
        def convertToTupleList(range_list: list, calc_list, vector: list, depht: int) -> None:
            if len(vector) < depht + 1:
                vector.append(0)
            else:
                vector[depht] = 0
            # range_list is empty so there is no given range
            if len(range_list) == 0:
                for i in range(len(calc_list)):
                    vector[depht] = i
                    if isinstance(calc_list[i], list):
                        convertToTupleList(range_list, calc_list[i], vector.copy(), depht + 1)
                    array_symbol.add(vector, calc_list[i])
                return
            index = 0
            if not isinstance(calc_list, list):
                print("Warning: Array Value is not a list, proceed to convert it in to one")
                if isinstance(calc_list, str):
                    if calc_list.startswith("'"):
                        calc_list = calc_list.strip("'")
                    else:
                        calc_list = calc_list.strip('"')
                calc_list = [calc_list for _ in range(len(range_list[0]))]
            if len(range_list[0]) < len(calc_list) and isinstance(calc_list, list):
                range_list[0] = range(range_list[0].start, len(calc_list) + range_list[0].start)
            for i in range_list[0]:
                vector[depht] = i
                if isinstance(calc_list[index], list):
                    convertToTupleList(range_list[1:], calc_list[index], vector.copy(), depht + 1)
                else:
                    array_symbol.add(vector, calc_list[index])
                index += 1
            return

        calcList = self.calc_arithmetic_expression(ctx, array_symbol)

        range_list = []
        for i in varctx.type_.arrayType().dimensions:
            if i.rangeDimension():
                j = i.rangeDimension()
                range_list.append(range(int(j.lowerBound.text), int(j.upperBound.text) + 1))
            else:
                j = i.sizeDimension()
                size = int(j.size.text) if j.size else 0
                range_list.append(range(size))
        vector = []
        convertToTupleList(range_list, calcList, vector, 0)

    def calc_arithmetic_expression(self, ctx: DeclarationParser.ArithmeticExpressionContext, variable_symbol: VariableSymbol):
        '''calculates a normal arithmetic expression for parameter'''
        if ctx.getChildCount() == 1:
            # must be a multiplication Expression
            return self.calc_multiplication_expression(ctx.multiplicationExpression(), variable_symbol)
        else:
            # has 3 children: left, operator and right
            leftValue = self.calc_multiplication_expression(ctx.left, variable_symbol)
            # is enum
            leftValue = leftValue[1] if isinstance(leftValue, tuple) else leftValue
            operator = ctx.op.getText()
            if operator == "+":
                operator = op.add
            else:
                operator = op.sub
            rightValue = self.calc_arithmetic_expression(ctx.right, variable_symbol)
            # is enum
            rightValue = rightValue[1] if isinstance(rightValue, tuple) else rightValue
            return operator(leftValue, rightValue)

    def calc_multiplication_expression(self, ctx: DeclarationParser.MultiplicationExpressionContext, variable_symbol: VariableSymbol):
        '''calculates a multiplication expression'''
        if ctx.getChildCount() == 1:
            return self.calc_value_expression(ctx.valueExpression(), variable_symbol)
        else:
            # has 3 children: left, operator, right
            left_value = self.calc_value_expression(ctx.left, variable_symbol)
            left_value = left_value[1] if isinstance(left_value, tuple) else left_value
            operator = ctx.op.getText()
            right_value = self.calc_multiplication_expression(ctx.right, variable_symbol)
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

    def calc_value_expression(self, ctx: DeclarationParser.ValueExpressionContext, variable_symbol: VariableSymbol):
        '''calculates a value expression'''
        if ctx.parenthesisExpression():
            return self.calc_parenthesis_expression(ctx.parenthesisExpression(), variable_symbol)
        if ctx.namedElementReference():
            return self.calc_named_element_reference(ctx.namedElementReference(), variable_symbol)
        if ctx.arrayExpression():
            return self.calc_array_expression(ctx.arrayExpression(), variable_symbol)
        if ctx.literalExpression():
            return self.calc_literal_expression(ctx.literalExpression())
        print("ValueExpressionError: No given Token to proceed in calculation")
        return None

    def calc_parenthesis_expression(self, ctx: DeclarationParser.ParenthesisExpressionContext, variable_symbol: VariableSymbol):
        '''calculates a parenthesis expression (expression = arithmetic expression)'''
        return self.calc_arithmetic_expression(ctx.expression, variable_symbol)

    def calc_named_element_reference(self, context: DeclarationParser.NamedElementReferenceContext, variable_symbol: VariableSymbol):
        '''resolves a named element reference (Enums, Parameter, etc.) also can handle wrong parser choice to handle true or false'''
        # what is attribute? element is maybe a group
        element_attribute = context.attribute.text if context.attribute else None
        if context.element.text == "true" or context.element.text == "false":
            print("WARNING: wrong parsing in variable", variable_symbol.name, "try to compensate to value", context.element.text)
            if context.element.text == "false":
                variable_symbol.val = False
            else:
                variable_symbol.val = True
            return variable_symbol.value
        element_value = self._scope.resolve_sync(context.element.text)
        if element_value:
            # just return the value here should work due to scopeing
            if element_attribute:
                if isinstance(element_value, EnumSymbol):
                    for index, value in element_value.enums:
                        if index == element_attribute:
                            return value
                    print("EnumError: Enum definition could not be found")
                    return 0
                for i in element_value.children():
                    if i.name == element_attribute:
                        return i.value
            else:
                return element_value.value
        else:
            if isinstance(variable_symbol.type, EnumSymbol):
                for i, j in variable_symbol.type.enums:
                    if i == context.element.text:
                        # just return the enums value
                        return i, j
            else:
                for elem in self._symbol_table.get_all_nested_symbols_sync():
                    if isinstance(elem, EnumSymbol):
                        for i, j in elem.enums:
                            if i == context.element.text:
                                print("WARNING: EnumType not given for variable", variable_symbol.name, "resolving may result in wrong reference")
                                return i, j
        print("Named Element", context.element.text, "could not be resolved")

    def calc_array_expression(self, ctx: DeclarationParser.ArrayExpressionContext, variable_symbol: VariableSymbol):
        '''calculates a array expression'''
        valueList = []
        for i in ctx.elements:
            valueList.append(self.calc_arithmetic_expression(i, variable_symbol))
        return valueList

    def calc_literal_expression(self, ctx: DeclarationParser.LiteralExpressionContext):
        '''calculates a literal expression'''
        return self.calc_literal(ctx.value)

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
            if isinstance(element, VariableSymbol):
                self.calc_variable(element)
            elif not hasattr(element, "children"):
                pass
            else:
                for i in element.children():
                    if isinstance(i, ScopedSymbol):
                        self._scope = i
                    recursion_helper(i)

        recursion_helper(self._symbol_table)
        return self._symbol_table


class ConfigurationCalculator(DeclarationCalculator):
    '''A calculator for configurated values of parameter'''

    def __init__(self, symbolTable: SymbolTable, configurationList: list):
        super().__init__(symbolTable)
        self.configurationList = configurationList

    def calculate(self) -> SymbolTable:
        '''writes the calculated values in value parameter of every (in order) configurated parameter'''
        for elem, index in self.configurationList:
            if isinstance(elem, ScopedSymbol):
                self._scope = elem
            else:
                self._scope = elem.parent()
            self.calc_variable(elem, index)
        return self._symbol_table

    def calc_variable(self, variable_symbol: VariableSymbol, index: int):
        '''calculates a parameter or an array'''
        ctx = variable_symbol.configuration[index]
        # check if the context is a Array or a simple Value
        if variable_symbol.is_array:
            # Array
            self.calc_arithmetic_expression_array(ctx, ctx.value, variable_symbol)
        else:
            # simple Value
            variable_symbol.val = self.calc_arithmetic_expression(ctx.value, variable_symbol)
            variable_symbol.is_tree = False

    def calc_arithmetic_expression_array(self, varctx: ConfigurationParser.ParameterAssignmentContext,
                                      ctx: ConfigurationParser.ArithmeticExpressionContext, array_symbol: ArraySymbol):
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
                    print("WARNING: didnt give enough values to ranged nd-array", array_symbol.name)
            return

        calc_list = self.calc_arithmetic_expression(ctx, array_symbol)

        range_list = []
        for i in varctx.selectors:
            if i.rangeSelector():
                j: ConfigurationParser.RangeSelectorContext = i.rangeSelector()
                range_list.append(range(int(j.lowerBound.text), int(j.upperBound.text) + 1))
            else:
                j: ConfigurationParser.ElementSelectorContext = i.elementSelector()
                element = int(j.element.text)
                range_list.append(range(element, element + 1))
        vector = []
        convert_to_tuple_list(range_list, calc_list, vector, 0)
