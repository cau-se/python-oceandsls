# Generated from TestGrammar.g4 by ANTLR 4.10.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,10,24,2,0,7,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,3,0,11,8,0,1,0,
        1,0,1,0,1,0,1,0,1,0,5,0,19,8,0,10,0,12,0,22,9,0,1,0,0,1,0,1,0,0,
        2,1,0,3,4,1,0,5,6,27,0,10,1,0,0,0,2,3,6,0,-1,0,3,4,5,1,0,0,4,5,3,
        0,0,0,5,6,5,2,0,0,6,11,1,0,0,0,7,11,5,9,0,0,8,11,5,7,0,0,9,11,5,
        8,0,0,10,2,1,0,0,0,10,7,1,0,0,0,10,8,1,0,0,0,10,9,1,0,0,0,11,20,
        1,0,0,0,12,13,10,5,0,0,13,14,7,0,0,0,14,19,3,0,0,6,15,16,10,4,0,
        0,16,17,7,1,0,0,17,19,3,0,0,5,18,12,1,0,0,0,18,15,1,0,0,0,19,22,
        1,0,0,0,20,18,1,0,0,0,20,21,1,0,0,0,21,1,1,0,0,0,22,20,1,0,0,0,3,
        10,18,20
    ]

class TestGrammarParser ( Parser ):

    grammarFileName = "TestGrammar.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'('", "')'", "'*'", "'/'", "'+'", "'-'" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "<INVALID>", "<INVALID>", "<INVALID>", "FOO", "BAR", 
                      "INT", "WS" ]

    RULE_expr = 0

    ruleNames =  [ "expr" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    T__3=4
    T__4=5
    T__5=6
    FOO=7
    BAR=8
    INT=9
    WS=10

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.10.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return TestGrammarParser.RULE_expr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class FooExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TestGrammarParser.ExprContext
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def FOO(self):
            return self.getToken(TestGrammarParser.FOO, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFooExpr" ):
                listener.enterFooExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFooExpr" ):
                listener.exitFooExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFooExpr" ):
                return visitor.visitFooExpr(self)
            else:
                return visitor.visitChildren(self)


    class BarExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TestGrammarParser.ExprContext
            super().__init__(parser)
            self.atmo = None # Token
            self.copyFrom(ctx)

        def BAR(self):
            return self.getToken(TestGrammarParser.BAR, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBarExpr" ):
                listener.enterBarExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBarExpr" ):
                listener.exitBarExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBarExpr" ):
                return visitor.visitBarExpr(self)
            else:
                return visitor.visitChildren(self)


    class NumberExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TestGrammarParser.ExprContext
            super().__init__(parser)
            self.atom = None # Token
            self.copyFrom(ctx)

        def INT(self):
            return self.getToken(TestGrammarParser.INT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNumberExpr" ):
                listener.enterNumberExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNumberExpr" ):
                listener.exitNumberExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNumberExpr" ):
                return visitor.visitNumberExpr(self)
            else:
                return visitor.visitChildren(self)


    class ParenExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TestGrammarParser.ExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def expr(self):
            return self.getTypedRuleContext(TestGrammarParser.ExprContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParenExpr" ):
                listener.enterParenExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParenExpr" ):
                listener.exitParenExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParenExpr" ):
                return visitor.visitParenExpr(self)
            else:
                return visitor.visitChildren(self)


    class InfixExprContext(ExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a TestGrammarParser.ExprContext
            super().__init__(parser)
            self.left = None # ExprContext
            self.op = None # Token
            self.right = None # ExprContext
            self.copyFrom(ctx)

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(TestGrammarParser.ExprContext)
            else:
                return self.getTypedRuleContext(TestGrammarParser.ExprContext,i)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterInfixExpr" ):
                listener.enterInfixExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitInfixExpr" ):
                listener.exitInfixExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitInfixExpr" ):
                return visitor.visitInfixExpr(self)
            else:
                return visitor.visitChildren(self)



    def expr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = TestGrammarParser.ExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 0
        self.enterRecursionRule(localctx, 0, self.RULE_expr, _p)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [TestGrammarParser.T__0]:
                localctx = TestGrammarParser.ParenExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx

                self.state = 3
                self.match(TestGrammarParser.T__0)
                self.state = 4
                self.expr(0)
                self.state = 5
                self.match(TestGrammarParser.T__1)
                pass
            elif token in [TestGrammarParser.INT]:
                localctx = TestGrammarParser.NumberExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 7
                localctx.atom = self.match(TestGrammarParser.INT)
                pass
            elif token in [TestGrammarParser.FOO]:
                localctx = TestGrammarParser.FooExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 8
                localctx.atom = self.match(TestGrammarParser.FOO)
                pass
            elif token in [TestGrammarParser.BAR]:
                localctx = TestGrammarParser.BarExprContext(self, localctx)
                self._ctx = localctx
                _prevctx = localctx
                self.state = 9
                localctx.atmo = self.match(TestGrammarParser.BAR)
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 20
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 18
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
                    if la_ == 1:
                        localctx = TestGrammarParser.InfixExprContext(self, TestGrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 12
                        if not self.precpred(self._ctx, 5):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 5)")
                        self.state = 13
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==TestGrammarParser.T__2 or _la==TestGrammarParser.T__3):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 14
                        localctx.right = self.expr(6)
                        pass

                    elif la_ == 2:
                        localctx = TestGrammarParser.InfixExprContext(self, TestGrammarParser.ExprContext(self, _parentctx, _parentState))
                        localctx.left = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_expr)
                        self.state = 15
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 16
                        localctx.op = self._input.LT(1)
                        _la = self._input.LA(1)
                        if not(_la==TestGrammarParser.T__4 or _la==TestGrammarParser.T__5):
                            localctx.op = self._errHandler.recoverInline(self)
                        else:
                            self._errHandler.reportMatch(self)
                            self.consume()
                        self.state = 17
                        localctx.right = self.expr(5)
                        pass

             
                self.state = 22
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[0] = self.expr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def expr_sempred(self, localctx:ExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 5)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 4)
         




