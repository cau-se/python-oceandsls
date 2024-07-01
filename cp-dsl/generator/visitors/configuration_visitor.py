"""SymbolTableVisitor module."""

__author__ = "reiner"

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

# util imports
from typing import Generic, Callable

# antlr4
from antlr4.tree.Tree import ParseTree
from antlr4 import InputStream, CommonTokenStream

# user relative imports
from model.symbols import T
from model.symbol_table import DeclarationModel
from model.model import GroupSymbol, FeatureSymbol
from model.units import UnitPrefix

from conflspserver.gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser
from conflspserver.gen.python.Configuration.ConfigurationVisitor import ConfigurationVisitor

import os

class GeneratorConfigurationVisitor(ConfigurationVisitor, Generic[T]):
    _symbol_table: DeclarationModel

    _generator_selector: str

    def __init__(self, symbol_table:DeclarationModel, cwd: str = "."):
        super().__init__()
        # creates a new symboltable with no duplicate symbols
        self._symbol_table = symbol_table
        # TODO scope marker
        # self._scope = self._symbol_table.addNewSymbolOfType( ScopedSymbol, None )
        self._scope = self._symbol_table
        self.cwd = cwd
        self.configuration_list = []

    @property
    def symbol_table(self) -> DeclarationModel:
        return self._symbol_table

    @property
    def generator_selector(self) -> str:
        return self._generator_selector

    def default_result(self) -> DeclarationModel:
        return self._symbol_table

    def visitConfigurationModel(self, ctx: ConfigurationParser.ConfigurationModelContext):
        return super().visitConfigurationModel(ctx)

    def visitParameterAssignment(self, ctx: ConfigurationParser.ParameterAssignmentContext):
        # define the given Parameter
        var_name = ctx.declaration.getText()  # set and get the variable name here
        prefix = self.visit(ctx.unit) if ctx.unit is not None else UnitPrefix.NoP
        # isArray = True if len(ctx.selectors) > 0 else False
        symbol = self._scope.get_all_nested_symbols_sync(var_name)[0]
        if prefix != UnitPrefix.NoP:
            symbol.unit.prefix = prefix
        symbol.configuration.append(ctx)
        self.configuration_list.append((symbol, len(symbol.configuration) - 1))

    def visitParameterGroup(self, ctx: ConfigurationParser.ParameterGroupContext):
        self.withScope(GroupSymbol, ctx, ctx.declaration.text, lambda: self.visitChildren(ctx))

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
        self.withScope(FeatureSymbol, ctx, ctx.declaration.text, lambda: self.visitChildren(ctx))

    def visitFeatureActivation(self, ctx: ConfigurationParser.FeatureActivationContext):
        for feature in self._scope.get_nested_symbols_of_type_sync(FeatureSymbol):
            if feature.name == ctx.declaration.text:
                try:
                    # if is_activated is set to false it is not none
                    feature.is_activated = True if ctx.deactivated else False
                except AttributeError:
                    print("WARNING: There was a None in Feature Configuration of " + str(feature.name))
                    pass

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
        self._symbol_table.addSymbol(scope)

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
        scope = self._symbol_table.get_all_nested_symbols_sync(name)
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
        if type == FeatureSymbol:
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
