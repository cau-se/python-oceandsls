# Generated from exampleDsl.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .exampleDslParser import exampleDslParser
else:
    from exampleDslParser import exampleDslParser

# This class defines a complete generic visitor for a parse tree produced by exampleDslParser.

class exampleDslVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by exampleDslParser#startProg.
    def visitStartProg(self, ctx:exampleDslParser.StartProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#printExprStat.
    def visitPrintExprStat(self, ctx:exampleDslParser.PrintExprStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#assignStat.
    def visitAssignStat(self, ctx:exampleDslParser.AssignStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#blankStat.
    def visitBlankStat(self, ctx:exampleDslParser.BlankStatContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#addSubExpr.
    def visitAddSubExpr(self, ctx:exampleDslParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#funRef.
    def visitFunRef(self, ctx:exampleDslParser.FunRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#numberExpr.
    def visitNumberExpr(self, ctx:exampleDslParser.NumberExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#parensExpr.
    def visitParensExpr(self, ctx:exampleDslParser.ParensExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#mulDivExpr.
    def visitMulDivExpr(self, ctx:exampleDslParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#idRef.
    def visitIdRef(self, ctx:exampleDslParser.IdRefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#argList.
    def visitArgList(self, ctx:exampleDslParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#varExpr.
    def visitVarExpr(self, ctx:exampleDslParser.VarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by exampleDslParser#funcExpr.
    def visitFuncExpr(self, ctx:exampleDslParser.FuncExprContext):
        return self.visitChildren(ctx)



del exampleDslParser