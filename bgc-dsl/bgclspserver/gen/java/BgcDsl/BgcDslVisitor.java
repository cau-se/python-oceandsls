// Generated from BgcDsl.g4 by ANTLR 4.13.1
package BgcDsl;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link BgcDslParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface BgcDslVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#bgcModel}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBgcModel(BgcDslParser.BgcModelContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#substanceDeclaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubstanceDeclaration(BgcDslParser.SubstanceDeclarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#parameterDeclaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameterDeclaration(BgcDslParser.ParameterDeclarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#environmentVariableDeclaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnvironmentVariableDeclaration(BgcDslParser.EnvironmentVariableDeclarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#primitiveTypes}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrimitiveTypes(BgcDslParser.PrimitiveTypesContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#compartment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCompartment(BgcDslParser.CompartmentContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#substanceState}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubstanceState(BgcDslParser.SubstanceStateContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#updateState}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUpdateState(BgcDslParser.UpdateStateContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#connection}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConnection(BgcDslParser.ConnectionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#substanceExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubstanceExpression(BgcDslParser.SubstanceExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#calculation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCalculation(BgcDslParser.CalculationContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#basicCalculation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBasicCalculation(BgcDslParser.BasicCalculationContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#alternativeCalculation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAlternativeCalculation(BgcDslParser.AlternativeCalculationContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#caseCalculation}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCaseCalculation(BgcDslParser.CaseCalculationContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#unit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnit(BgcDslParser.UnitContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#unitElement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnitElement(BgcDslParser.UnitElementContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#groupUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGroupUnit(BgcDslParser.GroupUnitContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#prefixUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrefixUnit(BgcDslParser.PrefixUnitContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArithmeticExpression(BgcDslParser.ArithmeticExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#eAdditionOperator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEAdditionOperator(BgcDslParser.EAdditionOperatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#multiplicationExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMultiplicationExpression(BgcDslParser.MultiplicationExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#eMultiplicationOperator}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEMultiplicationOperator(BgcDslParser.EMultiplicationOperatorContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#powerExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPowerExpression(BgcDslParser.PowerExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#valueExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitValueExpression(BgcDslParser.ValueExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#arrayExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArrayExpression(BgcDslParser.ArrayExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#functionCallingExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunctionCallingExpression(BgcDslParser.FunctionCallingExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#function}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunction(BgcDslParser.FunctionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#literalExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLiteralExpression(BgcDslParser.LiteralExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#literal}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitLiteral(BgcDslParser.LiteralContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#numberLiteral}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumberLiteral(BgcDslParser.NumberLiteralContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#stringLiteral}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStringLiteral(BgcDslParser.StringLiteralContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#parenthesisExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParenthesisExpression(BgcDslParser.ParenthesisExpressionContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#termReference}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTermReference(BgcDslParser.TermReferenceContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#subterm}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSubterm(BgcDslParser.SubtermContext ctx);
	/**
	 * Visit a parse tree produced by {@link BgcDslParser#qualifiedName}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQualifiedName(BgcDslParser.QualifiedNameContext ctx);
}