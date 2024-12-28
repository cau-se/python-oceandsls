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

__author__ = "reiner"

# util imports
from typing import Generic, Callable, List

# antlr4
from antlr4.tree.Tree import ParseTree
from antlr4.Token import CommonToken
from antlr4 import ParserRuleContext, TerminalNode

# user relative imports
from model.symbols import Scope, T, P
from model.declaration_model import DeclarationModel, ParameterGroup, Feature, Parameter, SelectorExpression
from model.unit_model import UnitPrefix
from model.arithmetic_model import ArithmeticExpression, MultiplicationExpression, EMultiplicationOperator, EAdditionOperator, \
    ArrayExpression, IntValue, FloatValue, StringValue
from model.type_system import EnumeralType, base_types
from common.logger import GeneratorLogger
from common.unit_processing import parse_unit

from conflspserver.gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser
from conflspserver.gen.python.Configuration.ConfigurationVisitor import ConfigurationVisitor

import os


class GeneratorConfigurationVisitor(ConfigurationVisitor, Generic[T]):
    _model: DeclarationModel

    _generator_selector: str

    def __init__(self, model: DeclarationModel, logger: GeneratorLogger):
        super().__init__()
        # creates a new symboltable with no duplicate symbols
        self._model = model
        # TODO scope marker
        # self._scope = self._symbol_table.addNewSymbolOfType( ScopedSymbol, None )
        self._scope = self._model
        self._type_scope = None
        self._logger = logger
        self.cwd = "."

        self.configuration_list = []

    def print_symbol(self, elements:list, level:int):
        result = ""
        for i in range(0,level+1):
            name = elements[i].text
            if result == "":
                result = f"{name}"
            else:
                result = f"{result}.{name}"
        return result

    @property
    def symbol_table(self) -> DeclarationModel:
        return self._model

    @property
    def generator_selector(self) -> str:
        return self._generator_selector

    def default_result(self) -> DeclarationModel:
        return self._model

    def visitConfigurationModel(self, ctx: ConfigurationParser.ConfigurationModelContext):
        model_name = ctx.declarationModel.text
        if self._model.name == model_name:
            self._model.configuration_name = ctx.name.text
            for activation in ctx.featureActivations:
                self.visitFeatureActivation(activation)
            for feature in ctx.featureConfigurations:
                self.visitFeatureConfiguration(feature)
            for group in ctx.parameterGroups:
                self.visitParameterGroup(group)

            return self._model
        else:
            print(f"ERROR: wrong declaration model {model_name}")

    def visitArithmeticExpression(self, ctx: ConfigurationParser.ArithmeticExpressionContext):
        if ctx.left is not None:
            if ctx.right is not None:
                left = self.visit(ctx.left)
                right = self.visit(ctx.right)
                op = self.visitEAdditionOperator(ctx.op)
                return ArithmeticExpression(ctx=ctx, unit=None, left=left, right=right, op=op)
            else:
                return self.visit(ctx.left)

        if len(ctx.children) == 1:
            expression = ctx.children[0]
            if isinstance(expression, ConfigurationParser.MultiplicationExpressionContext):
                return self.visitMultiplicationExpression(expression)
            else:
                print(f"ERROR unsupported type in ArithmeticExpression {type(expression)}")
                return None
        else:
            print("ERROR")
            return None

    def visitEAdditionOperator(self, ctx: ConfigurationParser.EAdditionOperatorContext):
        value = ctx.getText()
        if value == EAdditionOperator.ADD.value:
            return EAdditionOperator.ADD
        if value == EAdditionOperator.SUB.value:
            return EAdditionOperator.SUB

        print("Illegal addition operator")
        return None

    def visitMultiplicationExpression(self, ctx: ConfigurationParser.MultiplicationExpressionContext):
        if ctx.left is not None:
            if ctx.right is not None:
                left = self.visit(ctx.left)
                right = self.visit(ctx.right)
                op = self.visitEMultiplicationOperator(ctx.op)
                return MultiplicationExpression(ctx=ctx, unit=None, left=left, right=right, op=op)
            else:
                return self.visit(ctx.left)

        if len(ctx.children) == 1:
            expression = ctx.children[0]
            if isinstance(expression, ConfigurationParser.ValueExpressionContext):
                return self.visitValueExpression(expression)
            else:
                print(f"ERROR unsupported type in ValueExpressionContext {type(expression)}")
                return None
        else:
            print("ERROR")
            return None

    def visitEMultiplicationOperator(self, ctx: ConfigurationParser.EMultiplicationOperatorContext):
        value = ctx.getText()
        if value == EMultiplicationOperator.MULT.value:
            return EMultiplicationOperator.MULT
        if value == EMultiplicationOperator.DIV.value:
            return EMultiplicationOperator.DIV
        if value == EMultiplicationOperator.MOD.value:
            return EMultiplicationOperator.MOD

        return None

    def visitValueExpression(self, ctx: ConfigurationParser.ValueExpressionContext):
        if ctx.parenthesisExpression() is not None:
            return self.visitParenthesisExpression(ctx.parenthesisExpression())
        elif ctx.literalExpression() is not None:
            return self.visitLiteralExpression(ctx.literalExpression())
        elif ctx.namedElementReference() is not None:
            return self.visitNamedElementReference(ctx.namedElementReference())
        elif ctx.arrayExpression() is not None:
            return self.visitArrayExpression(ctx.arrayExpression())
        else:
            print(f"ERROR something {ctx} {type(ctx)}")
            return None

    def visitParenthesisExpression(self, ctx: ConfigurationParser.ParenthesisExpressionContext):
        return self.visitArithmeticExpression(ctx.arithmeticExpression())

    def visitArrayExpression(self, ctx: ConfigurationParser.ArrayExpressionContext):
        elements:List[ArithmeticExpression] = []
        for element in ctx.elements:
            elements.append(self.visit(element))
        return ArrayExpression(ctx=ctx, unit=None, elements=elements)

    def visitLiteralExpression(self, ctx: ConfigurationParser.LiteralExpressionContext):
        return self.visitLiteral(ctx.literal())

    def visitLiteral(self, ctx: ConfigurationParser.LiteralContext):
        if len(ctx.children) == 1:
            literal = ctx.children[0]
            return self.visit(literal)
        else:
            print("ERROR")
            return None

    def visitLongValue(self, ctx: ConfigurationParser.LongValueContext):
        return IntValue(ctx=ctx, unit=None, type=base_types["long"], value=int(ctx.value.text))

    def visitDoubleValue(self, ctx: ConfigurationParser.DoubleValueContext):
        return FloatValue(ctx=ctx, unit=None, type=base_types["double"], value=float(ctx.value.text))

    def visitStringValue(self, ctx: ConfigurationParser.StringValueContext):
        return StringValue(ctx=ctx, unit=None, type=base_types["string"], value=ctx.value.text[1:-1])

    def visitNamedElementReference(self, ctx: ConfigurationParser.NamedElementReferenceContext):
        depth = len(ctx.elements)
        scope = self._scope
        if depth > 1:
            for i in range(1,depth):
                scope = scope.parent

        # check whether it is a parameter
        parameter_level = 0
        param = True
        for i in range(0,depth):
            scope = scope.resolve_symbol(ctx.elements[i].text)
            if scope is None:
                parameter_level = i
                param = False
                break

        if param:
            return scope

        # check whether it is an enumeration
        if depth == 2: # Can be an enumeration
            data_type = self._model.types.get(ctx.elements[0].text)
            if isinstance(data_type, EnumeralType):
                enumeral = data_type.enumerals.get(ctx.elements[1].text, None)
                if enumeral is None:
                    self._logger.strict(ctx, f"Symbol {self.print_symbol(ctx.elements, 2)} does not refer to an enumeral nor parameter and parameter group")
                    return None
                else:
                    return enumeral
            else:
                self._logger.strict(ctx, f"Symbol {self.print_symbol(ctx.elements, 1)} does not refer to an enumeration type nor parameter and parameter group")
                return None

        # check whether it is an enumeration inferred by parameter type
        data_type = self._type_scope
        if isinstance(data_type, EnumeralType) or isinstance(data_type, InlineEnumeralType):
            enumeral = data_type.enumerals.get(ctx.elements[0].text, None)
            if enumeral is None:
                self._logger.strict(ctx, f"Symbol {self.print_symbol(ctx.elements, 2)} does not refer to an enumeral nor parameter and parameter group")
                return None
            else:
                return enumeral

        # Strange cases
        self._logger.strict(ctx, f"Symbol {self.print_symbol(ctx.elements, len(ctx.elements))} cannot be resolved.")
        return None

    def visitParameterAssignment(self, ctx: ConfigurationParser.ParameterAssignmentContext):
        # define the given Parameter
        var_name = ctx.declaration.getText()  # set and get the variable name here
        parameter:Parameter = self._scope.parameters.get(var_name)
        var_unit = None
        if ctx.unit is not None:
            unit:ConfigurationParser.UnitSpecificationContext = ctx.unit

            var_unit = parse_unit(unit.unit.text)

        self._type_scope = parameter.type

        if parameter is None:
            print(f"ERROR: Parameter {var_name} does not exist in {self._scope.name}")
            self._type_scope = None
            return None
        else:
            if len(ctx.selectors) > 0:
                selectors = []
                for s in ctx.selectors:
                    selectors.append(self.visitSelector(s))

                value = self.visitArithmeticExpression(ctx.value)
                value.unit = var_unit
                selector_expression = SelectorExpression(selectors, value)
                parameter.entries.append(selector_expression)
            else:
                value = self.visitArithmeticExpression(ctx.value)
                value.unit = var_unit
                parameter.entries.append(value)

            return parameter

    def visitParameterGroup(self, ctx: ConfigurationParser.ParameterGroupContext):
        group_name = ctx.declaration.text
        group:ParameterGroup = self._scope.resolve_parameter_group(group_name)
        if group == None:
            print(f"ERROR: Missing group {group_name}")
            return None

        parent_scope = self._scope
        self._scope = group

        for parameter_ctx in ctx.parameters:
            self.visitParameterAssignment(parameter_ctx)

        return group

    def visitSelector(self, ctx: ConfigurationParser.SelectorContext):
        vector = []
        vector.append(self.visitChildren(ctx))
        return vector

    def visitElementSelector(self, ctx: ConfigurationParser.ElementSelectorContext):
        return int(ctx.element.text)

    def visitRangeSelector(self, ctx: ConfigurationParser.RangeSelectorContext):
        return (int(ctx.lowerBound.text), int(ctx.upperBound.text))

    def visitUnitSpecification(self, ctx: ConfigurationParser.UnitSpecificationContext):
        return self.stringToPrefix(ctx.unit.text)

    def visitFeatureConfiguration(self, ctx: ConfigurationParser.FeatureConfigurationContext):
        feature_name = ctx.declaration.text
        feature:Feature = self._scope.resolve_feature(feature_name)
        if feature == None:
            print(f"ERROR: Missing {feature_name}")
            return None
        else:
            feature.is_activated = True

            parent_scope = self._scope
            self._scope = feature
            for activation in ctx.featureActivations:
                self.visitFeatureActivation(activation)
            for configuration in ctx.featureConfigurations:
                self.visitFeatureConfiguration(configuration)
            for group in ctx.parameterGroups:
                self.visitParameterGroup(group)
            self._scope = parent_scope

            return feature

    def visitFeatureActivation(self, ctx: ConfigurationParser.FeatureActivationContext):
        feature_name = ctx.declaration.text
        feature:Feature = self._scope.resolve_feature(feature_name)
        if feature == None:
            print(f"ERROR: Missing {feature_name} for activate {ctx.deactivated}")
            return None
        else:
            feature.is_activated = not ctx.deactivated
            return feature

    def visitInclude(self, ctx: ConfigurationParser.IncludeContext):
        info = ctx.importedNamespace.text.split(".")
        # visit configuration table
        confVisitor = ConfigurationCPVisitor(info[0] + "_ConfVisit")
        with open(os.path.join(self.cwd, info[0] + ".oconf")) as conf_file:
            data = conf_file.read()
            input_stream = InputStream(data)
            lexer = ConfigurationLexer(input_stream)
            stream = CommonTokenStream(lexer)
            dcl_parsed = ConfigurationParser(stream).configurationModel()
            confVisitor.visit(dcl_parsed)
            table = confVisitor._symbol_table
        scope = None
        # go through all symbols
        for i in range(1, len(info)):
            scope = table.get_all_nested_symbols_sync(info[i])[0]
        self._model.addSymbol(scope)

    def stringToPrefix(self, input: str):
        for prefix in UnitPrefix:
            if vars(prefix)["_name_"].lower() == input.lower():
                return prefix
        return UnitPrefix.NoP

    def withScope(self, t: type, tree: ParseTree, name: str, action: Callable) -> T:
        """
        Add a scoped symbol to the symboltable and recursively add all symbols inside this scope the symboltable
        :param t: Symbol type
        :param tree: Context of the scoped symbol
        :param name: Symbol name
        :param action: Lambda function to add children symbols to symboltable
        :return: Current scope
        """
        scope = self._model.get_all_nested_symbols_sync(name)
        if len(scope) < 1:
            print("Symbol with name " + str(name) + " could not be found")
            return
        elif len(scope) > 1:
            for elem in scope:
                if isinstance(elem, t):
                    scope = elem
                    break
        else:
            scope = scope[0]
        if type == Feature:
            scope.is_activated = True
        scope.configuration.append(tree)
        current_scope = self._scope
        self._scope = scope
        try:
            return action()
        finally:
            if self._scope:
                self._scope = current_scope
            else:
                print("scope not set")
