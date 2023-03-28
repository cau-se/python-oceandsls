// Generated from TestDrivenDev_DSL.g4 by ANTLR 4.12.0
package TestDrivenDev_DSL;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link TestDrivenDev_DSLParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface TestDrivenDev_DSLVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by {@link TestDrivenDev_DSLParser#test_suite}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_suite(TestDrivenDev_DSLParser.Test_suiteContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestDrivenDev_DSLParser#test_case}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_case(TestDrivenDev_DSLParser.Test_caseContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestDrivenDev_DSLParser#test_assertion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_assertion(TestDrivenDev_DSLParser.Test_assertionContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestDrivenDev_DSLParser#test_input}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_input(TestDrivenDev_DSLParser.Test_inputContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestDrivenDev_DSLParser#test_output}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTest_output(TestDrivenDev_DSLParser.Test_outputContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestDrivenDev_DSLParser#param}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParam(TestDrivenDev_DSLParser.ParamContext ctx);
	/**
	 * Visit a parse tree produced by the {@code strExpr}
	 * labeled alternative in {@link TestDrivenDev_DSLParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStrExpr(TestDrivenDev_DSLParser.StrExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code intExpr}
	 * labeled alternative in {@link TestDrivenDev_DSLParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIntExpr(TestDrivenDev_DSLParser.IntExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code addSubExpr}
	 * labeled alternative in {@link TestDrivenDev_DSLParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAddSubExpr(TestDrivenDev_DSLParser.AddSubExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code numberExpr}
	 * labeled alternative in {@link TestDrivenDev_DSLParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumberExpr(TestDrivenDev_DSLParser.NumberExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code parensExpr}
	 * labeled alternative in {@link TestDrivenDev_DSLParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParensExpr(TestDrivenDev_DSLParser.ParensExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code mulDivExpr}
	 * labeled alternative in {@link TestDrivenDev_DSLParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMulDivExpr(TestDrivenDev_DSLParser.MulDivExprContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestDrivenDev_DSLParser#directive}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDirective(TestDrivenDev_DSLParser.DirectiveContext ctx);
}