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

# Generated from Declaration.g4 by ANTLR 4.13.0
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,70,546,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,
        2,6,7,6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,
        13,7,13,2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,
        19,2,20,7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,2,25,7,25,2,
        26,7,26,2,27,7,27,2,28,7,28,2,29,7,29,2,30,7,30,2,31,7,31,2,32,7,
        32,2,33,7,33,2,34,7,34,2,35,7,35,2,36,7,36,2,37,7,37,2,38,7,38,2,
        39,7,39,2,40,7,40,2,41,7,41,2,42,7,42,2,43,7,43,2,44,7,44,2,45,7,
        45,2,46,7,46,2,47,7,47,2,48,7,48,2,49,7,49,2,50,7,50,2,51,7,51,2,
        52,7,52,2,53,7,53,2,54,7,54,2,55,7,55,2,56,7,56,2,57,7,57,2,58,7,
        58,2,59,7,59,2,60,7,60,2,61,7,61,2,62,7,62,2,63,7,63,2,64,7,64,2,
        65,7,65,2,66,7,66,2,67,7,67,2,68,7,68,2,69,7,69,1,0,1,0,1,0,1,0,
        1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,
        1,4,1,4,1,5,1,5,1,6,1,6,1,6,1,6,1,7,1,7,1,8,1,8,1,9,1,9,1,9,1,9,
        1,9,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,10,1,11,
        1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,11,1,12,1,12,1,12,1,12,1,12,
        1,12,1,12,1,12,1,12,1,13,1,13,1,13,1,13,1,14,1,14,1,14,1,14,1,14,
        1,14,1,14,1,14,1,14,1,14,1,14,1,14,1,15,1,15,1,15,1,15,1,15,1,15,
        1,15,1,15,1,15,1,16,1,16,1,17,1,17,1,18,1,18,1,19,1,19,1,20,1,20,
        1,20,1,20,1,20,1,20,1,21,1,21,1,21,1,21,1,21,1,22,1,22,1,23,1,23,
        1,24,1,24,1,24,1,25,1,25,1,25,1,25,1,26,1,26,1,26,1,26,1,26,1,26,
        1,27,1,27,1,27,1,27,1,27,1,27,1,28,1,28,1,28,1,28,1,29,1,29,1,29,
        1,29,1,29,1,30,1,30,1,30,1,30,1,30,1,31,1,31,1,31,1,31,1,31,1,32,
        1,32,1,32,1,32,1,32,1,33,1,33,1,33,1,33,1,33,1,34,1,34,1,34,1,34,
        1,34,1,34,1,35,1,35,1,35,1,35,1,35,1,36,1,36,1,36,1,36,1,36,1,37,
        1,37,1,37,1,37,1,37,1,37,1,38,1,38,1,38,1,38,1,38,1,39,1,39,1,39,
        1,39,1,39,1,39,1,40,1,40,1,40,1,40,1,40,1,41,1,41,1,41,1,41,1,41,
        1,42,1,42,1,42,1,42,1,42,1,42,1,43,1,43,1,43,1,43,1,43,1,44,1,44,
        1,44,1,44,1,44,1,44,1,45,1,45,1,45,1,45,1,45,1,45,1,46,1,46,1,46,
        1,46,1,46,1,46,1,47,1,47,1,47,1,47,1,47,1,48,1,48,1,48,1,48,1,49,
        1,49,1,49,1,49,1,49,1,49,1,49,1,50,1,50,1,50,1,50,1,50,1,50,1,50,
        1,51,1,51,1,51,1,51,1,51,1,51,1,51,1,52,1,52,1,52,1,52,1,52,1,53,
        1,53,1,53,1,53,1,53,1,53,1,53,1,53,1,54,1,54,1,54,1,54,1,54,1,54,
        1,54,1,55,1,55,1,55,1,55,1,55,1,56,1,56,1,57,1,57,1,58,1,58,1,59,
        1,59,1,60,3,60,441,8,60,1,60,1,60,1,61,3,61,446,8,61,1,61,3,61,449,
        8,61,1,61,1,61,1,61,1,61,3,61,455,8,61,1,61,3,61,458,8,61,1,62,1,
        62,1,62,1,62,1,62,1,62,1,62,1,62,1,62,3,62,469,8,62,1,63,3,63,472,
        8,63,1,63,3,63,475,8,63,1,63,5,63,478,8,63,10,63,12,63,481,9,63,
        1,64,4,64,484,8,64,11,64,12,64,485,1,65,1,65,1,65,1,65,5,65,492,
        8,65,10,65,12,65,495,9,65,1,65,1,65,1,65,1,65,1,65,5,65,502,8,65,
        10,65,12,65,505,9,65,1,65,3,65,508,8,65,1,66,4,66,511,8,66,11,66,
        12,66,512,1,66,1,66,1,67,1,67,1,67,1,67,5,67,521,8,67,10,67,12,67,
        524,9,67,1,67,1,67,1,67,1,67,1,67,1,68,1,68,1,68,1,68,5,68,535,8,
        68,10,68,12,68,538,9,68,1,68,3,68,541,8,68,1,68,1,68,1,69,1,69,1,
        522,0,70,1,1,3,2,5,3,7,4,9,5,11,6,13,7,15,8,17,9,19,10,21,11,23,
        12,25,13,27,14,29,15,31,16,33,17,35,18,37,19,39,20,41,21,43,22,45,
        23,47,24,49,25,51,26,53,27,55,28,57,29,59,30,61,31,63,32,65,33,67,
        34,69,35,71,36,73,37,75,38,77,39,79,40,81,41,83,42,85,43,87,44,89,
        45,91,46,93,47,95,48,97,49,99,50,101,51,103,52,105,53,107,54,109,
        55,111,56,113,57,115,58,117,59,119,60,121,61,123,62,125,63,127,64,
        129,65,131,66,133,67,135,68,137,69,139,70,1,0,9,2,0,69,69,101,101,
        3,0,65,90,95,95,97,122,4,0,48,57,65,90,95,95,97,122,1,0,48,57,2,
        0,34,34,92,92,2,0,39,39,92,92,3,0,9,10,13,13,32,32,3,0,10,10,13,
        13,124,124,3,0,10,10,13,13,63,63,563,0,1,1,0,0,0,0,3,1,0,0,0,0,5,
        1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,
        0,0,0,0,17,1,0,0,0,0,19,1,0,0,0,0,21,1,0,0,0,0,23,1,0,0,0,0,25,1,
        0,0,0,0,27,1,0,0,0,0,29,1,0,0,0,0,31,1,0,0,0,0,33,1,0,0,0,0,35,1,
        0,0,0,0,37,1,0,0,0,0,39,1,0,0,0,0,41,1,0,0,0,0,43,1,0,0,0,0,45,1,
        0,0,0,0,47,1,0,0,0,0,49,1,0,0,0,0,51,1,0,0,0,0,53,1,0,0,0,0,55,1,
        0,0,0,0,57,1,0,0,0,0,59,1,0,0,0,0,61,1,0,0,0,0,63,1,0,0,0,0,65,1,
        0,0,0,0,67,1,0,0,0,0,69,1,0,0,0,0,71,1,0,0,0,0,73,1,0,0,0,0,75,1,
        0,0,0,0,77,1,0,0,0,0,79,1,0,0,0,0,81,1,0,0,0,0,83,1,0,0,0,0,85,1,
        0,0,0,0,87,1,0,0,0,0,89,1,0,0,0,0,91,1,0,0,0,0,93,1,0,0,0,0,95,1,
        0,0,0,0,97,1,0,0,0,0,99,1,0,0,0,0,101,1,0,0,0,0,103,1,0,0,0,0,105,
        1,0,0,0,0,107,1,0,0,0,0,109,1,0,0,0,0,111,1,0,0,0,0,113,1,0,0,0,
        0,115,1,0,0,0,0,117,1,0,0,0,0,119,1,0,0,0,0,121,1,0,0,0,0,123,1,
        0,0,0,0,125,1,0,0,0,0,127,1,0,0,0,0,129,1,0,0,0,0,131,1,0,0,0,0,
        133,1,0,0,0,0,135,1,0,0,0,0,137,1,0,0,0,0,139,1,0,0,0,1,141,1,0,
        0,0,3,147,1,0,0,0,5,153,1,0,0,0,7,159,1,0,0,0,9,161,1,0,0,0,11,163,
        1,0,0,0,13,165,1,0,0,0,15,169,1,0,0,0,17,171,1,0,0,0,19,173,1,0,
        0,0,21,182,1,0,0,0,23,190,1,0,0,0,25,199,1,0,0,0,27,208,1,0,0,0,
        29,212,1,0,0,0,31,224,1,0,0,0,33,233,1,0,0,0,35,235,1,0,0,0,37,237,
        1,0,0,0,39,239,1,0,0,0,41,241,1,0,0,0,43,247,1,0,0,0,45,252,1,0,
        0,0,47,254,1,0,0,0,49,256,1,0,0,0,51,259,1,0,0,0,53,263,1,0,0,0,
        55,269,1,0,0,0,57,275,1,0,0,0,59,279,1,0,0,0,61,284,1,0,0,0,63,289,
        1,0,0,0,65,294,1,0,0,0,67,299,1,0,0,0,69,304,1,0,0,0,71,310,1,0,
        0,0,73,315,1,0,0,0,75,320,1,0,0,0,77,326,1,0,0,0,79,331,1,0,0,0,
        81,337,1,0,0,0,83,342,1,0,0,0,85,347,1,0,0,0,87,353,1,0,0,0,89,358,
        1,0,0,0,91,364,1,0,0,0,93,370,1,0,0,0,95,376,1,0,0,0,97,381,1,0,
        0,0,99,385,1,0,0,0,101,392,1,0,0,0,103,399,1,0,0,0,105,406,1,0,0,
        0,107,411,1,0,0,0,109,419,1,0,0,0,111,426,1,0,0,0,113,431,1,0,0,
        0,115,433,1,0,0,0,117,435,1,0,0,0,119,437,1,0,0,0,121,440,1,0,0,
        0,123,445,1,0,0,0,125,468,1,0,0,0,127,471,1,0,0,0,129,483,1,0,0,
        0,131,507,1,0,0,0,133,510,1,0,0,0,135,516,1,0,0,0,137,530,1,0,0,
        0,139,544,1,0,0,0,141,142,5,109,0,0,142,143,5,111,0,0,143,144,5,
        100,0,0,144,145,5,101,0,0,145,146,5,108,0,0,146,2,1,0,0,0,147,148,
        5,116,0,0,148,149,5,121,0,0,149,150,5,112,0,0,150,151,5,101,0,0,
        151,152,5,115,0,0,152,4,1,0,0,0,153,154,5,103,0,0,154,155,5,114,
        0,0,155,156,5,111,0,0,156,157,5,117,0,0,157,158,5,112,0,0,158,6,
        1,0,0,0,159,160,5,58,0,0,160,8,1,0,0,0,161,162,5,123,0,0,162,10,
        1,0,0,0,163,164,5,125,0,0,164,12,1,0,0,0,165,166,5,100,0,0,166,167,
        5,101,0,0,167,168,5,102,0,0,168,14,1,0,0,0,169,170,5,44,0,0,170,
        16,1,0,0,0,171,172,5,61,0,0,172,18,1,0,0,0,173,174,5,114,0,0,174,
        175,5,101,0,0,175,176,5,113,0,0,176,177,5,117,0,0,177,178,5,105,
        0,0,178,179,5,114,0,0,179,180,5,101,0,0,180,181,5,100,0,0,181,20,
        1,0,0,0,182,183,5,102,0,0,183,184,5,101,0,0,184,185,5,97,0,0,185,
        186,5,116,0,0,186,187,5,117,0,0,187,188,5,114,0,0,188,189,5,101,
        0,0,189,22,1,0,0,0,190,191,5,114,0,0,191,192,5,101,0,0,192,193,5,
        113,0,0,193,194,5,117,0,0,194,195,5,105,0,0,195,196,5,114,0,0,196,
        197,5,101,0,0,197,198,5,115,0,0,198,24,1,0,0,0,199,200,5,101,0,0,
        200,201,5,120,0,0,201,202,5,99,0,0,202,203,5,108,0,0,203,204,5,117,
        0,0,204,205,5,100,0,0,205,206,5,101,0,0,206,207,5,115,0,0,207,26,
        1,0,0,0,208,209,5,115,0,0,209,210,5,117,0,0,210,211,5,98,0,0,211,
        28,1,0,0,0,212,213,5,97,0,0,213,214,5,108,0,0,214,215,5,116,0,0,
        215,216,5,101,0,0,216,217,5,114,0,0,217,218,5,110,0,0,218,219,5,
        97,0,0,219,220,5,116,0,0,220,221,5,105,0,0,221,222,5,118,0,0,222,
        223,5,101,0,0,223,30,1,0,0,0,224,225,5,109,0,0,225,226,5,117,0,0,
        226,227,5,108,0,0,227,228,5,116,0,0,228,229,5,105,0,0,229,230,5,
        112,0,0,230,231,5,108,0,0,231,232,5,101,0,0,232,32,1,0,0,0,233,234,
        5,40,0,0,234,34,1,0,0,0,235,236,5,41,0,0,236,36,1,0,0,0,237,238,
        5,91,0,0,238,38,1,0,0,0,239,240,5,93,0,0,240,40,1,0,0,0,241,242,
        5,114,0,0,242,243,5,97,0,0,243,244,5,110,0,0,244,245,5,103,0,0,245,
        246,5,101,0,0,246,42,1,0,0,0,247,248,5,101,0,0,248,249,5,110,0,0,
        249,250,5,117,0,0,250,251,5,109,0,0,251,44,1,0,0,0,252,253,5,42,
        0,0,253,46,1,0,0,0,254,255,5,47,0,0,255,48,1,0,0,0,256,257,5,42,
        0,0,257,258,5,42,0,0,258,50,1,0,0,0,259,260,5,110,0,0,260,261,5,
        111,0,0,261,262,5,80,0,0,262,52,1,0,0,0,263,264,5,121,0,0,264,265,
        5,111,0,0,265,266,5,116,0,0,266,267,5,116,0,0,267,268,5,97,0,0,268,
        54,1,0,0,0,269,270,5,122,0,0,270,271,5,101,0,0,271,272,5,116,0,0,
        272,273,5,116,0,0,273,274,5,97,0,0,274,56,1,0,0,0,275,276,5,101,
        0,0,276,277,5,120,0,0,277,278,5,97,0,0,278,58,1,0,0,0,279,280,5,
        112,0,0,280,281,5,101,0,0,281,282,5,116,0,0,282,283,5,97,0,0,283,
        60,1,0,0,0,284,285,5,116,0,0,285,286,5,101,0,0,286,287,5,114,0,0,
        287,288,5,97,0,0,288,62,1,0,0,0,289,290,5,103,0,0,290,291,5,105,
        0,0,291,292,5,103,0,0,292,293,5,97,0,0,293,64,1,0,0,0,294,295,5,
        109,0,0,295,296,5,101,0,0,296,297,5,103,0,0,297,298,5,97,0,0,298,
        66,1,0,0,0,299,300,5,107,0,0,300,301,5,105,0,0,301,302,5,108,0,0,
        302,303,5,111,0,0,303,68,1,0,0,0,304,305,5,104,0,0,305,306,5,101,
        0,0,306,307,5,99,0,0,307,308,5,116,0,0,308,309,5,111,0,0,309,70,
        1,0,0,0,310,311,5,100,0,0,311,312,5,101,0,0,312,313,5,99,0,0,313,
        314,5,97,0,0,314,72,1,0,0,0,315,316,5,100,0,0,316,317,5,101,0,0,
        317,318,5,99,0,0,318,319,5,105,0,0,319,74,1,0,0,0,320,321,5,99,0,
        0,321,322,5,101,0,0,322,323,5,110,0,0,323,324,5,116,0,0,324,325,
        5,105,0,0,325,76,1,0,0,0,326,327,5,109,0,0,327,328,5,105,0,0,328,
        329,5,108,0,0,329,330,5,105,0,0,330,78,1,0,0,0,331,332,5,109,0,0,
        332,333,5,105,0,0,333,334,5,99,0,0,334,335,5,114,0,0,335,336,5,111,
        0,0,336,80,1,0,0,0,337,338,5,110,0,0,338,339,5,97,0,0,339,340,5,
        110,0,0,340,341,5,111,0,0,341,82,1,0,0,0,342,343,5,112,0,0,343,344,
        5,105,0,0,344,345,5,99,0,0,345,346,5,111,0,0,346,84,1,0,0,0,347,
        348,5,102,0,0,348,349,5,101,0,0,349,350,5,109,0,0,350,351,5,116,
        0,0,351,352,5,111,0,0,352,86,1,0,0,0,353,354,5,97,0,0,354,355,5,
        116,0,0,355,356,5,116,0,0,356,357,5,111,0,0,357,88,1,0,0,0,358,359,
        5,122,0,0,359,360,5,101,0,0,360,361,5,112,0,0,361,362,5,116,0,0,
        362,363,5,111,0,0,363,90,1,0,0,0,364,365,5,121,0,0,365,366,5,111,
        0,0,366,367,5,99,0,0,367,368,5,116,0,0,368,369,5,111,0,0,369,92,
        1,0,0,0,370,371,5,109,0,0,371,372,5,101,0,0,372,373,5,116,0,0,373,
        374,5,101,0,0,374,375,5,114,0,0,375,94,1,0,0,0,376,377,5,103,0,0,
        377,378,5,114,0,0,378,379,5,97,0,0,379,380,5,109,0,0,380,96,1,0,
        0,0,381,382,5,116,0,0,382,383,5,111,0,0,383,384,5,110,0,0,384,98,
        1,0,0,0,385,386,5,115,0,0,386,387,5,101,0,0,387,388,5,99,0,0,388,
        389,5,111,0,0,389,390,5,110,0,0,390,391,5,100,0,0,391,100,1,0,0,
        0,392,393,5,97,0,0,393,394,5,109,0,0,394,395,5,112,0,0,395,396,5,
        101,0,0,396,397,5,114,0,0,397,398,5,101,0,0,398,102,1,0,0,0,399,
        400,5,107,0,0,400,401,5,101,0,0,401,402,5,108,0,0,402,403,5,118,
        0,0,403,404,5,105,0,0,404,405,5,110,0,0,405,104,1,0,0,0,406,407,
        5,109,0,0,407,408,5,111,0,0,408,409,5,108,0,0,409,410,5,101,0,0,
        410,106,1,0,0,0,411,412,5,99,0,0,412,413,5,97,0,0,413,414,5,110,
        0,0,414,415,5,100,0,0,415,416,5,101,0,0,416,417,5,108,0,0,417,418,
        5,97,0,0,418,108,1,0,0,0,419,420,5,112,0,0,420,421,5,97,0,0,421,
        422,5,115,0,0,422,423,5,99,0,0,423,424,5,97,0,0,424,425,5,108,0,
        0,425,110,1,0,0,0,426,427,5,74,0,0,427,428,5,111,0,0,428,429,5,117,
        0,0,429,430,5,108,0,0,430,112,1,0,0,0,431,432,5,43,0,0,432,114,1,
        0,0,0,433,434,5,45,0,0,434,116,1,0,0,0,435,436,5,37,0,0,436,118,
        1,0,0,0,437,438,5,46,0,0,438,120,1,0,0,0,439,441,5,45,0,0,440,439,
        1,0,0,0,440,441,1,0,0,0,441,442,1,0,0,0,442,443,3,129,64,0,443,122,
        1,0,0,0,444,446,5,45,0,0,445,444,1,0,0,0,445,446,1,0,0,0,446,448,
        1,0,0,0,447,449,3,129,64,0,448,447,1,0,0,0,448,449,1,0,0,0,449,450,
        1,0,0,0,450,451,5,46,0,0,451,457,3,129,64,0,452,454,7,0,0,0,453,
        455,5,45,0,0,454,453,1,0,0,0,454,455,1,0,0,0,455,456,1,0,0,0,456,
        458,3,129,64,0,457,452,1,0,0,0,457,458,1,0,0,0,458,124,1,0,0,0,459,
        460,5,116,0,0,460,461,5,114,0,0,461,462,5,117,0,0,462,469,5,101,
        0,0,463,464,5,102,0,0,464,465,5,97,0,0,465,466,5,108,0,0,466,467,
        5,115,0,0,467,469,5,101,0,0,468,459,1,0,0,0,468,463,1,0,0,0,469,
        126,1,0,0,0,470,472,5,94,0,0,471,470,1,0,0,0,471,472,1,0,0,0,472,
        474,1,0,0,0,473,475,7,1,0,0,474,473,1,0,0,0,475,479,1,0,0,0,476,
        478,7,2,0,0,477,476,1,0,0,0,478,481,1,0,0,0,479,477,1,0,0,0,479,
        480,1,0,0,0,480,128,1,0,0,0,481,479,1,0,0,0,482,484,7,3,0,0,483,
        482,1,0,0,0,484,485,1,0,0,0,485,483,1,0,0,0,485,486,1,0,0,0,486,
        130,1,0,0,0,487,493,5,34,0,0,488,489,5,92,0,0,489,492,9,0,0,0,490,
        492,8,4,0,0,491,488,1,0,0,0,491,490,1,0,0,0,492,495,1,0,0,0,493,
        491,1,0,0,0,493,494,1,0,0,0,494,496,1,0,0,0,495,493,1,0,0,0,496,
        508,5,34,0,0,497,503,5,39,0,0,498,499,5,92,0,0,499,502,9,0,0,0,500,
        502,8,5,0,0,501,498,1,0,0,0,501,500,1,0,0,0,502,505,1,0,0,0,503,
        501,1,0,0,0,503,504,1,0,0,0,504,506,1,0,0,0,505,503,1,0,0,0,506,
        508,5,39,0,0,507,487,1,0,0,0,507,497,1,0,0,0,508,132,1,0,0,0,509,
        511,7,6,0,0,510,509,1,0,0,0,511,512,1,0,0,0,512,510,1,0,0,0,512,
        513,1,0,0,0,513,514,1,0,0,0,514,515,6,66,0,0,515,134,1,0,0,0,516,
        517,5,47,0,0,517,518,5,42,0,0,518,522,1,0,0,0,519,521,9,0,0,0,520,
        519,1,0,0,0,521,524,1,0,0,0,522,523,1,0,0,0,522,520,1,0,0,0,523,
        525,1,0,0,0,524,522,1,0,0,0,525,526,5,42,0,0,526,527,5,47,0,0,527,
        528,1,0,0,0,528,529,6,67,0,0,529,136,1,0,0,0,530,531,5,47,0,0,531,
        532,5,47,0,0,532,536,1,0,0,0,533,535,8,7,0,0,534,533,1,0,0,0,535,
        538,1,0,0,0,536,534,1,0,0,0,536,537,1,0,0,0,537,540,1,0,0,0,538,
        536,1,0,0,0,539,541,7,8,0,0,540,539,1,0,0,0,540,541,1,0,0,0,541,
        542,1,0,0,0,542,543,6,68,0,0,543,138,1,0,0,0,544,545,9,0,0,0,545,
        140,1,0,0,0,21,0,440,445,448,454,457,468,471,474,477,479,485,491,
        493,501,503,507,512,522,536,540,1,6,0,0
    ]

class DeclarationLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    T__3 = 4
    T__4 = 5
    T__5 = 6
    T__6 = 7
    T__7 = 8
    T__8 = 9
    T__9 = 10
    T__10 = 11
    T__11 = 12
    T__12 = 13
    T__13 = 14
    T__14 = 15
    T__15 = 16
    T__16 = 17
    T__17 = 18
    T__18 = 19
    T__19 = 20
    T__20 = 21
    T__21 = 22
    T__22 = 23
    T__23 = 24
    T__24 = 25
    T__25 = 26
    T__26 = 27
    T__27 = 28
    T__28 = 29
    T__29 = 30
    T__30 = 31
    T__31 = 32
    T__32 = 33
    T__33 = 34
    T__34 = 35
    T__35 = 36
    T__36 = 37
    T__37 = 38
    T__38 = 39
    T__39 = 40
    T__40 = 41
    T__41 = 42
    T__42 = 43
    T__43 = 44
    T__44 = 45
    T__45 = 46
    T__46 = 47
    T__47 = 48
    T__48 = 49
    T__49 = 50
    T__50 = 51
    T__51 = 52
    T__52 = 53
    T__53 = 54
    T__54 = 55
    T__55 = 56
    T__56 = 57
    T__57 = 58
    T__58 = 59
    T__59 = 60
    ELONG = 61
    EDOUBLE = 62
    EBoolean = 63
    ID = 64
    INT = 65
    STRING = 66
    WS = 67
    ML_COMMENT = 68
    SL_COMMENT = 69
    ANY_OTHER = 70

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'model'", "'types'", "'group'", "':'", "'{'", "'}'", "'def'", 
            "','", "'='", "'required'", "'feature'", "'requires'", "'excludes'", 
            "'sub'", "'alternative'", "'multiple'", "'('", "')'", "'['", 
            "']'", "'range'", "'enum'", "'*'", "'/'", "'**'", "'noP'", "'yotta'", 
            "'zetta'", "'exa'", "'peta'", "'tera'", "'giga'", "'mega'", 
            "'kilo'", "'hecto'", "'deca'", "'deci'", "'centi'", "'mili'", 
            "'micro'", "'nano'", "'pico'", "'femto'", "'atto'", "'zepto'", 
            "'yocto'", "'meter'", "'gram'", "'ton'", "'second'", "'ampere'", 
            "'kelvin'", "'mole'", "'candela'", "'pascal'", "'Joul'", "'+'", 
            "'-'", "'%'", "'.'" ]

    symbolicNames = [ "<INVALID>",
            "ELONG", "EDOUBLE", "EBoolean", "ID", "INT", "STRING", "WS", 
            "ML_COMMENT", "SL_COMMENT", "ANY_OTHER" ]

    ruleNames = [ "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", 
                  "T__7", "T__8", "T__9", "T__10", "T__11", "T__12", "T__13", 
                  "T__14", "T__15", "T__16", "T__17", "T__18", "T__19", 
                  "T__20", "T__21", "T__22", "T__23", "T__24", "T__25", 
                  "T__26", "T__27", "T__28", "T__29", "T__30", "T__31", 
                  "T__32", "T__33", "T__34", "T__35", "T__36", "T__37", 
                  "T__38", "T__39", "T__40", "T__41", "T__42", "T__43", 
                  "T__44", "T__45", "T__46", "T__47", "T__48", "T__49", 
                  "T__50", "T__51", "T__52", "T__53", "T__54", "T__55", 
                  "T__56", "T__57", "T__58", "T__59", "ELONG", "EDOUBLE", 
                  "EBoolean", "ID", "INT", "STRING", "WS", "ML_COMMENT", 
                  "SL_COMMENT", "ANY_OTHER" ]

    grammarFileName = "Declaration.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None

