# Generated from TestGrammar.g4 by ANTLR 4.12.0
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,12,110,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,5,1,
        5,1,6,1,6,1,7,1,7,1,8,4,8,49,8,8,11,8,12,8,50,1,8,1,8,1,9,4,9,56,
        8,9,11,9,12,9,57,1,10,3,10,61,8,10,1,10,1,10,4,10,65,8,10,11,10,
        12,10,66,1,10,4,10,70,8,10,11,10,12,10,71,1,10,1,10,5,10,76,8,10,
        10,10,12,10,79,9,10,3,10,81,8,10,1,10,3,10,84,8,10,3,10,86,8,10,
        1,11,1,11,1,11,5,11,91,8,11,10,11,12,11,94,9,11,3,11,96,8,11,1,12,
        1,12,3,12,100,8,12,1,12,1,12,1,13,1,13,1,14,3,14,107,8,14,1,14,1,
        14,0,0,15,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,
        0,25,0,27,0,29,12,1,0,6,2,0,9,9,32,32,2,0,65,90,97,122,1,0,49,57,
        2,0,69,69,101,101,2,0,43,43,45,45,1,0,48,57,119,0,1,1,0,0,0,0,3,
        1,0,0,0,0,5,1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,
        0,0,0,0,15,1,0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,29,1,
        0,0,0,1,31,1,0,0,0,3,33,1,0,0,0,5,35,1,0,0,0,7,37,1,0,0,0,9,39,1,
        0,0,0,11,41,1,0,0,0,13,43,1,0,0,0,15,45,1,0,0,0,17,48,1,0,0,0,19,
        55,1,0,0,0,21,60,1,0,0,0,23,95,1,0,0,0,25,97,1,0,0,0,27,103,1,0,
        0,0,29,106,1,0,0,0,31,32,5,42,0,0,32,2,1,0,0,0,33,34,5,47,0,0,34,
        4,1,0,0,0,35,36,5,43,0,0,36,6,1,0,0,0,37,38,5,45,0,0,38,8,1,0,0,
        0,39,40,5,40,0,0,40,10,1,0,0,0,41,42,5,41,0,0,42,12,1,0,0,0,43,44,
        5,61,0,0,44,14,1,0,0,0,45,46,5,44,0,0,46,16,1,0,0,0,47,49,7,0,0,
        0,48,47,1,0,0,0,49,50,1,0,0,0,50,48,1,0,0,0,50,51,1,0,0,0,51,52,
        1,0,0,0,52,53,6,8,0,0,53,18,1,0,0,0,54,56,7,1,0,0,55,54,1,0,0,0,
        56,57,1,0,0,0,57,55,1,0,0,0,57,58,1,0,0,0,58,20,1,0,0,0,59,61,5,
        45,0,0,60,59,1,0,0,0,60,61,1,0,0,0,61,85,1,0,0,0,62,64,5,46,0,0,
        63,65,3,27,13,0,64,63,1,0,0,0,65,66,1,0,0,0,66,64,1,0,0,0,66,67,
        1,0,0,0,67,86,1,0,0,0,68,70,3,27,13,0,69,68,1,0,0,0,70,71,1,0,0,
        0,71,69,1,0,0,0,71,72,1,0,0,0,72,80,1,0,0,0,73,77,5,46,0,0,74,76,
        3,27,13,0,75,74,1,0,0,0,76,79,1,0,0,0,77,75,1,0,0,0,77,78,1,0,0,
        0,78,81,1,0,0,0,79,77,1,0,0,0,80,73,1,0,0,0,80,81,1,0,0,0,81,83,
        1,0,0,0,82,84,3,25,12,0,83,82,1,0,0,0,83,84,1,0,0,0,84,86,1,0,0,
        0,85,62,1,0,0,0,85,69,1,0,0,0,86,22,1,0,0,0,87,96,5,48,0,0,88,92,
        7,2,0,0,89,91,3,27,13,0,90,89,1,0,0,0,91,94,1,0,0,0,92,90,1,0,0,
        0,92,93,1,0,0,0,93,96,1,0,0,0,94,92,1,0,0,0,95,87,1,0,0,0,95,88,
        1,0,0,0,96,24,1,0,0,0,97,99,7,3,0,0,98,100,7,4,0,0,99,98,1,0,0,0,
        99,100,1,0,0,0,100,101,1,0,0,0,101,102,3,23,11,0,102,26,1,0,0,0,
        103,104,7,5,0,0,104,28,1,0,0,0,105,107,5,13,0,0,106,105,1,0,0,0,
        106,107,1,0,0,0,107,108,1,0,0,0,108,109,5,10,0,0,109,30,1,0,0,0,
        14,0,50,57,60,66,71,77,80,83,85,92,95,99,106,1,0,1,0
    ]

class TestGrammarLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    OP_MUL = 1
    OP_DIV = 2
    OP_ADD = 3
    OP_SUB = 4
    PAR_L = 5
    PAR_R = 6
    EQUAL = 7
    SEP = 8
    WS = 9
    ID = 10
    NUM = 11
    NEWLINE = 12

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'*'", "'/'", "'+'", "'-'", "'('", "')'", "'='", "','" ]

    symbolicNames = [ "<INVALID>",
            "OP_MUL", "OP_DIV", "OP_ADD", "OP_SUB", "PAR_L", "PAR_R", "EQUAL", 
            "SEP", "WS", "ID", "NUM", "NEWLINE" ]

    ruleNames = [ "OP_MUL", "OP_DIV", "OP_ADD", "OP_SUB", "PAR_L", "PAR_R", 
                  "EQUAL", "SEP", "WS", "ID", "NUM", "INT", "EXP", "DIG", 
                  "NEWLINE" ]

    grammarFileName = "TestGrammar.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


