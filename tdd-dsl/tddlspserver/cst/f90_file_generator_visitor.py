"""File generator visitor module."""

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

# Util
import os
from typing import Dict, List, Optional, Tuple

# Jinja2
from jinja2 import Environment, FileSystemLoader

from symboltable import symbol_table
# User relative imports
from ..symboltable.symbol_table import FunctionSymbol, FundamentalType, SymbolTable, ModuleSymbol, RoutineSymbol, Type, VariableSymbol
from ..filewriter.file_writer import write_file
from ..gen.python.TestSuite.TestSuiteParser import TestSuiteParser
from ..gen.python.TestSuite.TestSuiteVisitor import TestSuiteVisitor
from ..utils.suggest_variables import get_scope


class F90FileGeneratorVisitor(TestSuiteVisitor):
    file_templates: Dict[int, str]
    template_path: str
    work_path: str
    cwd: str
    test_file_predicate: str
    environment: Environment
    ops: Dict[str, List]
    last_op_id: str
    file_suffix: str
    _symbol_table: SymbolTable
    found_ref: bool
    found_par: bool

    def __init__(
            self, template_path: str = "tdd-dsl/tddlspserver/filewriter/jinjatemplates/f90", files: Dict[str, Tuple[float, str, str]] = {},
            symbol_table: SymbolTable = None, work_path: str = "tdd-dsl/output", file_suffix: str = "f90", rel_file_path=None
    ):
        """
        Fortran 90 source code file generator. Builds template file dictionary from TestSuiteParser.ruleNames.

        Write/merge pFUnit-file to :test_path:/:test_folder:/:filename:.pf

        :param rel_file_path: rel path to source file
        :param template_path: absolute filepath for jinja templates
        :param work_path: path to generate test suite
        """
        super().__init__()
        self.overwrite = False
        self.overwrite_files: List[str] = []
        self.files: dict[str, Tuple[float, str, str]] = files
        self.template_path = template_path
        self.rel_file_path = rel_file_path
        self.work_path = work_path
        self.cwd = work_path
        self.file_suffix = file_suffix
        # Load Jinja2 templates
        self.environment = Environment(loader=FileSystemLoader(template_path), trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=False)

        # Variable flags
        self.found_ref = False
        self.found_par = False

        # Set symboltable
        self._symbol_table = symbol_table

        # Get template file names from grammar
        self.file_templates = {}
        i: int = 0
        for rule in TestSuiteParser.ruleNames:
            self.file_templates[i] = f"{rule}_template.txt"
            i += 1

        # Initialize dictionary to track operations of assertions
        self.ops = {}

        self.last_op_id = None

    @property
    def symbol_table(self) -> SymbolTable:
        return self._symbol_table

    # Visit a parse tree produced by TestSuiteParser#testSuite.
    def visitTestSuite(self, ctx: TestSuiteParser.TestSuiteContext):
        self.visitChildren(ctx)
        return self.files

    # Visit a parse tree produced by TestSuiteParser#testCase.
    def visitTestCase(self, ctx: TestSuiteParser.TestCaseContext) -> dict[str, Tuple[float, str, str]]:
        # Load Jinja2 template
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])

        module_symbols = self.visit(ctx.modules) if ctx.modules else None

        # Get operations defined in variables
        if ctx.vars_:
            self.visit(ctx.vars_)

        # Get operations defined in assertions
        for assertion in ctx.assertions:
            self.visit(assertion)

        # Lookup if operation exists in symboltable
        ops_names: List[str] = []
        ops_impl: List[str] = []
        for key, value_list in self.ops.items():
            scope = get_scope(ctx, self.symbol_table)
            routine_symbols = scope.get_symbols_of_type_and_name_sync(RoutineSymbol, key, False)

            # If operations does not exist or was added before, add to newly generated ops
            if not routine_symbols or value_list[4]:
                # Add with first found implementation
                ops_names.append(key)
                ops_impl.append(value_list[-1])

        # Write content to module if module is set
        for idx, module_symbol in enumerate(module_symbols):

            # Check test flags. E.g. overwrite flag
            self.overwrite = False
            if ctx.test_flags:
                self.visit(ctx.test_flags)

            if self.overwrite:
                # Merge all files that should overwrite other files

                # Set module file
                module_name = module_symbol.name
                module_file = ".".join([module_name, self.file_suffix])
                abs_path: str = os.path.join(self.work_path, module_file)

                if abs_path in self.overwrite_files:
                    self.overwrite = False
                else:
                    self.overwrite_files.append(abs_path)

            if module_symbol.file and not self.overwrite:
                # Module exists

                insert = True
                module_file = module_symbol.file

                if ops_names or ops_impl:
                    if idx == 0:
                        # Write content only to main module and only if operations are added
                        content = {module_symbol.name: [", ".join(ops_names), "\n\n".join(ops_impl)]}
                    else:
                        content = {module_symbol.name: ["", ""]}
                else:
                    content = {}

            else:
                # Module is new
                insert = False

                # Set module file
                module_name = module_symbol.name
                module_file = ".".join([module_name, self.file_suffix])
                module_symbol.file = module_file

                # Render template with new operations
                if idx == 0:
                    content = template.render(name=module_name, opsNames=ops_names, ops=ops_impl)
                else:
                    content = template.render(name=module_name)

            # Get absolute file path
            self.visit(ctx.srcpath)
            abs_path: str = os.path.join(self.work_path, module_file)

            # Get the file attributes for previously generated files
            file_attr = self.files.get(abs_path)

            # Write content to file
            self.files[abs_path] = write_file(abs_path, content, file_attr, insert)

        # Return list of generated files
        return self.files

    # Save the source path to scan for existing variables
    def visitSrcPath(self, ctx: TestSuiteParser.SrcPathContext):
        # Strip string terminals
        user_path: str = ctx.path.text.strip("\'")

        # TODO document
        # Update source directory
        # If the given path is an absolute path, then self._testPath is ignored and the joining is only the given path
        self.work_path = os.path.join(self.cwd, user_path)

    # Get list of used module symbols
    def visitUseModules(self, ctx: TestSuiteParser.UseModulesContext):

        # Accumulate module names
        module_symbols: List[ModuleSymbol] = []
        for module in ctx.modules:
            module_symbols.append(self.visit(module))

        return module_symbols

    # Find corresponding module symbol
    def visitTestModule(self, ctx: TestSuiteParser.TestModuleContext):
        # Return corresponding module symbol, optionally with implementing file and contain functions flag
        return get_scope(ctx, self.symbol_table)

    # Visit a parse tree produced by TestSuiteParser#testAssertion.
    def visitTestAssertion(self, ctx: TestSuiteParser.TestAssertionContext):
        # Load operation template
        template = self.environment.get_template(self.file_templates[ctx.getRuleIndex()])

        # Extract assertion line start/end
        start_stop: str
        if ctx.start is not None and ctx.stop is not None:
            start: str = "".join([str(ctx.start.line), ":", str(ctx.start.column)])
            stop: str = "".join([str(ctx.stop.line), ":", str(ctx.stop.column)])
            start_stop = "-".join([start, stop])
        else:
            start_stop = None

        tag_source: str = ", ".join([self.rel_file_path, start_stop]) if self.rel_file_path is not None and start_stop is not None else None
        tag: str = "auto-generated, src: " + tag_source if tag_source is not None else "auto-generated, src: unknown"

        # Extract id, optional arguments and inner ops
        self.visit(ctx.input_)

        # Update return type of last new operation if no function expression was in between
        if self.last_op_id:
            last_op = self.ops.get(self.last_op_id)
            return_type: str = self.visit(ctx.output)

            # Warn if return types do not match
            if last_op[2] and return_type is not last_op[2]:
                pass
            else:
                last_op[2] = return_type
            self.ops[self.last_op_id] = last_op

        # Generate fortran implementations for operations
        for key, value_list in self.ops.items():
            # Skip already implemented operations
            if len(value_list) == 6:
                continue

            # Get name, arguments, unit and returnType
            name = key
            # Arguments
            arg_names: List[str] = []
            args_decl: List[str] = []
            for idx, arg_type in enumerate(value_list[0]):
                arg_name = f"arg{idx}"
                arg_names.append(arg_name)
                args_decl.append(f"{arg_type.name}, INTENT(IN)  :: {arg_name}")

            unit = value_list[1]
            # Add unit parameter if unit exists
            arg_names += ["unit"] if unit is not None else []

            # ReturnType
            return_type = value_list[2].name if value_list[2] is not None else None

            routine_type: str = None
            if value_list[3] is FunctionSymbol:
                routine_type = "FUNCTION"
            elif value_list[3] is RoutineSymbol:
                routine_type = "SUBROUTINE"

            # Fortran implementation
            value_list.append(
                template.render(
                    routineType=routine_type,
                    tag=tag,
                    name=name,
                    argNames=arg_names,
                    unit=unit,
                    argsDecl=args_decl,
                    returnType=return_type))
            # Update operation list
            self.ops[key] = value_list

    # Visit a parse tree produced by TestSuiteParser#testVar.
    def visitTestVar(self, ctx: TestSuiteParser.TestVarContext):
        return self.visit(ctx.value)

    # Visit a parse tree produced by TestSuiteParser#testParameter.
    def visitTestParameter(self, ctx: TestSuiteParser.TestParameterContext):
        # Get value name and optional argument types
        parameter_type = self.visit(ctx.value)

        # Unit of expression
        expr_unit: str = self.visit(ctx.comment)

        # Update input unit of last new operation if no function expression was in between
        if self.last_op_id:
            last_op = self.ops.get(self.last_op_id)
            if not last_op[1]:
                last_op[1] = expr_unit
                self.ops[self.last_op_id] = last_op

        return parameter_type

    # Visit a parse tree produced by TestSuiteParser#emptyDesc.
    def visitEmptyDesc(self, ctx: TestSuiteParser.EmptyDescContext):
        # Return no unit
        return None

    # Visit a parse tree produced by TestSuiteParser#specDesc.
    def visitSpecDesc(self, ctx: TestSuiteParser.SpecDescContext):
        # Get unit of expression
        return self.visit(ctx.type_)

    # Visit a parse tree produced by TestSuiteParser#customUnit.
    def visitCustomUnit(self, ctx: TestSuiteParser.CustomUnitContext):
        # Return custom unit
        return ctx.name.text

    # Visit a parse tree produced by TestSuiteParser#siUnit.
    def visitSiUnit(self, ctx: TestSuiteParser.SiUnitContext):
        # Return si unit
        return ctx.type_.value.text

    # Visit a parse tree produced by TestSuiteParser#funRef.
    def visitFunRef(self, ctx: TestSuiteParser.FunRefContext):
        return self.addRoutine(ctx.procedure(), FunctionSymbol)

    # Visit a parse tree produced by TestSuiteParser#prcRef.
    def visitPrcRef(self, ctx: TestSuiteParser.PrcRefContext):
        return self.addRoutine(ctx, RoutineSymbol)

    def addRoutine(self, ctx: TestSuiteParser.PrcRefContext, t: type):
        # Get routine id
        name: str = ctx.ID().getText()

        # Get routine arguments
        args: List[str] = []
        for arg in ctx.args:
            args.append(self.visit(arg))

        # Lookup if routine exists in symboltable
        scope = get_scope(ctx, self.symbol_table)
        routine_symbol = scope.get_symbols_of_type_and_name_sync(t, name, False)
        is_generated: bool
        if routine_symbol:
            is_generated = routine_symbol[0].is_generated
            if isinstance(routine_symbol[0], FunctionSymbol):
                # Operation exists return return_type
                return_type: Optional[Type] = routine_symbol[0].return_type
            else:
                # Operation is new, return_type is unknown
                return_type: Optional[Type] = None
        else:
            # Operation is new, return_type is unknown
            is_generated = True
            return_type: Optional[Type] = None

        if not name.isupper():
            # Add operation to list of ops
            self.ops[name] = self.ops.get(name, [args, None, return_type, t, is_generated])
            self.last_op_id = name
        else:
            # Uppercase written operations are ignored as general fortran operations
            self.last_op_id = None

        # Return operation return_type
        return return_type

    # Visit a parse tree produced by TestSuiteParser#varRef.
    def visitVarRef(self, ctx: TestSuiteParser.VarRefContext):
        name = ctx.ID().getText()

        # Extract most local type of reference from symboltable
        scope = get_scope(ctx, self.symbol_table)
        var = scope.get_nested_symbols_of_type_and_name_sync(VariableSymbol, name)
        varType = var[0].attached_type if var else None

        # Return variable type
        return varType

    # Visit a parse tree produced by TestSuiteParser#parensExpr.
    def visitParensExpr(self, ctx: TestSuiteParser.ParensExprContext):
        innerType = self.visit(ctx.inner)
        return innerType

    # Visit a parse tree produced by TestSuiteParser#mulDivExpr.
    def visitMulDivExpr(self, ctx: TestSuiteParser.MulDivExprContext):
        # Extract left and right operator
        left_type = self.visit(ctx.left)
        right_type = self.visit(ctx.right)

        # Determine type of expression
        match (left_type, right_type):
            case [FundamentalType.real_type, _]:
                # If any of the operands are real then result of the operation will be real
                expr_type: str = FundamentalType.real_type
            case [_, FundamentalType.real_type]:
                # If any of the operands are real then result of the operation will be real
                expr_type: str = FundamentalType.real_type
            case [FundamentalType.integer_type, FundamentalType.integer_type]:
                if ctx.op == "*":
                    # If all the operands are integer then result of the operation will be integer
                    expr_type: str = FundamentalType.integer_type
                else:
                    expr_type: str = FundamentalType.real_type
            case [None, None]:
                # If both operands are None then result of the operation will be None
                expr_type: str = None
            case _:
                # Custom types have precedence
                expr_type: str = ctx.op.text.join([str(left_type), str(left_type)])

        # Mark last added operation as not last operation
        self.last_op_id = None

        # Return determined type
        return expr_type

    # Visit a parse tree produced by TestSuiteParser#addSubExpr.
    def visitAddSubExpr(self, ctx: TestSuiteParser.AddSubExprContext):
        # Extract left and right operator
        left_type = self.visit(ctx.left)
        right_type = self.visit(ctx.right)

        # Extract types from function references
        match (left_type, right_type):
            case [FundamentalType.real_type, _]:
                # If any of the operands are real then result of the operation will be real
                expr_type: str = FundamentalType.real_type
            case [_, FundamentalType.real_type]:
                # If any of the operands are real then result of the operation will be real
                expr_type: str = FundamentalType.real_type
            case [FundamentalType.integer_type, FundamentalType.integer_type]:
                # If all the operands are integer then result of the operation will be integer
                expr_type: str = FundamentalType.integer_type
            case [None, None]:
                # If both operands are None then result of the operation will be None
                expr_type: str = None
            case _:
                # Custom types have precedence
                expr_type: str = ctx.op.text.join([str(left_type), str(left_type)])

        # Mark last added operation as not last operation
        self.last_op_id = None

        # Return determined type
        return expr_type

    # Visit a parse tree produced by TestSuiteParser#signExpr.
    def visitSignExpr(self, ctx: TestSuiteParser.SignExprContext):
        inner_type = self.visit(ctx.inner)
        return inner_type

    # Visit a parse tree produced by TestSuiteParser#numberExpr.
    def visitNumberExpr(self, ctx: TestSuiteParser.NumberExprContext):
        # Power and decimal operation will be real
        return FundamentalType.real_type

    # Visit a parse tree produced by TestSuiteParser#strExpr.
    def visitStrExpr(self, ctx: TestSuiteParser.StrExprContext):
        # Custom types will be string
        return "character(len = *)"

    # Visit a parse tree produced by TestSuiteParser#intExpr.
    def visitIntExpr(self, ctx: TestSuiteParser.IntExprContext):
        # Integer operation will be integer
        return FundamentalType.integer_type

    # Visit a parse tree produced by TestSuiteParser#refExpr.
    def visitRefExpr(self, ctx: TestSuiteParser.RefExprContext):
        # Return reference type
        return self.visit(ctx.value)

    # Visit a parse tree produced by TestSuiteParser#overwritePF.
    def visitOverwriteF90(self, ctx: TestSuiteParser.OverwritePFContext):
        self.overwrite = True
