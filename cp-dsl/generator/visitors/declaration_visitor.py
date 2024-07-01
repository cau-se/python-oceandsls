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
from typing import Generic, Callable, Dict

# antlr4
from antlr4.tree.Tree import ParseTree
from antlr4.Token import CommonToken

# user relative imports
from model.symbol_table import DeclarationModel, Scope
from model.symbols import T, P
from model.model import GroupSymbol, FeatureSymbol, ParameterSymbol, \
    ArraySymbol, EKind, FeatureGroup
from model.type_system import EnumType, RangeType, ArrayType, Dimension
from model.units import FundamentalUnit, UnitPrefix, UnitKind, ComposedUnit, UnitSpecification
from common.logger import GeneratorLogger

from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser
from dcllspserver.gen.python.Declaration.DeclarationVisitor import DeclarationVisitor

# NOTE: Method names starting with visit are required to look like this, as parts of the grammar
# are named in that way

class GeneratorDeclarationVisitor(DeclarationVisitor, Generic[T]):

    _symbol_table: DeclarationModel

    def __init__(self, symbol_table:DeclarationModel, logger:GeneratorLogger):
        super().__init__()
        # creates a new symboltable with no duplicate symbols
        self._symbol_table = symbol_table
        # TODO scope marker
        # self._scope = self._symbol_table.add_new_symbol_of_type( ScopedSymbol, None )
        self._scope = self._symbol_table
        self.inline_int = 0
        self._logger = logger

    @property
    def symbol_table(self) -> DeclarationModel:
        return self._symbol_table

    def visitParamGroupAssignStat(self, ctx: DeclarationParser.ParamGroupAssignStatContext):
        parent_scope = self._scope
        name = ctx.name.text if ctx.name else "<ERROR>"
        description = ctx.description.text if ctx.description else ""

        try:
            group = self._scope._groups[name]
            self._scope = group
        except KeyError:
            group = GroupSymbol(name, description, self._scope)
            self._scope._groups[name] = group
            self._scope = group

        for d in ctx.parameterDeclarations:
            p = self.visitParamAssignStat(d)
            group.parameters[p.name] = p

        self._scope = parent_scope
        return group

    # Visit a parse tree produced by DeclarationParser#paramAssignStat.
    # 'def' name=ID type=paramType ':' unit=unitSpecification (',' description=STRING)? ('=' defaultValue=arithmeticExpression)?
    def visitParamAssignStat(self, ctx: DeclarationParser.ParamAssignStatContext):
        # define the given Parameter
        var_name = ctx.name.text if ctx.name else ""  # set and get the variable name here
        var_type = self.visit(ctx.type_)
        description = ctx.description.text if ctx.description else ""
        unit = self.visit(ctx.unit)

        parameter: ParameterSymbol = self._scope.resolve_symbol(var_name)
        if parameter is None:
            parameter = ParameterSymbol(var_name, description, None, unit, None)
            return parameter
        else:
            self._logger.error(f"Parameter redefined {var_name}")
            return None

    def visitParamType(self, ctx:DeclarationParser.ParamTypeContext):
        if (ctx.typeReference() is not None):
            return self.visitTypeReference(ctx.typeReference())
        if (ctx.arrayType() is not None):
            print(f"ARRAY {type(ctx.arrayType())}")
            return None

        return None

    def visitArrayType(self, ctx:DeclarationParser.ArrayTypeContext):
        base_type = self.resolve_type(self._scope, ctx.type_.getText())
        dimensions=[]
        for dimension in ctx.dimensions:
            dimensions.append(self.visit(dimension))
        return ArrayType(base_type, dimensions)

    def visitSizeDimension(self, ctx: DeclarationParser.SizeDimensionContext):
        return Dimension(0,ctx.size-1)

    def visitRangeDimension(self, ctx: DeclarationParser.RangeDimensionContext):
        return Dimension(ctx.lowerBound, ctx.upperBound)

    def visitTypeReference(self, ctx: DeclarationParser.TypeReferenceContext):
        return self.resolve_type(self._scope, ctx.getText())

    def visitFeatureAssignStat(self, ctx: DeclarationParser.FeatureAssignStatContext):
        name = ctx.name.text

        feature = self._scope._features.get(name, None)
        if feature is None:
            description = ctx.description.text
            print(f"FEATURE {name} {description}")
            feature = FeatureSymbol(name, description, self._scope)
            parent_scope = self._scope
            self._scope = feature
            contents = self.visitChildren(ctx)
            if contents is not None:
                for element in contents:
                    print(f"content {type(element)}")
            self._scope = parent_scope
            return feature
        else:
            print(f"Feature redefinition is illegal - should be allowed in relaxed mode")

    def visitFeatureGroupAssignStat(self, ctx: DeclarationParser.FeatureGroupAssignStatContext):
        mode = self.visitEKind(ctx.kind)
        print(f"FEATURE GROUP {mode}")
        group = FeatureGroup(mode, self._scope)
        parent_scope = self._scope
        self._scope = group
        self.visitChildren(ctx)
        self._scope = parent_scope

        return group

    def visitEKind(self, ctx: DeclarationParser.EKindContext):
        if ctx.multiple is not None:
            return EKind.MULTIPLE
        elif ctx.alternative is not None:
            return EKind.ALTERNATIVE
        else:
            print("ERROR")
            return None

    #
    # old code
    #

    def visitRangeType(self, ctx: DeclarationParser.RangeTypeContext):
        range_name = ctx.name.text
        old_symbol = self._scope.resolve_type(range_name)
        if old_symbol:
            old_symbol.minimum = ctx.minimum if ctx.minimum else old_symbol.minimum
            old_symbol.maximum = ctx.maximum if ctx.maximum else old_symbol.maximum
        self._scope.add_new_type(RangeType(range_name, type(ctx.type_), ctx.minimum, ctx.maximum))

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

    def find_next_enum_number(self, enumerals:Dict[str,int]) -> int:
        index = -1
        for key in enumerals.keys():
            if index < enumerals[key]:
                index = enumerals[key]
        return index + 1

    def check_enumeral_name(self, enum_item, enumerals:Dict[str,int]) -> bool:
        return enumerals.get(enum_item[0], None) != None

    def visitEnumerationType(self, ctx: DeclarationParser.EnumerationTypeContext):
        if ctx.name == None:
            self._logger.error(ctx,f"Enumeration type has no type name")
        else:
            enum_name = ctx.name.text
            enum_type = self._scope.resolve_type(enum_name)
            # create a new type if no old one exists
            if enum_type == None:
                enum_type = EnumType(enum_name)
                self._scope.add_new_type(enum_type)

            for i in ctx.enumeral():
                # enum_list representation: [(id, value),...]
                enum_item = self.visitEnumeral(i)
                if enum_item[1] == -1:
                    enum_item = (enum_item[0], self.find_next_enum_number(enum_type.enums))
                if self.check_enumeral_name(enum_item, enum_type.enums):
                    self._logger.strict(ctx, f"Enumeral {enum_item[0]} already exists in enumeration {enum_name}")
                else:
                    enum_type.enums[enum_item[0]] = enum_item[1]

    def visitEnumeral(self, ctx: DeclarationParser.EnumeralContext):
        if ctx.value:
            # return a tuple of id and value
            return (ctx.name.text, int(ctx.value.text))
        else:
            return (ctx.name.text, -1)

    def visitInlineEnumerationType(self, ctx: DeclarationParser.InlineEnumerationTypeContext):
        enumName = ""
        enumList = []
        self._enum_index = 0
        for i in ctx.enumeral():
            # enumList representation: [(id, value),...]
            enumList.append(self.visitEnumeral(i))
            self._enum_index += 1
        oldSymbol = self._scope.resolve_sync(enumName)
        if oldSymbol:
            enumName = "inline_" + str(self.inlineInt)
            self.inlineInt += 1
        symbol = self._symbol_table.add_new_symbol_of_type(EnumType, self._scope, enumName, enumList)
        symbol.context = ctx
        return symbol

    # Find model elements that contain types, i.e., the root element
    def resolve_type(self, node:Scope, type_name:str):
        print (f"NODE {node}")
        if node is None:
            print(f"No parent, cannot resolve type {type_name}")
            return None
        elif isinstance(node, DeclarationModel):
            return node.resolve_type(type_name)
        else:
            return self.resolve_type(node.parent, type_name)
