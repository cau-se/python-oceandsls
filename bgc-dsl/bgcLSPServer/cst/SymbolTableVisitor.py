"""This visitor collects variables and nodes in a SymbolTable."""

__author__ = 'stu90642'

# util imports
from typing import TypeVar, Generic, Dict, Optional, Callable, Any

# antlr4
from antlr4.tree.Tree import ParseTree

# user relative imports
from ..symbolTable.SymbolTable import ScopedSymbol, SymbolTable, P, T, VariableSymbol, RoutineSymbol, SymbolTableOptions
from ..gen.python.BgcDsl.BgcDslParser import BgcDslParser
from ..gen.python.BgcDsl.BgcDslVisitor import BgcDslVisitor


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

    # 5 mal das gleiche; kann man das kürzer/eleganter schreiben?
    def visitSubstanceDeclaration(self, ctx:BgcDslParser.SubstanceDeclarationContext):
        # TODO
        # save name, type
        # save unit as node
        self._symbolTable.addNewSymbolOfType( VariableSymbol, self._scope, ctx.name.text, ctx )
        return self.visitChildren( ctx )

    def visitParameterDeclaration(self, ctx:BgcDslParser.ParameterDeclarationContext):
        # TODO
        # save name, type
        # save unit, expression as node
        self._symbolTable.addNewSymbolOfType( VariableSymbol, self._scope, ctx.name.text, ctx )
        return self.visitChildren( ctx )

    def visitEnvironmentVariableDeclaration(self, ctx:BgcDslParser.EnvironmentVariableDeclarationContext):
        # TODO
        # save name, type
        # save unit, expression as node
        self._symbolTable.addNewSymbolOfType( VariableSymbol, self._scope, ctx.name.text, ctx )     
        return self.visitChildren( ctx )
             
    # Visit a parse tree produced by BgcDslParser#compartment.
    def visitCompartment(self, ctx:BgcDslParser.CompartmentContext):
        # TODO
        # save name
        # save node as expression
        self._symbolTable.addNewSymbolOfType( VariableSymbol, self._scope, ctx.name.text, ctx )
        return self.visitChildren(ctx)
    
    # Visit a parse tree produced by BgcDslParser#connection.
    def visitConnection(self, ctx:BgcDslParser.ConnectionContext):
        # TODO
        # save name
        # save node as expression
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
