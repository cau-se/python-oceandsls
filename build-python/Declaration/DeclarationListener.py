# Generated from Declaration.g4 by ANTLR 4.10.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .DeclarationParser import DeclarationParser
else:
    from DeclarationParser import DeclarationParser

# This class defines a complete listener for a parse tree produced by DeclarationParser.
class DeclarationListener(ParseTreeListener):

    # Enter a parse tree produced by DeclarationParser#declarationModel.
    def enterDeclarationModel(self, ctx:DeclarationParser.DeclarationModelContext):
        pass

    # Exit a parse tree produced by DeclarationParser#declarationModel.
    def exitDeclarationModel(self, ctx:DeclarationParser.DeclarationModelContext):
        pass


    # Enter a parse tree produced by DeclarationParser#namedElement.
    def enterNamedElement(self, ctx:DeclarationParser.NamedElementContext):
        pass

    # Exit a parse tree produced by DeclarationParser#namedElement.
    def exitNamedElement(self, ctx:DeclarationParser.NamedElementContext):
        pass


    # Enter a parse tree produced by DeclarationParser#parameterGroupDeclaration.
    def enterParameterGroupDeclaration(self, ctx:DeclarationParser.ParameterGroupDeclarationContext):
        pass

    # Exit a parse tree produced by DeclarationParser#parameterGroupDeclaration.
    def exitParameterGroupDeclaration(self, ctx:DeclarationParser.ParameterGroupDeclarationContext):
        pass


    # Enter a parse tree produced by DeclarationParser#parameterDeclaration.
    def enterParameterDeclaration(self, ctx:DeclarationParser.ParameterDeclarationContext):
        pass

    # Exit a parse tree produced by DeclarationParser#parameterDeclaration.
    def exitParameterDeclaration(self, ctx:DeclarationParser.ParameterDeclarationContext):
        pass


    # Enter a parse tree produced by DeclarationParser#featureDeclaration.
    def enterFeatureDeclaration(self, ctx:DeclarationParser.FeatureDeclarationContext):
        pass

    # Exit a parse tree produced by DeclarationParser#featureDeclaration.
    def exitFeatureDeclaration(self, ctx:DeclarationParser.FeatureDeclarationContext):
        pass


    # Enter a parse tree produced by DeclarationParser#featureGroupDeclaration.
    def enterFeatureGroupDeclaration(self, ctx:DeclarationParser.FeatureGroupDeclarationContext):
        pass

    # Exit a parse tree produced by DeclarationParser#featureGroupDeclaration.
    def exitFeatureGroupDeclaration(self, ctx:DeclarationParser.FeatureGroupDeclarationContext):
        pass


    # Enter a parse tree produced by DeclarationParser#eKind.
    def enterEKind(self, ctx:DeclarationParser.EKindContext):
        pass

    # Exit a parse tree produced by DeclarationParser#eKind.
    def exitEKind(self, ctx:DeclarationParser.EKindContext):
        pass


    # Enter a parse tree produced by DeclarationParser#paramType.
    def enterParamType(self, ctx:DeclarationParser.ParamTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#paramType.
    def exitParamType(self, ctx:DeclarationParser.ParamTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#inlineEnumerationType.
    def enterInlineEnumerationType(self, ctx:DeclarationParser.InlineEnumerationTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#inlineEnumerationType.
    def exitInlineEnumerationType(self, ctx:DeclarationParser.InlineEnumerationTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#typeReference.
    def enterTypeReference(self, ctx:DeclarationParser.TypeReferenceContext):
        pass

    # Exit a parse tree produced by DeclarationParser#typeReference.
    def exitTypeReference(self, ctx:DeclarationParser.TypeReferenceContext):
        pass


    # Enter a parse tree produced by DeclarationParser#arrayType.
    def enterArrayType(self, ctx:DeclarationParser.ArrayTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#arrayType.
    def exitArrayType(self, ctx:DeclarationParser.ArrayTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#dimension.
    def enterDimension(self, ctx:DeclarationParser.DimensionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#dimension.
    def exitDimension(self, ctx:DeclarationParser.DimensionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#sizeDimension.
    def enterSizeDimension(self, ctx:DeclarationParser.SizeDimensionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#sizeDimension.
    def exitSizeDimension(self, ctx:DeclarationParser.SizeDimensionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#rangeDimension.
    def enterRangeDimension(self, ctx:DeclarationParser.RangeDimensionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#rangeDimension.
    def exitRangeDimension(self, ctx:DeclarationParser.RangeDimensionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#declaredType.
    def enterDeclaredType(self, ctx:DeclarationParser.DeclaredTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#declaredType.
    def exitDeclaredType(self, ctx:DeclarationParser.DeclaredTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#rangeType.
    def enterRangeType(self, ctx:DeclarationParser.RangeTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#rangeType.
    def exitRangeType(self, ctx:DeclarationParser.RangeTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#enumerationType.
    def enterEnumerationType(self, ctx:DeclarationParser.EnumerationTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#enumerationType.
    def exitEnumerationType(self, ctx:DeclarationParser.EnumerationTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#enumeral.
    def enterEnumeral(self, ctx:DeclarationParser.EnumeralContext):
        pass

    # Exit a parse tree produced by DeclarationParser#enumeral.
    def exitEnumeral(self, ctx:DeclarationParser.EnumeralContext):
        pass


    # Enter a parse tree produced by DeclarationParser#unitSpecification.
    def enterUnitSpecification(self, ctx:DeclarationParser.UnitSpecificationContext):
        pass

    # Exit a parse tree produced by DeclarationParser#unitSpecification.
    def exitUnitSpecification(self, ctx:DeclarationParser.UnitSpecificationContext):
        pass


    # Enter a parse tree produced by DeclarationParser#basicUnit.
    def enterBasicUnit(self, ctx:DeclarationParser.BasicUnitContext):
        pass

    # Exit a parse tree produced by DeclarationParser#basicUnit.
    def exitBasicUnit(self, ctx:DeclarationParser.BasicUnitContext):
        pass


    # Enter a parse tree produced by DeclarationParser#sIUnit.
    def enterSIUnit(self, ctx:DeclarationParser.SIUnitContext):
        pass

    # Exit a parse tree produced by DeclarationParser#sIUnit.
    def exitSIUnit(self, ctx:DeclarationParser.SIUnitContext):
        pass


    # Enter a parse tree produced by DeclarationParser#customUnit.
    def enterCustomUnit(self, ctx:DeclarationParser.CustomUnitContext):
        pass

    # Exit a parse tree produced by DeclarationParser#customUnit.
    def exitCustomUnit(self, ctx:DeclarationParser.CustomUnitContext):
        pass


    # Enter a parse tree produced by DeclarationParser#composedUnit.
    def enterComposedUnit(self, ctx:DeclarationParser.ComposedUnitContext):
        pass

    # Exit a parse tree produced by DeclarationParser#composedUnit.
    def exitComposedUnit(self, ctx:DeclarationParser.ComposedUnitContext):
        pass


    # Enter a parse tree produced by DeclarationParser#ePrefix.
    def enterEPrefix(self, ctx:DeclarationParser.EPrefixContext):
        pass

    # Exit a parse tree produced by DeclarationParser#ePrefix.
    def exitEPrefix(self, ctx:DeclarationParser.EPrefixContext):
        pass


    # Enter a parse tree produced by DeclarationParser#eSIUnitType.
    def enterESIUnitType(self, ctx:DeclarationParser.ESIUnitTypeContext):
        pass

    # Exit a parse tree produced by DeclarationParser#eSIUnitType.
    def exitESIUnitType(self, ctx:DeclarationParser.ESIUnitTypeContext):
        pass


    # Enter a parse tree produced by DeclarationParser#arithmeticExpression.
    def enterArithmeticExpression(self, ctx:DeclarationParser.ArithmeticExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#arithmeticExpression.
    def exitArithmeticExpression(self, ctx:DeclarationParser.ArithmeticExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#eAdditionOperator.
    def enterEAdditionOperator(self, ctx:DeclarationParser.EAdditionOperatorContext):
        pass

    # Exit a parse tree produced by DeclarationParser#eAdditionOperator.
    def exitEAdditionOperator(self, ctx:DeclarationParser.EAdditionOperatorContext):
        pass


    # Enter a parse tree produced by DeclarationParser#multiplicationExpression.
    def enterMultiplicationExpression(self, ctx:DeclarationParser.MultiplicationExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#multiplicationExpression.
    def exitMultiplicationExpression(self, ctx:DeclarationParser.MultiplicationExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#eMultiplicationOperator.
    def enterEMultiplicationOperator(self, ctx:DeclarationParser.EMultiplicationOperatorContext):
        pass

    # Exit a parse tree produced by DeclarationParser#eMultiplicationOperator.
    def exitEMultiplicationOperator(self, ctx:DeclarationParser.EMultiplicationOperatorContext):
        pass


    # Enter a parse tree produced by DeclarationParser#valueExpression.
    def enterValueExpression(self, ctx:DeclarationParser.ValueExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#valueExpression.
    def exitValueExpression(self, ctx:DeclarationParser.ValueExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#literalExpression.
    def enterLiteralExpression(self, ctx:DeclarationParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#literalExpression.
    def exitLiteralExpression(self, ctx:DeclarationParser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#literal.
    def enterLiteral(self, ctx:DeclarationParser.LiteralContext):
        pass

    # Exit a parse tree produced by DeclarationParser#literal.
    def exitLiteral(self, ctx:DeclarationParser.LiteralContext):
        pass


    # Enter a parse tree produced by DeclarationParser#parenthesisExpression.
    def enterParenthesisExpression(self, ctx:DeclarationParser.ParenthesisExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#parenthesisExpression.
    def exitParenthesisExpression(self, ctx:DeclarationParser.ParenthesisExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#arrayExpression.
    def enterArrayExpression(self, ctx:DeclarationParser.ArrayExpressionContext):
        pass

    # Exit a parse tree produced by DeclarationParser#arrayExpression.
    def exitArrayExpression(self, ctx:DeclarationParser.ArrayExpressionContext):
        pass


    # Enter a parse tree produced by DeclarationParser#namedElementReference.
    def enterNamedElementReference(self, ctx:DeclarationParser.NamedElementReferenceContext):
        pass

    # Exit a parse tree produced by DeclarationParser#namedElementReference.
    def exitNamedElementReference(self, ctx:DeclarationParser.NamedElementReferenceContext):
        pass


    # Enter a parse tree produced by DeclarationParser#stringValue.
    def enterStringValue(self, ctx:DeclarationParser.StringValueContext):
        pass

    # Exit a parse tree produced by DeclarationParser#stringValue.
    def exitStringValue(self, ctx:DeclarationParser.StringValueContext):
        pass


    # Enter a parse tree produced by DeclarationParser#longValue.
    def enterLongValue(self, ctx:DeclarationParser.LongValueContext):
        pass

    # Exit a parse tree produced by DeclarationParser#longValue.
    def exitLongValue(self, ctx:DeclarationParser.LongValueContext):
        pass


    # Enter a parse tree produced by DeclarationParser#doubleValue.
    def enterDoubleValue(self, ctx:DeclarationParser.DoubleValueContext):
        pass

    # Exit a parse tree produced by DeclarationParser#doubleValue.
    def exitDoubleValue(self, ctx:DeclarationParser.DoubleValueContext):
        pass


    # Enter a parse tree produced by DeclarationParser#booleanValue.
    def enterBooleanValue(self, ctx:DeclarationParser.BooleanValueContext):
        pass

    # Exit a parse tree produced by DeclarationParser#booleanValue.
    def exitBooleanValue(self, ctx:DeclarationParser.BooleanValueContext):
        pass



del DeclarationParser