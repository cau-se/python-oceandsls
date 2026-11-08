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

from cpdsl.model.type_system import BaseType
from cpdsl.model.declaration_model import DeclarationModel, ParameterGroup, Parameter

from cpdsl.model.arithmetic_model import IntValue, StringValue, FloatValue

from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.configuration import CompileFlags

from generator.visitors.test_utils import AbstractTestGeneratorConfigurationVisitor, describe_expression

DECLARATION = """
        model eval
            group g : "group description" {
                def param1 int : meter = 3 + 4
                def param2 long : meter = 5
                def param3 string : "unit" = "message"
                def param4 float : meter = 2.0
            }"""

ENUMERATION_DECLARATION = """
    model eval
    types
        enum Color { red, green, blue }
    group my_group : "description" {
        def param Color : meter = %s
    }
    """


class TestArithmeticGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def configure(self, declaration, group_name, configuration):
        return self.parse_code(f"""
                configuration test : eval

                group {group_name} {{
                    {configuration}
                }}
                """, self.parse_declaration_code(declaration))

    @parameterized.expand([
        ("addition", "5 + 2", ("+", ("int", 5), ("int", 2))),
        # A configured addition
        # Input: 'param1: 5 + 2'
        # Expected Result: the entry 5 + 2

        ("subtraction", "5 - 2", ("-", ("int", 5), ("int", 2))),
        # A configured subtraction
        # Input: 'param1: 5 - 2'
        # Expected Result: the entry 5 - 2

        ("multiplication", "5 * 2", ("*", ("int", 5), ("int", 2))),
        # A configured multiplication
        # Input: 'param1: 5 * 2'
        # Expected Result: the entry 5 * 2

        ("division", "9 / 3", ("/", ("int", 9), ("int", 3))),
        # A configured division
        # Input: 'param1: 9 / 3'
        # Expected Result: the entry 9 / 3

        ("modulo", "9 % 4", ("%", ("int", 9), ("int", 4))),
        # A configured modulo
        # Input: 'param1: 9 % 4'
        # Expected Result: the entry 9 % 4

        ("parenthesis", "(10 * 4)", ("*", ("int", 10), ("int", 4))),
        # Parentheses around the whole expression
        # Input: 'param1: (10 * 4)'
        # Expected Result: the entry 10 * 4

        ("precedence", "2 + 3 * 4", ("+", ("int", 2), ("*", ("int", 3), ("int", 4)))),
        # Multiplication binds stronger than addition
        # Input: 'param1: 2 + 3 * 4'
        # Expected Result: the entry 2 + (3 * 4)

        ("grouped_addition", "(2 + 3) * 4", ("*", ("+", ("int", 2), ("int", 3)), ("int", 4))),
        # Parentheses group an addition
        # Input: 'param1: (2 + 3) * 4'
        # Expected Result: the entry (2 + 3) * 4
    ])
    def test_visitArithmeticExpression(self, test_name, expression, expected):
        model = self.configure(DECLARATION, "g", f"param1: {expression}")

        group: ParameterGroup = model.groups.get("g")
        self.assertIsInstance(group, ParameterGroup, test_name)
        self.assertEqual(("g", "group description"), (group.name, group.description), test_name)
        self.assertEqual(["param1", "param2", "param3", "param4"], list(group.parameters), test_name)
        parameter = group.parameters["param1"]
        self.assertEqual(BaseType("int"), parameter.type, test_name)
        self.assertEqual("", parameter.description, test_name)
        self.assertEqual(("+", ("int", 3), ("int", 4)), describe_expression(parameter.default_value), test_name)
        self.assertEqual([expected], [describe_expression(entry) for entry in parameter.entries], test_name)

    @parameterized.expand([
        ("int", "param1", "4", IntValue, 4, "long"),
        # long is the type used for int and long values
        # Input: 'param1: 4' for an int parameter
        # Expected Result: IntValue 4 of type long

        ("long", "param2", "2", IntValue, 2, "long"),
        # A long value
        # Input: 'param2: 2' for a long parameter
        # Expected Result: IntValue 2 of type long

        ("str", "param3", "\"aaa\"", StringValue, "aaa", "string"),
        # A string value without quotes
        # Input: 'param3: "aaa"' for a string parameter
        # Expected Result: StringValue aaa of type string

        ("float", "param4", "2.2", FloatValue, 2.2, "double"),
        # double is the type used for float values
        # Input: 'param4: 2.2' for a float parameter
        # Expected Result: FloatValue 2.2 of type double

        ("negative_float", "param4", "-1.5", FloatValue, -1.5, "double"),
        # A negative float value
        # Input: 'param4: -1.5'
        # Expected Result: FloatValue -1.5 of type double
    ])
    def test_visitValueExpression(self, test_name, name, value, expected_class, expected_value, expected_type):
        model = self.configure(DECLARATION, "g", f"{name}: {value}")

        expression = model.groups['g'].parameters[name].entries[0]

        self.assertIsInstance(expression, expected_class, test_name)
        self.assertEqual(expected_value, expression.value, test_name)
        self.assertEqual(BaseType(expected_type), expression.type, test_name)

    @parameterized.expand([
        ("literal_in_literal_expression", True, ConfigurationParser.LongValueContext, "10", IntValue, int, 10),
        # A literal that is part of a literal expression
        # Input: the literal of a literal expression with the long value 10
        # Expected Result: IntValue 10

        ("literal", False, ConfigurationParser.LongValueContext, "10", IntValue, int, 10),
        # A literal without parent
        # Input: a literal with the long value 10
        # Expected Result: IntValue 10

        ("double_literal", False, ConfigurationParser.DoubleValueContext, "2.5", FloatValue, float, 2.5),
        # A literal with a double value
        # Input: a literal with the double value 2.5
        # Expected Result: FloatValue 2.5

        ("string_literal", False, ConfigurationParser.StringValueContext, "\"abc\"", StringValue, str, "abc"),
        # A literal with a string value
        # Input: a literal with the string value "abc"
        # Expected Result: StringValue abc
    ])
    def test_visitLiteral(self, test_name, in_literal_expression, value_class, token, expected_class, expected_type,
                          expected_value):
        literal_expression = ConfigurationParser.LiteralExpressionContext(parent=None, parser=None)
        literal = ConfigurationParser.LiteralContext(parent=literal_expression if in_literal_expression else None,
                                                     parser=None)
        if in_literal_expression:
            literal_expression.addChild(literal)
        value = value_class(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token(token)

        result = self.make_visitor().visitLiteral(literal)

        self.assertIsInstance(result, expected_class, test_name)
        self.assertIsInstance(result.value, expected_type, test_name)
        self.assertEqual(expected_value, result.value, test_name)

    @parameterized.expand([
        ("long", "visitLongValue", ConfigurationParser.LongValueContext, "10", IntValue, int, 10),
        # A long value
        # Input: the long value context 10
        # Expected Result: IntValue 10

        ("double", "visitDoubleValue", ConfigurationParser.DoubleValueContext, "10.0", FloatValue, float, 10.0),
        # A double value
        # Input: the double value context 10.0
        # Expected Result: FloatValue 10.0

        ("string", "visitStringValue", ConfigurationParser.StringValueContext, "\"text message\"", StringValue, str,
         "text message"),
        # A string value without quotes
        # Input: the string value context "text message"
        # Expected Result: StringValue text message

        ("negative_long", "visitLongValue", ConfigurationParser.LongValueContext, "-3", IntValue, int, -3),
        # A negative long value
        # Input: the long value context -3
        # Expected Result: IntValue -3
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
        ("parameter_in_expression", "param_a: 1\nparam_b: param_a + 2", ("+", ("param", "param_a"), ("int", 2))),
        # A reference to a parameter of the same group in an expression
        # Input: 'param_a: 1' and 'param_b: param_a + 2'
        # Expected Result: the entry param_a + 2 referring to the parameter param_a

        ("parameter", "param_b: param_a", ("param", "param_a")),
        # A reference to a parameter of the same group
        # Input: 'param_b: param_a'
        # Expected Result: the entry param_a

        ("parameter_as_right_factor", "param_b: 2 * param_a", ("*", ("int", 2), ("param", "param_a"))),
        # A reference on the right side of an expression
        # Input: 'param_b: 2 * param_a'
        # Expected Result: the entry 2 * param_a
    ])
    def test_visitNamedElementReference_one_parameter(self, test_name, configuration, expected):
        model = self.configure("""
            model eval
            group g : "description" {
                def param_a int : meter = 0
                def param_b int : meter = 1
            }
            """, "g", configuration)

        group: ParameterGroup = model.groups.get("g")
        parameter_a: Parameter = group.parameters.get("param_a")
        parameter_b: Parameter = group.parameters.get("param_b")
        self.assertIsNotNone(parameter_a, test_name)
        self.assertIsNotNone(parameter_b, test_name)
        self.assertEqual([expected], [describe_expression(entry) for entry in parameter_b.entries], test_name)

    @parameterized.expand([
        ("qualified_reference", "my_group.param_a", ("param", "param_a")),
        # A qualified reference to a parameter of another group
        # Input: 'param_b: my_group.param_a' in the group other_group
        # Expected Result: the parameter param_a of my_group

        ("qualified_reference_in_expression", "my_group.param_a + 1", ("+", ("param", "param_a"), ("int", 1))),
        # A qualified reference in an expression
        # Input: 'param_b: my_group.param_a + 1'
        # Expected Result: the entry param_a + 1

        ("value", "3", ("int", 3)),
        # A value instead of the declared reference
        # Input: 'param_b: 3'
        # Expected Result: the entry 3
    ])
    def test_visitNamedElementReference_two_parameter(self, test_name, value, expected):
        model: DeclarationModel = self.configure("""
            model eval
            group my_group : "description" {
                def param_a int : meter = 0
            }
            group other_group : "other" {
                def param_b int : meter = my_group.param_a
            }
            """, "other_group", f"param_b: {value}")

        parameter_a: Parameter = model.groups.get("my_group").parameters.get("param_a")
        parameter_b: Parameter = model.groups.get("other_group").parameters.get("param_b")
        self.assertIsNotNone(parameter_a, test_name)
        self.assertIsNotNone(parameter_b, test_name)
        self.assertIs(parameter_a, parameter_b.default_value, test_name)
        self.assertEqual([expected], [describe_expression(entry) for entry in parameter_b.entries], test_name)
        if expected[0] == "param":
            self.assertIs(parameter_a, parameter_b.entries[0], test_name)

    @parameterized.expand([
        ("enumeral", "blue", "green", ("enum", "green", 1)),
        # An enumeral of the parameter type
        # Input: the default value blue, 'param: green'
        # Expected Result: the enumeral green with the value 1

        ("qualified_default", "Color.blue", "green", ("enum", "green", 1)),
        # The default value may be qualified by the type
        # Input: the default value Color.blue, 'param: green'
        # Expected Result: the enumeral green with the value 1

        ("first_enumeral", "blue", "red", ("enum", "red", 0)),
        # The first enumeral
        # Input: the default value blue, 'param: red'
        # Expected Result: the enumeral red with the value 0

        ("qualified_enumeral", "red", "Color.blue", ("enum", "blue", 2)),
        # A configured enumeral qualified by its type
        # Input: the default value red, 'param: Color.blue'
        # Expected Result: the enumeral blue with the value 2
    ])
    def test_visitNamedElementReference_enum(self, test_name, default, value, expected):
        model = self.configure(ENUMERATION_DECLARATION % default, "my_group", f"param: {value}")

        parameter: Parameter = model.groups.get("my_group").parameters.get("param")
        self.assertIsNotNone(parameter, test_name)
        self.assertEqual([expected], [describe_expression(entry) for entry in parameter.entries], test_name)

    @parameterized.expand([
        ("ints", "[ 1,3,5,7,9 ]", [("int", 1), ("int", 3), ("int", 5), ("int", 7), ("int", 9)]),
        # A configured array replaces the declared array
        # Input: the declared array [ 2,4,6,8,10 ], 'array: [ 1,3,5,7,9 ]'
        # Expected Result: the array entry [1,3,5,7,9]

        ("expressions", "[ 1 + 1, 2 ]", [("+", ("int", 1), ("int", 1)), ("int", 2)]),
        # Array elements may be expressions
        # Input: 'array: [ 1 + 1, 2 ]'
        # Expected Result: the array entry [1 + 1, 2]

        ("single_element", "[ 7 ]", [("int", 7)]),
        # An array with one element
        # Input: 'array: [ 7 ]'
        # Expected Result: the array entry [7]
    ])
    def test_visitArrayExpression(self, test_name, array, expected_elements):
        model: DeclarationModel = self.configure("""
                model eval
                    group my_group : "my group" {
                        def array int[5] : meter , "array description" = [ 2,4,6,8,10 ]
                    }
                """, "my_group", f"array: {array}")
        self.assertEqual("eval", model.name, test_name)

        parameter: Parameter = model.groups['my_group'].parameters['array']
        self.assertIsInstance(parameter, Parameter, test_name)
        self.assertEqual(("array", [("int", 2), ("int", 4), ("int", 6), ("int", 8), ("int", 10)]),
                         describe_expression(parameter.default_value), test_name)
        self.assertEqual([("array", expected_elements)], [describe_expression(entry) for entry in parameter.entries],
                         test_name)


if __name__ == '__main__':
    unittest.main()
