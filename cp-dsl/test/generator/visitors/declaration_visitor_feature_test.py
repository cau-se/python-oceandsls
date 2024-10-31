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
from model.declaration_model import DeclarationModel, ParameterGroup, Parameter, FeatureGroup, Feature, EKind
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

class TestFeatureGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def test_visitFeatureAssignStat_parameter(self):
        code = """
            model eval
                required feature Base : "Base description" {
                    group TestParams : "Parameter group description" {
                        def p1 int : meter , "p1 description" = 0
                    }
                }
        """

        model = self.parse_code(code)

    def test_visitFeatureAssignStat_requires_excludes(self):
        code = """
            model eval
                required feature Base : "Base description" {
                    sub alternative
                        feature Feat1 : "Feature one"
                        feature Feat2 : "Feature two"
                }
                feature Second : "Second description" {
                    requires Base
                }
                feature Alternate : "Alternate description" {
                    requires Base
                    excludes Base.Feat2
                }
        """

        model = self.parse_code(code)

        base_feature:Feature = model._features.get("Base")


    def create_feature(self, name:str, required: bool, description:str, parent:ParserRuleContext=None):
        feature = DeclarationParser.FeatureAssignStatContext(parser=None, ctx=parent)
        feature.required = self.set_token("required")
        feature.name = self.set_token(f"\"{name}\"")
        feature.description = self.set_token(f"\"{description}\"")

        return feature

    def test_visitFeatureGroupAssignStat_base(self):
        code = """
            model eval
                required feature Base : "Base description" {
                    sub alternative
                        feature Feat1 : "Feature one"
                        feature Feat2 : "Feature two"
                }
        """

        model = self.parse_code(code)

        base_feature:Feature = model._features.get("Base")
        self.assertIsInstance(base_feature, Feature, f"Wrong type {type(base_feature)}")
        self.assertEqual(base_feature.name, "Base", "Wrong feature")
        self.assertEqual(base_feature._description, "Base description", "Wrong description")
        self.assertEqual(base_feature._required, True, "Feature must be required")
        self.assertEqual(len(base_feature._feature_sets), 1, "Wrong number of feature groups")
        feature_set = base_feature._feature_sets[0]
        f1 = feature_set._features.get("Feat1")
        f2 = feature_set._features.get("Feat2")

        self.assertIsInstance(f1, Feature, f"Wrong type {type(f1)}")
        self.assertEqual(f1.name, "Feat1", "Wrong feature name")
        self.assertEqual(f1._description, "Feature one", "Wrong description")

        self.assertIsInstance(f2, Feature, f"Wrong type {type(f2)}")
        self.assertEqual(f2.name, "Feat2", "Wrong feature name")
        self.assertEqual(f2._description, "Feature two", "Wrong description")

    def test_visitEKind_alternative(self):
        kind_ctx = DeclarationParser.EKindContext(parent=None, parser=None)
        kind_ctx.alternative = self.set_token('alternative')

        result = self.make_visitor().visitEKind(kind_ctx)
        self.assertEqual(result, EKind.ALTERNATIVE, "Wrong kind of feature group")

    def test_visitEKind_multiple(self):
        kind_ctx = DeclarationParser.EKindContext(parent=None, parser=None)
        kind_ctx.multiple = self.set_token('multiple')

        result = self.make_visitor().visitEKind(kind_ctx)
        self.assertEqual(result, EKind.MULTIPLE, "Wrong kind of feature group")

if __name__ == '__main__':
    unittest.main()
