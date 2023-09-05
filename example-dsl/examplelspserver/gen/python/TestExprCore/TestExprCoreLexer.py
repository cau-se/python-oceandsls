# Generated from TestExprCore.g4 by ANTLR 4.13.0
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,11,56,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,1,0,1,0,1,0,1,0,1,1,1,1,
        1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,5,1,5,1,6,1,6,1,7,1,7,1,8,1,8,
        1,9,1,9,5,9,48,8,9,10,9,12,9,51,9,9,1,10,1,10,1,10,1,10,0,0,11,1,
        1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,1,0,9,2,0,86,86,
        118,118,2,0,65,65,97,97,2,0,82,82,114,114,2,0,76,76,108,108,2,0,
        69,69,101,101,2,0,84,84,116,116,2,0,65,90,97,122,4,0,48,57,65,90,
        95,95,97,122,3,0,9,10,13,13,32,32,56,0,1,1,0,0,0,0,3,1,0,0,0,0,5,
        1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,
        0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,1,23,1,0,0,0,3,27,1,
        0,0,0,5,31,1,0,0,0,7,33,1,0,0,0,9,35,1,0,0,0,11,37,1,0,0,0,13,39,
        1,0,0,0,15,41,1,0,0,0,17,43,1,0,0,0,19,45,1,0,0,0,21,52,1,0,0,0,
        23,24,7,0,0,0,24,25,7,1,0,0,25,26,7,2,0,0,26,2,1,0,0,0,27,28,7,3,
        0,0,28,29,7,4,0,0,29,30,7,5,0,0,30,4,1,0,0,0,31,32,5,43,0,0,32,6,
        1,0,0,0,33,34,5,45,0,0,34,8,1,0,0,0,35,36,5,42,0,0,36,10,1,0,0,0,
        37,38,5,47,0,0,38,12,1,0,0,0,39,40,5,61,0,0,40,14,1,0,0,0,41,42,
        5,40,0,0,42,16,1,0,0,0,43,44,5,41,0,0,44,18,1,0,0,0,45,49,7,6,0,
        0,46,48,7,7,0,0,47,46,1,0,0,0,48,51,1,0,0,0,49,47,1,0,0,0,49,50,
        1,0,0,0,50,20,1,0,0,0,51,49,1,0,0,0,52,53,7,8,0,0,53,54,1,0,0,0,
        54,55,6,10,0,0,55,22,1,0,0,0,2,0,49,1,0,1,0
    ]

class TestExprCoreLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    VAR = 1
    LET = 2
    PLUS = 3
    MINUS = 4
    MULTIPLY = 5
    DIVIDE = 6
    EQUAL = 7
    OPEN_PAR = 8
    CLOSE_PAR = 9
    ID = 10
    WS = 11

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'+'", "'-'", "'*'", "'/'", "'='", "'('", "')'" ]

    symbolicNames = [ "<INVALID>",
            "VAR", "LET", "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQUAL", 
            "OPEN_PAR", "CLOSE_PAR", "ID", "WS" ]

    ruleNames = [ "VAR", "LET", "PLUS", "MINUS", "MULTIPLY", "DIVIDE", "EQUAL", 
                  "OPEN_PAR", "CLOSE_PAR", "ID", "WS" ]

    grammarFileName = "TestExprCore.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None

