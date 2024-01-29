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
 *  This grammar defines keywords used for unit test description.
 *   - Types of preprocessing directives for pfUnit 4.0.
 *   - src: https://github.com/Goddard-Fortran-Ecosystem/pFUnit/blob/main/documentation/pFUnit3-ReferenceManual.pdf
 *
 *  author Sven Gundlach
 */
grammar Keyword;

/** Parser rules start with lowercase letters */
f90StdKey       : keyword  = 'ALLOCATABLE'              # arraySpec
                | keyword  = 'DIMENSION'                # arraySpec
                | keyword  = 'INTENT(IN)'               # argSpecInput
                | keyword  = 'INTENT(INOUT)'            # argSpecInOutput
                | keyword  = 'INTENT(OUT)'              # argSpecOutput
                | keyword  = 'PARAMETER'                # constantSpec
                | keyword  = STRING                     # customKey
                ;

/** Parser rules start with lowercase letters */
test_directive  : ppDirective  = 'NotAssociated'        /** @assertNotAssociated(xPtr) */
                | ppDirective  = 'Associated'           /** @assertAssociated(xPtr) */
                | ppDirective  = 'Fail'                 /** @assertfail(message='0') */
                | ppDirective  = 'ExceptionRaised'      /** @assertExceptionRaised(new_line('a')//'Expected: is <2>' // new_line('a') // '     but: was <1>') */
                | ppDirective  = 'True'                 /** @asserttrue(1 == 1, message='1') */
                | ppDirective  = 'False'                /** @assertfalse(1 == 2, message='1') */
                | ppDirective  = 'EqualUserDefined'     /** @assertEqualUserDefined(1,1, message='2') */
                | ppDirective  = 'All'                  /** @assertall([.true., .true.], message='1') */
                | ppDirective  = 'None'                 /** @assertnone([.false., .false.], message='1') */
                | ppDirective  = 'Any'                  /** @assertany([.true., .false.], message='1') */
                | ppDirective  = 'NotAll'               /** @assertnotall([.true., .false.], message='1') */
                | ppDirective  = 'SameShape'            /** @assertsameshape(a1, a2, message='2') */
                | ppDirective  = 'IsNaN'                /** @assertisnan(nan, message='1') */
                | ppDirective  = 'IsFinite'             /** @assertisfinite(1D0, message='1') */
                | ppDirective  = 'Equivalent'           /** @assertEquivalent(YES,YES, message='1') */
                /** tolarance only if input is of type real; D only if of type REAL(KIND(1D0)) */
                | ppDirective  = 'LessThan'             /** @assertlessthan( 1, 2.0, message='2', tolerance=1E-12) */
                | ppDirective  = 'LessThanOrEqual'      /** @assertlessthanorequal( 2, 2.0, message='2', tolerance=1E-12) */
                | ppDirective  = 'GreaterThan'          /** @assertgreaterthan( 2, 1.0, message='2', tolerance=1E-12) */
                | ppDirective  = 'GreaterThanOrEqual'   /** @assertgreaterthanorequal( 2, 2.0, message='2', tolerance=1E-12) 1D-12 if input of KIND() */
                | ppDirective  = 'Equal'                /** @assertequal( 1, 1, message='2', tolerance=1E-12) 1D-12 if input of KIND() */
                | ppDirective  = 'NotEqual'             /** @assertnotequal( 1, 2, message='2', tolerance=1E-12) 1D-12 if input of KIND() */
                | ppDirective  = 'RelativelyEqual'      /** @assertRelativelyEqual( 2, 2.0, message='2', tolerance=1E-12) 1D-12 if input of KIND() */
                | ppDirective  = '_that'                /** @assert_that(1, is(equal_to(1))) */
//                | ppDirective  = 'IsMemberOf'         /** Not Implemented */
//                | ppDirective  = 'Contains'           /** Not Implemented */
//                | ppDirective  = 'IsPermutationOf'    /** Not Implemented */
                ;