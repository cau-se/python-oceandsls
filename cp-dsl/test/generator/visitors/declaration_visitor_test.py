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
from model.symbol_table import Scope
from model.type_system import EnumType
from antlr4 import InputStream, CommonTokenStream

from dcllspserver.gen.python.Declaration.DeclarationLexer import DeclarationLexer
from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from common.logger import GeneratorLogger
from common.configuration import CompileFlags

class TestStream(InputStream):

    fileName = "test"

    def __init__(self, data: str) -> None:
        super().__init__(data)

class TestGeneratorDeclarationVisitor(unittest.TestCase):

    def test_visitEnumerationType(self):
        logger = GeneratorLogger(CompileFlags.STRICT)
        symbol_table = Scope()
        visitor = GeneratorDeclarationVisitor(symbol_table, logger)

        input_stream = TestStream("model eval types enum Color { red, green, blue }")

        lexer = DeclarationLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DeclarationParser(stream)

        visitor.visit(parser.declarationModel())

        result = symbol_table._types.get("Color")
        expected = EnumType("Color")
        expected.enums = {"red":0, "green":1, "blue":2}

        self.assertEqual(result.name, expected.name, "Names do not match")
        self.assertEqual(result.enums, expected.enums, "Not the same symbols")

if __name__ == '__main__':
    unittest.main()