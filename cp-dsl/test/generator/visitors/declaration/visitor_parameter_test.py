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

from model.declaration_model import ParameterGroup
from model.type_system import RangeType, BaseType

from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from model.declaration_model import DeclarationModel
from model.type_system import EnumeralType

from test_utils import AbstractTestGeneratorDeclarationVisitor

class TestGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    def test_visitParamGroupAssignStat(self):
        ctx = DeclarationParser.ParamGroupAssignStatContext(parser=None, ctx=DeclarationParser.DeclarationModelContext(parser=None))
        ctx.name = self.set_token("group_name")
        ctx.description = self.set_token("\"group description\"")

        result = self.make_visitor().visitParamGroupAssignStat(ctx)

        self.assertIsInstance(result, ParameterGroup, f"Wrong type {type(result)}")
        self.assertEqual(result.name, "group_name", "Wrong name")
        self.assertEqual(result.description, "group description", "Wrong description")


    def test_visitParamAssignStat_basic_type(self):
        model = self.parse_code("model eval group g : \"group description\" { def param1 int : meter = 0 }")

        group:ParameterGroup = model.groups.get("g")

        self.assertIsInstance(group, ParameterGroup, f"Wrong type {type(group)}")
        self.assertEqual(group.name, "g", "Wrong name")
        self.assertEqual(group.description, "group description", "Wrong description")

        t = BaseType("int")
        self.assertEqual(len(group.parameters.values()), 1, "Wrong number of parameters")
        for p in group.parameters.values():
            self.assertEqual(p.name, "param1", "Wrong param name")
            self.assertEqual(p.type, t, "Wrong type")
            print(f"DEFAULT VALUE TYPE {type(p.default_value)}")

            # TODO
#            self.assertEqual(p._unit, u, "Should be meter")
            self.assertEqual(p.default_value.value, 0, "Wrong value")
            self.assertEqual(p.description, "", "Wrong description")

    def test_visitParamType_type_reference(self):
        param_type_context = DeclarationParser.ParamTypeContext(parent=None, parser=None)
        type_reference = DeclarationParser.TypeReferenceContext(parent=param_type_context, parser=None)
        type_reference.type_ = self.set_token("r")
        param_type_context.addChild(type_reference)

        result = self.make_visitor(type=RangeType(name="r", type=int, minimum=0, maximum=10)).visitParamType(param_type_context)

        self.assertIsInstance(result, RangeType, "wrong type")
        self.assertEqual(result.name, "r", "wrong type name")

    def test_visitParamAssignStat_enumeration(self):
        model:DeclarationModel = self.parse_code("""
            model eval
                types
                    enum Color { red, green, blue }
                group group_name : "group description" {
                    def param1 Color : "pixel" = green
                }
        """)

        group:ParameterGroup = model.groups.get("group_name")

        self.assertIsInstance(group, ParameterGroup, f"Wrong type {type(group)}")
        self.assertEqual(group.name, "group_name", "Wrong name")
        self.assertEqual(group.description, "group description", "Wrong description")

        t:EnumeralType = model.types["Color"]

        self.assertEqual(len(group.parameters.values()), 1, "Wrong number of parameters")
        for p in group.parameters.values():
            self.assertEqual(p.name, "param1", "Wrong param name")
            self.assertEqual(p.type, t, "Wrong type")
            self.assertEqual(p.default_value.value, t.enumerals["green"].value, "Wrong value")
            self.assertEqual(p.description, "", "Wrong description")

    def test_visitParamType_type_reference(self):
        param_type_context = DeclarationParser.ParamTypeContext(parent=None, parser=None)
        type_reference = DeclarationParser.TypeReferenceContext(parent=param_type_context, parser=None)
        type_reference.type_ = self.set_token("r")
        param_type_context.addChild(type_reference)

        result = self.make_visitor(type=RangeType(name="r", type=int, minimum=0, maximum=10)).visitParamType(param_type_context)

        self.assertIsInstance(result, RangeType, "wrong type")
        self.assertEqual(result.name, "r", "wrong type name")

if __name__ == '__main__':
    unittest.main()
