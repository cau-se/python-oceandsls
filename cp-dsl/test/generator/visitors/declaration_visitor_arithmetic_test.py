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

from test_utils import AbstractTestGeneratorDeclarationVisitor

class TestArithmeticGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def test_visitArithmeticExpression(self):
        model = self.parse_code("model eval group g : \"group description\" { def param1 int : meter = 3 + 4 }")

        group:ParameterGroup = model._groups.get("g")

        self.assertIsInstance(group, ParameterGroup, f"Wrong type {type(group)}")
        self.assertEqual(group.name, "g", "Wrong name")
        self.assertEqual(group._description, "group description", "Wrong description")

        t = BaseType("int")
        self.assertEqual(len(group._parameters.values()), 1, "Wrong number of parameters")
        for p in group._parameters.values():
            self.assertEqual(p.name, "param1", "Wrong param name")
            self.assertEqual(p._type, t, "Wrong type")
            # TODO
#            self.assertEqual(p._unit, u, "Should be meter")
            self.assertIsInstance(p._default_value, ArithmeticExpression, "Wrong expression type")
            self.assertIsInstance(p._default_value.left, IntValue, "Wrong value type")
            self.assertEqual(p._default_value.left.value, 3, "Wrong value")
            self.assertIsInstance(p._default_value.right, IntValue, "Wrong value type")
            self.assertEqual(p._default_value.right.value, 4, "Wrong value")
            self.assertEqual(p._default_value.op, EAdditionOperator.ADD, "Wrong operation")
            self.assertEqual(p._description, "", "Wrong description")


    def test_visitMultiplicationExpression(self):
        model = self.parse_code("model eval group g : \"group description\" { def param1 int : meter = 3 * 4 }")

        group:ParameterGroup = model._groups.get("g")

        self.assertIsInstance(group, ParameterGroup, f"Wrong type {type(group)}")
        self.assertEqual(group.name, "g", "Wrong name")
        self.assertEqual(group._description, "group description", "Wrong description")

        t = BaseType("int")
        self.assertEqual(len(group._parameters.values()), 1, "Wrong number of parameters")
        for p in group._parameters.values():
            self.assertEqual(p.name, "param1", "Wrong param name")
            self.assertEqual(p._type, t, "Wrong type")
            # TODO
#            self.assertEqual(p._unit, u, "Should be meter")
            self.assertIsInstance(p._default_value, MultiplicationExpression, "Wrong expression type")
            self.assertIsInstance(p._default_value.left, IntValue, "Wrong value type")
            self.assertEqual(p._default_value.left.value, 3, "Wrong value")
            self.assertIsInstance(p._default_value.right, IntValue, "Wrong value type")
            self.assertEqual(p._default_value.right.value, 4, "Wrong value")
            self.assertEqual(p._default_value.op, EMultiplicationOperator.MULT, "Wrong operator")
            self.assertEqual(p._description, "", "Wrong description")

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

    # Named elements can be references to an enumeral or another property or in future a feature
    # The test must therefor test whether an group property, an enumeration and an inline enumeration can be resolved.

    # This test tests property, local
    def test_visitNamedElementReference_one_parameter(self):
        model = self.parse_code("""
            model eval
            group test : "description" {
                def param_a int : meter = 0
                def param_b int : meter = param_a
            }
            """)

        group:ParameterGroup = model._groups.get("test")
        parameter_a:Parameter = group._parameters.get("param_a")
        parameter_b:Parameter = group._parameters.get("param_b")

        self.assertNotEqual(parameter_a, None, "Missing parameter a")
        self.assertNotEqual(parameter_b, None, "Missing parameter b")

        expression:ArithmeticExpression = parameter_b._default_value

        self.assertNotEqual(expression, None, "Missing expression")

        self.assertIsInstance(expression, Parameter, "Wrong type, Parameter expected")
        self.assertEqual(parameter_a, expression, "Reference to the wrong element")

    # This test tests property, local
    def test_visitNamedElementReference_two_parameter(self):
        model = self.parse_code("""
            model eval
            group test : "description" {
                def param_a int : meter = 0
            }
            group test2 : "other" {
                def param_b int : meter = test.param_a
            }
            """)

        group_a:ParameterGroup = model._groups.get("test")
        parameter_a:Parameter = group_a._parameters.get("param_a")
        group_b:ParameterGroup = model._groups.get("test2")
        parameter_b:Parameter = group_b._parameters.get("param_b")

        self.assertNotEqual(parameter_a, None, "Missing parameter a")
        self.assertNotEqual(parameter_b, None, "Missing parameter b")

        expression:ArithmeticExpression = parameter_b._default_value

        self.assertNotEqual(expression, None, "Missing expression")

        self.assertIsInstance(expression, Parameter, "Wrong type, Parameter expected")
        self.assertEqual(parameter_a, expression, "Reference to the wrong element")

    # This test tests enum based on context
    def test_visitNamedElementReference_one_enum(self):
        model = self.parse_code("""
            model eval
            types
                enum Color { red, green, blue }
            group test : "description" {
                def param Color : meter = blue
            }
            """)

        group:ParameterGroup = model._groups.get("test")
        parameter:Parameter = group._parameters.get("param")
        expression:ArithmeticExpression = parameter._default_value

        self.assertNotEqual(parameter, None, "Missing parameter")
        self.assertNotEqual(expression, None, "Missing expression")
        self.assertIsInstance(expression, Enumeral, "Missing enumeral")
        self.assertEqual(expression.name, "blue", "Wrong enumeral name")
        self.assertEqual(expression.value, 2, "Wrong enumeral value")

    def test_visitNamedElementReference_two_enum(self):
        model = self.parse_code("""
            model eval
            types
                enum Color { red, green, blue }
            group test : "description" {
                def param Color : meter = Color.blue
            }
            """)

        group:ParameterGroup = model._groups.get("test")
        parameter:Parameter = group._parameters.get("param")
        expression:ArithmeticExpression = parameter._default_value

        self.assertNotEqual(parameter, None, "Missing parameter")
        self.assertNotEqual(expression, None, "Missing expression")
        self.assertIsInstance(expression, Enumeral, "Missing enumeral")
        self.assertEqual(expression.name, "blue", "Wrong enumeral name")
        self.assertEqual(expression.value, 2, "Wrong enumeral value")


if __name__ == '__main__':
    unittest.main()