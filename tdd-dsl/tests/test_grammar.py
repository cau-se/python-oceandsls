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
"""Grammar tests based on the examples of the TDD-DSL paper (Gundlach et al., Listings 1 and 3)."""

import os
import unittest

from parameterized import parameterized

from odsllib.lsp.parsing import parse_source
from tddlspserver.gen.python.TestSuite.TestSuiteLexer import TestSuiteLexer
from tddlspserver.gen.python.TestSuite.TestSuiteParser import TestSuiteParser

DATA = os.path.join(os.path.dirname(__file__), "data")


def parse(text: str):
    return parse_source(text, TestSuiteLexer, TestSuiteParser, "testSuite")


def read(name: str) -> str:
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return f.read()


HEADER = "suite su:\ntest t1:\n    srcpath: 'src'\n"
LISTING1 = read("paper_listing1.tdd")
LISTING3 = read("paper_listing3.tdd")


def unit_assertion(unit: str) -> str:
    return HEADER + f"    assert Equal:\n        in:\n            1D0, {unit}\n        out:\n            1D0\n"


def type_of(context, attribute: str):
    """The context class of a child (left, right), None if the context has no such child."""
    child = getattr(context, attribute, None)
    return None if child is None else type(child)


class TestGrammar(unittest.TestCase):

    def first_case(self, text: str):
        result = parse(text)
        self.assertEqual([], [d.message for d in result.diagnostics])
        return result.tree.cases[0]

    def assertion_unit(self, text: str):
        """The unit spec context of the first assertion's input parameter."""
        return self.first_case(text).assertions[0].input_.testParameter().comment.type_

    @parameterized.expand([
        ("paper_listing1", LISTING1, 1),
        # The test case of Listing 1 of the paper
        # Input: tests/data/paper_listing1.tdd
        # Expected Result: no diagnostics, one test case

        ("paper_listing3", LISTING3, 1),
        # The test case of Listing 3 of the paper
        # Input: tests/data/paper_listing3.tdd
        # Expected Result: no diagnostics, one test case

        ("minimal_suite", HEADER, 1),
        # A test case with only the required source path
        # Input: suite su, test t1 with srcpath 'src'
        # Expected Result: no diagnostics, one test case

        ("two_test_cases", HEADER + "test t2:\n    srcpath: 'b'\n", 2),
        # A suite with several test cases
        # Input: test cases t1 and t2, each with a source path
        # Expected Result: no diagnostics, two test cases
    ])
    def test_valid_input_parses_without_errors(self, test_name, text, expected_cases):
        result = parse(text)
        self.assertEqual([], [d.message for d in result.diagnostics], test_name)
        self.assertEqual(expected_cases, len(result.tree.cases), test_name)

    @parameterized.expand([
        ("listing1_name", LISTING1, lambda case: case.name.text, "test_fT_ME"),
        # The name of the test case
        # Input: paper Listing 1
        # Expected Result: 'test_fT_ME'

        ("listing1_flags", LISTING1, lambda case: [f.getText() for f in case.test_flags.overwriteFlag()],
         ["pf", "cmake"]),
        # The overwrite flags
        # Input: paper Listing 1
        # Expected Result: 'pf' and 'cmake'

        ("listing1_srcpath", LISTING1, lambda case: case.srcpath.path.text,
         "'tdd-dsl/input/tdd_dev/UVic_example_opem'"),
        # The source path
        # Input: paper Listing 1
        # Expected Result: the quoted path of the UVic example

        ("listing1_modules", LISTING1, lambda case: [m.name.text for m in case.modules.modules], ["cfo_example"]),
        # The modules under test
        # Input: paper Listing 1
        # Expected Result: 'cfo_example'

        ("listing1_variables", LISTING1, lambda case: [v.decl.name.getText() for v in case.vars_.vars_],
         ["dp", "xIntercept", "yIntercept"]),
        # The declared variables
        # Input: paper Listing 1
        # Expected Result: 'dp', 'xIntercept' and 'yIntercept'

        ("listing1_assertions", LISTING1, lambda case: len(case.assertions), 2),
        # The number of assertions
        # Input: paper Listing 1
        # Expected Result: 2

        ("listing1_directive", LISTING1, lambda case: case.assertions[0].directive.getText(), "Equal"),
        # The directive of the first assertion
        # Input: paper Listing 1
        # Expected Result: 'Equal'

        ("listing3_derived_type", LISTING3, lambda case: case.vars_.vars_[1].decl.name.getText(), "test_box"),
        # A variable of a derived type
        # Input: paper Listing 3
        # Expected Result: the second variable is 'test_box'

        ("listing3_elements", LISTING3, lambda case: [e.name.getText() for e in case.vars_.vars_[1].elements][:2],
         ["salinity", "temperature"]),
        # The elements of the derived type variable
        # Input: paper Listing 3
        # Expected Result: the first elements are 'salinity' and 'temperature'

        ("listing3_procedure", LISTING3, lambda case: case.assertions[0].input_.procedures[0].getText(),
         "test_env%co2(test_box,4)"),
        # A type-bound procedure call as input
        # Input: paper Listing 3
        # Expected Result: 'test_env%co2(test_box,4)'
    ])
    def test_case_structure(self, test_name, text, select, expected):
        self.assertEqual(expected, select(self.first_case(text)), test_name)

    @parameterized.expand([
        ("paper_listing3", LISTING3, TestSuiteParser.MulDivUnitContext, TestSuiteParser.StdUnitContext,
         TestSuiteParser.ExpUnitContext, "mol*kg**-1"),
        # 'mol * kg ** -1': kg is lexed as one identifier, '-1' as a signed number and '**' binds stronger than '*'
        # Input: paper Listing 3
        # Expected Result: a product of 'mol' and the power 'kg ** -1'

        ("negative_exponent", unit_assertion("m * s ** -2"), TestSuiteParser.MulDivUnitContext,
         TestSuiteParser.StdUnitContext, TestSuiteParser.ExpUnitContext, "m*s**-2"),
        # A negative exponent of the right factor
        # Input: unit 'm * s ** -2'
        # Expected Result: a product of 'm' and the power 's ** -2'

        ("division", unit_assertion("kg / m ** 3"), TestSuiteParser.MulDivUnitContext,
         TestSuiteParser.StdUnitContext, TestSuiteParser.ExpUnitContext, "kg/m**3"),
        # '**' binds stronger than '/'
        # Input: unit 'kg / m ** 3'
        # Expected Result: a quotient of 'kg' and the power 'm ** 3'

        ("parenthesized_base", unit_assertion("(m / s) ** 2"), TestSuiteParser.ExpUnitContext, None, None,
         "(m/s)**2"),
        # Parentheses group the base of a power
        # Input: unit '(m / s) ** 2'
        # Expected Result: a power of the parenthesized quotient
    ])
    def test_compound_units(self, test_name, text, expected_type, expected_left, expected_right, expected_text):
        unit = self.assertion_unit(text)
        self.assertIsInstance(unit, expected_type, test_name)
        self.assertEqual((expected_left, expected_right), (type_of(unit, "left"), type_of(unit, "right")), test_name)
        self.assertEqual(expected_text, unit.getText(), test_name)

    @parameterized.expand([
        ("si_unit", "K", "K"),
        # An SI base unit
        # Input: unit 'K'
        # Expected Result: 'K'

        ("acceleration", "m * s ** -2", "m*s**-2"),
        # A product with a negative exponent
        # Input: unit 'm * s ** -2'
        # Expected Result: 'm*s**-2'

        ("density", "kg / m ** 3", "kg/m**3"),
        # A quotient with a power
        # Input: unit 'kg / m ** 3'
        # Expected Result: 'kg/m**3'

        ("prefixed_unit", "km", "km"),
        # A unit with an SI prefix
        # Input: unit 'km'
        # Expected Result: 'km'

        ("parenthesized_unit", "(m / s) ** 2", "(m/s)**2"),
        # A power of a parenthesized unit
        # Input: unit '(m / s) ** 2'
        # Expected Result: '(m/s)**2'

        ("custom_unit", "'ppm'", "'ppm'"),
        # A custom unit as a string
        # Input: unit "'ppm'"
        # Expected Result: "'ppm'"

        ("area", "m ** 2", "m**2"),
        # A power of a unit
        # Input: unit 'm ** 2'
        # Expected Result: 'm**2'
    ])
    def test_units(self, test_name, unit, expected):
        self.assertEqual(expected, self.assertion_unit(unit_assertion(unit)).getText(), test_name)

    @parameterized.expand([
        ("tonne", "t"),
        # The unit symbol of tonnes is a valid variable name
        # Input: variable 't'
        # Expected Result: declared, referenced and used as output as 't'

        ("metre", "m"),
        # The unit symbol of metres
        # Input: variable 'm'
        # Expected Result: 'm' everywhere

        ("second", "s"),
        # The unit symbol of seconds
        # Input: variable 's'
        # Expected Result: 's' everywhere

        ("kilo", "k"),
        # The SI prefix kilo
        # Input: variable 'k'
        # Expected Result: 'k' everywhere

        ("kelvin", "K"),
        # The unit symbol of kelvin
        # Input: variable 'K'
        # Expected Result: 'K' everywhere

        ("mole", "mol"),
        # The unit symbol of moles
        # Input: variable 'mol'
        # Expected Result: 'mol' everywhere

        ("atto", "a"),
        # The SI prefix atto
        # Input: variable 'a'
        # Expected Result: 'a' everywhere
    ])
    def test_unit_symbols_are_valid_variable_names(self, test_name, name):
        """Unit symbols are keywords of the unit sub-language but must remain usable as Fortran variable names."""
        text = HEADER + f"    var:\n        {name}: real = 1D0\n    assert Equal:\n" \
                        f"        in:\n            f({name}), K\n        out:\n            {name}\n"
        case = self.first_case(text)
        self.assertEqual(name, case.vars_.vars_[0].decl.name.getText(), test_name)
        self.assertEqual(name, case.assertions[0].output.value.getText(), test_name)

    @parameterized.expand([
        ("sign_of_left_summand", "-a + b", TestSuiteParser.AddSubExprContext, TestSuiteParser.SignExprContext,
         TestSuiteParser.RefExprContext),
        # The sign binds stronger than the addition
        # Input: '-a + b'
        # Expected Result: a sum of '-a' and 'b'

        ("sign_of_right_summand", "a + -b", TestSuiteParser.AddSubExprContext, TestSuiteParser.RefExprContext,
         TestSuiteParser.SignExprContext),
        # A sign after the operator
        # Input: 'a + -b'
        # Expected Result: a sum of 'a' and '-b'

        ("sign_of_factor", "-a * b", TestSuiteParser.MulDivExprContext, TestSuiteParser.SignExprContext,
         TestSuiteParser.RefExprContext),
        # The sign binds stronger than the multiplication
        # Input: '-a * b'
        # Expected Result: a product of '-a' and 'b'

        ("subtraction", "a - b", TestSuiteParser.AddSubExprContext, TestSuiteParser.RefExprContext,
         TestSuiteParser.RefExprContext),
        # A binary minus is no sign
        # Input: 'a - b'
        # Expected Result: a difference of 'a' and 'b'
    ])
    def test_sign_precedence(self, test_name, expression, expected_type, expected_left, expected_right):
        value = self.first_case(HEADER + f"    var:\n        x: real = {expression}\n").vars_.vars_[0].value
        self.assertIsInstance(value, expected_type, test_name)
        self.assertEqual((expected_left, expected_right), (type(value.left), type(value.right)), test_name)

    @parameterized.expand([
        ("missing_colon", "suite su\n", "missing ':'"),
        # The suite header needs a colon
        # Input: 'suite su' without colon
        # Expected Result: an error mentioning the missing ':'

        ("missing_srcpath", "suite su:\ntest t1:\n    modules:\n        m1\n", "modules"),
        # The source path is required before the modules
        # Input: a test case with modules but without srcpath
        # Expected Result: an error at 'modules'

        ("unknown_directive", "suite su:\ntest t1:\n    srcpath: 'src'\n    assert Foo:\n", "Foo"),
        # Only the known assertion directives are accepted
        # Input: 'assert Foo:'
        # Expected Result: an error mentioning 'Foo'

        ("missing_suite_name", "suite:\n", "missing ID"),
        # The suite needs a name
        # Input: 'suite:'
        # Expected Result: an error about the missing identifier

        ("missing_variable_colon", HEADER + "    var:\n        x real\n", "missing ':' at 'real'"),
        # A variable declaration separates name and type by a colon
        # Input: 'x real'
        # Expected Result: an error about the missing ':' before 'real'
    ])
    def test_invalid_input_is_reported(self, test_name, text, message_part):
        result = parse(text)
        messages = [d.message for d in result.diagnostics]
        self.assertTrue(result.has_errors, test_name)
        self.assertTrue(any(message_part in message for message in messages), f"{test_name}: {messages}")


if __name__ == '__main__':
    unittest.main()
