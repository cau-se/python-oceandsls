"""SymbolTableVisitor module."""

__author__ = "sgu"

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

import os
import logging
import shutil
# Util imports
from typing import Callable, Generic, List

# Antlr4
from antlr4.tree.Tree import ParseTree

# User relative imports
from ..fxca.util.fxtran_utils import filter_xml, get_files, write_decorate_src_xml
from ..gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from ..gen.python.TestSuite.TestSuiteVisitor import TestSuiteVisitor
from ..symboltable.symbol_table import FunctionSymbol, ModuleSymbol, ParameterSymbol, RoutineSymbol, ScopedSymbol, SymbolTable, SymbolTableOptions, \
    TestCaseSymbol, VariableSymbol, P, T, get_fundamental_type

# Debug Log
logger = logging.getLogger(__name__)

class SymbolTableVisitor(TestSuiteVisitor, Generic[T]):
    _symbol_table: SymbolTable
    _test_path: str

    def __init__(self, name: str = "", test_work_path: str = "tdd-dsl/output", fxtran_path: str = "fxtran"):
        super().__init__()
        self.fxtran_path = fxtran_path
        self._symbol_table = SymbolTable(name, SymbolTableOptions(False))
        self._scope = None
        self._test_work_path = test_work_path
        self._test_path = ""

    @property
    def symbol_table(self) -> SymbolTable:
        return self._symbol_table

    @property
    def work_path(self) -> str:
        return self._test_work_path

    # Visit a parse tree produced by TestSuiteParser#test_suite.
    def visitTest_suite(self, ctx: TestSuiteParser.Test_suiteContext):
        self.visitChildren(ctx)
        return self.symbol_table

    # Visit a parse tree produced by TestSuiteParser#test_case.
    def visitTest_case(self, ctx: TestSuiteParser.Test_caseContext):
        # Extract symbols from path, scope and variables
        return self.with_scope(ctx, TestCaseSymbol, lambda: self.visitChildren(ctx), ctx.ID().getText())

    # Visit a parse tree produced by TestSuiteParser#test_var.
    def visitTest_var(self, ctx: TestSuiteParser.Test_varContext):
        decl = self.visit(ctx.varDeclaration())
        return self._symbol_table.add_new_symbol_of_type(VariableSymbol, self._scope, decl[0], ctx.value, decl[1], decl[2])

    # Visit a parse tree produced by TestSuiteParser#varDeclaration.
    def visitVarDeclaration(self, ctx: TestSuiteParser.VarDeclarationContext):
        name = ctx.name.text
        # Map variable type to symboltable type
        var_type = get_fundamental_type(self.visit(ctx.type_)) if ctx.type_ else None
        keys = []
        for key in ctx.keys:
            keys.append(key.keyword.text)
        return name, var_type, keys

    # Visit a parse tree produced by TestSuiteParser#mulDivExpr.
    def visitMulDivExpr(self, ctx: TestSuiteParser.MulDivExprContext):
        # Concatenate operators with op
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        ops: List[str] = [left, right]

        return ctx.op.text.join(ops)

    # Visit a parse tree produced by TestSuiteParser#addSubExpr.
    def visitAddSubExpr(self, ctx: TestSuiteParser.AddSubExprContext):
        # Concatenate operators with op
        ops: List[str] = [self.visit(ctx.left), self.visit(ctx.right)]

        return ctx.op.text.join(ops)

    # Visit a parse tree produced by TestSuiteParser#signExpr.
    def visitSignExpr(self, ctx: TestSuiteParser.SignExprContext):
        # Return inner type
        return self.visit(ctx.inner)

    # Visit a parse tree produced by TestSuiteParser#numberExpr.
    def visitNumberExpr(self, ctx: TestSuiteParser.NumberExprContext):
        # Return user input
        return ctx.value.text

    # Visit a parse tree produced by TestSuiteParser#strExpr.
    def visitStrExpr(self, ctx: TestSuiteParser.StrExprContext):
        # Return user input
        return ctx.value.text

    # Visit a parse tree produced by TestSuiteParser#intExpr.
    def visitIntExpr(self, ctx: TestSuiteParser.IntExprContext):
        # Return user input
        return ctx.value.text

    # Visit a parse tree produced by TestSuiteParser#refExpr.
    def visitRefExpr(self, ctx: TestSuiteParser.RefExprContext):
        # Forward reference type
        return self.visit(ctx.value)

    # Visit a parse tree produced by TestSuiteParser#ref.
    def visitRef(self, ctx: TestSuiteParser.RefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TestSuiteParser#funRef.
    def visitFunRef(self, ctx: TestSuiteParser.FunRefContext):
        name = ctx.ID().getText()
        args = []
        for arg in ctx.args:
            args.append(self.visit(arg))
        return name + "(" + ", ".join(args) + ")"

    # Visit a parse tree produced by TestSuiteParser#varRef.
    def visitVarRef(self, ctx: TestSuiteParser.VarRefContext):
        name = ctx.ID().getText()
        return name

    # Visit a parse tree produced by TestSuiteParser#enm.
    def visitEnm(self, ctx: TestSuiteParser.EnmContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TestSuiteParser#enumType.
    def visitEnumType(self, ctx: TestSuiteParser.EnumTypeContext):
        enums: List[str] = []
        for enum in ctx.values:
            if isinstance(enum, str):
                enums.append(self.visit(enum))
        return "(" + ", ".join(enums) + ")"

    # Visit a parse tree produced by TestSuiteParser#enum.
    def visitEnum(self, ctx: TestSuiteParser.EnumContext):
        name: str = self.visit(ctx.name)
        if ctx.value:
            value = ctx.value.text
            return name + "=" + value
        else:
            return name

    # Visit a parse tree produced by TestSuiteParser#array.
    def visitArray(self, ctx: TestSuiteParser.ArrayContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by TestSuiteParser#arrayType.
    def visitArrayType(self, ctx: TestSuiteParser.ArrayTypeContext):
        ar_type: str = self.visit(ctx.type_)
        dims: List[str] = []
        for dim in ctx.dimensions:
            dims.append(self.visit(dim))
        return ar_type + "[" + ", ".join(dims) + "]"

    # Visit a parse tree produced by TestSuiteParser#sizeDim.
    def visitSizeDim(self, ctx: TestSuiteParser.SizeDimContext):
        return ctx.size

    # Visit a parse tree produced by TestSuiteParser#rangeDim.
    def visitRangeDim(self, ctx: TestSuiteParser.RangeDimContext):
        return ctx.lowerBound + ":" + ctx.upperBound

    # Save the source path to scan for existing variables
    def visitSrc_path(self, ctx: TestSuiteParser.Src_pathContext):
        # Strip string terminals
        user_path: str = ctx.path.text.strip("\'")

        # TODO document
        # Update source directory
        # If the given path is an absolute path, then self._testPath is ignored and the joining is only the given path
        self._test_path: str = os.path.join(self._test_work_path, user_path)

    # Get rendered list of used modules
    def visitUse_modules(self, ctx: TestSuiteParser.Use_modulesContext):

        # Add module symbols to symboltable for XML scope filter
        module_symbols: List[ModuleSymbol] = []
        for module in ctx.modules:
            module_symbols.append(self.visit(module))

        xml_path = os.path.join(self._test_path, "tmp")
        # Write XML files
        write_decorate_src_xml(self._test_path, xml_path, fxtran_path=self.fxtran_path)

        # Get Fortran files
        xml_files = get_files(xml_path, "*.[fF]90.xml")

        for path, filename in xml_files:
            xml_elements = filter_xml(os.path.join(path, filename), True, module_symbols)

            # Add scopes
            for scope_type, scope_name, scope_args, return_type, parent_scopes, is_generated in xml_elements[1]:

                # Top level symbols are omitted as only filtered modules are in the current test case
                # Resolve scope
                parent_scopes: List[str] = parent_scopes.split(".") if parent_scopes else []
                scope_sym: ScopedSymbol = self._scope
                for scope in parent_scopes:
                    scope_sym = scope_sym.resolve_sync(scope)

                match scope_type:
                    case "module":
                        # Insert module with current scope name
                        self._symbol_table.add_new_symbol_of_type(ModuleSymbol, scope_sym, scope_name, None, self._scope)
                    case "subroutine":
                        current_scope = self._scope
                        self._scope = scope_sym
                        # Insert Subroutine symbol with current scope name
                        self.with_scope(None, RoutineSymbol, lambda: list(map(lambda arg: self.addRoutineParams(arg), scope_args)), scope_name)
                        self._scope = current_scope
                    case "function":
                        current_scope = self._scope
                        # Map type to symboltable
                        return_type = get_fundamental_type(return_type)
                        self._scope = scope_sym
                        # Insert Function symbol with scope name, parameters and return type
                        self.with_scope(None, FunctionSymbol, lambda: list(
                            map(lambda arg: self.addRoutineParams(arg), scope_args)), scope_name, return_type, is_generated)
                        self._scope = current_scope
                    case _:
                        continue

            # Add variables
            for variable_name, variable_type, variableScope in xml_elements[0]:
                # Get scope from symboltable
                variableScope: List[str] = variableScope.split(".")
                scope_sym = self._scope
                for scope in variableScope:
                    scope_sym = scope_sym.resolve_sync(scope)

                # Map type to symboltable
                variable_type = get_fundamental_type(variable_type)

                # Add the variable to the symboltable
                self._symbol_table.add_new_symbol_of_type(VariableSymbol, scope_sym, variable_name, None, variable_type)
        try:
            # Remove temporary xml files
            shutil.rmtree(xml_path)
        except OSError as e:
            logger.error("Error deleting temporary xml directory : %s - %s." % (e.filename, e.strerror))

    # Visit a parse tree produced by TestSuiteParser#test_module.
    def visitTest_module(self, ctx: TestSuiteParser.Test_moduleContext):
        # Add module to symboltable and return module symbol to included modules of testcase
        return self.with_scope(ctx, ModuleSymbol, lambda: self._scope, ctx.name.text, None, self._scope)

    def addRoutineParams(self, paramName: str = None):
        self._symbol_table.add_new_symbol_of_type(ParameterSymbol, self._scope, paramName)

    def with_scope(self, tree: ParseTree, t: type, action: Callable, *my_args: P.args or None, **my_kwargs: P.kwargs or None) -> T:
        """
        Add a scoped symbol to the symboltable and recursively add all symbols inside this scope the symboltable
        :param tree: Context of the scoped symbol
        :param sibling: Add scoped symbol as sibling of current scope
        :param t: Symbol type
        :param action: Lambda function to add children symbols to symboltable
        :param my_args: Arguments of symbol type
        :param my_kwargs: k_arguments of symbol type
        :return: Current scope
        """
        # Add scoped symbol to symboltable
        scope = self._symbol_table.add_new_symbol_of_type(t, self._scope, *my_args, **my_kwargs)
        scope.context = tree
        # Update Scope to the new symbol and save the old scope (mihgt be changed if scope is inserted above current scope)
        current_scope = self._scope
        self._scope = scope
        try:
            # Add children symbols inside this scope
            return action()
        finally:
            # Restore to scope of newly added scoped symbol
            self._scope = current_scope
