// Generated from TestSuite.g4 by ANTLR 4.12.0
package TestSuite;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link TestSuiteParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface TestSuiteVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#test_suite}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_suite(TestSuiteParser.Test_suiteContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#test_case}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_case(TestSuiteParser.Test_caseContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#test_assertion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_assertion(TestSuiteParser.Test_assertionContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#test_input}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_input(TestSuiteParser.Test_inputContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#test_output}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_output(TestSuiteParser.Test_outputContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#parameter}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParameter(TestSuiteParser.ParameterContext ctx);
	/**
	 * Visit a parse tree produced by the {@code emptyDesc}
	 * labeled alternative in {@link TestSuiteParser#optionalParDesc}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEmptyDesc(TestSuiteParser.EmptyDescContext ctx);
	/**
	 * Visit a parse tree produced by the {@code specDesc}
	 * labeled alternative in {@link TestSuiteParser#optionalParDesc}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecDesc(TestSuiteParser.SpecDescContext ctx);
	/**
	 * Visit a parse tree produced by the {@code emptyComment}
	 * labeled alternative in {@link TestSuiteParser#optionalComment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEmptyComment(TestSuiteParser.EmptyCommentContext ctx);
	/**
	 * Visit a parse tree produced by the {@code specComment}
	 * labeled alternative in {@link TestSuiteParser#optionalComment}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSpecComment(TestSuiteParser.SpecCommentContext ctx);
	/**
	 * Visit a parse tree produced by the {@code nameDecl}
	 * labeled alternative in {@link TestSuiteParser#parameterDeclaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNameDecl(TestSuiteParser.NameDeclContext ctx);
	/**
	 * Visit a parse tree produced by the {@code typeDecl}
	 * labeled alternative in {@link TestSuiteParser#parameterDeclaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTypeDecl(TestSuiteParser.TypeDeclContext ctx);
	/**
	 * Visit a parse tree produced by the {@code combinedDecl}
	 * labeled alternative in {@link TestSuiteParser#parameterDeclaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCombinedDecl(TestSuiteParser.CombinedDeclContext ctx);
	/**
	 * Visit a parse tree produced by the {@code strExpr}
	 * labeled alternative in {@link TestSuiteParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStrExpr(TestSuiteParser.StrExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code intExpr}
	 * labeled alternative in {@link TestSuiteParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIntExpr(TestSuiteParser.IntExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code addSubExpr}
	 * labeled alternative in {@link TestSuiteParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAddSubExpr(TestSuiteParser.AddSubExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code numberExpr}
	 * labeled alternative in {@link TestSuiteParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumberExpr(TestSuiteParser.NumberExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code parensExpr}
	 * labeled alternative in {@link TestSuiteParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParensExpr(TestSuiteParser.ParensExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code mulDivExpr}
	 * labeled alternative in {@link TestSuiteParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMulDivExpr(TestSuiteParser.MulDivExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#directive}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDirective(TestSuiteParser.DirectiveContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#paramType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParamType(TestSuiteParser.ParamTypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#typeRef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTypeRef(TestSuiteParser.TypeRefContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#enumType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnumType(TestSuiteParser.EnumTypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#enum}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnum(TestSuiteParser.EnumContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#arrayType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArrayType(TestSuiteParser.ArrayTypeContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#dim}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDim(TestSuiteParser.DimContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#sizeDim}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSizeDim(TestSuiteParser.SizeDimContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#rangeDim}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRangeDim(TestSuiteParser.RangeDimContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#unitSpec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnitSpec(TestSuiteParser.UnitSpecContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#composedUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitComposedUnit(TestSuiteParser.ComposedUnitContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#basicUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBasicUnit(TestSuiteParser.BasicUnitContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#siUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSiUnit(TestSuiteParser.SiUnitContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#customUnit}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCustomUnit(TestSuiteParser.CustomUnitContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUnitPrefix(TestSuiteParser.UnitPrefixContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSiType(TestSuiteParser.SiTypeContext ctx);
}