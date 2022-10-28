// Generated from java-escape by ANTLR 4.11.1
package TestGrammar;
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link TestGrammarParser}.
 */
public interface TestGrammarListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by the {@code startProg}
	 * labeled alternative in {@link TestGrammarParser#prog}.
	 * @param ctx the parse tree
	 */
	void enterStartProg(TestGrammarParser.StartProgContext ctx);
	/**
	 * Exit a parse tree produced by the {@code startProg}
	 * labeled alternative in {@link TestGrammarParser#prog}.
	 * @param ctx the parse tree
	 */
	void exitStartProg(TestGrammarParser.StartProgContext ctx);
	/**
	 * Enter a parse tree produced by the {@code printExprStat}
	 * labeled alternative in {@link TestGrammarParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterPrintExprStat(TestGrammarParser.PrintExprStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code printExprStat}
	 * labeled alternative in {@link TestGrammarParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitPrintExprStat(TestGrammarParser.PrintExprStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code assignStat}
	 * labeled alternative in {@link TestGrammarParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterAssignStat(TestGrammarParser.AssignStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code assignStat}
	 * labeled alternative in {@link TestGrammarParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitAssignStat(TestGrammarParser.AssignStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code blankStat}
	 * labeled alternative in {@link TestGrammarParser#stat}.
	 * @param ctx the parse tree
	 */
	void enterBlankStat(TestGrammarParser.BlankStatContext ctx);
	/**
	 * Exit a parse tree produced by the {@code blankStat}
	 * labeled alternative in {@link TestGrammarParser#stat}.
	 * @param ctx the parse tree
	 */
	void exitBlankStat(TestGrammarParser.BlankStatContext ctx);
	/**
	 * Enter a parse tree produced by the {@code funcExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterFuncExpr(TestGrammarParser.FuncExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code funcExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitFuncExpr(TestGrammarParser.FuncExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code addSubExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterAddSubExpr(TestGrammarParser.AddSubExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code addSubExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitAddSubExpr(TestGrammarParser.AddSubExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code numberExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterNumberExpr(TestGrammarParser.NumberExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code numberExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitNumberExpr(TestGrammarParser.NumberExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code parensExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterParensExpr(TestGrammarParser.ParensExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code parensExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitParensExpr(TestGrammarParser.ParensExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code mulDivExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterMulDivExpr(TestGrammarParser.MulDivExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code mulDivExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitMulDivExpr(TestGrammarParser.MulDivExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code idExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void enterIdExpr(TestGrammarParser.IdExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code idExpr}
	 * labeled alternative in {@link TestGrammarParser#expr}.
	 * @param ctx the parse tree
	 */
	void exitIdExpr(TestGrammarParser.IdExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code argList}
	 * labeled alternative in {@link TestGrammarParser#exprList}.
	 * @param ctx the parse tree
	 */
	void enterArgList(TestGrammarParser.ArgListContext ctx);
	/**
	 * Exit a parse tree produced by the {@code argList}
	 * labeled alternative in {@link TestGrammarParser#exprList}.
	 * @param ctx the parse tree
	 */
	void exitArgList(TestGrammarParser.ArgListContext ctx);
}