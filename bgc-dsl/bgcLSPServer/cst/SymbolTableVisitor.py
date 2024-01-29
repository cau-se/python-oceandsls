"""This visitor collects variables and nodes in a SymbolTable."""

__author__ = 'stu90642'

# util imports
from typing import TypeVar, Generic, Dict, Optional, Callable, Any



# antlr4
from antlr4.tree.Tree import ParseTree

# user relative imports
from ..symbolTable.SymbolTable import (ScopedSymbol, SymbolTable, P, T, VariableSymbol, RoutineSymbol,
                                       SymbolTableOptions, UnitSymbol, FundamentalUnit, FundamentalType, UnitPrefix,
                                       UnitKind,ReferenceKind, AggregatedUnit, CompartmentSymbol
                                       )
from ..gen.python.BgcDsl.BgcDslParser import BgcDslParser
from ..gen.python.BgcDsl.BgcDslVisitor import BgcDslVisitor


def _stringToPrefix(input: str):
    for prefix in UnitPrefix:
        if prefix.name.lower() == input.lower():
            return prefix
    return UnitPrefix.NoP


def _stringToUnitType(input: str):
    for kind in UnitKind:
        if vars(kind)["_name_"].lower() == input.lower():
            return kind
    return UnitKind.Unknown


class SymbolTableVisitor( BgcDslVisitor, Generic[T] ):
    _symbolTable: SymbolTable

    def __init__(self, name: str = '', ):
        super().__init__()
        self._symbolTable = SymbolTable( name, SymbolTableOptions( False ) )
        # TODO scope marker
        # self._scope = self._symbolTable.addNewSymbolOfType( ScopedSymbol, None )
        self._scope = None

    @property
    def symbolTable(self) -> SymbolTable:
        return self._symbolTable

    def defaultResult(self) -> SymbolTable:
        return self._symbolTable

    def visitUnit(self, ctx:BgcDslParser.UnitContext):
        elements = []
        for element in ctx.elements:
            elements.append(self.visitUnitElement(element))

        return AggregatedUnit("bla", elements )

    def visitPrefixUnit(self, ctx:BgcDslParser.PrefixUnitContext):
        prefix = _stringToPrefix(str(ctx.UNIT_STRING()))
        unit = _stringToUnitType(str(ctx.UNIT_STRING()))
        return FundamentalUnit(unit, baseTypes=[],
                               unitPrefix=prefix,
                               unitKind=unit,
                               referenceKind=ReferenceKind.Irrelevant)

    def visitGroupUnit(self, ctx:BgcDslParser.GroupUnitContext):
        fundamental_units = []
        for element in ctx.elements:
            fundamental_units.append(self.visitUnitElement(element))

        return AggregatedUnit("bla", fundamental_units)

    # Visit a parse tree produced by BgcDslParser#substanceDeclaration.
    def visitSubstanceDeclaration(self, ctx:BgcDslParser.SubstanceDeclarationContext):
        # TODO
        # save type
        # save unit as node
#        unit =self.visit(ctx.unit)
        self._symbolTable.addNewSymbolOfType( VariableSymbol,
                                              self._scope,
                                              ctx.name.text,
                                              ctx,
                                              attached_unit=ctx.unit(),
                                              attached_type=ctx.type_)

        return self.visitChildren( ctx )

    def visitParameterDeclaration(self, ctx:BgcDslParser.ParameterDeclarationContext):
        # TODO
        # save type
        # save unit, expression as node

 #       unit = ctx.unit()
        unit_node = self.visit(ctx.unit())
        self._symbolTable.addNewSymbolOfType( VariableSymbol,
                                              self._scope,
                                              ctx.name.text,
                                              value=ctx,
                                              attached_unit=unit_node,
                                              attached_type=ctx.type_ )
        return self.visitChildren( ctx )

    def visitEnvironmentVariableDeclaration(self, ctx:BgcDslParser.EnvironmentVariableDeclarationContext):
        # TODO
        # save type
        # save unit, expression as node
        unit = ctx.unit()
        unit_node = self.visitUnit(unit)
        self._symbolTable.addNewSymbolOfType( VariableSymbol, self._scope,
                                              ctx.name.text,
                                              value = ctx,
                                              attached_unit = unit_node,
                                              attached_type = ctx.type_)
        return self.visitChildren( ctx )

    # Visit a parse tree produced by BgcDslParser#compartment.

    def visitCompartment(self, ctx:BgcDslParser.CompartmentContext):

        self._symbolTable.addNewSymbolOfType(CompartmentSymbol, self._scope, ctx.name.text, value=ctx )
        return self.visitChildren(ctx)

    # Visit a parse tree produced by BgcDslParser#connection.
    def visitConnection(self, ctx:BgcDslParser.ConnectionContext):
        # TODO
        # the name needs to be more complex, here:
        name = ctx.name.text + ' from ' + ctx.sourceCompartment.text + ' to ' + ctx.targetCompartment.text
        self._symbolTable.addNewSymbolOfType( VariableSymbol, self._scope, name, ctx )
        return self.visitChildren(ctx)

    # def visitFuncExpr(self, ctx: TestGrammarParser.FuncExprContext):
    #     return self.withScope( ctx, RoutineSymbol, lambda: self.visitChildren( ctx ), ctx.ID().getText() )

    def withScope(self, tree: ParseTree, t: type, action: Callable, *my_args: P.args or None,
                  **my_kwargs: P.kwargs or None) -> T:
        scope = self._symbolTable.addNewSymbolOfType( t, self._scope, *my_args, **my_kwargs )
        scope.context = tree
        self._scope = scope
        try:
            return action()
        finally:
            self._scope = scope.parent()
