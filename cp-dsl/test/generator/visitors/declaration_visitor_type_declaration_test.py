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


    def test_visitDeclarationModel(self):
        model = self.parse_code("model eval")
        self.assertEqual(model.name, "eval", "Name not set")

    def test_visitDeclaredType(self):
        self.fail()

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

    def test_visitParamType_inline_enumeration_type(self):
        param_type_context = DeclarationParser.ParamTypeContext(parent=None, parser=None)
        inline_enumeration_type = DeclarationParser.InlineEnumerationTypeContext(parent=param_type_context, parser=None)

        enum1 = DeclarationParser.EnumeralContext(parent=inline_enumeration_type, parser=None)
        enum1.name = self.set_token("FIRST")
        enum1.value = self.set_token(1)
        inline_enumeration_type.addChild(enum1)

        enum2 = DeclarationParser.EnumeralContext(parent=inline_enumeration_type, parser=None)
        enum2.name = self.set_token("SECOND")
        enum2.value = self.set_token(2)
        inline_enumeration_type.addChild(enum2)

        inline_enumeration_type.values = [enum1, enum2]

        param_type_context.addChild(inline_enumeration_type)

        result = self.make_visitor().visitParamType(param_type_context)

        self.assertIsInstance(result, InlineEnumeralType, "wrong type")
        self.assertEqual(len(result._enumerals),2, "Wrong number")
        self.assertEqual(list(result._enumerals.keys()), ["FIRST", "SECOND"], "Wrong keys")
        enumerals = list(result._enumerals.values())
        self.assertEqual(enumerals[0].name, "FIRST", "Wrong name")
        self.assertEqual(enumerals[0].value, 1, "Wrong value")
        self.assertEqual(enumerals[1].name, "SECOND", "Wrong name")
        self.assertEqual(enumerals[1].value, 2, "Wrong value")

    def test_visitParamType_array_type(self):
        param_type_context = DeclarationParser.ParamTypeContext(parent=None, parser=None)
        array_type_context = DeclarationParser.ArrayTypeContext(parent=param_type_context, parser=None)
        array_type_context.type_ = self.set_token("int")

        dim1 = DeclarationParser.SizeDimensionContext(parent=array_type_context, parser=None)
        dim1.size = self.set_token(5)
        array_type_context.addChild(dim1)

        dim2 = DeclarationParser.RangeDimensionContext(parent=array_type_context, parser=None)
        dim2.lowerBound = self.set_token(2)
        dim2.upperBound = self.set_token(10)
        array_type_context.addChild(dim2)

        array_type_context.dimensions = [dim1, dim2]
        param_type_context.addChild(array_type_context)

        result = self.make_visitor().visitParamType(param_type_context)

        self.assertIsInstance(result, ArrayType, "wrong type")
        self.assertEqual(len(result._dimensions), 2, "Wrong number of dimensions")
        self.assertEqual(result._dimensions[0].lower, 0, "Wrong lower bound")
        self.assertEqual(result._dimensions[0].upper, 4, "Wrong upper bound")
        self.assertEqual(result._dimensions[1].lower, 2, "Wrong lower bound")
        self.assertEqual(result._dimensions[1].upper, 10, "Wrong upper bound")

    def test_visitArrayType(self):
        array_type_context = DeclarationParser.ArrayTypeContext(parent=None, parser=None)
        array_type_context.type_ = self.set_token("int")

        dim1 = DeclarationParser.SizeDimensionContext(parent=array_type_context, parser=None)
        dim1.size = self.set_token(5)
        array_type_context.addChild(dim1)

        dim2 = DeclarationParser.RangeDimensionContext(parent=array_type_context, parser=None)
        dim2.lowerBound = self.set_token(2)
        dim2.upperBound = self.set_token(10)
        array_type_context.addChild(dim2)

        array_type_context.dimensions = [dim1, dim2]

        result:ArrayType = self.make_visitor().visitArrayType(array_type_context)

        self.assertIsInstance(result, ArrayType, "wrong type")
        self.assertEqual(len(result._dimensions), 2, "Wrong number of dimensions")
        self.assertEqual(result._dimensions[0].lower, 0, "Wrong lower bound")
        self.assertEqual(result._dimensions[0].upper, 4, "Wrong upper bound")
        self.assertEqual(result._dimensions[1].lower, 2, "Wrong lower bound")
        self.assertEqual(result._dimensions[1].upper, 10, "Wrong upper bound")

    def test_visitSizeDimension_code_with_value(self):
        self.visitSizeDimension_code("10")

    def test_visitSizeDimension_code_without_value(self):
        self.visitSizeDimension_code("")

    def visitSizeDimension_code(self, size:str):
        code = """
            model eval
                group test: "" {
                    def param int[""" + size + """] : meter
                }
        """
        model = self.parse_code(code)

        group:ParameterGroup = model._groups.get("test")

        for p in group._parameters.values():
            type:ArrayType = p._type

            self.assertIsInstance(type, ArrayType, "Wrong type")
            self.assertEqual(len(type._dimensions), 1, "Wrong number of dimensions")
            dim:Dimension = type._dimensions[0]
            self.assertEqual(dim.lower, 0, "Wrong lower bound")
            if size == "":
                self.assertEqual(dim.upper, None, "Wrong upper bound")
            else:
                self.assertEqual(dim.upper, int(size)-1, "Wrong upper bound")


    def test_visitSizeDimension_with_value(self):
        size_dimension = DeclarationParser.SizeDimensionContext(parent=None, parser=None)
        size_dimension.size = self.set_token("9")

        result = self.make_visitor().visitSizeDimension(size_dimension)

        self.assertIsInstance(result, Dimension, "Wrong type")
        self.assertEqual(result.lower, 0, "Wrong lower bound")
        self.assertEqual(result.upper, 8, "Wrong upper bound")

    def test_visitSizeDimension_without_value(self):
        size_dimension = DeclarationParser.SizeDimensionContext(parent=None, parser=None)
        size_dimension.size = None

        result = self.make_visitor().visitSizeDimension(size_dimension)

        self.assertIsInstance(result, Dimension, "Wrong type")
        self.assertEqual(result.lower, 0, "Wrong lower bound")
        self.assertEqual(result.upper, None, "Wrong upper bound")

    def visitRangeDimension_code(self, lower:int, upper:int):
        if lower is None:
            if upper is None:
                range = ":"
            else:
                range = f":{upper}"
        else:
            if upper is None:
                range = f"{lower}:"
            else:
                range = f"{lower}:{upper}"

        code = """
            model eval
                group test: "" {
                    def param int[""" + range + """] : meter
                }
        """
        model = self.parse_code(code)

        group:ParameterGroup = model._groups.get("test")

        for p in group._parameters.values():
            type:ArrayType = p._type

            self.assertIsInstance(type, ArrayType, "Wrong type")
            self.assertEqual(len(type._dimensions), 1, "Wrong number of dimensions")
            dim:Dimension = type._dimensions[0]

            self.assertEqual(dim.lower, lower, "Wrong lower bound")
            self.assertEqual(dim.upper, upper, "Wrong upper bound")

    def test_visitRangeDimension_code_lu(self):
        self.visitRangeDimension_code(3,7)

    def test_visitRangeDimension_code_xu(self):
        self.visitRangeDimension_code(None,7)

    def test_visitRangeDimension_code_lx(self):
        self.visitRangeDimension_code(3,None)

    def test_visitTypeReference(self):
        type_reference = DeclarationParser.TypeReferenceContext(parent=None, parser=None)
        type_reference.type_ = self.set_token("r")

        result = self.make_visitor(type=RangeType(name="r", type=int, minimum=0, maximum=10)).visitTypeReference(type_reference)

        self.assertIsInstance(result, RangeType, "wrong type")
        self.assertEqual(result.name, "r", "wrong type name")

    def test_visitInlineEnumerationType(self):
        model = self.parse_code("model eval group g : \"group description\" { def param1 ( RED, GREEN, BLUE ) : meter = BLUE }")

        group:ParameterGroup = model._groups.get("g")

        self.assertIsInstance(group, ParameterGroup, f"Wrong type {type(group)}")
        self.assertEqual(group.name, "g", "Wrong name")
        self.assertEqual(group._description, "group description", "Wrong description")

        self.assertEqual(len(group._parameters.values()), 1, "Wrong number of parameters")
        for p in group._parameters.values():
            self.assertEqual(p.name, "param1", "Wrong param name")
            self.assertIsInstance(p._type, InlineEnumeralType, "Wrong type")
            enumeral_type:InlineEnumeralType = p._type
            self.assertEqual(len(enumeral_type._enumerals), 3, "Wrong number of enumerals")
            self.assertEqual(enumeral_type._enumerals.get("RED").name, "RED", "Not red")
            self.assertEqual(enumeral_type._enumerals.get("RED").value, 0, "Not 0 for red")
            self.assertEqual(enumeral_type._enumerals.get("GREEN").name, "GREEN", "Not green")
            self.assertEqual(enumeral_type._enumerals.get("GREEN").value, 1, "Not 1 for green")
            self.assertEqual(enumeral_type._enumerals.get("BLUE").name, "BLUE", "Not blue")
            self.assertEqual(enumeral_type._enumerals.get("BLUE").value, 2, "Not 2 for blue")


if __name__ == '__main__':
    unittest.main()
