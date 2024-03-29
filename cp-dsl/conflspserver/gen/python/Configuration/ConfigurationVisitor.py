# Generated from Configuration.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .ConfigurationParser import ConfigurationParser
else:
    from ConfigurationParser import ConfigurationParser

# This class defines a complete generic visitor for a parse tree produced by ConfigurationParser.

class ConfigurationVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by ConfigurationParser#configurationModel.
    def visitConfigurationModel(self, ctx:ConfigurationParser.ConfigurationModelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#include.
    def visitInclude(self, ctx:ConfigurationParser.IncludeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#featureActivation.
    def visitFeatureActivation(self, ctx:ConfigurationParser.FeatureActivationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#featureConfiguration.
    def visitFeatureConfiguration(self, ctx:ConfigurationParser.FeatureConfigurationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#parameterGroup.
    def visitParameterGroup(self, ctx:ConfigurationParser.ParameterGroupContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#parameterAssignment.
    def visitParameterAssignment(self, ctx:ConfigurationParser.ParameterAssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#selector.
    def visitSelector(self, ctx:ConfigurationParser.SelectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#elementSelector.
    def visitElementSelector(self, ctx:ConfigurationParser.ElementSelectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#rangeSelector.
    def visitRangeSelector(self, ctx:ConfigurationParser.RangeSelectorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#unitSpecification.
    def visitUnitSpecification(self, ctx:ConfigurationParser.UnitSpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#qualifiedName.
    def visitQualifiedName(self, ctx:ConfigurationParser.QualifiedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#arithmeticExpression.
    def visitArithmeticExpression(self, ctx:ConfigurationParser.ArithmeticExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#eAdditionOperator.
    def visitEAdditionOperator(self, ctx:ConfigurationParser.EAdditionOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#multiplicationExpression.
    def visitMultiplicationExpression(self, ctx:ConfigurationParser.MultiplicationExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#eMultiplicationOperator.
    def visitEMultiplicationOperator(self, ctx:ConfigurationParser.EMultiplicationOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#valueExpression.
    def visitValueExpression(self, ctx:ConfigurationParser.ValueExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#literalExpression.
    def visitLiteralExpression(self, ctx:ConfigurationParser.LiteralExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#literal.
    def visitLiteral(self, ctx:ConfigurationParser.LiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#parenthesisExpression.
    def visitParenthesisExpression(self, ctx:ConfigurationParser.ParenthesisExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#arrayExpression.
    def visitArrayExpression(self, ctx:ConfigurationParser.ArrayExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#namedElementReference.
    def visitNamedElementReference(self, ctx:ConfigurationParser.NamedElementReferenceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#stringValue.
    def visitStringValue(self, ctx:ConfigurationParser.StringValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#longValue.
    def visitLongValue(self, ctx:ConfigurationParser.LongValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#doubleValue.
    def visitDoubleValue(self, ctx:ConfigurationParser.DoubleValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ConfigurationParser#booleanValue.
    def visitBooleanValue(self, ctx:ConfigurationParser.BooleanValueContext):
        return self.visitChildren(ctx)



del ConfigurationParser