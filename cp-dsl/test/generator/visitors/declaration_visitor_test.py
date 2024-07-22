#  Copyright (c) 2023.  OceanDSL (https://oceandsl.uni-kiel.de)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

__author__ = "reiner"

import unittest
from generator.visitors.declaration_visitor import GeneratorDeclarationVisitor
from model.declaration_model import DeclarationModel, ParameterGroup
from model.type_system import EnumeralType, Enumeral, RangeType
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken

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
        pass

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
        ctx.name = self.set_token("param_name")
        ctx.description = self.set_token("param description")

        result = self.make_visitor().visitParamGroupAssignStat(ctx)

        self.assertIsInstance(result, ParameterGroup, f"Wrong type {type(result)}")
        self.assertEqual(result.name, "param_name", "Wrong name")
        self.assertEqual(result._description, "param description", "Wrong description")

    def test_visitParamAssignStat(self):
        pass

    def test_visitParamType(self):
        pass

    def test_visitArrayType(self):
        pass

    def test_visitSizeDimension(self):
        pass

    def test_visitRangeDimension(self):
        pass

    def test_visitTypeReference(self):
        pass

    def test_visitFeatureAssignStat(self):
        pass

    def test_visitFeatureGroupAssignStat(self):
        pass

    def test_visitEKind(self):
        pass

    def test_visitArithmeticExpression(self):
        pass

    def test_visitMultiplicationExpression(self):
        pass

    def test_visitValueExpression(self):
        pass

    def test_visitParenthesisExpression(self):
        pass

    def test_visitLiteralExpression(self):
        pass

    def test_visitLiteral(self):
        pass

    def test_visitLongValue(self):
        pass

    def test_visitDoubleValue(self):
        pass

    def test_visitStringValue(self):
        pass

    def test_visitNamedElementReference(self):
        pass

    def test_visitSiunit(self):
        pass

    def test_visitCustomunit(self):
        pass

    def test_visitBasicUnit(self):
        pass

    def test_visitUnitSpecification(self):
        pass

    def test_visitComposedUnit(self):
        pass

    def test_visitInlineEnumerationType(self):
        pass

    def make_visitor(self) -> GeneratorDeclarationVisitor:
        model = DeclarationModel()
        return GeneratorDeclarationVisitor(model, self.logger)

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