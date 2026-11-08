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

from cpdsl.model.declaration_model import ParameterGroup
from cpdsl.model.type_system import RangeType, BaseType, EnumeralType
from cpdsl.model.unit_model import SIUnit, UnitKind, CustomUnit

from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from cpdsl.model.declaration_model import DeclarationModel

from generator.visitors.test_utils import AbstractTestGeneratorDeclarationVisitor

ENUMERATION_MODEL = """
    model eval
        types
            enum Color { red, green, blue }
        group group_name : "group description" {
            def param1 Color : "pixel" = %s
        }
"""


class TestParameterGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    @parameterized.expand([
        ("group_with_description", "group_name", "\"group description\"", "group_name", "group description"),
        # The quotes of the description are removed
        # Input: the group group_name with the description "group description"
        # Expected Result: the group group_name with the description group description

        ("empty_description", "g", "\"\"", "g", ""),
        # An empty description
        # Input: the group g with the description ""
        # Expected Result: the group g with an empty description

        ("description_with_punctuation", "physics", "\"Ocean physics: mixing, advection\"", "physics",
         "Ocean physics: mixing, advection"),
        # Punctuation in the description is kept
        # Input: the group physics with the description "Ocean physics: mixing, advection"
        # Expected Result: the description without quotes
    ])
    def test_visitParamGroupAssignStat(self, test_name, name, description, expected_name, expected_description):
        ctx = DeclarationParser.ParamGroupAssignStatContext(parser=None,
                                                            ctx=DeclarationParser.DeclarationModelContext(parser=None))
        ctx.name = self.set_token(name)
        ctx.description = self.set_token(description)

        result = self.make_visitor().visitParamGroupAssignStat(ctx)

        self.assertIsInstance(result, ParameterGroup, test_name)
        self.assertEqual(expected_name, result.name, test_name)
        self.assertEqual(expected_description, result.description, test_name)

    @parameterized.expand([
        ("int_with_unit", "def param1 int : meter = 0", "param1", BaseType("int"), SIUnit(None, UnitKind.Meter), 0,
         ""),
        # A parameter of a basic type with an SI unit
        # Input: 'def param1 int : meter = 0'
        # Expected Result: param1 of type int, unit meter, default value 0, no description

        ("float_with_custom_unit", "def p2 float : \"p2 unit\" = 1.5", "p2", BaseType("float"), CustomUnit("p2 unit"),
         1.5, ""),
        # A string after the colon is a custom unit
        # Input: 'def p2 float : "p2 unit" = 1.5'
        # Expected Result: p2 of type float, the custom unit p2 unit, default value 1.5

        ("with_description", "def p3 int : meter , \"p3 description\" = 3", "p3", BaseType("int"),
         SIUnit(None, UnitKind.Meter), 3, "p3 description"),
        # Regression: the quotes of parameter descriptions were kept, unlike those of groups and features
        # Input: 'def p3 int : meter , "p3 description" = 3'
        # Expected Result: p3 with the description p3 description without quotes

        ("empty_description", "def p4 int : meter , \"\" = 4", "p4", BaseType("int"), SIUnit(None, UnitKind.Meter), 4,
         ""),
        # An empty description
        # Input: 'def p4 int : meter , "" = 4'
        # Expected Result: p4 with an empty description
    ])
    def test_visitParamAssignStat_basic_type(self, test_name, declaration, expected_name, expected_type,
                                             expected_unit, expected_value, expected_description):
        model = self.parse_code(f"model eval group g : \"group description\" {{ {declaration} }}")

        group: ParameterGroup = model.groups.get("g")
        self.assertIsInstance(group, ParameterGroup, test_name)
        self.assertEqual(("g", "group description"), (group.name, group.description), test_name)
        self.assertEqual([expected_name], list(group.parameters), test_name)
        parameter = group.parameters[expected_name]
        self.assertEqual(expected_type, parameter.type, test_name)
        self.assertEqual(expected_unit, parameter.unit, test_name)
        self.assertEqual(expected_value, parameter.default_value.value, test_name)
        self.assertEqual(expected_description, parameter.description, test_name)

    @parameterized.expand([
        ("range_type", RangeType(name="r", type=int, minimum=0, maximum=10), "r", RangeType),
        # A reference to a range type
        # Input: the range type r declared in the model, the type reference r
        # Expected Result: the range type r

        ("enumeration_type", EnumeralType(name="Color"), "Color", EnumeralType),
        # A reference to an enumeration type
        # Input: the enumeration type Color declared in the model, the type reference Color
        # Expected Result: the enumeration type Color

        ("base_type_name", BaseType("length"), "length", BaseType),
        # A reference to a named base type
        # Input: the named type length declared in the model, the type reference length
        # Expected Result: the type length
    ])
    def test_visitParamType_type_reference(self, test_name, declared_type, reference, expected_class):
        param_type_context = DeclarationParser.ParamTypeContext(parent=None, parser=None)
        type_reference = DeclarationParser.TypeReferenceContext(parent=param_type_context, parser=None)
        type_reference.type_ = self.set_token(reference)
        param_type_context.addChild(type_reference)

        result = self.make_visitor(type=declared_type).visitParamType(param_type_context)

        self.assertIsInstance(result, expected_class, test_name)
        self.assertIs(declared_type, result, test_name)
        self.assertEqual(reference, result.name, test_name)

    @parameterized.expand([
        ("red", "red"),
        # The first enumeral as default value
        # Input: 'def param1 Color : "pixel" = red'
        # Expected Result: the default value of the enumeral red

        ("green", "green"),
        # An enumeral in the middle
        # Input: 'def param1 Color : "pixel" = green'
        # Expected Result: the default value of the enumeral green

        ("blue", "blue"),
        # The last enumeral
        # Input: 'def param1 Color : "pixel" = blue'
        # Expected Result: the default value of the enumeral blue
    ])
    def test_visitParamAssignStat_enumeration(self, test_name, enumeral):
        model: DeclarationModel = self.parse_code(ENUMERATION_MODEL % enumeral)

        group: ParameterGroup = model.groups.get("group_name")
        self.assertIsInstance(group, ParameterGroup, test_name)
        self.assertEqual(("group_name", "group description"), (group.name, group.description), test_name)

        color: EnumeralType = model.types["Color"]
        self.assertEqual(["param1"], list(group.parameters), test_name)
        parameter = group.parameters["param1"]
        self.assertEqual(color, parameter.type, test_name)
        self.assertEqual(color.enumerals[enumeral].value, parameter.default_value.value, test_name)
        self.assertEqual("", parameter.description, test_name)


if __name__ == '__main__':
    unittest.main()
