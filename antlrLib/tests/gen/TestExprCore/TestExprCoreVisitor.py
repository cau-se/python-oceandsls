# Generated from TestExprCore.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .TestExprCoreParser import TestExprCoreParser
else:
    from TestExprCoreParser import TestExprCoreParser

# This class defines a complete generic visitor for a parse tree produced by TestExprCoreParser.

class TestExprCoreVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TestExprCoreParser#expression.
    def visitExpression(self, ctx:TestExprCoreParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#assignment.
    def visitAssignment(self, ctx:TestExprCoreParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#simpleExpression.
    def visitSimpleExpression(self, ctx:TestExprCoreParser.SimpleExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#variableRef.
    def visitVariableRef(self, ctx:TestExprCoreParser.VariableRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#functionRef.
    def visitFunctionRef(self, ctx:TestExprCoreParser.FunctionRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TestExprCoreParser#identifier.
    def visitIdentifier(self, ctx:TestExprCoreParser.IdentifierContext):
        return self.visitChildren(ctx)



del TestExprCoreParser