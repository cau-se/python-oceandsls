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
 *  PhysicalUnits and must match the filename: PhysicalUnits.g4
 *
 *  This grammar defines the units for physical values.
 *
 *  author Sven Gundlach
 */
grammar PhysicalUnits;

/** Imports include all rules, imported rules are overwritten by existing rules */
import CommonLexerRules;

/** Arithmetic expression for value calculation */
unitSpec             : '(' type=unitSpec ')'                            # parensUnit    /** Parenthesized expression */
                        | left=unitSpec op=('*' | '/') right=unitSpec   # mulDivUnit    /** Multiplication, Division have precedence */
                        | type=unitSpec op='**' exponent=INT            # expUnit       /** Addition, Subtraction have not precedence */
                        | type=siUnit                                   # stdUnit
                        | type=customUnit                               # cstUnit
                        ;

siUnit          : (prefix=unitPrefix)? type=siType
                ;

customUnit      : name=STRING
                ;

/** SI prefixes */
unitPrefix      : value = 'noP' # noP
                | value = 'Q'   # quetta
                | value = 'R'   # ronna
                | value = 'Y'   # yotta
                | value = 'Z'   # zetta
                | value   = 'E' # exa
                | value  = 'P'  # peta
                | value  = 'T'  # tera
                | value  = 'G'  # giga
                | value  = 'M'  # mega
                | value  = 'k'  # kilo
                | value = 'h'   # hecto
                | value  = 'da' # deca
                | value  = 'd'  # deci
                | value = 'c'   # centi
                | value  = 'm'  # mili
                | value = 'μ'   # micro
                | value  = 'n'  # nano
                | value  = 'p'  # pico
                | value = 'f'   # femto
                | value  = 'a'  # atto
                | value = 'z'   # zepto
                | value = 'y'   # yocto
                | value = 'r'   # ronto
                | value = 'q'   # quecto
                ;

/** SI Unit symbols */
siType          : value = 's'   # second
                | value = 'm'   # metre
                | value = 'g'   # gram
                | value = 'A'   # ampere
                | value = 'K'   # kelvin
                | value = 'mol' # mole
                | value = 'cd'  # candela
                | value = 'Pa'  # pascal
                | value = 'J'   # joule
                | value = 't'   # ton
                ;
