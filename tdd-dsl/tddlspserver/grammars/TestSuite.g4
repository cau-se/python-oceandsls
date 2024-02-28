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
 *  This grammar defines TDD-DSL for test-driven development.
 *
 *  author Sven Gundlach
 */
grammar TestSuite;

/** Imports include all rules, imported rules are overwritten by existing rules */
import Keyword, Typing, Reference, PhysicalUnits, CommonLexerRules;

/** Test_suite ; top-level rule; begin parsing here */
testSuite               : 'suite' name=ID ':' NEWLINE
                          (cases+=testCase)?           /** Ends on newline */
                          (cases+=testCase)*           /** Ends on newline */
                        ;

/** Test case ends on newline */
testCase                : 'test' name=ID ':' NEWLINE
                          (test_flags=testFlag)?               /** Ends on newline */
                          ()'srcpath' ':' srcpath=srcPath      /** Ends on newline */
                          (modules=useModules)?                /** Ends on newline */
                          (vars=testVars)?                     /** Ends on newline */
                          (assertions+=testAssertion)?         /** Ends on newline */
                          (assertions+=testAssertion)*         /** Ends on newline */
                        ;

testFlag                : 'overwrite' ':' overwriteFlag (',' overwriteFlag)* NEWLINE
                        ;

overwriteFlag           : 'pf'                                               # overwritePF
                        | 'cmake'                                            # overwriteCMake
                        | 'f90'                                              # overwriteF90
                        ;

/** Placeholder for code completion of system path to source code files; ends on newline */
srcPath                 : path=STRING NEWLINE
                        ;

/** Variables used in test case; ends on newline*/
testVars                : 'var' ':' NEWLINE
                          vars+=testVar+
                        ;

/** Variables used in test case*/
testVar                : decl=varDeclaration ('=' value=expr)? comment=optionalDesc  /** Ends on newline */
                        ;

/** Declaration of variables used in test cases  */
varDeclaration          : name=ID ':' type=paramType (',' keys+=f90StdKey (',' keys+=f90StdKey)*)?
                        ;

/** Modules used in the test; ends on newline*/
useModules              : 'modules' ':'  NEWLINE
                          modules+=testModule+
                        ;

/** Modules names; ends on newline*/
testModule              : name=ID NEWLINE
                        ;

/** Test assertion; ends on newline */
testAssertion           : 'assert' directive=testDirective ':' NEWLINE
                          'in' ':' NEWLINE input=extendedTestParameter /** Ends on newline */
                          'out' ':' NEWLINE output=testParameter       /** Ends on newline */
                          attr=pubAttributes (comment=COMMENT)?        /** Ends on newline */
                        ;

/** Arguments of pfUnit prepparser rules start with lowercase letters */
pubAttributes           : ('tolerance' ':' tol=expr NEWLINE)?
                          ('failmessage' ':' msg=STRING NEWLINE)?
                          ('whitespace' '=' ign='IGNORE_DIFFERENCES' NEWLINE)?       /** Option for assertEqual */
                        ;

/** Input for optional subroutine call; ends on newline */
extendedTestParameter   : ('call' ':' procedure NEWLINE                                  /** Ends on newline */
                          (procedure NEWLINE)*)?                                  /** Ends on newline */
                          testParameter                                                    /** Ends on newline */
                        ;

/** IO parameter; ends on newline */
testParameter          : (decl=parameterDeclaration '=')? value=expr comment=optionalDesc  /** Ends on newline */
                        ;

/** Optional description for declarations; ensures non description to be newline */
optionalDesc            : NEWLINE                                            # emptyDesc
                        | ',' type=unitSpec comment=optionalComment          # specDesc      /** Ends on newline */
                        ;

/** Ensure non comment to be newline */
optionalComment         : NEWLINE                                            # emptyComment
                        | comment=COMMENT                                    # specComment   /** Ends on newline */
                        ;

/** Optional IO parameter declaration */
parameterDeclaration    : name=reference                                     # nameDecl
                        | type=paramType                                     # typeDecl
                        | name=reference ':' type=paramType                  # combinedDecl
                        ;