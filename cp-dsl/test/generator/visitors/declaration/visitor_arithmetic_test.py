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
from cpdsl.model.type_system import BaseType
from cpdsl.model.arithmetic_model import IntValue, StringValue, FloatValue

from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.configuration import CompileFlags

from generator.visitors.test_utils import AbstractTestGeneratorDeclarationVisitor, describe_expression

VALUE_CONTEXTS = {"long": DeclarationParser.LongValueContext, "double": DeclarationParser.DoubleValueContext,
                  "string": DeclarationParser.StringValueContext}

ENUMERATION_TYPES = """
            types
                enum Color { red, green, blue }"""


class TestArithmeticGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def default_value(self, expression):
        model = self.parse_code(
            f"model eval group g : \"group description\" {{ def param1 int : meter = {expression} }}")

        group: ParameterGroup = model.groups.get("g")
        self.assertIsInstance(group, ParameterGroup)
        self.assertEqual(("g", "group description"), (group.name, group.description))
        self.assertEqual(["param1"], list(group.parameters))
        parameter = group.parameters["param1"]
        self.assertEqual(BaseType("int"), parameter.type)
        self.assertEqual("", parameter.description)
        return parameter.default_value

    def literal_context(self, kind, token, parent=None):
        """A literal context with a long, double or string value context for the token."""
        literal = DeclarationParser.LiteralContext(parent=parent, parser=None)
        value = VALUE_CONTEXTS[kind](parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token(token)
        return literal

    def value_expression_context(self, kind, token, parenthesis=False):
        """A value expression context of a literal, optionally wrapped into a parenthesis expression."""
        ctx = DeclarationParser.ValueExpressionContext(parser=None, parent=None)
        parent = ctx
        if parenthesis:
            parenthesis_expression = DeclarationParser.ParenthesisExpressionContext(parent=ctx, parser=None)
            ctx.addChild(parenthesis_expression)
            arithmetic_expression = DeclarationParser.ArithmeticExpressionContext(parent=parenthesis_expression,
                                                                                  parser=None)
            parenthesis_expression.addChild(arithmetic_expression)
            multiplication_expression = DeclarationParser.MultiplicationExpressionContext(parent=arithmetic_expression,
                                                                                          parser=None)
            arithmetic_expression.addChild(multiplication_expression)
            parent = DeclarationParser.ValueExpressionContext(parser=multiplication_expression, parent=None)
            multiplication_expression.addChild(parent)
        literal_expression = DeclarationParser.LiteralExpressionContext(parent=parent, parser=None)
        parent.addChild(literal_expression)
        literal_expression.addChild(self.literal_context(kind, token, literal_expression))
        return ctx

    @parameterized.expand([
        ("addition", "3 + 4", ("+", ("int", 3), ("int", 4))),
        # An addition
        # Input: 'def param1 int : meter = 3 + 4'
        # Expected Result: an arithmetic expression 3 + 4

        ("subtraction", "3 - 4", ("-", ("int", 3), ("int", 4))),
        # A subtraction
        # Input: 'def param1 int : meter = 3 - 4'
        # Expected Result: an arithmetic expression 3 - 4

        ("multiplication", "3 * 4", ("*", ("int", 3), ("int", 4))),
        # A multiplication
        # Input: 'def param1 int : meter = 3 * 4'
        # Expected Result: a multiplication expression 3 * 4

        ("division", "6 / 2", ("/", ("int", 6), ("int", 2))),
        # A division
        # Input: 'def param1 int : meter = 6 / 2'
        # Expected Result: a multiplication expression 6 / 2

        ("modulo", "7 % 3", ("%", ("int", 7), ("int", 3))),
        # A modulo
        # Input: 'def param1 int : meter = 7 % 3'
        # Expected Result: a multiplication expression 7 % 3

        ("precedence", "2 + 3 * 4", ("+", ("int", 2), ("*", ("int", 3), ("int", 4)))),
        # Multiplication binds stronger than addition
        # Input: 'def param1 int : meter = 2 + 3 * 4'
        # Expected Result: 2 + (3 * 4)

        ("precedence_left", "2 * 3 + 4", ("+", ("*", ("int", 2), ("int", 3)), ("int", 4))),
        # Multiplication binds stronger on the left as well
        # Input: 'def param1 int : meter = 2 * 3 + 4'
        # Expected Result: (2 * 3) + 4

        ("parenthesis", "(2 + 3) * 4", ("*", ("+", ("int", 2), ("int", 3)), ("int", 4))),
        # Parentheses group an addition
        # Input: 'def param1 int : meter = (2 + 3) * 4'
        # Expected Result: (2 + 3) * 4

        ("negative_value", "-2", ("int", -2)),
        # A negative literal
        # Input: 'def param1 int : meter = -2'
        # Expected Result: the int value -2

        ("float_value", "1.5", ("float", 1.5)),
        # A float literal
        # Input: 'def param1 int : meter = 1.5'
        # Expected Result: the float value 1.5

        ("string_value", "\"text\"", ("str", "text")),
        # A string literal without quotes
        # Input: 'def param1 int : meter = "text"'
        # Expected Result: the string value text

        ("boolean_value", "true", ("bool", True)),
        # A boolean literal
        # Input: 'def param1 int : meter = true'
        # Expected Result: the boolean value True
    ])
    def test_visitArithmeticExpression(self, test_name, expression, expected):
        self.assertEqual(expected, describe_expression(self.default_value(expression)), test_name)

    @parameterized.expand([
        ("int", "long", "10", False, IntValue, int, 10),
        # A long literal in a value expression
        # Input: a value expression with the long value 10
        # Expected Result: IntValue 10

        ("float", "double", "10.0", False, FloatValue, float, 10.0),
        # A double literal in a value expression
        # Input: a value expression with the double value 10.0
        # Expected Result: FloatValue 10.0

        ("str", "string", "\"text message\"", False, StringValue, str, "text message"),
        # A string literal in a value expression; the quotes are removed
        # Input: a value expression with the string value "text message"
        # Expected Result: StringValue text message

        ("parenthesis", "long", "10", True, IntValue, int, 10),
        # A parenthesized literal in a value expression
        # Input: a value expression with a parenthesis expression of the long value 10
        # Expected Result: IntValue 10

        ("parenthesis_float", "double", "2.5", True, FloatValue, float, 2.5),
        # A parenthesized double literal
        # Input: a value expression with a parenthesis expression of the double value 2.5
        # Expected Result: FloatValue 2.5
    ])
    def test_visitValueExpression(self, test_name, kind, token, parenthesis, expected_class, expected_type,
                                  expected_value):
        result = self.make_visitor().visitValueExpression(self.value_expression_context(kind, token, parenthesis))

        self.assertIsInstance(result, expected_class, test_name)
        self.assertIsInstance(result.value, expected_type, test_name)
        self.assertEqual(expected_value, result.value, test_name)

    @parameterized.expand([
        ("parenthesis_expression", "parenthesis"),
        # A parenthesis expression is visited down to its literal
        # Input: a parenthesis expression of the long value 10
        # Expected Result: IntValue 10

        ("literal_in_literal_expression", "literal_expression"),
        # A literal that is part of a literal expression
        # Input: the literal of a literal expression with the long value 10
        # Expected Result: IntValue 10

        ("literal", "literal"),
        # A literal without parent
        # Input: a literal with the long value 10
        # Expected Result: IntValue 10
    ])
    def test_visit_nested_literal(self, test_name, entry):
        visitor = self.make_visitor()
        if entry == "parenthesis":
            ctx = self.value_expression_context("long", "10", parenthesis=True).getChild(0)
            result = visitor.visitParenthesisExpression(ctx)
        elif entry == "literal_expression":
            literal_expression = DeclarationParser.LiteralExpressionContext(parent=None, parser=None)
            literal = self.literal_context("long", "10", literal_expression)
            literal_expression.addChild(literal)
            result = visitor.visitLiteral(literal)
        else:
            result = visitor.visitLiteral(self.literal_context("long", "10"))

        self.assertIsInstance(result, IntValue, test_name)
        self.assertIsInstance(result.value, int, test_name)
        self.assertEqual(10, result.value, test_name)

    @parameterized.expand([
        ("long", "visitLongValue", DeclarationParser.LongValueContext, "10", IntValue, int, 10),
        # A long value
        # Input: the long value context 10
        # Expected Result: IntValue 10

        ("long_zero", "visitLongValue", DeclarationParser.LongValueContext, "0", IntValue, int, 0),
        # Zero
        # Input: the long value context 0
        # Expected Result: IntValue 0

        ("double", "visitDoubleValue", DeclarationParser.DoubleValueContext, "10.0", FloatValue, float, 10.0),
        # A double value
        # Input: the double value context 10.0
        # Expected Result: FloatValue 10.0

        ("double_negative", "visitDoubleValue", DeclarationParser.DoubleValueContext, "-2.5", FloatValue, float,
         -2.5),
        # A negative double value
        # Input: the double value context -2.5
        # Expected Result: FloatValue -2.5

        ("string", "visitStringValue", DeclarationParser.StringValueContext, "\"text message\"", StringValue, str,
         "text message"),
        # A string value without quotes
        # Input: the string value context "text message"
        # Expected Result: StringValue text message

        ("empty_string", "visitStringValue", DeclarationParser.StringValueContext, "\"\"", StringValue, str, ""),
        # An empty string
        # Input: the string value context ""
        # Expected Result: StringValue with an empty string
    ])
    def test_visit_value(self, test_name, method, context_class, token, expected_class, expected_type,
                         expected_value):
        value = context_class(parent=None, parser=None)
        value.value = self.set_token(token)

        result = getattr(self.make_visitor(), method)(value)

        self.assertIsInstance(result, expected_class, test_name)
        self.assertIsInstance(result.value, expected_type, test_name)
        self.assertEqual(expected_value, result.value, test_name)

    # Named elements can be references to an enumeral or another property or in future a feature.
    # The test must therefore test whether a group property, an enumeration and an inline enumeration can be resolved.
    @parameterized.expand([
        ("parameter_in_same_group", "", """
            group test : "description" {
                def param_a int : meter = 0
                def param_b int : meter = param_a
            }""", "test", ("param", "param_a")),
        # A reference to a parameter of the same group
        # Input: 'def param_b int : meter = param_a' in the group of param_a
        # Expected Result: the parameter param_a

        ("parameter_in_other_group", "", """
            group test : "description" {
                def param_a int : meter = 0
            }
            group test2 : "other" {
                def param_b int : meter = test.param_a
            }""", "test2", ("param", "param_a")),
        # A qualified reference to a parameter of another group
        # Input: 'def param_b int : meter = test.param_a' in the group test2
        # Expected Result: the parameter param_a of the group test

        ("enumeral", ENUMERATION_TYPES, """
            group test : "description" {
                def param_b Color : meter = blue
            }""", "test", ("enum", "blue", 2)),
        # An enumeral of the parameter type
        # Input: 'def param_b Color : meter = blue'
        # Expected Result: the enumeral blue with the value 2

        ("qualified_enumeral", ENUMERATION_TYPES, """
            group test : "description" {
                def param_b Color : meter = Color.blue
            }""", "test", ("enum", "blue", 2)),
        # An enumeral qualified by its type
        # Input: 'def param_b Color : meter = Color.blue'
        # Expected Result: the enumeral blue with the value 2

        ("first_enumeral", ENUMERATION_TYPES, """
            group test : "description" {
                def param_b Color : meter = red
            }""", "test", ("enum", "red", 0)),
        # The first enumeral
        # Input: 'def param_b Color : meter = red'
        # Expected Result: the enumeral red with the value 0
    ])
    def test_visitNamedElementReference(self, test_name, types, groups, group_name, expected):
        model: DeclarationModel = self.parse_code(f"model eval{types}{groups}")

        parameter: Parameter = model.groups[group_name].parameters.get("param_b")
        self.assertIsNotNone(parameter, test_name)
        self.assertEqual(expected, describe_expression(parameter.default_value), test_name)
        if expected[0] == "param":
            self.assertIs(model.groups["test"].parameters["param_a"], parameter.default_value, test_name)

    @parameterized.expand([
        ("ints", "[ 2,4,6,8,10 ]", [("int", 2), ("int", 4), ("int", 6), ("int", 8), ("int", 10)]),
        # An array of int values
        # Input: 'def array int[5] : meter , "array description" = [ 2,4,6,8,10 ]'
        # Expected Result: an array expression of the five int values

        ("floats", "[ 1.5, 2.5 ]", [("float", 1.5), ("float", 2.5)]),
        # An array of float values
        # Input: '= [ 1.5, 2.5 ]'
        # Expected Result: an array expression of the two float values

        ("expressions", "[ 1 + 1, 2 ]", [("+", ("int", 1), ("int", 1)), ("int", 2)]),
        # Array elements may be expressions
        # Input: '= [ 1 + 1, 2 ]'
        # Expected Result: an array expression of 1 + 1 and 2

        ("single_element", "[ 7 ]", [("int", 7)]),
        # An array with one element
        # Input: '= [ 7 ]'
        # Expected Result: an array expression of 7
    ])
    def test_visitArrayExpression(self, test_name, array, expected_elements):
        model: DeclarationModel = self.parse_code(f"""
                model eval
                    group my_group : "my group" {{
                        def array int[5] : meter , "array description" = {array}
                    }}
                """)
        self.assertEqual("eval", model.name, test_name)

        group: ParameterGroup = model.groups['my_group']
        self.assertIsInstance(group, ParameterGroup, test_name)
        parameter: Parameter = group.parameters['array']
        self.assertIsInstance(parameter, Parameter, test_name)
        self.assertEqual(("array", expected_elements), describe_expression(parameter.default_value), test_name)


if __name__ == '__main__':
    unittest.main()
