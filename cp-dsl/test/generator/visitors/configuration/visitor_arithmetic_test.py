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

from model.type_system import Enumeral, BaseType
from model.declaration_model import DeclarationModel, ParameterGroup, Parameter

from model.arithmetic_model import IntValue, StringValue, FloatValue, ArithmeticExpression, MultiplicationExpression, \
    EMultiplicationOperator, EAdditionOperator, ArrayExpression

from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser

from common.logger import GeneratorLogger
from common.configuration import CompileFlags

from test_utils import AbstractTestGeneratorConfigurationVisitor

class TestGeneratorConfigurationVisitor(AbstractTestGeneratorConfigurationVisitor):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def create_model(self):
        model = self.parse_declaration_code("""
                model eval
                    group g : "group description" {
                        def param1 int : meter = 3 + 4
                        def param2 long : meter = 5
                        def param3 string : "unit" = "message"
                        def param4 float : meter = 2.0
                    }""")
        return model

    def test_visitArithmeticExpression(self):
        model = self.parse_code("""
                configuration test : eval

                group g {
                    param1: 5 + 2
                }
                """, self.create_model())

        group:ParameterGroup = model.groups.get("g")

        self.assertIsInstance(group, ParameterGroup, f"Wrong type {type(group)}")
        self.assertEqual(group.name, "g", "Wrong name")
        self.assertEqual(group.description, "group description", "Wrong description")

        t = BaseType("int")
        self.assertEqual(len(group.parameters.values()), 4, "Wrong number of parameters")
        for p in group.parameters.values():
            if p.name == "param1":
                self.assertEqual(p.name, "param1", "Wrong param name")
                self.assertEqual(p.type, t, "Wrong type")
                # TODO
#                self.assertEqual(p.unit, u, "Should be meter")
                self.assertEqual(len(p.entries), 1, "Wrong number of entries")
                entry:IntValue = p.entries[0]
                self.assertIsInstance(entry, ArithmeticExpression, "Wrong expression type")
                self.assertIsInstance(entry.left, IntValue, "Wrong value type")
                self.assertEqual(entry.left.value, 5, "Wrong value")
                self.assertIsInstance(entry.right, IntValue, "Wrong value type")
                self.assertEqual(entry.right.value, 2, "Wrong value")
                self.assertEqual(entry.op, EAdditionOperator.ADD, "Wrong operation")
                self.assertEqual(p.description, "", "Wrong description")


    def test_visitMultiplicationExpression(self):
        model = self.parse_code("""
                configuration test : eval

                group g {
                    param1: 5 * 2
                }
                """, self.create_model())

        group:ParameterGroup = model.groups.get("g")

        self.assertIsInstance(group, ParameterGroup, f"Wrong type {type(group)}")
        self.assertEqual(group.name, "g", "Wrong name")
        self.assertEqual(group.description, "group description", "Wrong description")

        t = BaseType("int")
        for p in group.parameters.values():
            if p.name == "param1":
                self.assertEqual(p.name, "param1", "Wrong param name")
                self.assertEqual(p.type, t, "Wrong type")
                # TODO
#            self.assertEqual(p.unit, u, "Should be meter")
                self.assertEqual(len(p.entries), 1, "Wrong number of entries")
                entry:IntValue = p.entries[0]
                self.assertIsInstance(entry, MultiplicationExpression, "Wrong expression type")
                self.assertIsInstance(entry.left, IntValue, "Wrong value type")
                self.assertEqual(entry.left.value, 5, "Wrong value")
                self.assertIsInstance(entry.right, IntValue, "Wrong value type")
                self.assertEqual(entry.right.value, 2, "Wrong value")
                self.assertEqual(entry.op, EMultiplicationOperator.MULT, "Wrong operation")
                self.assertEqual(p.description, "", "Wrong description")

    def test_visitValueExpression_int(self):
        model = self.parse_code("""
                configuration test : eval

                group g {
                    param1: 4
                }
                """, self.create_model())

        group:ParameterGroup = model.groups['g']
        param:Parameter = group.parameters['param1']
        expression:IntValue = param.entries[0]

        t = BaseType("long") # long is the type used for int and long value

        self.assertIsInstance(expression, IntValue, "Wrong type")
        self.assertEqual(expression.value, 4, "Wrong value")
        self.assertEqual(expression.type, t, "Wrong type")

    def test_visitValueExpression_long(self):
        model = self.parse_code("""
                configuration test : eval

                group g {
                    param2: 2
                }
                """, self.create_model())

        group:ParameterGroup = model.groups['g']
        param:Parameter = group.parameters['param2']
        expression:IntValue = param.entries[0]

        t = BaseType("long")

        self.assertIsInstance(expression, IntValue, "Wrong type")
        self.assertEqual(expression.value, 2, "Wrong value")
        self.assertEqual(expression.type, t, "Wrong type")

    def test_visitValueExpression_str(self):
        model = self.parse_code("""
                configuration test : eval

                group g {
                    param3: "aaa"
                }
                """, self.create_model())

        group:ParameterGroup = model.groups['g']
        param:Parameter = group.parameters['param3']
        expression:IntValue = param.entries[0]

        t = BaseType("string")

        self.assertIsInstance(expression, StringValue, "Wrong type")
        self.assertEqual(expression.value, "aaa", "Wrong value")
        self.assertEqual(expression.type, t, "Wrong type")

    def test_visitValueExpression_float(self):
        model = self.parse_code("""
                configuration test : eval

                group g {
                    param4: 2.2
                }
                """, self.create_model())

        group:ParameterGroup = model.groups['g']
        param:Parameter = group.parameters['param4']
        expression:FloatValue = param.entries[0]

        t = BaseType("double") # double is the float type for values

        self.assertIsInstance(expression, FloatValue, "Wrong type")
        self.assertEqual(expression.value, 2.2, "Wrong value")
        self.assertEqual(expression.type, t, "Wrong type")

    def test_visitParenthesisExpression(self):
        model = self.parse_code("""
            configuration test : eval

            group g {
                param1: (10 * 4)
            }
            """, self.create_model())

        group:ParameterGroup = model.groups['g']
        param1:Parameter = group.parameters['param1']
        expression = param1.entries[0]

        self.assertEqual(expression.op, EMultiplicationOperator.MULT, "Wrong operator")

        left = expression.left
        right = expression.right

        self.assertIsInstance(left, IntValue, "Should be an IntValue (1)")
        self.assertIsInstance(left.value, int, "Wrong value type (1)")
        self.assertEqual(left.value, 10, "Incorrect value (1)")

        self.assertIsInstance(right, IntValue, "Should be an IntValue (2)")
        self.assertIsInstance(right.value, int, "Wrong value type (2)")
        self.assertEqual(right.value, 4, "Incorrect value (2)")

    def test_visitLiteralExpression(self):
        literalExpression = ConfigurationParser.LiteralExpressionContext(parent=None, parser=None)
        literal = ConfigurationParser.LiteralContext(parent=literalExpression, parser=None)
        literalExpression.addChild(literal)
        value = ConfigurationParser.LongValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("10")

        result = self.make_visitor().visitLiteral(literal)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitLiteral(self):
        literal = ConfigurationParser.LiteralContext(parent=None, parser=None)
        value = ConfigurationParser.LongValueContext(parent=literal, parser=None)
        literal.addChild(value)
        value.value = self.set_token("10")

        result = self.make_visitor().visitLiteral(literal)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitLongValue(self):
        value = ConfigurationParser.LongValueContext(parent=None, parser=None)
        value.value = self.set_token("10")

        result = self.make_visitor().visitLongValue(value)
        self.assertIsInstance(result, IntValue, "Should be an IntValue")
        self.assertIsInstance(result.value, int, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitDoubleValue(self):
        value = ConfigurationParser.DoubleValueContext(parent=None, parser=None)
        value.value = self.set_token("10.0")

        result = self.make_visitor().visitDoubleValue(value)
        self.assertIsInstance(result, FloatValue, "Should be an FloatValue")
        self.assertIsInstance(result.value, float, "Wrong value type")
        self.assertEqual(result.value, 10, "Incorrect value")

    def test_visitStringValue(self):
        value = ConfigurationParser.StringValueContext(parent=None, parser=None)
        value.value = self.set_token("\"text message\"")

        result = self.make_visitor().visitStringValue(value)
        self.assertIsInstance(result, StringValue, "Should be an StringValue")
        self.assertIsInstance(result.value, str, "Wrong value type")
        self.assertEqual(result.value, "text message", "Incorrect value")

    # Named elements can be references to an enumeral or another property or in future a feature
    # The test must therefor test whether an group property, an enumeration and an inline enumeration can be resolved.

    # This test tests property, local
    def test_visitNamedElementReference_one_parameter(self):
        model = self.parse_declaration_code("""
            model eval
            group g : "description" {
                def param_a int : meter = 0
                def param_b int : meter = 1
            }
            """)

        model = self.parse_code("""
            configuration test : eval

            group g {
                param_a: 1
                param_b: param_a + 2
            }
            """, model)

        group:ParameterGroup = model.groups.get("g")
        parameter_a:Parameter = group.parameters.get("param_a")
        parameter_b:Parameter = group.parameters.get("param_b")

        self.assertNotEqual(parameter_a, None, "Missing parameter a")
        self.assertNotEqual(parameter_b, None, "Missing parameter b")

        expression:ArithmeticExpression = parameter_b.entries[0]

        self.assertNotEqual(expression, None, "Missing expression")

        self.assertIsInstance(expression, ArithmeticExpression, "Wrong type, ArithmeticExpression expected")
        self.assertEqual(parameter_a, expression.left, "Reference to the wrong element")

    # This test tests property, local
    def test_visitNamedElementReference_two_parameter(self):
        model = self.parse_declaration_code("""
            model eval
            group my_group : "description" {
                def param_a int : meter = 0
            }
            group other_group : "other" {
                def param_b int : meter = my_group.param_a
            }
            """)

        model = self.parse_code("""
            configuration test : eval

            group other_group {
                param_b: my_group.param_a
            }
            """, model)


        group_a:ParameterGroup = model.groups.get("my_group")
        parameter_a:Parameter = group_a.parameters.get("param_a")
        group_b:ParameterGroup = model.groups.get("other_group")
        parameter_b:Parameter = group_b.parameters.get("param_b")

        self.assertNotEqual(parameter_a, None, "Missing parameter a")
        self.assertNotEqual(parameter_b, None, "Missing parameter b")

        expression:ArithmeticExpression = parameter_b.entries[0]

        self.assertNotEqual(expression, None, "Missing expression")

        self.assertIsInstance(expression, Parameter, "Wrong type, Parameter expected")
        self.assertEqual(parameter_a, expression, "Reference to the wrong element")

    # This test tests enum based on context
    def test_visitNamedElementReference_one_enum(self):
        model:DeclarationModel = self.parse_declaration_code("""
            model eval
            types
                enum Color { red, green, blue }
            group my_group : "description" {
                def param Color : meter = blue
            }
            """)

        model = self.parse_code("""
            configuration test : eval

            group my_group {
                param: green
            }
            """, model)

        group:ParameterGroup = model.groups.get("my_group")
        parameter:Parameter = group.parameters.get("param")
        expression:ArithmeticExpression = parameter.entries[0]

        self.assertNotEqual(parameter, None, "Missing parameter")
        self.assertNotEqual(expression, None, "Missing expression")
        self.assertIsInstance(expression, Enumeral, "Missing enumeral")
        self.assertEqual(expression.name, "green", "Wrong enumeral name")
        self.assertEqual(expression.value, 1, "Wrong enumeral value")

    def test_visitNamedElementReference_two_enum(self):
        model = self.parse_declaration_code("""
            model eval
            types
                enum Color { red, green, blue }
            group my_group : "description" {
                def param Color : meter = Color.blue
            }
            """)

        model = self.parse_code("""
            configuration test : eval

            group my_group {
                param: green
            }
            """, model)

        group:ParameterGroup = model.groups.get("my_group")
        parameter:Parameter = group.parameters.get("param")
        expression:ArithmeticExpression = parameter.entries[0]

        self.assertNotEqual(parameter, None, "Missing parameter")
        self.assertNotEqual(expression, None, "Missing expression")
        self.assertIsInstance(expression, Enumeral, "Missing enumeral")
        self.assertEqual(expression.name, "green", "Wrong enumeral name")
        self.assertEqual(expression.value, 1, "Wrong enumeral value")

    def test_visitArrayExpression(self):
        model:DeclarationModel = self.parse_declaration_code("""
                model eval
                    group my_group : "my group" {
                        def array int[5] : meter , "array description" = [ 2,4,6,8,10 ]
                    }
                """)
        self.assertEqual(model.name, "eval", "Name not set")

        group:ParameterGroup = model.groups['my_group']
        self.assertIsInstance(group, ParameterGroup, "Parameter group 'my_group' not found")
        array:Parameter = group.parameters['array']
        self.assertIsInstance(array, Parameter, "Parameter 'array' not found.")
        expr:ArrayExpression = array.default_value
        self.assertIsInstance(expr, ArrayExpression, "Not an array expression")
        self.assertEqual(len(expr.elements), 5, "Wrong number of elements")
        for element in expr.elements:
            self.assertIsInstance(element, IntValue, "Wrong value type")

if __name__ == '__main__':
    unittest.main()
