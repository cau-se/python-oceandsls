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
from ..symboltable.symbol_table import SymbolTable, VariableSymbol, ArraySymbol, ScopedSymbol, EnumSymbol
from ..gen.python.Configuration.ConfigurationParser import ConfigurationParser
from ..gen.python.Declaration.DeclarationParser import DeclarationParser
from ..symboltable.symbol_table import ArraySymbol, SymbolTable


class DeclarationCalculator():
    '''A calculator for default values of parameter'''

    def __init__(self, symbol_table: SymbolTable) -> None:
        self._symbol_table = symbol_table
        self._scope = symbol_table

    def calcVariable(self, variable_symbol: VariableSymbol):
        '''calculates a variable or a array and writes its value'''
        # check if the context is a Array or a simple Value
        context = variable_symbol.context
        if variable_symbol.is_array:
            # Array
            if context.defaultValue:
                self.calcArithmeticExpressionArray(context, context.defaultValue, variable_symbol)
                variable_symbol.is_tree = False
            else:
                variable_symbol.val = None
                print("WARNING: no default value defined for Array", variable_symbol.name)
        else:
            # simple Value
            if context.defaultValue:
                variable_symbol.val = self.calcArithmeticExpression(context.defaultValue, variable_symbol)
                variable_symbol.is_tree = False
            else:
                variable_symbol.val = None
                print("WARNING: no default value defined for Variable", variable_symbol.name)

    def calcArithmeticExpressionArray(self, varctx: DeclarationParser.ParamAssignStatContext,
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

        calcList = self.calcArithmeticExpression(ctx, array_symbol)

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

    def calcArithmeticExpression(self, ctx: DeclarationParser.ArithmeticExpressionContext, variableSymbol: VariableSymbol):
        '''calculates a normal arithmetic expression for parameter'''
        if ctx.getChildCount() == 1:
            # must be a multiplication Expression
            return self.calcMultiplicationExpression(ctx.multiplicationExpression(), variableSymbol)
        else:
            # has 3 children: left, operator and right
            leftValue = self.calcMultiplicationExpression(ctx.left, variableSymbol)
            # is enum
            leftValue = leftValue[1] if isinstance(leftValue, tuple) else leftValue
            operator = ctx.op.getText()
            if operator == "+":
                operator = op.add
            else:
                operator = op.sub
            rightValue = self.calcArithmeticExpression(ctx.right, variableSymbol)
            # is enum
            rightValue = rightValue[1] if isinstance(rightValue, tuple) else rightValue
            return operator(leftValue, rightValue)

    def calcMultiplicationExpression(self, ctx: DeclarationParser.MultiplicationExpressionContext, variableSymbol: VariableSymbol):
        '''calculates a multiplication expression'''
        if ctx.getChildCount() == 1:
            return self.calcValueExpression(ctx.valueExpression(), variableSymbol)
        else:
            # has 3 children: left, operator, right
            leftValue = self.calcValueExpression(ctx.left, variableSymbol)
            leftValue = leftValue[1] if isinstance(leftValue, tuple) else leftValue
            operator = ctx.op.getText()
            rightValue = self.calcMultiplicationExpression(ctx.right, variableSymbol)
            # is enum
            rightValue = rightValue[1] if isinstance(rightValue, tuple) else rightValue
            if operator == "*":
                operator = op.mul
            # if int then //
            elif operator == "/":
                if isinstance(leftValue, int) and isinstance(rightValue, int):
                    operator = op.floordiv
                else:
                    operator = op.truediv
            else:
                operator = op.mod
            return operator(leftValue, rightValue)

    def calcValueExpression(self, ctx: DeclarationParser.ValueExpressionContext, variableSymbol: VariableSymbol):
        '''calculates a value expression'''
        if ctx.parenthesisExpression():
            return self.calcParenthesisExpression(ctx.parenthesisExpression(), variableSymbol)
        if ctx.namedElementReference():
            return self.calcNamedElementReference(ctx.namedElementReference(), variableSymbol)
        if ctx.arrayExpression():
            return self.calcArrayExpression(ctx.arrayExpression(), variableSymbol)
        if ctx.literalExpression():
            return self.calcLiteralExpression(ctx.literalExpression())
        print("ValueExpressionError: No given Token to proceed in calculation")
        return None

    def calcParenthesisExpression(self, ctx: DeclarationParser.ParenthesisExpressionContext, variableSymbol: VariableSymbol):
        '''calculates a parenthesis expression (expression = arithmetic expression)'''
        return self.calcArithmeticExpression(ctx.expression, variableSymbol)

    def calcNamedElementReference(self, context: DeclarationParser.NamedElementReferenceContext, variable_symbol: VariableSymbol):
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

    def calcArrayExpression(self, ctx: DeclarationParser.ArrayExpressionContext, variableSymbol: VariableSymbol):
        '''calculates a array expression'''
        valueList = []
        for i in ctx.elements:
            valueList.append(self.calcArithmeticExpression(i, variableSymbol))
        return valueList

    def calcLiteralExpression(self, ctx: DeclarationParser.LiteralExpressionContext):
        '''calculates a literal expression'''
        return self.calcLiteral(ctx.value)

    def calcLiteral(self, ctx: DeclarationParser.LiteralContext):
        '''calculates a literal (string, long, double, boolean)'''
        if ctx.stringValue():
            return ctx.stringValue().value.text.strip('"')
        if ctx.longValue():
            return int(ctx.longValue().value.text)
        if ctx.doubleValue():
            return float(ctx.doubleValue().value.text)
        if ctx.booleanValue():
            if ctx.booleanValue().value.text == "false":
                return False
            return True

    def calculate(self) -> SymbolTable:
        '''writes the calculated values in the value parameter of every paremeter found in symbol_table'''

        def recursionHelper(elem):
            if isinstance(elem, VariableSymbol):
                self.calcVariable(elem)
            elif not hasattr(elem, "children"):
                pass
            else:
                for i in elem.children():
                    if isinstance(i, ScopedSymbol):
                        self._scope = i
                    recursionHelper(i)

        recursionHelper(self._symbol_table)
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
            self.calcVariable(elem, index)
        return self._symbol_table

    def calcVariable(self, variableSymbol: VariableSymbol, index: int):
        '''calculates a parameter or an array'''
        ctx = variableSymbol.configuration[index]
        # check if the context is a Array or a simple Value
        if variableSymbol.is_array:
            # Array
            self.calcArithmeticExpressionArray(ctx, ctx.value, variableSymbol)
        else:
            # simple Value
            variableSymbol.val = self.calcArithmeticExpression(ctx.value, variableSymbol)
            variableSymbol.is_tree = False

    def calcArithmeticExpressionArray(self, varctx: ConfigurationParser.ParameterAssignmentContext,
                                      ctx: ConfigurationParser.ArithmeticExpressionContext, arraySymbol: ArraySymbol):
        '''calculates a array configuration'''

        # tupleList representation: list[2:4,5] = [range(2,4), range(5)]
        # wanted: list[2,4:8] = [[(4,1),(5,2),(6,3),(7,4),(8,5)],[(4,1),(5,2),(6,3),(7,4),(8,5)],[(4,1),(5,2),(6,3),(7,4),(8,5)]]
        def convertToTupleList(rangeList: list, calcList, vector: list, depht: int) -> list:
            if len(vector) < depht + 1:
                vector.append(0)
            else:
                vector[depht] = 0
            # rangeList is empty so there is no given range
            if len(rangeList) == 0:
                for i in range(len(calcList)):
                    vector[depht] = i
                    if isinstance(calcList[i], list):
                        convertToTupleList(rangeList, calcList[i], vector.copy(), depht + 1)
                    arraySymbol.add(vector, calcList[i])
                return
            index = 0
            if not isinstance(calcList, list):
                print("Warning: Array Value is not a list, proceed to convert it in to one", arraySymbol.name, "=", calcList)
                if isinstance(calcList, str):
                    if calcList.startswith("'"):
                        calcList = calcList.strip("'")
                    else:
                        calcList = calcList.strip('"')
                calcList = [calcList for _ in range(len(rangeList[0]))]
                print("Converted to:", calcList)
            if len(rangeList[0]) < len(calcList) and isinstance(calcList, list):
                rangeList[0] = range(rangeList[0].start, len(calcList) + rangeList[0].start)
            for i in rangeList[0]:
                vector[depht] = i
                if not len(calcList) == 0:
                    if isinstance(calcList[index], list):
                        convertToTupleList(rangeList[1:], calcList[index], vector.copy(), depht + 1)
                    else:
                        arraySymbol.add(vector, calcList[index])
                    index += 1
                else:
                    print("WARNING: didnt give enough values to ranged nd-array", arraySymbol.name)
            return

        calcList = self.calcArithmeticExpression(ctx, arraySymbol)

        rangeList = []
        for i in varctx.selectors:
            if i.rangeSelector():
                j: ConfigurationParser.RangeSelectorContext = i.rangeSelector()
                rangeList.append(range(int(j.lowerBound.text), int(j.upperBound.text) + 1))
            else:
                j: ConfigurationParser.ElementSelectorContext = i.elementSelector()
                element = int(j.element.text)
                rangeList.append(range(element, element + 1))
        vector = []
        convertToTupleList(rangeList, calcList, vector, 0)
