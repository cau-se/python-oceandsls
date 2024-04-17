// Generated from TestSuite.g4 by ANTLR 4.13.1
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
	 * Visit a parse tree produced by {@link TestSuiteParser#testSuite}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestSuite(TestSuiteParser.TestSuiteContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#testCase}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestCase(TestSuiteParser.TestCaseContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#testFlag}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestFlag(TestSuiteParser.TestFlagContext ctx);
	/**
	 * Visit a parse tree produced by the {@code overwritePF}
	 * labeled alternative in {@link TestSuiteParser#overwriteFlag}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOverwritePF(TestSuiteParser.OverwritePFContext ctx);
	/**
	 * Visit a parse tree produced by the {@code overwriteCMake}
	 * labeled alternative in {@link TestSuiteParser#overwriteFlag}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOverwriteCMake(TestSuiteParser.OverwriteCMakeContext ctx);
	/**
	 * Visit a parse tree produced by the {@code overwriteF90}
	 * labeled alternative in {@link TestSuiteParser#overwriteFlag}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitOverwriteF90(TestSuiteParser.OverwriteF90Context ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#srcPath}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSrcPath(TestSuiteParser.SrcPathContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#testVars}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestVars(TestSuiteParser.TestVarsContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#testVar}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestVar(TestSuiteParser.TestVarContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#varElement}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarElement(TestSuiteParser.VarElementContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#varDeclaration}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarDeclaration(TestSuiteParser.VarDeclarationContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#useModules}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitUseModules(TestSuiteParser.UseModulesContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#testModule}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestModule(TestSuiteParser.TestModuleContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#testAssertion}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestAssertion(TestSuiteParser.TestAssertionContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#pubAttributes}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPubAttributes(TestSuiteParser.PubAttributesContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#extendedTestParameter}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExtendedTestParameter(TestSuiteParser.ExtendedTestParameterContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#testParameter}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestParameter(TestSuiteParser.TestParameterContext ctx);
	/**
	 * Visit a parse tree produced by the {@code emptyDesc}
	 * labeled alternative in {@link TestSuiteParser#optionalDesc}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEmptyDesc(TestSuiteParser.EmptyDescContext ctx);
	/**
	 * Visit a parse tree produced by the {@code specDesc}
	 * labeled alternative in {@link TestSuiteParser#optionalDesc}.
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
	 * Visit a parse tree produced by the {@code arraySpec}
	 * labeled alternative in {@link TestSuiteParser#f90StdKey}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArraySpec(TestSuiteParser.ArraySpecContext ctx);
	/**
	 * Visit a parse tree produced by the {@code argSpecInput}
	 * labeled alternative in {@link TestSuiteParser#f90StdKey}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgSpecInput(TestSuiteParser.ArgSpecInputContext ctx);
	/**
	 * Visit a parse tree produced by the {@code argSpecInOutput}
	 * labeled alternative in {@link TestSuiteParser#f90StdKey}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgSpecInOutput(TestSuiteParser.ArgSpecInOutputContext ctx);
	/**
	 * Visit a parse tree produced by the {@code argSpecOutput}
	 * labeled alternative in {@link TestSuiteParser#f90StdKey}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArgSpecOutput(TestSuiteParser.ArgSpecOutputContext ctx);
	/**
	 * Visit a parse tree produced by the {@code constantSpec}
	 * labeled alternative in {@link TestSuiteParser#f90StdKey}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitConstantSpec(TestSuiteParser.ConstantSpecContext ctx);
	/**
	 * Visit a parse tree produced by the {@code pointerSpec}
	 * labeled alternative in {@link TestSuiteParser#f90StdKey}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPointerSpec(TestSuiteParser.PointerSpecContext ctx);
	/**
	 * Visit a parse tree produced by the {@code procedureSpec}
	 * labeled alternative in {@link TestSuiteParser#f90StdKey}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitProcedureSpec(TestSuiteParser.ProcedureSpecContext ctx);
	/**
	 * Visit a parse tree produced by the {@code customKey}
	 * labeled alternative in {@link TestSuiteParser#f90StdKey}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCustomKey(TestSuiteParser.CustomKeyContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#testDirective}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTestDirective(TestSuiteParser.TestDirectiveContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ref}
	 * labeled alternative in {@link TestSuiteParser#paramType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRef(TestSuiteParser.RefContext ctx);
	/**
	 * Visit a parse tree produced by the {@code enm}
	 * labeled alternative in {@link TestSuiteParser#paramType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitEnm(TestSuiteParser.EnmContext ctx);
	/**
	 * Visit a parse tree produced by the {@code array}
	 * labeled alternative in {@link TestSuiteParser#paramType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitArray(TestSuiteParser.ArrayContext ctx);
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
	 * Visit a parse tree produced by the {@code size}
	 * labeled alternative in {@link TestSuiteParser#dim}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSize(TestSuiteParser.SizeContext ctx);
	/**
	 * Visit a parse tree produced by the {@code range}
	 * labeled alternative in {@link TestSuiteParser#dim}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRange(TestSuiteParser.RangeContext ctx);
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
	 * Visit a parse tree produced by the {@code strExpr}
	 * labeled alternative in {@link TestSuiteParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStrExpr(TestSuiteParser.StrExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code intExpr}
	 * labeled alternative in {@link TestSuiteParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitIntExpr(TestSuiteParser.IntExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code addSubExpr}
	 * labeled alternative in {@link TestSuiteParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAddSubExpr(TestSuiteParser.AddSubExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code signExpr}
	 * labeled alternative in {@link TestSuiteParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSignExpr(TestSuiteParser.SignExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code refExpr}
	 * labeled alternative in {@link TestSuiteParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRefExpr(TestSuiteParser.RefExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code numberExpr}
	 * labeled alternative in {@link TestSuiteParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNumberExpr(TestSuiteParser.NumberExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code parensExpr}
	 * labeled alternative in {@link TestSuiteParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParensExpr(TestSuiteParser.ParensExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code mulDivExpr}
	 * labeled alternative in {@link TestSuiteParser#expr}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMulDivExpr(TestSuiteParser.MulDivExprContext ctx);
	/**
	 * Visit a parse tree produced by the {@code funRef}
	 * labeled alternative in {@link TestSuiteParser#reference}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFunRef(TestSuiteParser.FunRefContext ctx);
	/**
	 * Visit a parse tree produced by the {@code varRef}
	 * labeled alternative in {@link TestSuiteParser#reference}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarRef(TestSuiteParser.VarRefContext ctx);
	/**
	 * Visit a parse tree produced by the {@code prcRef}
	 * labeled alternative in {@link TestSuiteParser#procedure}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPrcRef(TestSuiteParser.PrcRefContext ctx);
	/**
	 * Visit a parse tree produced by {@link TestSuiteParser#varID}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitVarID(TestSuiteParser.VarIDContext ctx);
	/**
	 * Visit a parse tree produced by the {@code parensUnit}
	 * labeled alternative in {@link TestSuiteParser#unitSpec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitParensUnit(TestSuiteParser.ParensUnitContext ctx);
	/**
	 * Visit a parse tree produced by the {@code mulDivUnit}
	 * labeled alternative in {@link TestSuiteParser#unitSpec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMulDivUnit(TestSuiteParser.MulDivUnitContext ctx);
	/**
	 * Visit a parse tree produced by the {@code cstUnit}
	 * labeled alternative in {@link TestSuiteParser#unitSpec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCstUnit(TestSuiteParser.CstUnitContext ctx);
	/**
	 * Visit a parse tree produced by the {@code expUnit}
	 * labeled alternative in {@link TestSuiteParser#unitSpec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExpUnit(TestSuiteParser.ExpUnitContext ctx);
	/**
	 * Visit a parse tree produced by the {@code stdUnit}
	 * labeled alternative in {@link TestSuiteParser#unitSpec}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitStdUnit(TestSuiteParser.StdUnitContext ctx);
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
	 * Visit a parse tree produced by the {@code noP}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNoP(TestSuiteParser.NoPContext ctx);
	/**
	 * Visit a parse tree produced by the {@code quetta}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQuetta(TestSuiteParser.QuettaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ronna}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRonna(TestSuiteParser.RonnaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code yotta}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYotta(TestSuiteParser.YottaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code zetta}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZetta(TestSuiteParser.ZettaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code exa}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitExa(TestSuiteParser.ExaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code peta}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPeta(TestSuiteParser.PetaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code tera}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTera(TestSuiteParser.TeraContext ctx);
	/**
	 * Visit a parse tree produced by the {@code giga}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGiga(TestSuiteParser.GigaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code mega}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMega(TestSuiteParser.MegaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code kilo}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitKilo(TestSuiteParser.KiloContext ctx);
	/**
	 * Visit a parse tree produced by the {@code hecto}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitHecto(TestSuiteParser.HectoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code deca}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDeca(TestSuiteParser.DecaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code deci}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitDeci(TestSuiteParser.DeciContext ctx);
	/**
	 * Visit a parse tree produced by the {@code centi}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCenti(TestSuiteParser.CentiContext ctx);
	/**
	 * Visit a parse tree produced by the {@code mili}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMili(TestSuiteParser.MiliContext ctx);
	/**
	 * Visit a parse tree produced by the {@code micro}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMicro(TestSuiteParser.MicroContext ctx);
	/**
	 * Visit a parse tree produced by the {@code nano}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitNano(TestSuiteParser.NanoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code pico}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPico(TestSuiteParser.PicoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code femto}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitFemto(TestSuiteParser.FemtoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code atto}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAtto(TestSuiteParser.AttoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code zepto}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitZepto(TestSuiteParser.ZeptoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code yocto}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitYocto(TestSuiteParser.YoctoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ronto}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitRonto(TestSuiteParser.RontoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code quecto}
	 * labeled alternative in {@link TestSuiteParser#unitPrefix}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitQuecto(TestSuiteParser.QuectoContext ctx);
	/**
	 * Visit a parse tree produced by the {@code second}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitSecond(TestSuiteParser.SecondContext ctx);
	/**
	 * Visit a parse tree produced by the {@code metre}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMetre(TestSuiteParser.MetreContext ctx);
	/**
	 * Visit a parse tree produced by the {@code gram}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitGram(TestSuiteParser.GramContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ampere}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitAmpere(TestSuiteParser.AmpereContext ctx);
	/**
	 * Visit a parse tree produced by the {@code kelvin}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitKelvin(TestSuiteParser.KelvinContext ctx);
	/**
	 * Visit a parse tree produced by the {@code mole}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitMole(TestSuiteParser.MoleContext ctx);
	/**
	 * Visit a parse tree produced by the {@code candela}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitCandela(TestSuiteParser.CandelaContext ctx);
	/**
	 * Visit a parse tree produced by the {@code pascal}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitPascal(TestSuiteParser.PascalContext ctx);
	/**
	 * Visit a parse tree produced by the {@code joule}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitJoule(TestSuiteParser.JouleContext ctx);
	/**
	 * Visit a parse tree produced by the {@code ton}
	 * labeled alternative in {@link TestSuiteParser#siType}.
	 * @param ctx the parse tree
	 * @return the visitor result
	 */
	T visitTon(TestSuiteParser.TonContext ctx);
}