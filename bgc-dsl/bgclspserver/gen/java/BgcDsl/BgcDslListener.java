// Generated from BgcDsl.g4 by ANTLR 4.13.1
package BgcDsl;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link BgcDslParser}.
 */
public interface BgcDslListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#bgcModel}.
	 * @param ctx the parse tree
	 */
	void enterBgcModel(BgcDslParser.BgcModelContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#bgcModel}.
	 * @param ctx the parse tree
	 */
	void exitBgcModel(BgcDslParser.BgcModelContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#substanceDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterSubstanceDeclaration(BgcDslParser.SubstanceDeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#substanceDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitSubstanceDeclaration(BgcDslParser.SubstanceDeclarationContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#parameterDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterParameterDeclaration(BgcDslParser.ParameterDeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#parameterDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitParameterDeclaration(BgcDslParser.ParameterDeclarationContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#environmentVariableDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterEnvironmentVariableDeclaration(BgcDslParser.EnvironmentVariableDeclarationContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#environmentVariableDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitEnvironmentVariableDeclaration(BgcDslParser.EnvironmentVariableDeclarationContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#primitiveTypes}.
	 * @param ctx the parse tree
	 */
	void enterPrimitiveTypes(BgcDslParser.PrimitiveTypesContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#primitiveTypes}.
	 * @param ctx the parse tree
	 */
	void exitPrimitiveTypes(BgcDslParser.PrimitiveTypesContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#compartment}.
	 * @param ctx the parse tree
	 */
	void enterCompartment(BgcDslParser.CompartmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#compartment}.
	 * @param ctx the parse tree
	 */
	void exitCompartment(BgcDslParser.CompartmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#substanceState}.
	 * @param ctx the parse tree
	 */
	void enterSubstanceState(BgcDslParser.SubstanceStateContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#substanceState}.
	 * @param ctx the parse tree
	 */
	void exitSubstanceState(BgcDslParser.SubstanceStateContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#updateState}.
	 * @param ctx the parse tree
	 */
	void enterUpdateState(BgcDslParser.UpdateStateContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#updateState}.
	 * @param ctx the parse tree
	 */
	void exitUpdateState(BgcDslParser.UpdateStateContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#connection}.
	 * @param ctx the parse tree
	 */
	void enterConnection(BgcDslParser.ConnectionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#connection}.
	 * @param ctx the parse tree
	 */
	void exitConnection(BgcDslParser.ConnectionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#substanceExpression}.
	 * @param ctx the parse tree
	 */
	void enterSubstanceExpression(BgcDslParser.SubstanceExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#substanceExpression}.
	 * @param ctx the parse tree
	 */
	void exitSubstanceExpression(BgcDslParser.SubstanceExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#calculation}.
	 * @param ctx the parse tree
	 */
	void enterCalculation(BgcDslParser.CalculationContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#calculation}.
	 * @param ctx the parse tree
	 */
	void exitCalculation(BgcDslParser.CalculationContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#basicCalculation}.
	 * @param ctx the parse tree
	 */
	void enterBasicCalculation(BgcDslParser.BasicCalculationContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#basicCalculation}.
	 * @param ctx the parse tree
	 */
	void exitBasicCalculation(BgcDslParser.BasicCalculationContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#alternativeCalculation}.
	 * @param ctx the parse tree
	 */
	void enterAlternativeCalculation(BgcDslParser.AlternativeCalculationContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#alternativeCalculation}.
	 * @param ctx the parse tree
	 */
	void exitAlternativeCalculation(BgcDslParser.AlternativeCalculationContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#caseCalculation}.
	 * @param ctx the parse tree
	 */
	void enterCaseCalculation(BgcDslParser.CaseCalculationContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#caseCalculation}.
	 * @param ctx the parse tree
	 */
	void exitCaseCalculation(BgcDslParser.CaseCalculationContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#unit}.
	 * @param ctx the parse tree
	 */
	void enterUnit(BgcDslParser.UnitContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#unit}.
	 * @param ctx the parse tree
	 */
	void exitUnit(BgcDslParser.UnitContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#unitElement}.
	 * @param ctx the parse tree
	 */
	void enterUnitElement(BgcDslParser.UnitElementContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#unitElement}.
	 * @param ctx the parse tree
	 */
	void exitUnitElement(BgcDslParser.UnitElementContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#groupUnit}.
	 * @param ctx the parse tree
	 */
	void enterGroupUnit(BgcDslParser.GroupUnitContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#groupUnit}.
	 * @param ctx the parse tree
	 */
	void exitGroupUnit(BgcDslParser.GroupUnitContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#prefixUnit}.
	 * @param ctx the parse tree
	 */
	void enterPrefixUnit(BgcDslParser.PrefixUnitContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#prefixUnit}.
	 * @param ctx the parse tree
	 */
	void exitPrefixUnit(BgcDslParser.PrefixUnitContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 */
	void enterArithmeticExpression(BgcDslParser.ArithmeticExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 */
	void exitArithmeticExpression(BgcDslParser.ArithmeticExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#eAdditionOperator}.
	 * @param ctx the parse tree
	 */
	void enterEAdditionOperator(BgcDslParser.EAdditionOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#eAdditionOperator}.
	 * @param ctx the parse tree
	 */
	void exitEAdditionOperator(BgcDslParser.EAdditionOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#multiplicationExpression}.
	 * @param ctx the parse tree
	 */
	void enterMultiplicationExpression(BgcDslParser.MultiplicationExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#multiplicationExpression}.
	 * @param ctx the parse tree
	 */
	void exitMultiplicationExpression(BgcDslParser.MultiplicationExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#eMultiplicationOperator}.
	 * @param ctx the parse tree
	 */
	void enterEMultiplicationOperator(BgcDslParser.EMultiplicationOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#eMultiplicationOperator}.
	 * @param ctx the parse tree
	 */
	void exitEMultiplicationOperator(BgcDslParser.EMultiplicationOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#powerExpression}.
	 * @param ctx the parse tree
	 */
	void enterPowerExpression(BgcDslParser.PowerExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#powerExpression}.
	 * @param ctx the parse tree
	 */
	void exitPowerExpression(BgcDslParser.PowerExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#valueExpression}.
	 * @param ctx the parse tree
	 */
	void enterValueExpression(BgcDslParser.ValueExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#valueExpression}.
	 * @param ctx the parse tree
	 */
	void exitValueExpression(BgcDslParser.ValueExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#arrayExpression}.
	 * @param ctx the parse tree
	 */
	void enterArrayExpression(BgcDslParser.ArrayExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#arrayExpression}.
	 * @param ctx the parse tree
	 */
	void exitArrayExpression(BgcDslParser.ArrayExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#functionCallingExpression}.
	 * @param ctx the parse tree
	 */
	void enterFunctionCallingExpression(BgcDslParser.FunctionCallingExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#functionCallingExpression}.
	 * @param ctx the parse tree
	 */
	void exitFunctionCallingExpression(BgcDslParser.FunctionCallingExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#function}.
	 * @param ctx the parse tree
	 */
	void enterFunction(BgcDslParser.FunctionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#function}.
	 * @param ctx the parse tree
	 */
	void exitFunction(BgcDslParser.FunctionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#literalExpression}.
	 * @param ctx the parse tree
	 */
	void enterLiteralExpression(BgcDslParser.LiteralExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#literalExpression}.
	 * @param ctx the parse tree
	 */
	void exitLiteralExpression(BgcDslParser.LiteralExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(BgcDslParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(BgcDslParser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#numberLiteral}.
	 * @param ctx the parse tree
	 */
	void enterNumberLiteral(BgcDslParser.NumberLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#numberLiteral}.
	 * @param ctx the parse tree
	 */
	void exitNumberLiteral(BgcDslParser.NumberLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#stringLiteral}.
	 * @param ctx the parse tree
	 */
	void enterStringLiteral(BgcDslParser.StringLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#stringLiteral}.
	 * @param ctx the parse tree
	 */
	void exitStringLiteral(BgcDslParser.StringLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#parenthesisExpression}.
	 * @param ctx the parse tree
	 */
	void enterParenthesisExpression(BgcDslParser.ParenthesisExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#parenthesisExpression}.
	 * @param ctx the parse tree
	 */
	void exitParenthesisExpression(BgcDslParser.ParenthesisExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#termReference}.
	 * @param ctx the parse tree
	 */
	void enterTermReference(BgcDslParser.TermReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#termReference}.
	 * @param ctx the parse tree
	 */
	void exitTermReference(BgcDslParser.TermReferenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#subterm}.
	 * @param ctx the parse tree
	 */
	void enterSubterm(BgcDslParser.SubtermContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#subterm}.
	 * @param ctx the parse tree
	 */
	void exitSubterm(BgcDslParser.SubtermContext ctx);
	/**
	 * Enter a parse tree produced by {@link BgcDslParser#qualifiedName}.
	 * @param ctx the parse tree
	 */
	void enterQualifiedName(BgcDslParser.QualifiedNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link BgcDslParser#qualifiedName}.
	 * @param ctx the parse tree
	 */
	void exitQualifiedName(BgcDslParser.QualifiedNameContext ctx);
}