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

from cpdsl.model.declaration_model import DeclarationModel, ParameterGroup
from cpdsl.model.type_system import EnumeralType, Enumeral, RangeType, ArrayType, Dimension, InlineEnumeralType, \
    BaseType

from dcllspserver.gen.python.Declaration.DeclarationParser import DeclarationParser

from cpdsl.common.logger import GeneratorLogger
from cpdsl.common.configuration import CompileFlags

from generator.visitors.test_utils import AbstractTestGeneratorDeclarationVisitor

TEMPERATURE = ("range", 0, 273)
COLOR = ("enum", {"red": 0, "green": 1, "blue": 2})


class TestGeneratorDeclarationVisitor(AbstractTestGeneratorDeclarationVisitor):

    logger = GeneratorLogger(CompileFlags.STRICT)

    def check_type(self, test_name, declared_type, expected):
        """Check a range ("range", minimum, maximum) or enumeration ("enum", {enumeral: value}) type."""
        if expected[0] == "range":
            self.assertIsInstance(declared_type, RangeType, test_name)
            self.assertEqual(expected[1:], (declared_type.minimum, declared_type.maximum), test_name)
        else:
            self.assertIsInstance(declared_type, EnumeralType, test_name)
            self.assertEqual({name: Enumeral(name, value) for name, value in expected[1].items()},
                             declared_type.enumerals, test_name)

    def array_type_context(self, dimensions, parent=None):
        """An arrayType context of int with ("size", n) and ("range", lower, upper) dimensions."""
        array_type_context = DeclarationParser.ArrayTypeContext(parent=parent, parser=None)
        array_type_context.type_ = self.set_token("int")
        array_type_context.dimensions = []
        for dimension in dimensions:
            if dimension[0] == "size":
                ctx = DeclarationParser.SizeDimensionContext(parent=array_type_context, parser=None)
                ctx.size = self.set_token(dimension[1])
            else:
                ctx = DeclarationParser.RangeDimensionContext(parent=array_type_context, parser=None)
                ctx.lowerBound = self.set_token(dimension[1])
                ctx.upperBound = self.set_token(dimension[2])
            array_type_context.addChild(ctx)
            array_type_context.dimensions.append(ctx)
        return array_type_context

    def parameter_type(self, declaration):
        """The type of the parameter param of the group test declared by the given type and unit."""
        model = self.parse_code(f"model eval group test: \"\" {{ def param {declaration} }}")
        group: ParameterGroup = model.groups.get("test")
        return group.parameters["param"].type

    @parameterized.expand([
        ("range_and_enumeration", "range Temperature int [0: 273] enum Color { red, green, blue }",
         {"Temperature": TEMPERATURE, "Color": COLOR}),
        # Several declared types
        # Input: the range type Temperature [0: 273] and the enumeration Color { red, green, blue }
        # Expected Result: both types

        ("range", "range Temperature int [0: 273]", {"Temperature": TEMPERATURE}),
        # A range type
        # Input: 'range Temperature int [0: 273]'
        # Expected Result: the range type Temperature from 0 to 273

        ("enumeration", "enum Color { red, green, blue }", {"Color": COLOR}),
        # An enumeration type, the enumerals are numbered in order
        # Input: 'enum Color { red, green, blue }'
        # Expected Result: the enumeration type Color with red 0, green 1 and blue 2

        ("float_range", "range Depth float [-10.5: 0]", {"Depth": ("range", -10.5, 0.0)}),
        # A range of floats with a negative minimum
        # Input: 'range Depth float [-10.5: 0]'
        # Expected Result: the range type Depth from -10.5 to 0.0

        ("two_ranges", "range Temperature int [0: 273] range Level int [1: 5]",
         {"Temperature": TEMPERATURE, "Level": ("range", 1, 5)}),
        # Several types of the same kind
        # Input: the range types Temperature [0: 273] and Level [1: 5]
        # Expected Result: both range types
    ])
    def test_visitDeclaredType(self, test_name, declarations, expected_types):
        model: DeclarationModel = self.parse_code(f"model eval types {declarations}")

        self.assertEqual(list(expected_types), list(model.types), test_name)
        for name, expected in expected_types.items():
            self.assertEqual(name, model.types[name].name, test_name)
            self.check_type(f"{test_name}: {name}", model.types[name], expected)

    @parameterized.expand([
        ("first_enumeral", "red", "0", Enumeral("red", 0)),
        # An enumeral with a value
        # Input: the enumeral red with the value 0
        # Expected Result: Enumeral red 0

        ("other_value", "blue", "2", Enumeral("blue", 2)),
        # The value is converted to int
        # Input: the enumeral blue with the value '2'
        # Expected Result: Enumeral blue 2

        ("without_value", "x", None, Enumeral("x", -1)),
        # The value of an enumeral without value is -1 (it is set by the enumeration)
        # Input: the enumeral x without value
        # Expected Result: Enumeral x -1
    ])
    def test_visitEnumeral(self, test_name, name, value, expected):
        ctx = DeclarationParser.EnumeralContext(parent=None, parser=None, invokingState=1)
        ctx.name = self.set_token(name)
        ctx.value = None if value is None else self.set_token(value)

        result = self.make_visitor().visitEnumeral(ctx)

        self.assertIsInstance(result, Enumeral, test_name)
        self.assertEqual(expected, result, test_name)

    @parameterized.expand([
        ("two_enumerals", [("FIRST", 1), ("SECOND", 2)]),
        # An inline enumeration with explicit values
        # Input: the enumerals FIRST 1 and SECOND 2
        # Expected Result: an inline enumeration type with FIRST 1 and SECOND 2 in order

        ("one_enumeral", [("ONLY", 0)]),
        # An inline enumeration with a single enumeral
        # Input: the enumeral ONLY 0
        # Expected Result: an inline enumeration type with ONLY 0

        ("three_enumerals", [("LOW", 1), ("MID", 5), ("HIGH", 10)]),
        # Values need not be consecutive
        # Input: the enumerals LOW 1, MID 5 and HIGH 10
        # Expected Result: an inline enumeration type with LOW 1, MID 5 and HIGH 10
    ])
    def test_visitParamType_inline_enumeration_type(self, test_name, enumerals):
        param_type_context = DeclarationParser.ParamTypeContext(parent=None, parser=None)
        inline_enumeration_type = DeclarationParser.InlineEnumerationTypeContext(parent=param_type_context, parser=None)
        inline_enumeration_type.values = []
        for name, value in enumerals:
            enumeral = DeclarationParser.EnumeralContext(parent=inline_enumeration_type, parser=None)
            enumeral.name = self.set_token(name)
            enumeral.value = self.set_token(value)
            inline_enumeration_type.addChild(enumeral)
            inline_enumeration_type.values.append(enumeral)
        param_type_context.addChild(inline_enumeration_type)

        result = self.make_visitor().visitParamType(param_type_context)

        self.assertIsInstance(result, InlineEnumeralType, test_name)
        self.assertEqual([name for name, _ in enumerals], list(result.enumerals.keys()), test_name)
        self.assertEqual([Enumeral(name, value) for name, value in enumerals], list(result.enumerals.values()),
                         test_name)

    @parameterized.expand([
        ("param_type_size_and_range", True, [("size", 5), ("range", 2, 10)], [(0, 4), (2, 10)]),
        # An array type as parameter type
        # Input: a parameter type with the array type int[5, 2:10]
        # Expected Result: the dimensions 0..4 and 2..10

        ("size_and_range", False, [("size", 5), ("range", 2, 10)], [(0, 4), (2, 10)]),
        # A size dimension counts from 0
        # Input: the array type int[5, 2:10]
        # Expected Result: the dimensions 0..4 and 2..10

        ("size", False, [("size", 3)], [(0, 2)]),
        # A single size dimension
        # Input: the array type int[3]
        # Expected Result: the dimension 0..2

        ("range", False, [("range", 1, 4)], [(1, 4)]),
        # A single range dimension
        # Input: the array type int[1:4]
        # Expected Result: the dimension 1..4
    ])
    def test_visitArrayType(self, test_name, as_param_type, dimensions, expected_dimensions):
        if as_param_type:
            param_type_context = DeclarationParser.ParamTypeContext(parent=None, parser=None)
            param_type_context.addChild(self.array_type_context(dimensions, param_type_context))
            result = self.make_visitor().visitParamType(param_type_context)
        else:
            result = self.make_visitor().visitArrayType(self.array_type_context(dimensions))

        self.assertIsInstance(result, ArrayType, test_name)
        self.assertEqual(expected_dimensions, [(d.lower, d.upper) for d in result.dimensions], test_name)

    @parameterized.expand([
        ("with_value", "10", (0, 9)),
        # A size counts from 0
        # Input: 'def param int[10] : meter'
        # Expected Result: the dimension 0..9

        ("without_value", "", (0, None)),
        # A dimension without size is open
        # Input: 'def param int[] : meter'
        # Expected Result: the dimension 0..None

        ("size_one", "1", (0, 0)),
        # A size of one
        # Input: 'def param int[1] : meter'
        # Expected Result: the dimension 0..0

        ("several_dimensions", "3,1:4", (0, 2), (1, 4)),
        # Dimensions are separated by commas
        # Input: 'def param int[3,1:4] : meter'
        # Expected Result: the dimensions 0..2 and 1..4
    ])
    def test_visitSizeDimension_code(self, test_name, size, *expected_dimensions):
        array_type: ArrayType = self.parameter_type(f"int[{size}] : meter")

        self.assertIsInstance(array_type, ArrayType, test_name)
        self.assertEqual(BaseType("int"), array_type.type, test_name)
        self.assertEqual(list(expected_dimensions), [(d.lower, d.upper) for d in array_type.dimensions], test_name)

    @parameterized.expand([
        ("with_value", "9", (0, 8)),
        # A size dimension counts from 0
        # Input: a size dimension with the size 9
        # Expected Result: the dimension 0..8

        ("without_value", None, (0, None)),
        # A size dimension without size is open
        # Input: a size dimension without size
        # Expected Result: the dimension 0..None

        ("size_one", "1", (0, 0)),
        # A size of one
        # Input: a size dimension with the size 1
        # Expected Result: the dimension 0..0
    ])
    def test_visitSizeDimension(self, test_name, size, expected_bounds):
        size_dimension = DeclarationParser.SizeDimensionContext(parent=None, parser=None)
        size_dimension.size = None if size is None else self.set_token(size)

        result = self.make_visitor().visitSizeDimension(size_dimension)

        self.assertIsInstance(result, Dimension, test_name)
        self.assertEqual(expected_bounds, (result.lower, result.upper), test_name)

    @parameterized.expand([
        ("lower_and_upper", "3:7", 3, 7),
        # A range with both bounds
        # Input: 'def param int[3:7] : meter'
        # Expected Result: the dimension 3..7

        ("upper_only", ":7", None, 7),
        # A range without lower bound
        # Input: 'def param int[:7] : meter'
        # Expected Result: the dimension None..7

        ("lower_only", "3:", 3, None),
        # A range without upper bound
        # Input: 'def param int[3:] : meter'
        # Expected Result: the dimension 3..None

        ("open", ":", None, None),
        # A range without bounds
        # Input: 'def param int[:] : meter'
        # Expected Result: the dimension None..None

        ("negative_lower_bound", "-1:1", -1, 1),
        # A negative lower bound
        # Input: 'def param int[-1:1] : meter'
        # Expected Result: the dimension -1..1
    ])
    def test_visitRangeDimension_code(self, test_name, dimension, lower, upper):
        array_type: ArrayType = self.parameter_type(f"int[{dimension}] : meter")

        self.assertIsInstance(array_type, ArrayType, test_name)
        self.assertEqual([(lower, upper)], [(d.lower, d.upper) for d in array_type.dimensions], test_name)

    @parameterized.expand([
        ("range_type", RangeType(name="r", type=int, minimum=0, maximum=10), "r", RangeType),
        # A reference to a declared range type
        # Input: the type reference r, the range type r declared in the model
        # Expected Result: the range type r

        ("enumeration_type", EnumeralType("Color"), "Color", EnumeralType),
        # A reference to a declared enumeration type
        # Input: the type reference Color, the enumeration type Color declared in the model
        # Expected Result: the enumeration type Color

        ("named_base_type", BaseType("length"), "length", BaseType),
        # A reference to another declared type
        # Input: the type reference length, the type length declared in the model
        # Expected Result: the type length
    ])
    def test_visitTypeReference(self, test_name, declared_type, reference, expected_class):
        type_reference = DeclarationParser.TypeReferenceContext(parent=None, parser=None)
        type_reference.type_ = self.set_token(reference)

        result = self.make_visitor(type=declared_type).visitTypeReference(type_reference)

        self.assertIsInstance(result, expected_class, test_name)
        self.assertIs(declared_type, result, test_name)

    @parameterized.expand([
        ("three_enumerals", "( RED, GREEN, BLUE ) : meter = BLUE", {"RED": 0, "GREEN": 1, "BLUE": 2}, "BLUE"),
        # An inline enumeration numbers its enumerals in order
        # Input: 'def param1 ( RED, GREEN, BLUE ) : meter = BLUE'
        # Expected Result: RED 0, GREEN 1 and BLUE 2, the default value BLUE

        ("two_enumerals", "( ON, OFF ) : meter = OFF", {"ON": 0, "OFF": 1}, "OFF"),
        # Two enumerals
        # Input: 'def param1 ( ON, OFF ) : meter = OFF'
        # Expected Result: ON 0 and OFF 1, the default value OFF

        ("one_enumeral", "( SINGLE ) : meter = SINGLE", {"SINGLE": 0}, "SINGLE"),
        # A single enumeral
        # Input: 'def param1 ( SINGLE ) : meter = SINGLE'
        # Expected Result: SINGLE 0, the default value SINGLE
    ])
    def test_visitInlineEnumerationType(self, test_name, declaration, expected_enumerals, expected_default):
        model = self.parse_code(f"model eval group g : \"group description\" {{ def param1 {declaration} }}")

        group: ParameterGroup = model.groups.get("g")
        self.assertIsInstance(group, ParameterGroup, test_name)
        self.assertEqual(("g", "group description"), (group.name, group.description), test_name)
        self.assertEqual(["param1"], list(group.parameters), test_name)
        parameter = group.parameters["param1"]
        self.assertIsInstance(parameter.type, InlineEnumeralType, test_name)
        self.assertEqual({name: Enumeral(name, value) for name, value in expected_enumerals.items()},
                         parameter.type.enumerals, test_name)
        self.assertEqual(Enumeral(expected_default, expected_enumerals[expected_default]), parameter.default_value,
                         test_name)

    @parameterized.expand([
        ("duplicate", "( RED, RED )", ["RED"], ["RED"]),
        # A duplicate enumeral is reported and not added
        # Input: 'def param1 ( RED, RED ) : meter'
        # Expected Result: one error about RED, the enumeral RED once

        ("duplicate_after_other", "( A, B, A )", ["A"], ["A", "B"]),
        # A duplicate after another enumeral
        # Input: 'def param1 ( A, B, A ) : meter'
        # Expected Result: one error about A, the enumerals A and B

        ("triplicate", "( X, X, X )", ["X", "X"], ["X"]),
        # Every repetition is reported
        # Input: 'def param1 ( X, X, X ) : meter'
        # Expected Result: two errors about X, the enumeral X once
    ])
    def test_visitInlineEnumerationType_duplicate_enumeral(self, test_name, enumeration, expected_duplicates,
                                                           expected_enumerals):
        known_messages = len(self.logger.messages)
        model = self.parse_code(f"model eval group g : \"\" {{ def param1 {enumeration} : meter }}")

        messages = [message for _, _, message in self.logger.messages[known_messages:]]
        self.assertEqual([f"Enumeral {name} already exists in the inline enumeration" for name in expected_duplicates],
                         messages, test_name)
        self.assertEqual(expected_enumerals, list(model.groups["g"].parameters["param1"].type.enumerals), test_name)


if __name__ == '__main__':
    unittest.main()
