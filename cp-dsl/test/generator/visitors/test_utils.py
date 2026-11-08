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
from cpdsl.model.declaration_model import DeclarationModel
from antlr4 import InputStream, CommonTokenStream
from antlr4.Token import CommonToken
from antlr4 import TerminalNode
from antlr4.tree.Tree import TerminalNodeImpl

from cpdsl.generator.visitors.declaration_visitor import GeneratorDeclarationVisitor
from cpdsl.generator.visitors.configuration_visitor import GeneratorConfigurationVisitor

from dcllspserver.gen.python.Declaration.DeclarationLexer import DeclarationLexer
from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from conflspserver.gen.python.Configuration.ConfigurationLexer import ConfigurationLexer
from conflspserver.gen.python.Configuration.ConfigurationParser import ConfigurationParser

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.configuration import CompileFlags
from cpdsl.model.declaration_model import Parameter
from cpdsl.model.type_system import Enumeral
from cpdsl.model.arithmetic_model import ArithmeticExpression, MultiplicationExpression, EAdditionOperator, \
    EMultiplicationOperator, IntValue, FloatValue, StringValue, BooleanValue, ArrayExpression

class TestStream(InputStream):

    fileName = "test"

    def __init__(self, data: str) -> None:
        super().__init__(data)

class AbstractTestGeneratorDeclarationVisitor(unittest.TestCase):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def make_visitor(self, type=None) -> GeneratorDeclarationVisitor:
        model = DeclarationModel()
        if type is not None:
            model.types[type.name] = type
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

class AbstractTestGeneratorConfigurationVisitor(unittest.TestCase):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def make_visitor(self, type=None) -> GeneratorConfigurationVisitor:
        model = DeclarationModel()
        if type is not None:
            model.types[type.name] = type
        return GeneratorConfigurationVisitor(model, self.logger)

    def set_terminal(self, value:str) -> TerminalNode:
        return TerminalNodeImpl(self.set_token(value))

    def set_token(self, value:str) -> CommonToken:
        token = CommonToken()
        token.text = value
        return token

    def parse_code(self, code:str, model: DeclarationModel) -> DeclarationModel:
        visitor = GeneratorConfigurationVisitor(model, self.logger)

        input_stream = TestStream(code)

        lexer = ConfigurationLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = ConfigurationParser(stream)

        visitor.visit(parser.configurationModel())

        return model

    def parse_declaration_code(self, code:str) -> DeclarationModel:
        model = DeclarationModel()
        visitor = GeneratorDeclarationVisitor(model, self.logger)

        input_stream = TestStream(code)

        lexer = DeclarationLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = DeclarationParser(stream)

        visitor.visit(parser.declarationModel())

        return model


ARITHMETIC_OPERATORS = {EAdditionOperator.ADD: "+", EAdditionOperator.SUB: "-", EMultiplicationOperator.MULT: "*",
                        EMultiplicationOperator.DIV: "/", EMultiplicationOperator.MOD: "%"}


def describe_expression(expression):
    """A comparable description of an expression of the arithmetic model as nested tuples, e.g.
    ('+', ('int', 3), ('int', 4)) for 3 + 4, ('param', 'a') for a parameter reference and ('enum', 'red', 0) for an
    enumeral."""
    if isinstance(expression, (ArithmeticExpression, MultiplicationExpression)):
        return (ARITHMETIC_OPERATORS.get(expression.op, expression.op), describe_expression(expression.left),
                describe_expression(expression.right))
    for value_class, kind in ((IntValue, "int"), (FloatValue, "float"), (StringValue, "str"), (BooleanValue, "bool")):
        if isinstance(expression, value_class):
            return (kind, expression.value)
    if isinstance(expression, Parameter):
        return ("param", expression.name)
    if isinstance(expression, Enumeral):
        return ("enum", expression.name, expression.value)
    if isinstance(expression, ArrayExpression):
        return ("array", [describe_expression(element) for element in expression.elements])
    return expression
