// Generated from Configuration.g4 by ANTLR 4.13.1
package Configuration;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link ConfigurationParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface ConfigurationVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#configurationModel}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConfigurationModel(ConfigurationParser.ConfigurationModelContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#include}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitInclude(ConfigurationParser.IncludeContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#featureActivation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFeatureActivation(ConfigurationParser.FeatureActivationContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#featureConfiguration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFeatureConfiguration(ConfigurationParser.FeatureConfigurationContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#parameterGroup}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameterGroup(ConfigurationParser.ParameterGroupContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#parameterAssignment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameterAssignment(ConfigurationParser.ParameterAssignmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#selector}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSelector(ConfigurationParser.SelectorContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#elementSelector}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitElementSelector(ConfigurationParser.ElementSelectorContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#rangeSelector}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRangeSelector(ConfigurationParser.RangeSelectorContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#unitSpecification}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnitSpecification(ConfigurationParser.UnitSpecificationContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#qualifiedName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQualifiedName(ConfigurationParser.QualifiedNameContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArithmeticExpression(ConfigurationParser.ArithmeticExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#eAdditionOperator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEAdditionOperator(ConfigurationParser.EAdditionOperatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#multiplicationExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultiplicationExpression(ConfigurationParser.MultiplicationExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#eMultiplicationOperator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEMultiplicationOperator(ConfigurationParser.EMultiplicationOperatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#valueExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitValueExpression(ConfigurationParser.ValueExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#literalExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLiteralExpression(ConfigurationParser.LiteralExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLiteral(ConfigurationParser.LiteralContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#parenthesisExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParenthesisExpression(ConfigurationParser.ParenthesisExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#arrayExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArrayExpression(ConfigurationParser.ArrayExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#namedElementReference}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNamedElementReference(ConfigurationParser.NamedElementReferenceContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#stringValue}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStringValue(ConfigurationParser.StringValueContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#longValue}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLongValue(ConfigurationParser.LongValueContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#doubleValue}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDoubleValue(ConfigurationParser.DoubleValueContext ctx);
	/**
	 * Visit a parse tree produced by {@link ConfigurationParser#booleanValue}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBooleanValue(ConfigurationParser.BooleanValueContext ctx);
}