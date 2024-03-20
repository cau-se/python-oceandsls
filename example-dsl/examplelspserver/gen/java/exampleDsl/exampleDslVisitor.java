// Generated from exampleDsl.g4 by ANTLR 4.13.1
package exampleDsl;
import org.antlr.v4.runtime.tree.ParseTreeVisitor;

/**
 * This interface defines a complete generic visitor for a parse tree produced
 * by {@link exampleDslParser}.
 *
 * @param <T> The return type of the visit operation. Use {@link Void} for
 * operations with no return type.
 */
public interface exampleDslVisitor<T> extends ParseTreeVisitor<T> {
	/**
	 * Visit a parse tree produced by the {@code startProg}
	 * labeled alternative in {@link exampleDslParser#prog}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStartProg(exampleDslParser.StartProgContext ctx);
	/**
	 * Visit a parse tree produced by the {@code printExprStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrintExprStat(exampleDslParser.PrintExprStatContext ctx);
	/**
	 * Visit a parse tree produced by the {@code assignStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAssignStat(exampleDslParser.AssignStatContext ctx);
	/**
	 * Visit a parse tree produced by the {@code blankStat}
	 * labeled alternative in {@link exampleDslParser#stat}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitBlankStat(exampleDslParser.BlankStatContext ctx);
	/**
	 * Visit a parse tree produced by the {@code addSubExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAddSubExpr(exampleDslParser.AddSubExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code funRef}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunRef(exampleDslParser.FunRefContext ctx);
	/**
	 * Visit a parse tree produced by the {@code numberExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumberExpr(exampleDslParser.NumberExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code parensExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParensExpr(exampleDslParser.ParensExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code mulDivExpr}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMulDivExpr(exampleDslParser.MulDivExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code idRef}
	 * labeled alternative in {@link exampleDslParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIdRef(exampleDslParser.IdRefContext ctx);
	/**
	 * Visit a parse tree produced by the {@code argList}
	 * labeled alternative in {@link exampleDslParser#exprList}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgList(exampleDslParser.ArgListContext ctx);
	/**
	 * Visit a parse tree produced by the {@code varExpr}
	 * labeled alternative in {@link exampleDslParser#variableRef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarExpr(exampleDslParser.VarExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code funcExpr}
	 * labeled alternative in {@link exampleDslParser#functionRef}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFuncExpr(exampleDslParser.FuncExprContext ctx);
}