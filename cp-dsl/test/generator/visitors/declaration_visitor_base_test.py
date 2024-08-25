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
from model.type_system import EnumeralType, Enumeral, RangeType, BaseType, ArrayType, Dimension, InternalEnumeralType, Enumeral
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

    #########################################
    # Utility functions
    #########################################
    # TODO move to a general and abstract test class

    def make_visitor(self, type=None) -> GeneratorDeclarationVisitor:
        model = DeclarationModel()
        if type is not None:
            model._types[type.name] = type
        return GeneratorDeclarationVisitor(model, self.logger)

    def set_terminal(self, value:str) -> TerminalNode:
        return TerminalNodeImpl(self.set_token(value))

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
