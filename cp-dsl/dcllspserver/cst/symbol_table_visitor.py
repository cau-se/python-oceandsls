"""SymbolTableVisitor module."""

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

# util imports
from typing import Generic, Callable

# antlr4
from antlr4.tree.Tree import ParseTree
from antlr4.Token import CommonToken

# user relative imports
from model.symbol_table import DeclarationModel, P, T, DuplicateSymbolError
from model.declaration_model import GroupSymbol, FeatureSymbol, ParameterSymbol, \
    EnumSymbol, ArraySymbol, RangeSymbol
from model.unit_model import FundamentalUnit, UnitPrefix, UnitKind, ComposedUnit, UnitSpecification

from ..gen.python.Declaration.DeclarationParser import DeclarationParser
from ..gen.python.Declaration.DeclarationVisitor import DeclarationVisitor

# NOTE: Method names starting with visit are required to look like this, as parts of the grammar
# are named in that way


class DeclarationCPVisitor(DeclarationVisitor, Generic[T]):

    _symbol_table: DeclarationModel

    def __init__(self, symbol_table: DeclarationModel):
        super().__init__()
        # creates a new symboltable with no duplicate symbols
        self._symbol_table = symbol_table
        # TODO scope marker
        # self._scope = self._symbol_table.add_new_symbol_of_type( ScopedSymbol, None )
        self._scope = self._symbol_table
        self.inlineInt = 0
        self._enumIndex = 0

    @property
    def symbol_table(self) -> DeclarationModel:
        return self._symbol_table

    def default_result(self) -> DeclarationModel:
        return self._symbol_table

    # Visit a parse tree produced by DeclarationParser#paramAssignStat.
    # 'def' name=ID type=paramType ':' unit=unitSpecification (',' description=STRING)? ('=' defaultValue=arithmeticExpression)?
    def visitParamAssignStat(self, ctx: DeclarationParser.ParamAssignStatContext):

        # define the given Parameter
        varName = ctx.name.text if ctx.name else ""  # set and get the variable name here
        oldSymbol: ParameterSymbol = self._scope.resolve_sync(varName)
        unit = self.visit(ctx.unit)
        varType = self._scope.resolve_sync(ctx.type_.getText())
        varType = varType if varType else self.visit(ctx.type_)
        description = ctx.description.text if ctx.description else ""
        # if it is a Array, it was already created, so no need for a variable Symbol
        # if the varName already exists in scope, just overwrite it
        if isinstance(varType, ArraySymbol):
            if oldSymbol is None:
                varType.name = ctx.name.text
                varType.unit = unit
                varType.context = ctx
                varType.description = description
                return varType
            else:
                self._scope.removeSymbol(varType)
        if oldSymbol is not None:
            oldSymbol.unit = unit if unit else oldSymbol.unit
            oldSymbol.type = varType if varType else oldSymbol.type
            oldSymbol.description = description if description else oldSymbol.description
            if not oldSymbol.context.defaultValue:
                oldSymbol.context = ctx
            if ctx.defaultValue and oldSymbol.context.defaultValue:
                print("ERROR: cannot merge", varName, "values")
            symbol = oldSymbol
        else:
            symbol = self._symbol_table.add_new_symbol_of_type(ParameterSymbol, self._scope, varName, description, ctx, unit, varType)
            symbol.context = ctx
        return symbol

    def stringToPrefix(self, input: str):
        for prefix in UnitPrefix:
            if vars(prefix)["_name_"].lower() == input.lower():
                return prefix
        return UnitPrefix.NoP

    def stringToUnitType(self, input: str):
        for kind in UnitKind:
            if vars(kind)["_name_"].lower() == input.lower():
                return kind
        return UnitKind.Unknown

    # sIUnit                      :   (prefix=ePrefix)? type=eSIUnitType #siUnit;
    def visitSiunit(self, ctx: DeclarationParser.SIUnitContext):
        return FundamentalUnit(name=ctx.type_.getText() if ctx.type_ else "",
                               unit_prefix=self.stringToPrefix(ctx.prefix.getText() if ctx.prefix else ""),
                               unit_kind=self.stringToUnitType(ctx.type_.getText() if ctx.type_ else ""))

    # customUnit                  :   name=STRING #customunit;
    def visitCustomunit(self, ctx: DeclarationParser.CustomUnitContext):
        # TODO: Set Prefix and type in customUnit either
        return FundamentalUnit(name=ctx.name.text if ctx.name.text else "")

    def visitBasicUnit(self, ctx: DeclarationParser.BasicUnitContext):
        if isinstance(ctx, CommonToken):
            return float(ctx.text)
        if ctx.sIUnit():
            return self.visit(ctx.sIUnit())
        if ctx.customUnit():
            return self.visit(ctx.customUnit())
        if ctx.unitSpecification():
            return self.visit(ctx.unitSpecification())

    def visitUnitSpecification(self, ctx: DeclarationParser.UnitSpecificationContext):
        retVal = UnitSpecification()
        for elem in ctx.units:
            retVal.add(self.visit(elem))
        return retVal

    def visitComposedUnit(self, ctx: DeclarationParser.ComposedUnitContext):
        if ctx.denominator:
            return ComposedUnit(numerator=self.visitBasicUnit(ctx.numerator), denominator=self.visitBasicUnit(ctx.denominator))
        if ctx.exponent:
            return ComposedUnit(numerator=self.visitBasicUnit(ctx.numerator), exponent=self.visitBasicUnit(ctx.exponent))
        return ComposedUnit(basicUnit=self.visitChildren(ctx))

    def visitParamGroupAssignStat(self, ctx: DeclarationParser.ParamGroupAssignStatContext):
        description = ctx.description.text if ctx.description else ""
        return self.withScope(ctx, GroupSymbol, lambda: self.visitChildren(ctx), ctx.name.text if ctx.name else "", ParameterSymbol, description)

    # CHANGES sgu:
    #   featureDeclaration ID is saved as attribute 'name'

    def visitFeatureAssignStat(self, ctx: DeclarationParser.FeatureAssignStatContext):
        return self.withScope(ctx, FeatureSymbol, lambda: self.visitChildren(ctx), ctx.name.text, ctx.description.text)

    def visitFeatureGroupAssignStat(self, ctx: DeclarationParser.FeatureGroupAssignStatContext):
        return self.withScope(ctx, GroupSymbol, lambda: self.visitChildren(ctx), "", FeatureSymbol, "")

    def visitEnumerationType(self, ctx: DeclarationParser.EnumerationTypeContext):
        enum_name = ctx.name.text if ctx.name else ""
        enum_list = []
        self._enumIndex = 0
        for i in ctx.enumeral():
            # enum_list representation: [(id, value),...]
            enum_list.append(self.visitEnumeral(i))
            self._enumIndex += 1
        oldSymbol = self._scope.resolve_sync(enum_name)
        if oldSymbol:
            oldSymbol.enums += enum_list
        else:
            symbol = self._symbol_table.add_new_symbol_of_type(EnumSymbol, self._scope, enum_name, enum_list)
            symbol.context = ctx

    def visitEnumeral(self, ctx: DeclarationParser.EnumeralContext):
        if ctx.value:
            # return a tuple of id and value
            return (ctx.name.text, int(ctx.value.text))
        else:
            return (ctx.name.text, self._enumIndex)

    def visitInlineEnumerationType(self, ctx: DeclarationParser.InlineEnumerationTypeContext):
        enumName = ""
        enumList = []
        self._enumIndex = 0
        for i in ctx.enumeral():
            # enumList representation: [(id, value),...]
            enumList.append(self.visitEnumeral(i))
            self._enumIndex += 1
        oldSymbol = self._scope.resolve_sync(enumName)
        if oldSymbol:
            enumName = "inline_" + str(self.inlineInt)
            self.inlineInt += 1
        symbol = self._symbol_table.add_new_symbol_of_type(EnumSymbol, self._scope, enumName, enumList)
        symbol.context = ctx
        return symbol

    def visitTypeReference(self, ctx: DeclarationParser.TypeReferenceContext):
        return ctx.type_.text

    def visitArrayType(self, ctx: DeclarationParser.ArrayTypeContext):
        bounds = []
        for i in ctx.dimensions:
            bounds.append(self.visit(i))
        symbol = self._symbol_table.add_new_symbol_of_type(ArraySymbol, self._scope, "array_temp", bounds[0][1], bounds[0][0])
        # context will be set in visitparameterassignement
        # symbol.context = ctx
        symbol.type = self._scope.resolve_sync(ctx.type_.text)
        return symbol

    def visitSizeDimension(self, ctx: DeclarationParser.SizeDimensionContext):
        return (0, int(ctx.size.text) if ctx.size else 0)

    def visitRangeDimension(self, ctx: DeclarationParser.RangeDimensionContext):
        return ((int(ctx.lowerBound.text) if ctx.lowerBound else 0), (int(ctx.upperBound.text) if ctx.upperBound else 0))

    def visitRangeType(self, ctx: DeclarationParser.RangeTypeContext):
        rangeName = ctx.name.text
        oldSymbol = self._scope.resolve_sync(rangeName)
        if oldSymbol:
            oldSymbol.minimum = ctx.minimum if ctx.minimum else oldSymbol.minimum
            oldSymbol.maximum = ctx.maximum if ctx.maximum else oldSymbol.maximum
        symbol = self._symbol_table.add_new_symbol_of_type(RangeSymbol, self._scope, rangeName, type(ctx.type_), ctx.minimum, ctx.maximum)
        symbol.context = ctx

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
        try:
            scope = self._symbol_table.add_new_symbol_of_type(t, self._scope, *my_args, **my_kwargs)
        except DuplicateSymbolError:
            print("WARNING: Duplicate declaration of var:", my_args[0], "Proceed with merging")
            scope = self._scope.resolve_sync(my_args[0])
            if isinstance(scope, FeatureSymbol):
                scope.description = my_args[1]
            else:
                scope.description = my_args[2]
        scope.context = tree
        # next line is not present in confdsl
        current_scope = self._scope
        self._scope = scope
        try:
            return action()
        finally:
            self._scope = current_scope
            # Alternative ending used in conf DSL
            # self._scope = scope.parent()
