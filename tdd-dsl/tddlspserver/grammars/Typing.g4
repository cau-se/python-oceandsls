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
 *  Typing and must match the filename: Typing.g4
 *
 *  This grammar defines object typing.
 *
 *  author Sven Gundlach
 */
grammar Typing;

/** Imports include all rules, imported rules are overwritten by existing rules */
import Reference, CommonLexerRules;

/** Parser rules start with lowercase letters */
paramType       : type=typeRef                                          # ref
                | type=enumType                                         # enm
                | type=arrayType                                        # array
                ;

typeRef         : type=reference
                ;

enumType        : '(' values+=enum ( ',' values+=enum)* ')'
                ;

enum            : name=reference ('=' value=INT)?
                ;

arrayType       : type=reference '[' dimensions+=dim (',' dimensions+=dim)* ']'
                ;

dim             : type=sizeDim                                          # size
                | type=rangeDim                                         # range
                ;

sizeDim         : (size=INT)?
                ;

rangeDim        : lowerBound=INT ':'
                |                ':' upperBound=INT
                | lowerBound=INT ':' upperBound=INT
                ;
