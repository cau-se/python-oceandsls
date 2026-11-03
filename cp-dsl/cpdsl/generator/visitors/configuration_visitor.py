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
from cpdsl.model.symbols import Scope, T, P
from cpdsl.generator.visitors.expression_visitor import ExpressionVisitorMixin
from cpdsl.model.declaration_model import DeclarationModel, ParameterGroup, Feature, Parameter, SelectorExpression
from cpdsl.model.unit_model import UnitPrefix
from cpdsl.model.arithmetic_model import ArithmeticExpression, MultiplicationExpression, EMultiplicationOperator, EAdditionOperator, \
    ArrayExpression, IntValue, FloatValue, StringValue, BooleanValue
from cpdsl.model.type_system import ArrayType, EnumeralType, InlineEnumeralType, base_types
from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.unit_processing import parse_unit

from conflspserver.gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser
from conflspserver.gen.python.Configuration.ConfigurationVisitor import ConfigurationVisitor

import os

import logging
_log = logging.getLogger(__name__)  # diagnostics go to logging, never to stdout


class GeneratorConfigurationVisitor(ExpressionVisitorMixin, ConfigurationVisitor, Generic[T]):
    _parser = ConfigurationParser

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

    @property
    def generator_selector(self) -> str:
        return self._generator_selector

    def default_result(self) -> DeclarationModel:
        return self._model

    def visitConfigurationModel(self, ctx: ConfigurationParser.ConfigurationModelContext):
        model_name = ctx.declarationModel.text
        if self._model.name == model_name:
            self._model.configuration_name = ctx.name.text
            for include in ctx.includes:
                self._logger.strict(include, f"Include of {include.importedNamespace.getText()} is not supported yet")
            for activation in ctx.featureActivations:
                self.visitFeatureActivation(activation)
            for feature in ctx.featureConfigurations:
                self.visitFeatureConfiguration(feature)
            for group in ctx.parameterGroups:
                self.visitParameterGroup(group)

            return self._model
        else:
            self._logger.strict(ctx, f"Configuration refers to declaration model {model_name}, but {self._model.name} was loaded")

    def visitParameterAssignment(self, ctx: ConfigurationParser.ParameterAssignmentContext):
        # define the given Parameter
        var_name = ctx.declaration.getText()  # set and get the variable name here
        parameter:Parameter = self._scope.parameters.get(var_name)
        var_unit = None
        if ctx.unit is not None:
            unit:ConfigurationParser.UnitSpecificationContext = ctx.unit

            var_unit = parse_unit(unit.getText())

        if parameter is None:
            self._logger.strict(ctx, f"Parameter {var_name} does not exist in {self._scope.name}")
            self._type_scope = None
            return None
        else:
            self._type_scope = parameter.type
            if len(ctx.selectors) > 0:
                selectors = []
                for s in ctx.selectors:
                    selectors.append(self.visitSelector(s))

                value = self.visitArithmeticExpression(ctx.value)
                if value is None:
                    self._logger.strict(ctx, f"Invalid value for parameter {var_name}")
                    return None
                value.unit = var_unit
                selector_expression = SelectorExpression(selectors, value)
                parameter.entries.append(selector_expression)
            else:
                value = self.visitArithmeticExpression(ctx.value)
                if value is None:
                    self._logger.strict(ctx, f"Invalid value for parameter {var_name}")
                    return None
                value.unit = var_unit
                parameter.entries.append(value)

            return parameter

    def visitParameterGroup(self, ctx: ConfigurationParser.ParameterGroupContext):
        group_name = ctx.declaration.text
        group:ParameterGroup = self._scope.resolve_parameter_group(group_name)
        if group == None:
            self._logger.strict(ctx, f"Missing group {group_name}")
            return None

        parent_scope = self._scope
        self._scope = group
        try:
            for parameter_ctx in ctx.parameters:
                self.visitParameterAssignment(parameter_ctx)
        finally:
            # Restore the scope; otherwise following groups were resolved inside this group
            self._scope = parent_scope

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
        return self.stringToPrefix(ctx.getText())

    def visitFeatureConfiguration(self, ctx: ConfigurationParser.FeatureConfigurationContext):
        feature_name = ctx.declaration.text
        feature:Feature = self._scope.resolve_feature(feature_name)
        if feature == None:
            self._logger.strict(ctx, f"Missing feature {feature_name}")
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
            self._logger.strict(ctx, f"Missing feature {feature_name} to {'deactivate' if ctx.deactivated else 'activate'}")
            return None
        else:
            feature.is_activated = not ctx.deactivated
            return feature

    def visitInclude(self, ctx: ConfigurationParser.IncludeContext):
        # Work in progress (not called yet, includes are reported in visitConfigurationModel): uses the configuration
        # symbol table of the former conflspserver, so ConfigurationCPVisitor, InputStream and CommonTokenStream are
        # not defined here.
        # pylint: disable=undefined-variable
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
            _log.error("Symbol with name " + str(name) + " could not be found")
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
                _log.error("scope not set")
