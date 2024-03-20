"""This visitor collects variables and nodes in a SymbolTable."""

__author__ = "stu90642"

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

# user relative imports
from ..symboltable.symbol_table import SymbolTable, P, T, VariableSymbol, SymbolTableOptions
from ..gen.python.BgcDsl.BgcDslParser import BgcDslParser
from ..gen.python.BgcDsl.BgcDslVisitor import BgcDslVisitor


class SymbolTableVisitor(BgcDslVisitor, Generic[T]):
    _symbolTable: SymbolTable

    def __init__(self, name: str = '', ):
        super().__init__()
        self._symbolTable = SymbolTable(name, SymbolTableOptions(False))
        # TODO scope marker
        # self._scope = self._symbolTable.addNewSymbolOfType( ScopedSymbol, None )
        self._scope = None

    @property
    def symbolTable(self) -> SymbolTable:
        return self._symbolTable

    def defaultResult(self) -> SymbolTable:
        return self._symbolTable

    # Visit a parse tree produced by BgcDslParser#substanceDeclaration.
    def visitSubstanceDeclaration(self, ctx: BgcDslParser.SubstanceDeclarationContext):
        # TODO
        # save type
        # save unit as node
        self._symbolTable.addNewSymbolOfType(VariableSymbol, self._scope, ctx.name.text, ctx)
        return self.visitChildren(ctx)

    def visitParameterDeclaration(self, ctx: BgcDslParser.ParameterDeclarationContext):
        # TODO
        # save type
        # save unit, expression as node
        self._symbolTable.addNewSymbolOfType(VariableSymbol, self._scope, ctx.name.text, ctx)
        return self.visitChildren(ctx)

    def visitEnvironmentVariableDeclaration(self, ctx: BgcDslParser.EnvironmentVariableDeclarationContext):
        # TODO
        # save type
        # save unit, expression as node
        self._symbolTable.addNewSymbolOfType(VariableSymbol, self._scope, ctx.name.text, ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by BgcDslParser#compartment.
    def visitCompartment(self, ctx: BgcDslParser.CompartmentContext):
        # TODO
        # save node as expression
        self._symbolTable.addNewSymbolOfType(VariableSymbol, self._scope, ctx.name.text, ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by BgcDslParser#connection.
    def visitConnection(self, ctx: BgcDslParser.ConnectionContext):
        # TODO
        # save name
        # save node as expression
        # the name needs to be more complex, here:
        name = ctx.name.text + ' from ' + ctx.sourceCompartment.text + ' to ' + ctx.targetCompartment.text
        self._symbolTable.addNewSymbolOfType(VariableSymbol, self._scope, name, ctx)
        return self.visitChildren(ctx)

    # def visitFuncExpr(self, ctx: TestGrammarParser.FuncExprContext):
    #     return self.withScope( ctx, RoutineSymbol, lambda: self.visitChildren( ctx ), ctx.ID().getText() )

    def withScope(self, tree: ParseTree, t: type, action: Callable, *my_args: P.args or None, **my_kwargs: P.kwargs or None) -> T:
        """
        Add a scoped symbol to the symboltable and recursively add all symbols inside this scope the symboltable
        :param tree: Context of the scoped symbol
        :param t: Symbol type
        :param action: Lambda function to add children symbols to symboltable
        :param my_args: Arguments of symbol type
        :param my_kwargs: named Arguments of symbol type
        :return: Current scope
        """
        # Add scoped symbol to symboltable
        scope = self._symbol_table.add_new_symbol_of_type(t, self._scope, *my_args, **my_kwargs)
        scope.context = tree
        # Update Scope to the new symbol and save the old scope (mihgt be changed if scope is inserted above current scope)
        current_scope = self._scope
        self._scope = scope
        try:
            return action()
        finally:
            self._scope = current_scope
