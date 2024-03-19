// Generated from Declaration.g4 by ANTLR 4.13.1
package Declaration;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link DeclarationParser}.
 */
public interface DeclarationListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#declarationModel}.
	 * @param ctx the parse tree
	 */
	void enterDeclarationModel(DeclarationParser.DeclarationModelContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#declarationModel}.
	 * @param ctx the parse tree
	 */
	void exitDeclarationModel(DeclarationParser.DeclarationModelContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#namedElement}.
	 * @param ctx the parse tree
	 */
	void enterNamedElement(DeclarationParser.NamedElementContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#namedElement}.
	 * @param ctx the parse tree
	 */
	void exitNamedElement(DeclarationParser.NamedElementContext ctx);
	/**
	 * Enter a parse tree produced by the {@code paramGroupAssignStat}
	 * labeled alternative in {@link DeclarationParser#parameterGroupDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterParamGroupAssignStat(DeclarationParser.ParamGroupAssignStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code paramGroupAssignStat}
	 * labeled alternative in {@link DeclarationParser#parameterGroupDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitParamGroupAssignStat(DeclarationParser.ParamGroupAssignStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code paramAssignStat}
	 * labeled alternative in {@link DeclarationParser#parameterDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterParamAssignStat(DeclarationParser.ParamAssignStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code paramAssignStat}
	 * labeled alternative in {@link DeclarationParser#parameterDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitParamAssignStat(DeclarationParser.ParamAssignStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code featureAssignStat}
	 * labeled alternative in {@link DeclarationParser#featureDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterFeatureAssignStat(DeclarationParser.FeatureAssignStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code featureAssignStat}
	 * labeled alternative in {@link DeclarationParser#featureDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitFeatureAssignStat(DeclarationParser.FeatureAssignStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code featureGroupAssignStat}
	 * labeled alternative in {@link DeclarationParser#featureGroupDeclaration}.
	 * @param ctx the parse tree
	 */
	void enterFeatureGroupAssignStat(DeclarationParser.FeatureGroupAssignStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code featureGroupAssignStat}
	 * labeled alternative in {@link DeclarationParser#featureGroupDeclaration}.
	 * @param ctx the parse tree
	 */
	void exitFeatureGroupAssignStat(DeclarationParser.FeatureGroupAssignStatContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#eKind}.
	 * @param ctx the parse tree
	 */
	void enterEKind(DeclarationParser.EKindContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#eKind}.
	 * @param ctx the parse tree
	 */
	void exitEKind(DeclarationParser.EKindContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#paramType}.
	 * @param ctx the parse tree
	 */
	void enterParamType(DeclarationParser.ParamTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#paramType}.
	 * @param ctx the parse tree
	 */
	void exitParamType(DeclarationParser.ParamTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#inlineEnumerationType}.
	 * @param ctx the parse tree
	 */
	void enterInlineEnumerationType(DeclarationParser.InlineEnumerationTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#inlineEnumerationType}.
	 * @param ctx the parse tree
	 */
	void exitInlineEnumerationType(DeclarationParser.InlineEnumerationTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#typeReference}.
	 * @param ctx the parse tree
	 */
	void enterTypeReference(DeclarationParser.TypeReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#typeReference}.
	 * @param ctx the parse tree
	 */
	void exitTypeReference(DeclarationParser.TypeReferenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#arrayType}.
	 * @param ctx the parse tree
	 */
	void enterArrayType(DeclarationParser.ArrayTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#arrayType}.
	 * @param ctx the parse tree
	 */
	void exitArrayType(DeclarationParser.ArrayTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#dimension}.
	 * @param ctx the parse tree
	 */
	void enterDimension(DeclarationParser.DimensionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#dimension}.
	 * @param ctx the parse tree
	 */
	void exitDimension(DeclarationParser.DimensionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#sizeDimension}.
	 * @param ctx the parse tree
	 */
	void enterSizeDimension(DeclarationParser.SizeDimensionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#sizeDimension}.
	 * @param ctx the parse tree
	 */
	void exitSizeDimension(DeclarationParser.SizeDimensionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#rangeDimension}.
	 * @param ctx the parse tree
	 */
	void enterRangeDimension(DeclarationParser.RangeDimensionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#rangeDimension}.
	 * @param ctx the parse tree
	 */
	void exitRangeDimension(DeclarationParser.RangeDimensionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#declaredType}.
	 * @param ctx the parse tree
	 */
	void enterDeclaredType(DeclarationParser.DeclaredTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#declaredType}.
	 * @param ctx the parse tree
	 */
	void exitDeclaredType(DeclarationParser.DeclaredTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#rangeType}.
	 * @param ctx the parse tree
	 */
	void enterRangeType(DeclarationParser.RangeTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#rangeType}.
	 * @param ctx the parse tree
	 */
	void exitRangeType(DeclarationParser.RangeTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#enumerationType}.
	 * @param ctx the parse tree
	 */
	void enterEnumerationType(DeclarationParser.EnumerationTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#enumerationType}.
	 * @param ctx the parse tree
	 */
	void exitEnumerationType(DeclarationParser.EnumerationTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#enumeral}.
	 * @param ctx the parse tree
	 */
	void enterEnumeral(DeclarationParser.EnumeralContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#enumeral}.
	 * @param ctx the parse tree
	 */
	void exitEnumeral(DeclarationParser.EnumeralContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#unitSpecification}.
	 * @param ctx the parse tree
	 */
	void enterUnitSpecification(DeclarationParser.UnitSpecificationContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#unitSpecification}.
	 * @param ctx the parse tree
	 */
	void exitUnitSpecification(DeclarationParser.UnitSpecificationContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#basicUnit}.
	 * @param ctx the parse tree
	 */
	void enterBasicUnit(DeclarationParser.BasicUnitContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#basicUnit}.
	 * @param ctx the parse tree
	 */
	void exitBasicUnit(DeclarationParser.BasicUnitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code siunit}
	 * labeled alternative in {@link DeclarationParser#sIUnit}.
	 * @param ctx the parse tree
	 */
	void enterSiunit(DeclarationParser.SiunitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code siunit}
	 * labeled alternative in {@link DeclarationParser#sIUnit}.
	 * @param ctx the parse tree
	 */
	void exitSiunit(DeclarationParser.SiunitContext ctx);
	/**
	 * Enter a parse tree produced by the {@code customunit}
	 * labeled alternative in {@link DeclarationParser#customUnit}.
	 * @param ctx the parse tree
	 */
	void enterCustomunit(DeclarationParser.CustomunitContext ctx);
	/**
	 * Exit a parse tree produced by the {@code customunit}
	 * labeled alternative in {@link DeclarationParser#customUnit}.
	 * @param ctx the parse tree
	 */
	void exitCustomunit(DeclarationParser.CustomunitContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#composedUnit}.
	 * @param ctx the parse tree
	 */
	void enterComposedUnit(DeclarationParser.ComposedUnitContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#composedUnit}.
	 * @param ctx the parse tree
	 */
	void exitComposedUnit(DeclarationParser.ComposedUnitContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#ePrefix}.
	 * @param ctx the parse tree
	 */
	void enterEPrefix(DeclarationParser.EPrefixContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#ePrefix}.
	 * @param ctx the parse tree
	 */
	void exitEPrefix(DeclarationParser.EPrefixContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#eSIUnitType}.
	 * @param ctx the parse tree
	 */
	void enterESIUnitType(DeclarationParser.ESIUnitTypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#eSIUnitType}.
	 * @param ctx the parse tree
	 */
	void exitESIUnitType(DeclarationParser.ESIUnitTypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 */
	void enterArithmeticExpression(DeclarationParser.ArithmeticExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 */
	void exitArithmeticExpression(DeclarationParser.ArithmeticExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#eAdditionOperator}.
	 * @param ctx the parse tree
	 */
	void enterEAdditionOperator(DeclarationParser.EAdditionOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#eAdditionOperator}.
	 * @param ctx the parse tree
	 */
	void exitEAdditionOperator(DeclarationParser.EAdditionOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#multiplicationExpression}.
	 * @param ctx the parse tree
	 */
	void enterMultiplicationExpression(DeclarationParser.MultiplicationExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#multiplicationExpression}.
	 * @param ctx the parse tree
	 */
	void exitMultiplicationExpression(DeclarationParser.MultiplicationExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#eMultiplicationOperator}.
	 * @param ctx the parse tree
	 */
	void enterEMultiplicationOperator(DeclarationParser.EMultiplicationOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#eMultiplicationOperator}.
	 * @param ctx the parse tree
	 */
	void exitEMultiplicationOperator(DeclarationParser.EMultiplicationOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#valueExpression}.
	 * @param ctx the parse tree
	 */
	void enterValueExpression(DeclarationParser.ValueExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#valueExpression}.
	 * @param ctx the parse tree
	 */
	void exitValueExpression(DeclarationParser.ValueExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#literalExpression}.
	 * @param ctx the parse tree
	 */
	void enterLiteralExpression(DeclarationParser.LiteralExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#literalExpression}.
	 * @param ctx the parse tree
	 */
	void exitLiteralExpression(DeclarationParser.LiteralExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#literal}.
	 * @param ctx the parse tree
	 */
	void enterLiteral(DeclarationParser.LiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#literal}.
	 * @param ctx the parse tree
	 */
	void exitLiteral(DeclarationParser.LiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#parenthesisExpression}.
	 * @param ctx the parse tree
	 */
	void enterParenthesisExpression(DeclarationParser.ParenthesisExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#parenthesisExpression}.
	 * @param ctx the parse tree
	 */
	void exitParenthesisExpression(DeclarationParser.ParenthesisExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#arrayExpression}.
	 * @param ctx the parse tree
	 */
	void enterArrayExpression(DeclarationParser.ArrayExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#arrayExpression}.
	 * @param ctx the parse tree
	 */
	void exitArrayExpression(DeclarationParser.ArrayExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#namedElementReference}.
	 * @param ctx the parse tree
	 */
	void enterNamedElementReference(DeclarationParser.NamedElementReferenceContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#namedElementReference}.
	 * @param ctx the parse tree
	 */
	void exitNamedElementReference(DeclarationParser.NamedElementReferenceContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#stringValue}.
	 * @param ctx the parse tree
	 */
	void enterStringValue(DeclarationParser.StringValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#stringValue}.
	 * @param ctx the parse tree
	 */
	void exitStringValue(DeclarationParser.StringValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#longValue}.
	 * @param ctx the parse tree
	 */
	void enterLongValue(DeclarationParser.LongValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#longValue}.
	 * @param ctx the parse tree
	 */
	void exitLongValue(DeclarationParser.LongValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#doubleValue}.
	 * @param ctx the parse tree
	 */
	void enterDoubleValue(DeclarationParser.DoubleValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#doubleValue}.
	 * @param ctx the parse tree
	 */
	void exitDoubleValue(DeclarationParser.DoubleValueContext ctx);
	/**
	 * Enter a parse tree produced by {@link DeclarationParser#booleanValue}.
	 * @param ctx the parse tree
	 */
	void enterBooleanValue(DeclarationParser.BooleanValueContext ctx);
	/**
	 * Exit a parse tree produced by {@link DeclarationParser#booleanValue}.
	 * @param ctx the parse tree
	 */
	void exitBooleanValue(DeclarationParser.BooleanValueContext ctx);
}