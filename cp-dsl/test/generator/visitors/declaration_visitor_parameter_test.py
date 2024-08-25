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
        self.assertEqual(len(group._parameters.values()), 1, "Wrong number of parameters")
        for p in group._parameters.values():
            self.assertEqual(p.name, "param1", "Wrong param name")
            self.assertEqual(p._type, t, "Wrong type")
            # TODO
#            self.assertEqual(p._unit, u, "Should be meter")
            self.assertEqual(p._default_value.value, 0, "Wrong value")
            self.assertEqual(p._description, "", "Wrong description")


    def test_visitParamType_type_reference(self):
        param_type_context = DeclarationParser.ParamTypeContext(parent=None, parser=None)
        type_reference = DeclarationParser.TypeReferenceContext(parent=param_type_context, parser=None)
        type_reference.type_ = self.set_token("r")
        param_type_context.addChild(type_reference)

        result = self.make_visitor(type=RangeType(name="r", type=int, minimum=0, maximum=10)).visitParamType(param_type_context)

        self.assertIsInstance(result, RangeType, "wrong type")
        self.assertEqual(result.name, "r", "wrong type name")


