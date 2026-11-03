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
from typing import Generic, Dict

# antlr4
from antlr4.Token import CommonToken
from antlr4 import ParserRuleContext, TerminalNode

# user relative imports
from cpdsl.model.symbols import Scope, T
from cpdsl.generator.visitors.expression_visitor import ExpressionVisitorMixin
from cpdsl.model.declaration_model import DeclarationModel, Parameter, ParameterGroup, Feature, FeatureGroup, EKind
from cpdsl.model.type_system import EnumeralType, InlineEnumeralType, Enumeral, RangeType, ArrayType, Dimension, base_types
from cpdsl.model.unit_model import UnitPrefix, UnitKind, UnitSpecification, SIUnit, CustomUnit, DivisionUnit, ExponentUnit
from cpdsl.common.logger import GeneratorLogger

from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser
from dcllspserver.gen.python.Declaration.DeclarationVisitor import DeclarationVisitor

import logging
_log = logging.getLogger(__name__)  # diagnostics go to logging, never to stdout

# NOTE: Method names starting with visit are required to look like this, as parts of the grammar
# are named in that way

# NOTE: DiagnosticListener bei Sven im Code ansehen

class GeneratorDeclarationVisitor(ExpressionVisitorMixin, DeclarationVisitor, Generic[T]):
    _parser = DeclarationParser


    _model: DeclarationModel

    def __init__(self, symbol_table: DeclarationModel, logger: GeneratorLogger):
        super().__init__()
        # creates a new symboltable with no duplicate symbols
        self._model = symbol_table
        # TODO scope marker
        # self._scope = self._symbol_table.add_new_symbol_of_type( ScopedSymbol, None )
        self._scope = self._model
        self._type_scope = None
        self.inline_int = 0
        self._logger = logger
        # (list to add to, feature reference context, scope of the declaring feature)
        self._pending_references = []

    def visitDeclarationModel(self, ctx: DeclarationParser.DeclarationModelContext):
        self._model.name = ctx.name.text
        for type in ctx.types:
            type_definition = self.visitDeclaredType(type)
            self._model.types[type_definition.name] = type_definition

        for group in ctx.parameterGroupDeclarations:
            group_declaration = self.visitParamGroupAssignStat(group)
            self._model.groups[group_declaration.name] = group_declaration

        for feature in ctx.featureDeclarations:
            feature_declaration = self.visitFeatureAssignStat(feature)
            if feature_declaration is not None:
                self._model.features[feature_declaration.name] = feature_declaration

        self.resolve_feature_references()
        return self._scope

    def resolve_feature_references(self):
        """Resolve requires/excludes references collected while visiting feature declarations."""
        current_scope = self._scope
        for target_list, reference_ctx, scope in self._pending_references:
            self._scope = scope
            feature = self.visitFeatureReference(reference_ctx)
            if isinstance(feature, Feature):
                target_list.append(feature)
        self._scope = current_scope
        self._pending_references = []

    def visitDeclaredType(self, ctx: DeclarationParser.DeclaredTypeContext):
        if ctx.rangeType() is not None:
            return self.visitRangeType(ctx.rangeType())
        elif ctx.enumerationType() is not None:
            return self.visitEnumerationType(ctx.enumerationType())
        else:
            self._logger.strict(ctx, f"Unsupported data type declaration.")
            return None

    def visitRangeType(self, ctx: DeclarationParser.RangeTypeContext):
        range_name = ctx.name.text
        old_symbol = self.resolve_type(self._scope, range_name)
        if old_symbol:
            self._logger.strict(ctx, "Redefining ranges")
        type = self.resolve_type(self._model, ctx.type_.text)
        if type is not None:
            if ctx.minimum.longValue() is not None:
                minimum = ctx.minimum.longValue().value.text
            else:
                minimum = ctx.minimum.doubleValue().value.text
            if ctx.maximum.longValue() is not None:
                maximum = ctx.maximum.longValue().value.text
            else:
                maximum = ctx.maximum.doubleValue().value.text
            if type.name in ["byte", "short", "int", "long"]:
                return RangeType(range_name, type, int(minimum), int(maximum))
            else:
                return RangeType(range_name, type, float(minimum), float(maximum))
        else:
            self._logger.strict(ctx, f"Unknown type {ctx.type_}")
            return None

    def visitEnumerationType(self, ctx: DeclarationParser.EnumerationTypeContext):
        enum_name = ctx.name.text
        enum_type: EnumeralType = self.resolve_type(self._scope, enum_name)
        # create a new type if no old one exists
        if enum_type is None:
            enum_type = EnumeralType(enum_name)
            self._model.add_new_type(enum_type)

        for enumeral in ctx.values:
            # enum_list representation: [(id, value),...]
            enum_item = self.visitEnumeral(enumeral)
            if enum_item.value == -1:
                enum_item.value = self.find_next_enum_number(enum_type.enumerals)
            if self.check_enumeral_name(enum_item, enum_type.enumerals):
                self._logger.strict(ctx, f"Enumeral {enum_item} already exists in enumeration {enum_name}")
            else:
                enum_type.enumerals[enum_item.name] = enum_item

        return enum_type

    def visitInlineEnumerationType(self, ctx: DeclarationParser.InlineEnumerationTypeContext):
        enum_type = InlineEnumeralType()

        for i in ctx.values:
            # enum_list representation: [(id, value),...]
            enum_item = self.visitEnumeral(i)
            if enum_item.value == -1:
                enum_item.value = self.find_next_enum_number(enum_type.enumerals)
            if self.check_enumeral_name(enum_item, enum_type.enumerals):
                self._logger.strict(ctx, f"Enumeral {enum_item.name} already exists in the inline enumeration")
            else:
                enum_type.enumerals[enum_item.name] = enum_item

        return enum_type

    def visitEnumeral(self, ctx: DeclarationParser.EnumeralContext):
        if ctx.value:
            # return a tuple of id and value
            return Enumeral(ctx.name.text, int(ctx.value.text))
        else:
            return Enumeral(ctx.name.text, -1)

    def visitParamGroupAssignStat(self, ctx: DeclarationParser.ParamGroupAssignStatContext):
        parent_scope = self._scope
        name = ctx.name.text if ctx.name else "<ERROR>"
        description = ctx.description.text[1:-1] if ctx.description else ""

        try:
            group = self._scope.groups[name]
            self._scope = group
        except KeyError:
            group = ParameterGroup(name, description, self._scope)
            self._scope.groups[name] = group
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
        self._type_scope = var_type

        description = ctx.description.text if ctx.description else ""
        unit = self.visit(ctx.unit)

        parameter: Parameter = self._scope.resolve_parameters(var_name)
        if parameter is None:
            parameter = Parameter(var_name, var_type, unit, description, self._scope)
            if ctx.defaultValue is not None:
                expression = self.visitArithmeticExpression(ctx.defaultValue)
                parameter.default_value = expression
            self._type_scope = None
            return parameter
        else:
            self._logger.strict(ctx, f"Parameter redefined {var_name}")
            self._type_scope = None
            return parameter

    def visitParamType(self, ctx: DeclarationParser.ParamTypeContext):
        if (ctx.typeReference() is not None):
            return self.visitTypeReference(ctx.typeReference())
        if (ctx.arrayType() is not None):
            return self.visitArrayType(ctx.arrayType())
        if (ctx.inlineEnumerationType() is not None):
            return self.visitInlineEnumerationType(ctx.inlineEnumerationType())

        return None

    def visitArrayType(self, ctx:DeclarationParser.ArrayTypeContext):
        base_type = self.resolve_type(self._scope, ctx.type_.text)
        dimensions=[]

        for dimension in ctx.dimensions:
            dimensions.append(self.visit(dimension))
        return ArrayType(base_type, dimensions)

    def visitSizeDimension(self, ctx: DeclarationParser.SizeDimensionContext):
        size:CommonToken = ctx.size
        if size is not None:
            return Dimension(0,int(size.text)-1)
        else:
            return Dimension(0,None)

    def visitRangeDimension(self, ctx: DeclarationParser.RangeDimensionContext):
        lower_bound_token:CommonToken = ctx.lowerBound
        if lower_bound_token is None:
            lower_bound = None
        else:
            lower_bound = int(lower_bound_token.text)
        upper_bound_token:CommonToken = ctx.upperBound
        if upper_bound_token is None:
            upper_bound = None
        else:
            upper_bound = int(upper_bound_token.text)
        return Dimension(lower_bound, upper_bound)

    def visitTypeReference(self, ctx: DeclarationParser.TypeReferenceContext):
        type = self.resolve_type(self._scope, ctx.type_.text)
        if type is None:
            self._logger.strict(ctx, f"Unknown type {ctx.type_.text}")
        return type

    def visitFeatureAssignStat(self, ctx: DeclarationParser.FeatureAssignStatContext):
        name = ctx.name.text

        feature = self._scope.resolve_symbol(name)
        if feature is None:
            description = ctx.description.text[1:-1]
            feature = Feature(name, description, self._scope)
            feature.required = ctx.required is not None

            # Feature references are resolved after all features are declared, so features can refer to features
            # declared later in the model (see resolve_feature_references)
            for required in ctx.requires:
                self._pending_references.append((feature.requires, required, self._scope))
            for excluded in ctx.excludes:
                self._pending_references.append((feature.excludes, excluded, self._scope))

            parent_scope = self._scope
            self._scope = feature

            # Parameter groups local to the feature (they were not collected before)
            for group in ctx.parameterGroupDeclarations:
                group_declaration = self.visitParamGroupAssignStat(group)
                feature.groups[group_declaration.name] = group_declaration

            for group in ctx.featureGroupDeclarations:
                feature.feature_sets.append(self.visitFeatureGroupAssignStat(group))

            self._scope = parent_scope
            return feature
        else:
            self._logger.strict(ctx, f"Feature redefinition is not allowed")

    def visitFeatureReference(self, ctx: DeclarationParser.FeatureReferenceContext):
        depth = len(ctx.elements)
        scope = self._scope
        if depth > 1:
            for i in range(1,depth-1):
                scope = scope.parent

        for i in range(0,depth):
            scope = scope.resolve_symbol(ctx.elements[i].text)
            if scope is None:
                self._logger.strict(ctx, f"Feature {self.print_symbol(ctx.elements, i)} does not exist")
                return None
            if not isinstance(scope, Feature):
                self._logger.strict(ctx, f"Feature {self.print_symbol(ctx.elements, i)} does not refer to a feature")

        return scope


    def visitFeatureGroupAssignStat(self, ctx: DeclarationParser.FeatureGroupAssignStatContext):
        kind = self.visitEKind(ctx.kind)
        group = FeatureGroup(kind=kind, parent=self._scope)
        parent_scope = self._scope

        for declaration in ctx.featureDeclarations:
            feature = self.visitFeatureAssignStat(declaration)
            group.features[feature.name] = feature

        self._scope = parent_scope

        return group

    def visitEKind(self, ctx: DeclarationParser.EKindContext):
        if ctx.multiple is not None:
            return EKind.MULTIPLE
        elif ctx.alternative is not None:
            return EKind.ALTERNATIVE
        else:
            self._logger.strict(ctx, "Unknown feature group type. Internal Error")
            return None

    ##################################
    # Units
    ##################################

    def print_tree(self, ctx: ParserRuleContext, indent: str):
        _log.debug("V %s NODE %s %s", indent, ctx, type(ctx))
        if isinstance(ctx, TerminalNode):
            return
        for c in ctx.children:
            self.print_tree(c, indent + "  ")

    def visitUnitSpecification(self, ctx: DeclarationParser.UnitSpecificationContext):
        if len(ctx.units) == 1:
            return self.visit(ctx.units[0])
        else:
            units = []
            for u in ctx.units:
                units.append(self.visit(u))
            return UnitSpecification(units)

    def visitSiunit(self, ctx: DeclarationParser.SiunitContext):
        prefix = None
        if ctx.prefix is not None:
            prefix = self.visitEPrefix(ctx.prefix)

        kind = self.visitESIUnitType(ctx.type_)
        return SIUnit(prefix=prefix, kind=kind)

    def visitESIUnitType(self, ctx: DeclarationParser.ESIUnitTypeContext):
        if ctx.ampere is not None:
            return UnitKind.Ampere
        if ctx.candela is not None:
            return UnitKind.Candela
        if ctx.gram is not None:
            return UnitKind.Gram
        if ctx.joule is not None:
            return UnitKind.Joule
        if ctx.kelvin is not None:
            return UnitKind.Kelvin
        if ctx.meter is not None:
            return UnitKind.Meter
        if ctx.mole is not None:
            return UnitKind.Mole
        if ctx.pascal is not None:
            return UnitKind.Pascal
        if ctx.second is not None:
            return UnitKind.Second

        if ctx.ton is not None:
            return UnitKind.ton

        self._logger.strict(ctx, f"Unknown unit kind {ctx}")
        return UnitKind.Unknown

    def visitEPrefix(self, ctx: DeclarationParser.EPrefixContext):
        # Quetta = 1
        # Ronna = 2
        if ctx.yotta is not None:
            return UnitPrefix.Yotta
        if ctx.zetta is not None:
            return UnitPrefix.Zetta
        if ctx.exa is not None:
            return UnitPrefix.Exa
        if ctx.peta is not None:
            return UnitPrefix.Peta
        if ctx.tera is not None:
            return UnitPrefix.Tera
        if ctx.giga is not None:
            return UnitPrefix.Giga
        if ctx.mega is not None:
            return UnitPrefix.Mega
        if ctx.kilo is not None:
            return UnitPrefix.Kilo
        if ctx.hecto is not None:
            return UnitPrefix.Hecto
        if ctx.deca is not None:
            return UnitPrefix.Deca
        if ctx.deci is not None:
            return UnitPrefix.Deci
        if ctx.centi is not None:
            return UnitPrefix.Centi
        if ctx.mili is not None:
            return UnitPrefix.Milli
        if ctx.micro is not None:
            return UnitPrefix.Micro
        if ctx.nano is not None:
            return UnitPrefix.Nano
        if ctx.pico is not None:
            return UnitPrefix.Pico
        if ctx.femto is not None:
            return UnitPrefix.Femto
        if ctx.atto is not None:
            return UnitPrefix.Atto
        if ctx.zepto is not None:
            return UnitPrefix.Zepto
        if ctx.yocto is not None:
            return UnitPrefix.Yocto
        # if ctx.ronto is not None: return UnitPrefix.Ronto
        # if ctx.quecto is not None: return UnitPrefix.Quecto

        self._logger.strict(ctx, f"Unknown prefix {ctx}")
        return UnitPrefix.NoP

    def visitCustomunit(self, ctx: DeclarationParser.CustomunitContext):
        return CustomUnit(name=ctx.name.text[1:-1])

    def visitComposedUnit(self, ctx: DeclarationParser.ComposedUnitContext):
        if ctx.numerator is None:
            return self.visitBasicUnit(ctx.basicUnit(0))
        numerator = self.visit(ctx.numerator)
        if ctx.denominator is not None:
            denominator = self.visit(ctx.denominator)
            return DivisionUnit(numerator=numerator, denominator=denominator)
        if ctx.exponent is not None:
            return ExponentUnit(unit=numerator, exponent=int(ctx.exponent.text))

        self._logger.strict(ctx, "Illegal unit")

    ##################################
    # Utility functions
    ##################################

    # Find model elements that contain types, i.e., the root element
    def resolve_type(self, node: Scope, type_name: str):
        type = base_types.get(type_name, None)
        if type is not None:
            return type
        if node is None:
            _log.error("No parent, cannot resolve type %s", type_name)
            return None
        elif isinstance(node, DeclarationModel):
            return node.resolve_type(type_name)
        else:
            return self.resolve_type(node.parent, type_name)

    #
    #
    #
    #
    # old code
    #
    #
    #
    #
    #

    def find_next_enum_number(self, enumerals: Dict[str, int]) -> int:
        index = -1
        for key in enumerals.keys():
            if index < enumerals[key].value:
                index = enumerals[key].value
        return index + 1

    def check_enumeral_name(self, enum_item, enumerals: Dict[str, int]) -> bool:
        return enumerals.get(enum_item.name, None) is not None
