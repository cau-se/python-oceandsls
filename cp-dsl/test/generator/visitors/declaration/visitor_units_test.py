#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributedBaseType on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

__author__ = "reiner"

import unittest

from parameterized import parameterized

from cpdsl.model.declaration_model import DeclarationModel, ParameterGroup, Parameter
from cpdsl.model.unit_model import UnitSpecification, UnitKind, UnitPrefix, SIUnit, CustomUnit, DivisionUnit, \
    ExponentUnit

from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.configuration import CompileFlags

from generator.visitors.test_utils import AbstractTestGeneratorDeclarationVisitor

METER = SIUnit(kind=UnitKind.Meter, prefix=None)
GINI = CustomUnit(name="gini")


class TestUnitGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    logger = GeneratorLogger(CompileFlags.STRICT)

    @parameterized.expand([
        ("no_prefix", None, "meter", None, UnitKind.Meter),
        # sIUnit : (prefix=ePrefix)? type=eSIUnitType #siunit; without prefix
        # Input: the unit type meter without prefix
        # Expected Result: meter without prefix

        ("prefix", "kilo", "meter", UnitPrefix.Kilo, UnitKind.Meter),
        # A unit with prefix
        # Input: the prefix kilo and the unit type meter
        # Expected Result: kilometer

        ("other_unit", "mega", "gram", UnitPrefix.Mega, UnitKind.Gram),
        # Another prefix and unit type
        # Input: the prefix mega and the unit type gram
        # Expected Result: megagram

        ("unit_without_prefix", None, "second", None, UnitKind.Second),
        # Another unit type without prefix
        # Input: the unit type second
        # Expected Result: second without prefix
    ])
    def test_visitSiunit(self, test_name, prefix, kind, expected_prefix, expected_kind):
        ctx = DeclarationParser.SiunitContext(parser=None,
                                              ctx=DeclarationParser.SIUnitContext(parent=None, parser=None))
        ctx.prefix = None
        if prefix is not None:
            ctx.prefix = DeclarationParser.EPrefixContext(parser=None, parent=ctx)
            setattr(ctx.prefix, prefix, self.set_token(prefix))
        ctx.type_ = DeclarationParser.ESIUnitTypeContext(parser=None, parent=ctx)
        setattr(ctx.type_, kind, self.set_token(kind))

        result = self.make_visitor().visitSiunit(ctx)

        self.assertIsInstance(result, SIUnit, test_name)
        self.assertEqual(expected_prefix, result.prefix, test_name)
        self.assertEqual(expected_kind, result.kind, test_name)

    @parameterized.expand([
        ("name", "\"gini\"", "gini"),
        # The quotes of a custom unit are removed
        # Input: the custom unit "gini"
        # Expected Result: the custom unit gini

        ("name_with_space", "\"mol photons\"", "mol photons"),
        # Custom units may contain spaces
        # Input: the custom unit "mol photons"
        # Expected Result: the custom unit mol photons

        ("percent", "\"%\"", "%"),
        # Custom units may be symbols
        # Input: the custom unit "%"
        # Expected Result: the custom unit %
    ])
    def test_visitCustomunit(self, test_name, name, expected_name):
        ctx = DeclarationParser.CustomunitContext(parser=None, ctx=DeclarationParser.CustomUnitContext(parser=None))
        ctx.name = self.set_token(name)

        result = self.make_visitor().visitCustomunit(ctx)

        self.assertIsInstance(result, CustomUnit, test_name)
        self.assertEqual(expected_name, result.name, test_name)

    @parameterized.expand([
        ("one_unit", "meter", METER),
        # A single unit is not wrapped into a unit specification
        # Input: 'def param int : meter'
        # Expected Result: meter

        ("prefixed_unit", "kilo meter", SIUnit(kind=UnitKind.Meter, prefix=UnitPrefix.Kilo)),
        # A unit with prefix
        # Input: 'def param int : kilo meter'
        # Expected Result: kilometer

        ("two_units", "meter * \"gini\"", UnitSpecification(units=[METER, GINI])),
        # A product of units
        # Input: 'def param int : meter * "gini"'
        # Expected Result: a unit specification of meter and gini

        ("division", "\"num\" / \"denominator\"", DivisionUnit(numerator=CustomUnit(name="num"),
                                                               denominator=CustomUnit(name="denominator"))),
        # A division of custom units
        # Input: 'def param int : "num" / "denominator"'
        # Expected Result: num divided by denominator

        ("si_division", "kilo gram / second", DivisionUnit(
            numerator=SIUnit(kind=UnitKind.Gram, prefix=UnitPrefix.Kilo),
            denominator=SIUnit(kind=UnitKind.Second, prefix=None))),
        # A division of SI units
        # Input: 'def param int : kilo gram / second'
        # Expected Result: kilogram divided by second

        ("exponent", "meter ** 2", ExponentUnit(unit=METER, exponent=2)),
        # A unit with exponent
        # Input: 'def param int : meter ** 2'
        # Expected Result: meter to the power of 2
    ])
    def test_visitUnitSpecification_code(self, test_name, unit_code, expected_unit):
        model: DeclarationModel = self.parse_code(f"model eval group a : \"bla\" {{ def param int : {unit_code} }} ")
        group: ParameterGroup = model.groups.get("a")
        parameter: Parameter = group.parameters.get("param")

        self.assertEqual(expected_unit, parameter.unit, test_name)

    def unit_specification_context(self, units):
        """A unitSpecification context of composed units, each an SI unit type or a quoted custom unit."""
        ctx = DeclarationParser.UnitSpecificationContext(parser=None, parent=None)
        for unit in units:
            ctx_composed = DeclarationParser.ComposedUnitContext(parser=None, parent=ctx)
            ctx.addChild(ctx_composed)
            ctx.units.append(ctx_composed)
            ctx_basic = DeclarationParser.BasicUnitContext(parser=None, parent=ctx_composed)
            ctx_composed.addChild(ctx_basic)
            terminal = self.set_terminal(unit)
            if unit.startswith("\""):
                ctx_custom = DeclarationParser.CustomunitContext(parser=None, ctx=ctx_basic)
                ctx_basic.addChild(ctx_custom)
                ctx_custom.addChild(terminal)
                ctx_custom.name = terminal.getSymbol()
            else:
                ctx_si = DeclarationParser.SiunitContext(parser=None, ctx=ctx_basic)
                ctx_basic.addChild(ctx_si)
                ctx_type = DeclarationParser.ESIUnitTypeContext(parser=None, parent=ctx_si)
                ctx_si.addChild(ctx_type)
                ctx_si.type_ = ctx_type
                ctx_type.addChild(terminal)
                setattr(ctx_type, unit, terminal)
        return ctx

    @parameterized.expand([
        ("one_si_unit", ["meter"], METER),
        # A specification of one unit is that unit
        # Input: a unit specification context with meter
        # Expected Result: meter

        ("si_and_custom_unit", ["meter", "\"gini\""], UnitSpecification(units=[METER, GINI])),
        # Several units form a unit specification
        # Input: a unit specification context with meter and "gini"
        # Expected Result: a unit specification of meter and gini

        ("one_custom_unit", ["\"gini\""], GINI),
        # A specification of one custom unit is that unit
        # Input: a unit specification context with "gini"
        # Expected Result: gini

        ("three_units", ["meter", "second", "\"gini\""],
         UnitSpecification(units=[METER, SIUnit(kind=UnitKind.Second, prefix=None), GINI])),
        # Three units
        # Input: a unit specification context with meter, second and "gini"
        # Expected Result: a unit specification of meter, second and gini
    ])
    def test_visitUnitSpecification(self, test_name, units, expected_unit):
        result = self.make_visitor().visitUnitSpecification(self.unit_specification_context(units))
        self.assertEqual(expected_unit, result, test_name)


if __name__ == '__main__':
    unittest.main()
