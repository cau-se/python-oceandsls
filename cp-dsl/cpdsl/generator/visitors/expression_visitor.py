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
"""Visitor methods for the expressions, literals and references shared by the declaration and configuration grammars.

Both grammars import the same expression rules (Expression.g4), so the generated parsers have equally named contexts.
:class:`ExpressionVisitorMixin` builds the model expressions from them for :class:`GeneratorDeclarationVisitor` and
:class:`GeneratorConfigurationVisitor`, which set ``_parser`` to their parser class.
"""

import logging
from typing import List

from cpdsl.model.arithmetic_model import ArithmeticExpression, MultiplicationExpression, EMultiplicationOperator, \
    EAdditionOperator, ArrayExpression, IntValue, FloatValue, StringValue, BooleanValue
from cpdsl.model.declaration_model import DeclarationModel
from cpdsl.model.type_system import ArrayType, EnumeralType, InlineEnumeralType, base_types

_log = logging.getLogger(__name__)  # diagnostics go to logging, never to stdout


class ExpressionVisitorMixin:
    """Expression rules of the model visitors; expects ``_parser``, ``_model``, ``_scope``, ``_type_scope`` and
    ``_logger`` of the visitor and its ``visit()`` method."""

    _parser = None  # the generated parser class, whose context classes the expressions are checked against

    def print_symbol(self, elements:list, level:int):
        """Qualified name of the elements up to index ``level`` (at most all elements)."""
        return ".".join(element.text for element in elements[:level + 1])

    @property
    def symbol_table(self) -> DeclarationModel:
        return self._model

    def visitArithmeticExpression(self, ctx):
        if ctx.left is not None:
            if ctx.right is not None:
                left = self.visit(ctx.left)
                right = self.visit(ctx.right)
                op = self.visitEAdditionOperator(ctx.op)
                return ArithmeticExpression(ctx=ctx, unit=None, left=left, right=right, op=op)
            else:
                return self.visit(ctx.left)

        if len(ctx.children) == 1:
            expression = ctx.children[0]
            if isinstance(expression, self._parser.MultiplicationExpressionContext):
                return self.visitMultiplicationExpression(expression)
            else:
                _log.error(f"ERROR unsupported type in ArithmeticExpression {type(expression)}")
                return None
        else:
            _log.error("ERROR")
            return None

    def visitEAdditionOperator(self, ctx):
        value = ctx.getText()
        if value == EAdditionOperator.ADD.value:
            return EAdditionOperator.ADD
        if value == EAdditionOperator.SUB.value:
            return EAdditionOperator.SUB

        _log.error("Illegal addition operator")
        return None

    def visitMultiplicationExpression(self, ctx):
        if ctx.left is not None:
            if ctx.right is not None:
                left = self.visit(ctx.left)
                right = self.visit(ctx.right)
                op = self.visitEMultiplicationOperator(ctx.op)
                return MultiplicationExpression(ctx=ctx, unit=None, left=left, right=right, op=op)
            else:
                return self.visit(ctx.left)

        if len(ctx.children) == 1:
            expression = ctx.children[0]
            if isinstance(expression, self._parser.ValueExpressionContext):
                return self.visitValueExpression(expression)
            else:
                _log.error(f"ERROR unsupported type in ValueExpressionContext {type(expression)}")
                return None
        else:
            _log.error("ERROR")
            return None

    def visitEMultiplicationOperator(self, ctx):
        value = ctx.getText()
        if value == EMultiplicationOperator.MULT.value:
            return EMultiplicationOperator.MULT
        if value == EMultiplicationOperator.DIV.value:
            return EMultiplicationOperator.DIV
        if value == EMultiplicationOperator.MOD.value:
            return EMultiplicationOperator.MOD

        return None

    def visitValueExpression(self, ctx):
        if ctx.parenthesisExpression() is not None:
            return self.visitParenthesisExpression(ctx.parenthesisExpression())
        elif ctx.literalExpression() is not None:
            return self.visitLiteralExpression(ctx.literalExpression())
        elif ctx.namedElementReference() is not None:
            return self.visitNamedElementReference(ctx.namedElementReference())
        elif ctx.arrayExpression() is not None:
            return self.visitArrayExpression(ctx.arrayExpression())
        else:
            _log.error(f"ERROR something {ctx} {type(ctx)}")
            return None

    def visitParenthesisExpression(self, ctx):
        return self.visitArithmeticExpression(ctx.arithmeticExpression())

    def visitArrayExpression(self, ctx):
        elements:List[ArithmeticExpression] = []
        for element in ctx.elements:
            elements.append(self.visit(element))
        return ArrayExpression(ctx=ctx, unit=None, elements=elements)

    def visitLiteralExpression(self, ctx):
        return self.visitLiteral(ctx.literal())

    def visitLiteral(self, ctx):
        if len(ctx.children) == 1:
            literal = ctx.children[0]
            return self.visit(literal)
        else:
            _log.error("ERROR")
            return None

    def visitLongValue(self, ctx):
        return IntValue(ctx=ctx, unit=None, type=base_types["long"], value=int(ctx.value.text))

    def visitDoubleValue(self, ctx):
        return FloatValue(ctx=ctx, unit=None, type=base_types["double"], value=float(ctx.value.text))

    def visitStringValue(self, ctx):
        return StringValue(ctx=ctx, unit=None, type=base_types["string"], value=ctx.value.text[1:-1])

    def visitBooleanValue(self, ctx):
        return BooleanValue(ctx=ctx, unit=None, type=base_types["boolean"], value=ctx.value.text == "true")

    def visitNamedElementReference(self, ctx):
        depth = len(ctx.elements)
        scope = self._scope
        if depth > 1:
            for i in range(1,depth):
                scope = scope.parent

        # check whether it is a parameter
        parameter_level = 0
        param = True
        for i in range(0,depth):
            scope = scope.resolve_symbol(ctx.elements[i].text)
            if scope is None:
                parameter_level = i
                param = False
                break

        if param:
            return scope

        # check whether it is an enumeration
        if depth == 2: # Can be an enumeration
            data_type = self._model.types.get(ctx.elements[0].text)
            if isinstance(data_type, EnumeralType):
                enumeral = data_type.enumerals.get(ctx.elements[1].text, None)
                if enumeral is None:
                    self._logger.strict(ctx, f"Symbol {self.print_symbol(ctx.elements, 2)} does not refer to an enumeral nor parameter and parameter group")
                    return None
                else:
                    return enumeral
            else:
                self._logger.strict(ctx, f"Symbol {self.print_symbol(ctx.elements, 1)} does not refer to an enumeration type nor parameter and parameter group")
                return None

        # check whether it is an enumeration inferred by parameter type (or by the element type of an array)
        data_type = self._type_scope
        if isinstance(data_type, ArrayType):
            data_type = data_type.type
        if isinstance(data_type, EnumeralType) or isinstance(data_type, InlineEnumeralType):
            enumeral = data_type.enumerals.get(ctx.elements[0].text, None)
            if enumeral is None:
                self._logger.strict(ctx, f"Symbol {self.print_symbol(ctx.elements, 2)} does not refer to an enumeral nor parameter and parameter group")
                return None
            else:
                return enumeral

        # Strange cases
        self._logger.strict(ctx, f"Symbol {self.print_symbol(ctx.elements, len(ctx.elements))} cannot be resolved.")
        return None
