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
test_suite              : 'suite' name=ID ':' NEWLINE
                          (cases+=test_case)?           /** Ends on newline */
                          (cases+=test_case)*           /** Ends on newline */
                        ;

/** Test case ends on newline */
test_case               : 'test' name=ID ':' NEWLINE
                          (test_flags=test_flag)?               /** Ends on newline */
                          ()'srcpath' ':' srcpath=src_path      /** Ends on newline */
                          (modules=use_modules)?                /** Ends on newline */
                          (vars=test_vars)?                     /** Ends on newline */
                          (assertions+=test_assertion)?         /** Ends on newline */
                          (assertions+=test_assertion)*         /** Ends on newline */
                        ;

test_flag               : 'overwrite' ':' overwrite_flag (',' overwrite_flag)* NEWLINE
                        ;

overwrite_flag          : 'pf'                                               # overwritePF
                        | 'cmake'                                            # overwriteCMake
                        | 'f90'                                              # overwriteF90
                        ;

/** Placeholder for code completion of system path to source code files; ends on newline */
src_path                : path=STRING NEWLINE
                        ;

/** Variables used in test case; ends on newline*/
test_vars               : 'var' ':' NEWLINE
                          vars+=test_var+
                        ;

/** Variables used in test case*/
test_var                : decl=varDeclaration ('=' value=expr)? comment=optionalDesc  /** Ends on newline */
                        ;

/** Declaration of variables used in test cases  */
varDeclaration          : name=ID ':' type=paramType (',' keys+=f90StdKey (',' keys+=f90StdKey)*)?
                        ;

/** Modules used in the test; ends on newline*/
use_modules            : 'modules' ':'  NEWLINE
                          modules+=test_module+
                        ;

/** Modules names; ends on newline*/
test_module             : name=ID NEWLINE
                        ;

/** Test assertion; ends on newline */
test_assertion          : 'assert' directive=test_directive ':' NEWLINE
                          'in' ':' NEWLINE input=test_parameter     /** ends on newline */
                          'out' ':' NEWLINE output=test_parameter   /** ends on newline */
                          attr=pubAttributes (comment=COMMENT)?     /** ends on newline */
                        ;

/** Arguments of pfUnit prepparser rules start with lowercase letters */
pubAttributes           : ('tolerance' ':' tol=expr NEWLINE)?
                          ('failmessage' ':' msg=STRING NEWLINE)?
                          ('whitespace' '=' ign='IGNORE_DIFFERENCES' NEWLINE)?       /** Option for assertEqual */
                        ;

/** IO parameter; ends on newline */
test_parameter          : (decl=parameterDeclaration '=')? value=expr comment=optionalDesc  /** Ends on newline */
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