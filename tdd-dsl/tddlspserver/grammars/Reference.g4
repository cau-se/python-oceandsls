/**
 *  Copyright (C) 2021 OceanDSL (https://oceandsl.uni-kiel.de)
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Grammars always start with a grammar header. This grammar is called
 *  TestDrivenDev and must match the filename: TestDrivenDev.g4
 *
 *  This grammars defines referenceable rules
 *
 *  author Sven Gundlach
 */
grammar Reference;

/** Imports include all rules, imported rules are overwritten by existing rules */
import CommonLexerRules;

/** Arithmetic expression for value calculation */
expr                    : '(' inner=expr ')'                                # parensExpr    /** Parenthesized expression */
                        | left=expr op=('*' | '/') right=expr               # mulDivExpr    /** Multiplication, Division have precedence */
                        | left=expr op=('+' | '-') right=expr               # addSubExpr    /** Addition, Subtraction have not precedence */
                        | op=('+' | '-') inner=expr                         # signExpr
                        | value=(NUM | DP)                                  # numberExpr
                        | value=STRING                                      # strExpr
                        | value=INT                                         # intExpr
                        | value=reference                                   # refExpr
                        ;

/** Procedure or variables to lookup in the symboltable */
reference               : procedure                                         # funRef        /** Function call like f(), f(x), f(1,2) */
                        | name=varID                                        # varRef
                        ;

/** Procedure to lookup in the symboltable and for direct call */
procedure               : name=varID '(' (args+=expr(',' args+=expr)*)? ')' # prcRef   /** Procedure call like f(), f(x), f(1,2) */
                        ;

varID                   : baseName=ID ('%' elementName=ID)?
                        ;