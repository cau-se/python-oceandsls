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

import pytest

from odsllib.lsp.parsing import parse_source
from tddlspserver.gen.python.TestSuite.TestSuiteLexer import TestSuiteLexer
from tddlspserver.gen.python.TestSuite.TestSuiteParser import TestSuiteParser

DATA = os.path.join(os.path.dirname(__file__), "data")


def parse(text: str):
    return parse_source(text, TestSuiteLexer, TestSuiteParser, "testSuite")


def read(name: str) -> str:
    with open(os.path.join(DATA, name), encoding="utf-8") as f:
        return f.read()


def first_case(text: str):
    result = parse(text)
    assert result.diagnostics == [], [d.message for d in result.diagnostics]
    return result.tree.cases[0]


def assertion_unit(text: str, index: int = 0, side: str = "input"):
    """Return the unit spec context of an assertion's input/output parameter."""
    assertion = first_case(text).assertions[index]
    parameter = assertion.input_.testParameter() if side == "input" else assertion.output
    return parameter.comment.type_


HEADER = "suite su:\ntest t1:\n    srcpath: 'src'\n"


@pytest.mark.parametrize("name", ["paper_listing1.tdd", "paper_listing3.tdd"])
def test_paper_listings_parse_without_errors(name):
    result = parse(read(name))
    assert result.diagnostics == [], [d.message for d in result.diagnostics]
    assert len(result.tree.cases) == 1


def test_listing1_structure():
    case = first_case(read("paper_listing1.tdd"))
    assert case.name.text == "test_fT_ME"
    assert [f.getText() for f in case.test_flags.overwriteFlag()] == ["pf", "cmake"]
    assert case.srcpath.path.text == "'tdd-dsl/input/tdd_dev/UVic_example_opem'"
    assert [m.name.text for m in case.modules.modules] == ["cfo_example"]
    assert [v.decl.name.getText() for v in case.vars_.vars_] == ["dp", "xIntercept", "yIntercept"]
    assert len(case.assertions) == 2
    assert case.assertions[0].directive.getText() == "Equal"


def test_listing3_structure():
    case = first_case(read("paper_listing3.tdd"))
    test_box = case.vars_.vars_[1]
    assert test_box.decl.name.getText() == "test_box"
    assert [e.name.getText() for e in test_box.elements][:2] == ["salinity", "temperature"]
    assertion = case.assertions[0]
    assert assertion.input_.procedures[0].getText() == "test_env%co2(test_box,4)"


def test_compound_unit_with_negative_exponent():
    """'mol * kg ** -1' (paper Listing 3): kg is lexed as one identifier and '-1' as a signed number."""
    unit = assertion_unit(read("paper_listing3.tdd"))
    assert isinstance(unit, TestSuiteParser.MulDivUnitContext)
    assert isinstance(unit.right, TestSuiteParser.ExpUnitContext), "'**' must bind stronger than '*'"
    assert unit.getText() == "mol*kg**-1"


@pytest.mark.parametrize("unit", ["K", "m * s ** -2", "kg / m ** 3", "km", "(m / s) ** 2", "'ppm'", "m ** 2"])
def test_units(unit):
    text = HEADER + f"    assert Equal:\n        in:\n            1D0, {unit}\n        out:\n            1D0\n"
    assert assertion_unit(text).getText() == unit.replace(" ", "")


@pytest.mark.parametrize("name", ["t", "m", "s", "k", "K", "mol", "a"])
def test_unit_symbols_are_valid_variable_names(name):
    """Unit symbols are keywords of the unit sub-language but must remain usable as Fortran variable names."""
    text = HEADER + f"    var:\n        {name}: real = 1D0\n    assert Equal:\n        in:\n            f({name}), K\n" \
                    f"        out:\n            {name}\n"
    case = first_case(text)
    assert case.vars_.vars_[0].decl.name.getText() == name
    assert case.assertions[0].output.value.getText() == name


def test_sign_binds_stronger_than_addition():
    case = first_case(HEADER + "    var:\n        x: real = -a + b\n")
    value = case.vars_.vars_[0].value
    assert isinstance(value, TestSuiteParser.AddSubExprContext)
    assert isinstance(value.left, TestSuiteParser.SignExprContext)


@pytest.mark.parametrize("text, message_part", [
    ("suite su\n", "missing ':'"),
    ("suite su:\ntest t1:\n    modules:\n        m1\n", "modules"),  # srcpath is required
    ("suite su:\ntest t1:\n    srcpath: 'src'\n    assert Foo:\n", "Foo"),
])
def test_invalid_input_is_reported(text, message_part):
    result = parse(text)
    assert result.has_errors
    assert any(message_part in d.message for d in result.diagnostics), [d.message for d in result.diagnostics]
