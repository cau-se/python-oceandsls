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
from generator.visitors.declaration_visitor import GeneratorDeclarationVisitor
from model.declaration_model import DeclarationModel, ParameterGroup, Parameter, FeatureGroup, Feature
from model.type_system import EnumeralType, Enumeral, RangeType, BaseType, ArrayType, Dimension, InlineEnumeralType, Enumeral
from model.unit_model import UnitSpecification, UnitKind, UnitPrefix, SIUnit, CustomUnit, DivisionUnit, ExponentUnit
from model.arithmetic_model import IntValue, StringValue, FloatValue, ArithmeticExpression, MultiplicationExpression, EMultiplicationOperator, EAdditionOperator
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken
from antlr4 import ParserRuleContext, TerminalNode
from antlr4.tree.Tree import TerminalNodeImpl

from dcllspserver.gen.python.Declaration.DeclarationLexer import DeclarationLexer
from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from common.logger import GeneratorLogger
from common.configuration import CompileFlags

class TestStream(InputStream):

    fileName = "test"

    def __init__(self, data: str) -> None:
        super().__init__(data)

class TestGeneratorDeclarationVisitor(unittest.TestCase):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def test_visitSiunit_no_prefix(self):
        # sIUnit                      :   (prefix=ePrefix)? type=eSIUnitType #siunit;
        ctx = DeclarationParser.SiunitContext(parser=None, ctx = DeclarationParser.SIUnitContext(parent=None, parser=None))
        ctx.prefix = None
        ctx.type_ = DeclarationParser.ESIUnitTypeContext(parser=None, parent=ctx)
        ctx.type_.meter = self.set_token("meter")

        result = self.make_visitor().visitSiunit(ctx)
        unit = SIUnit(kind=UnitKind.Meter, prefix=None)

        self.assertIsInstance(result, SIUnit, "Wrong type")
        self.assertEqual(result.prefix, None, "Wrong prefix")
        self.assertEqual(result.kind, UnitKind.Meter, "Wrong unit kind")

    def test_visitSiunit_prefix(self):
        # sIUnit                      :   (prefix=ePrefix)? type=eSIUnitType #siunit;
        ctx = DeclarationParser.SiunitContext(parser=None, ctx = DeclarationParser.SIUnitContext(parent=None, parser=None))
        ctx.prefix = DeclarationParser.EPrefixContext(parser=None, parent=ctx)
        ctx.prefix.kilo = self.set_token("kilo")
        ctx.type_ = DeclarationParser.ESIUnitTypeContext(parser=None, parent=ctx)
        ctx.type_.meter = self.set_token("meter")

        result = self.make_visitor().visitSiunit(ctx)
        unit = SIUnit(kind=UnitKind.Meter, prefix=None)

        self.assertIsInstance(result, SIUnit, "Wrong type")
        self.assertEqual(result.prefix, UnitPrefix.Kilo, "Wrong prefix")
        self.assertEqual(result.kind, UnitKind.Meter, "Wrong unit kind")

    def test_visitCustomunit(self):
        ctx = DeclarationParser.CustomunitContext(parser=None, ctx = DeclarationParser.CustomUnitContext(parser=None))
        ctx.name = self.set_token("gini")

        result = self.make_visitor().visitCustomunit(ctx)

        self.assertIsInstance(result, CustomUnit, "Wrong type")
        self.assertEqual(result.name, "gini", "Wrong type")

    def print_tree(self, ctx:ParserRuleContext, indent:str):
        print(f"T{indent} NODE {ctx} {type(ctx)}")
        if isinstance(ctx,TerminalNode):
            return
        for c in ctx.children:
            self.print_tree(c,indent + "  ")

    def test_visitUnitSpecification_code_one(self):
        model = self.parse_code("model eval group a : \"bla\" { def param int : meter } ")
        group:ParameterGroup = model._groups.get("a")
        parameter:Parameter = group._parameters.get("param")

        unit_meter = SIUnit(kind=UnitKind.Meter, prefix=None)

        p_unit:SIUnit = parameter._unit
        self.assertIsInstance(p_unit, SIUnit, "Wrong type")
        self.assertEqual(p_unit, unit_meter, "Wrong unit")

    def test_visitUnitSpecification_code_two(self):
        model = self.parse_code("model eval group a : \"bla\" { def param int : meter * \"gini\" } ")
        group:ParameterGroup = model._groups.get("a")
        parameter:Parameter = group._parameters.get("param")

        unit_meter = SIUnit(kind=UnitKind.Meter, prefix=None)
        unit_gini = CustomUnit(name="gini")

        p_unit:UnitSpecification = parameter._unit
        self.assertIsInstance(p_unit, UnitSpecification, "Wrong type")
        p_unit_meter = p_unit.units[0]
        p_unit_gini = p_unit.units[1]
        self.assertEqual(p_unit_meter, unit_meter, "Wrong unit")
        self.assertEqual(p_unit_gini, unit_gini, "Wrong unit")

    def test_visitUnitSpecification_one(self):
        ctx = DeclarationParser.UnitSpecificationContext(parser=None, parent=None)
        ctx_composed = DeclarationParser.ComposedUnitContext(parser=None, parent=ctx)
        ctx.addChild(ctx_composed)
        ctx.units.append(ctx_composed)
        ctx_si = DeclarationParser.BasicUnitContext(parser=None, parent=ctx_composed)
        ctx_composed.addChild(ctx_si)
        ctx_meter = DeclarationParser.SiunitContext(parser=None, ctx=ctx_si)
        ctx_si.addChild(ctx_meter)
        ctx_t = DeclarationParser.ESIUnitTypeContext(parser=None, parent=ctx_meter)
        ctx_meter.addChild(ctx_t)
        ctx_meter.type_ = ctx_t
        meter = self.set_terminal("meter")
        ctx_t.addChild(meter)
        ctx_t.meter = meter

        result:SIUnit = self.make_visitor().visitUnitSpecification(ctx)

        self.assertIsInstance(result, SIUnit, "Wrong type")
        self.assertEqual(result.kind, UnitKind.Meter, "Wrong unit kind")

    def test_visitUnitSpecification_two(self):
        ctx = DeclarationParser.UnitSpecificationContext(parser=None, parent=None)
        ctx_composed_meter = DeclarationParser.ComposedUnitContext(parser=None, parent=ctx)
        ctx.addChild(ctx_composed_meter)
        ctx.units.append(ctx_composed_meter)
        ctx_si = DeclarationParser.BasicUnitContext(parser=None, parent=ctx_composed_meter)
        ctx_composed_meter.addChild(ctx_si)
        ctx_meter = DeclarationParser.SiunitContext(parser=None, ctx=ctx_si)
        ctx_si.addChild(ctx_meter)
        ctx_t = DeclarationParser.ESIUnitTypeContext(parser=None, parent=ctx_meter)
        ctx_meter.addChild(ctx_t)
        ctx_meter.type_ = ctx_t
        meter = self.set_terminal("meter")
        ctx_t.addChild(meter)
        ctx_t.meter = meter

        ctx_composed_gini = DeclarationParser.ComposedUnitContext(parser=None, parent=ctx)
        ctx.addChild(ctx_composed_gini)
        ctx.units.append(ctx_composed_gini)
        ctx_basic = DeclarationParser.BasicUnitContext(parser=None, parent=ctx_composed_gini)
        ctx_composed_gini.addChild(ctx_basic)
        ctx_gini = DeclarationParser.CustomunitContext(parser=None, ctx=ctx_basic)
        ctx_basic.addChild(ctx_gini)
        gini:TerminalNodeImpl = self.set_terminal("\"gini\"")
        ctx_gini.addChild(gini)
        ctx_gini.name = gini.getSymbol()

        result:UnitSpecification = self.make_visitor().visitUnitSpecification(ctx)

        self.assertIsInstance(result, UnitSpecification, "Wrong type")
        self.assertEqual(len(result.units),2, "Wrong number of units")
        unit1:SIUnit = result.units[0]
        self.assertIsInstance(unit1, SIUnit, "Wrong type")
        self.assertEqual(unit1.kind, UnitKind.Meter, "Wrong unit kind")
        unit2:CustomUnit = result.units[1]
        self.assertIsInstance(unit2, CustomUnit, "Wrong type")
        self.assertEqual(unit2.name, "gini", "Wrong kind")


    def test_visitComposedUnit(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()
