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
from model.declaration_model import DeclarationModel, ParameterGroup, Parameter
from model.type_system import EnumeralType, Enumeral, RangeType, BaseType
from model.unit_model import UnitSpecification, UnitKind, UnitPrefix, SIUnit, CustomUnit, DivisionUnit, ExponentUnit
from model.arithmetic_model import IntValue, StringValue, FloatValue
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

    def test_visitDeclarationModel(self):
        model = self.parse_code("model eval")
        self.assertEqual(model.name, "eval", "Name not set")

    def test_visitDeclaredType(self):
        self.fail()

    def test_visitRangeType(self):
        model = self.parse_code("model eval types range Temperature int [0: 273]")

        result = model._types.get("Temperature")
        self.assertIsInstance(result, RangeType, "Not the correct data type")
        self.assertEqual(result.minimum, 0, "Wrong minimum")
        self.assertEqual(result.maximum, 273, "Wrong maximum")

    def test_visitEnumerationType(self):
        model = self.parse_code("model eval types enum Color { red, green, blue }")

        result = model._types.get("Color")
        self.assertIsInstance(result, EnumeralType, "Not the correct data type")
        enumerals = {"red":0, "green":1, "blue":2}
        enums = {}
        for e in enumerals.items():
            enums[e[0]] = Enumeral(e[0], e[1])
        expected = EnumeralType("Color", enumerals=enums)

        self.assertEqual(result.name, expected.name, "Names do not match")
        self.assertEqual(result._enumerals, expected._enumerals, "Not the same symbols")

    def test_visitEnumeral(self):
        ctx = DeclarationParser.EnumeralContext(parent=None, parser=None, invokingState=1)
        ctx.name = self.set_token("red")
        ctx.value = self.set_token("0")

        result = self.make_visitor().visitEnumeral(ctx)

        self.assertIsInstance(result, Enumeral, f"Wrong type {type(result)}")
        self.assertEqual(result.name, "red", "Wrong name")
        self.assertEqual(result.value, 0)

    def test_visitParamGroupAssignStat(self):
        ctx = DeclarationParser.ParamGroupAssignStatContext(parser=None, ctx=DeclarationParser.DeclarationModelContext(parser=None))
        ctx.name = self.set_token("group_name")
        ctx.description = self.set_token("\"group description\"")

        result = self.make_visitor().visitParamGroupAssignStat(ctx)

        self.assertIsInstance(result, ParameterGroup, f"Wrong type {type(result)}")
        self.assertEqual(result.name, "group_name", "Wrong name")
        self.assertEqual(result._description, "group description", "Wrong description")

    def test_visitParamAssignStat(self):
        model = self.parse_code("model eval group g : \"group description\" { def param1 int : meter = 0 }")

        group:ParameterGroup = model._groups.get("g")

        self.assertIsInstance(group, ParameterGroup, f"Wrong type {type(group)}")
        self.assertEqual(group.name, "g", "Wrong name")
        self.assertEqual(group._description, "group description", "Wrong description")

        t = BaseType("int")
        for p in group._parameters.values():
            self.assertEqual(p.name, "param1", "Wrong param name")
            self.assertEqual(p._type, t, "Wrong type")
            # TODO
#            self.assertEqual(p._unit, u, "Should be meter")
            self.assertEqual(p._default_value.value, 0, "Wrong value")
            self.assertEqual(p._description, "", "Wrong description")


    def test_visitParamType(self):
        self.fail()

    def test_visitArrayType(self):
        self.fail()

    def test_visitSizeDimension(self):
        self.fail()

    def test_visitRangeDimension(self):
        self.fail()

    def test_visitTypeReference(self):
        typeReference = DeclarationParser.TypeReferenceContext(parent=None, parser=None)
        typeReference.type_ = self.set_token("r")

        result = self.make_visitor(type=RangeType(name="r", type=int, minimum=0, maximum=10)).visitTypeReference(typeReference)

        self.assertIsInstance(result, RangeType, "wrong type")
        self.assertEqual(result.name, "r", "wrong type name")

    def test_visitFeatureAssignStat(self):
        self.fail()

    def test_visitFeatureGroupAssignStat(self):
        self.fail()

    def test_visitEKind(self):
        self.fail()

    def test_visitArithmeticExpression(self):
        self.fail()

    def test_visitMultiplicationExpression(self):
        self.fail()

    def test_visitValueExpression_parenthesis(self):
        ctx = DeclarationParser.ValueExpressionContext(parser=None, parent=None)
        parenthesisExpression = DeclarationParser.ParenthesisExpressionContext(parent=ctx, parser=None)
        ctx.addChild(parenthesisExpression)
        arithmeticExpression = DeclarationParser.ArithmeticExpressionContext(parent=parenthesisExpression, parser=None)
        parenthesisExpression.addChild(arithmeticExpression)
        multiplicationExpression = DeclarationParser.MultiplicationExpressionContext(parent=arithmeticExpression, parser=None)
        arithmeticExpression.addChild(multiplicationExpression)
        valueExpression = DeclarationParser.ValueExpressionContext(parser=multiplicationExpression, parent=None)
        multiplicationExpression.addChild(valueExpression)
        literalExpression = DeclarationParser.LiteralExpressionContext(parent=valueExpression, parser=None)
        valueExpression.addChild(literalExpression)
        literal = DeclarationParser.LiteralContext(parent=literalExpression, parser=None)
        literalExpression.addChild(literal)
        value = DeclarationParser.LongValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("10")

        result = self.make_visitor().visitValueExpression(ctx)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def prepare_value_expression(self):
        ctx = DeclarationParser.ValueExpressionContext(parser=None, parent=None)
        literalExpression = DeclarationParser.LiteralExpressionContext(parent=ctx, parser=None)
        ctx.addChild(literalExpression)
        literal = DeclarationParser.LiteralContext(parent=literalExpression, parser=None)
        literalExpression.addChild(literal)

        return (ctx, literal)

    def test_visitValueExpression_int(self):
        r = self.prepare_value_expression()
        ctx = r[0]
        literal = r[1]
        value = DeclarationParser.LongValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("10")

        result = self.make_visitor().visitValueExpression(ctx)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitValueExpression_float(self):
        r = self.prepare_value_expression()
        ctx = r[0]
        literal = r[1]
        value = DeclarationParser.DoubleValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("10.0")

        result = self.make_visitor().visitValueExpression(ctx)
        self.assertIsInstance(result, FloatValue, "Should be an FloatValue")
        self.assertIsInstance(result.value, float, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitValueExpression_str(self):
        r = self.prepare_value_expression()
        ctx = r[0]
        literal = r[1]
        value = DeclarationParser.StringValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("\"text message\"")

        result = self.make_visitor().visitValueExpression(ctx)
        self.assertIsInstance(result, StringValue, "Should be an StringValue")
        self.assertIsInstance(result.value, str, "Wrong value type")
        self.assertEqual(result.value, "text message", "Incorrect value")

    def test_visitParenthesisExpression(self):
        parenthesisExpression = DeclarationParser.ParenthesisExpressionContext(parent=None, parser=None)
        arithmeticExpression = DeclarationParser.ArithmeticExpressionContext(parent=parenthesisExpression, parser=None)
        parenthesisExpression.addChild(arithmeticExpression)
        multiplicationExpression = DeclarationParser.MultiplicationExpressionContext(parent=arithmeticExpression, parser=None)
        arithmeticExpression.addChild(multiplicationExpression)
        valueExpression = DeclarationParser.ValueExpressionContext(parser=multiplicationExpression, parent=None)
        multiplicationExpression.addChild(valueExpression)
        literalExpression = DeclarationParser.LiteralExpressionContext(parent=valueExpression, parser=None)
        valueExpression.addChild(literalExpression)
        literal = DeclarationParser.LiteralContext(parent=literalExpression, parser=None)
        literalExpression.addChild(literal)
        value = DeclarationParser.LongValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("10")

        result = self.make_visitor().visitParenthesisExpression(parenthesisExpression)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitLiteralExpression(self):
        literalExpression = DeclarationParser.LiteralExpressionContext(parent=None, parser=None)
        literal = DeclarationParser.LiteralContext(parent=literalExpression, parser=None)
        literalExpression.addChild(literal)
        value = DeclarationParser.LongValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("10")

        result = self.make_visitor().visitLiteral(literal)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitLiteral(self):
        literal = DeclarationParser.LiteralContext(parent=None, parser=None)
        value = DeclarationParser.LongValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("10")

        result = self.make_visitor().visitLiteral(literal)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitLongValue(self):
        value = DeclarationParser.LongValueContext(parent=None, parser=None)
        value.value = self.set_token("10")

        result = self.make_visitor().visitLongValue(value)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitDoubleValue(self):
        value = DeclarationParser.DoubleValueContext(parent=None, parser=None)
        value.value = self.set_token("10.0")

        result = self.make_visitor().visitDoubleValue(value)
        self.assertIsInstance(result, FloatValue, "Should be an FloatValue")
        self.assertIsInstance(result.value, float, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitStringValue(self):
        value = DeclarationParser.StringValueContext(parent=None, parser=None)
        value.value = self.set_token("\"text message\"")

        result = self.make_visitor().visitStringValue(value)
        self.assertIsInstance(result, StringValue, "Should be an StringValue")
        self.assertIsInstance(result.value, str, "Wrong value type")
        self.assertEqual(result.value, "text message", "Incorrect value")

    def test_visitNamedElementReference(self):
        self.fail()

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

    def test_visitInlineEnumerationType(self):
        self.fail()

    #########################################
    # Utility functions
    #########################################
    # TODO move to a general and abstract test class

    def make_visitor(self, type=None) -> GeneratorDeclarationVisitor:
        model = DeclarationModel()
        if type is not None:
            model._types[type.name] = type
        return GeneratorDeclarationVisitor(model, self.logger)

    def set_terminal(self, value:str) -> TerminalNode:
        return TerminalNodeImpl(self.set_token(value))

    def set_token(self, value:str) -> CommonToken:
        token = CommonToken()
        token.text = value
        return token

    def parse_code(self, code:str) -> DeclarationModel:
        model = DeclarationModel()
        visitor = GeneratorDeclarationVisitor(model, self.logger)

        input_stream = TestStream(code)

        lexer = DeclarationLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DeclarationParser(stream)

        visitor.visit(parser.declarationModel())

        return model

if __name__ == '__main__':
    unittest.main()