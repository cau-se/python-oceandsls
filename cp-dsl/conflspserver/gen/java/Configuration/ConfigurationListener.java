// Generated from Configuration.g4 by ANTLR 4.13.1
package Configuration;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ConfigurationParser}.
 */
public interface ConfigurationListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#configurationModel}.
	 * @param ctx the parse tree
	 */
	void enterConfigurationModel(ConfigurationParser.ConfigurationModelContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#configurationModel}.
	 * @param ctx the parse tree
	 */
	void exitConfigurationModel(ConfigurationParser.ConfigurationModelContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#include}.
	 * @param ctx the parse tree
	 */
	void enterInclude(ConfigurationParser.IncludeContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#include}.
	 * @param ctx the parse tree
	 */
	void exitInclude(ConfigurationParser.IncludeContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#featureActivation}.
	 * @param ctx the parse tree
	 */
	void enterFeatureActivation(ConfigurationParser.FeatureActivationContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#featureActivation}.
	 * @param ctx the parse tree
	 */
	void exitFeatureActivation(ConfigurationParser.FeatureActivationContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#featureConfiguration}.
	 * @param ctx the parse tree
	 */
	void enterFeatureConfiguration(ConfigurationParser.FeatureConfigurationContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#featureConfiguration}.
	 * @param ctx the parse tree
	 */
	void exitFeatureConfiguration(ConfigurationParser.FeatureConfigurationContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#parameterGroup}.
	 * @param ctx the parse tree
	 */
	void enterParameterGroup(ConfigurationParser.ParameterGroupContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#parameterGroup}.
	 * @param ctx the parse tree
	 */
	void exitParameterGroup(ConfigurationParser.ParameterGroupContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#parameterAssignment}.
	 * @param ctx the parse tree
	 */
	void enterParameterAssignment(ConfigurationParser.ParameterAssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#parameterAssignment}.
	 * @param ctx the parse tree
	 */
	void exitParameterAssignment(ConfigurationParser.ParameterAssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#selector}.
	 * @param ctx the parse tree
	 */
	void enterSelector(ConfigurationParser.SelectorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#selector}.
	 * @param ctx the parse tree
	 */
	void exitSelector(ConfigurationParser.SelectorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#elementSelector}.
	 * @param ctx the parse tree
	 */
	void enterElementSelector(ConfigurationParser.ElementSelectorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#elementSelector}.
	 * @param ctx the parse tree
	 */
	void exitElementSelector(ConfigurationParser.ElementSelectorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#rangeSelector}.
	 * @param ctx the parse tree
	 */
	void enterRangeSelector(ConfigurationParser.RangeSelectorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#rangeSelector}.
	 * @param ctx the parse tree
	 */
	void exitRangeSelector(ConfigurationParser.RangeSelectorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#unitSpecification}.
	 * @param ctx the parse tree
	 */
	void enterUnitSpecification(ConfigurationParser.UnitSpecificationContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#unitSpecification}.
	 * @param ctx the parse tree
	 */
	void exitUnitSpecification(ConfigurationParser.UnitSpecificationContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#qualifiedName}.
	 * @param ctx the parse tree
	 */
	void enterQualifiedName(ConfigurationParser.QualifiedNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#qualifiedName}.
	 * @param ctx the parse tree
	 */
	void exitQualifiedName(ConfigurationParser.QualifiedNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 */
	void enterArithmeticExpression(ConfigurationParser.ArithmeticExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 */
	void exitArithmeticExpression(ConfigurationParser.ArithmeticExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#eAdditionOperator}.
	 * @param ctx the parse tree
	 */
	void enterEAdditionOperator(ConfigurationParser.EAdditionOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#eAdditionOperator}.
	 * @param ctx the parse tree
	 */
	void exitEAdditionOperator(ConfigurationParser.EAdditionOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#multiplicationExpression}.
	 * @param ctx the parse tree
	 */
	void enterMultiplicationExpression(ConfigurationParser.MultiplicationExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#multiplicationExpression}.
	 * @param ctx the parse tree
	 */
	void exitMultiplicationExpression(ConfigurationParser.MultiplicationExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#eMultiplicationOperator}.
	 * @param ctx the parse tree
	 */
	void enterEMultiplicationOperator(ConfigurationParser.EMultiplicationOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#eMultiplicationOperator}.
	 * @param ctx the parse tree
	 */
	void exitEMultiplicationOperator(ConfigurationParser.EMultiplicationOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#valueExpression}.
	 * @param ctx the parse tree
	 */
	void enterValueExpression(ConfigurationParser.ValueExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#valueExpression}.
	 * @param ctx the parse tree
	 */
	void exitValueExpression(ConfigurationParser.ValueExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#literalExpression}.
	 * @param ctx the parse tree
	 */
	void enterLiteralExpression(ConfigurationParser.LiteralExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#literalExpression}.
	 * @param ctx the parse tree
	 */
	void exitLiteralExpression(ConfigurationParser.LiteralExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(ConfigurationParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(ConfigurationParser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#parenthesisExpression}.
	 * @param ctx the parse tree
	 */
	void enterParenthesisExpression(ConfigurationParser.ParenthesisExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#parenthesisExpression}.
	 * @param ctx the parse tree
	 */
	void exitParenthesisExpression(ConfigurationParser.ParenthesisExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#arrayExpression}.
	 * @param ctx the parse tree
	 */
	void enterArrayExpression(ConfigurationParser.ArrayExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#arrayExpression}.
	 * @param ctx the parse tree
	 */
	void exitArrayExpression(ConfigurationParser.ArrayExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#namedElementReference}.
	 * @param ctx the parse tree
	 */
	void enterNamedElementReference(ConfigurationParser.NamedElementReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#namedElementReference}.
	 * @param ctx the parse tree
	 */
	void exitNamedElementReference(ConfigurationParser.NamedElementReferenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#stringValue}.
	 * @param ctx the parse tree
	 */
	void enterStringValue(ConfigurationParser.StringValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#stringValue}.
	 * @param ctx the parse tree
	 */
	void exitStringValue(ConfigurationParser.StringValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#longValue}.
	 * @param ctx the parse tree
	 */
	void enterLongValue(ConfigurationParser.LongValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#longValue}.
	 * @param ctx the parse tree
	 */
	void exitLongValue(ConfigurationParser.LongValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#doubleValue}.
	 * @param ctx the parse tree
	 */
	void enterDoubleValue(ConfigurationParser.DoubleValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#doubleValue}.
	 * @param ctx the parse tree
	 */
	void exitDoubleValue(ConfigurationParser.DoubleValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link ConfigurationParser#booleanValue}.
	 * @param ctx the parse tree
	 */
	void enterBooleanValue(ConfigurationParser.BooleanValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link ConfigurationParser#booleanValue}.
	 * @param ctx the parse tree
	 */
	void exitBooleanValue(ConfigurationParser.BooleanValueContext ctx);
}