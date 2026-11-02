// Generated from BgcDsl.g4 by ANTLR 4.13.1
package BgcDsl;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class BgcDslParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, T__21=22, T__22=23, T__23=24, 
		T__24=25, T__25=26, T__26=27, T__27=28, T__28=29, T__29=30, T__30=31, 
		T__31=32, T__32=33, T__33=34, T__34=35, T__35=36, T__36=37, T__37=38, 
		T__38=39, T__39=40, NUMBER=41, CUSTOM_STRING=42, UNIT_STRING=43, INT=44, 
		ID=45, NUM=46, WS=47, COMMENT=48;
	public static final int
		RULE_bgcModel = 0, RULE_substanceDeclaration = 1, RULE_parameterDeclaration = 2, 
		RULE_environmentVariableDeclaration = 3, RULE_primitiveTypes = 4, RULE_compartment = 5, 
		RULE_substanceState = 6, RULE_updateState = 7, RULE_connection = 8, RULE_substanceExpression = 9, 
		RULE_calculation = 10, RULE_basicCalculation = 11, RULE_alternativeCalculation = 12, 
		RULE_caseCalculation = 13, RULE_unit = 14, RULE_unitElement = 15, RULE_groupUnit = 16, 
		RULE_prefixUnit = 17, RULE_arithmeticExpression = 18, RULE_eAdditionOperator = 19, 
		RULE_multiplicationExpression = 20, RULE_eMultiplicationOperator = 21, 
		RULE_powerExpression = 22, RULE_valueExpression = 23, RULE_arrayExpression = 24, 
		RULE_functionCallingExpression = 25, RULE_function = 26, RULE_literalExpression = 27, 
		RULE_literal = 28, RULE_numberLiteral = 29, RULE_stringLiteral = 30, RULE_parenthesisExpression = 31, 
		RULE_termReference = 32, RULE_subterm = 33, RULE_qualifiedName = 34;
	private static String[] makeRuleNames() {
		return new String[] {
			"bgcModel", "substanceDeclaration", "parameterDeclaration", "environmentVariableDeclaration", 
			"primitiveTypes", "compartment", "substanceState", "updateState", "connection", 
			"substanceExpression", "calculation", "basicCalculation", "alternativeCalculation", 
			"caseCalculation", "unit", "unitElement", "groupUnit", "prefixUnit", 
			"arithmeticExpression", "eAdditionOperator", "multiplicationExpression", 
			"eMultiplicationOperator", "powerExpression", "valueExpression", "arrayExpression", 
			"functionCallingExpression", "function", "literalExpression", "literal", 
			"numberLiteral", "stringLiteral", "parenthesisExpression", "termReference", 
			"subterm", "qualifiedName"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'model'", "'substances'", "'parameters'", "'diagnostics'", "'='", 
			"'int'", "'float'", "'double'", "'string'", "'abstract'", "'compartment'", 
			"'extends'", "'{'", "'states'", "'}'", "'update'", "'connection'", "'('", 
			"','", "')'", "'from'", "'to'", "'calc'", "'alternatives'", "':'", "'case'", 
			"'::'", "'^'", "'+'", "'-'", "'*'", "'/'", "'%'", "'['", "']'", "'exp'", 
			"'inverse'", "'max'", "'>'", "'.'", null, null, null, "'this one has been deactivated'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, "NUMBER", "CUSTOM_STRING", "UNIT_STRING", 
			"INT", "ID", "NUM", "WS", "COMMENT"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "BgcDsl.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public BgcDslParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BgcModelContext extends ParserRuleContext {
		public Token name;
		public SubstanceDeclarationContext substanceDeclaration;
		public List<SubstanceDeclarationContext> substanceDeclarations = new ArrayList<SubstanceDeclarationContext>();
		public ParameterDeclarationContext parameterDeclaration;
		public List<ParameterDeclarationContext> parameterDeclarations = new ArrayList<ParameterDeclarationContext>();
		public EnvironmentVariableDeclarationContext environmentVariableDeclaration;
		public List<EnvironmentVariableDeclarationContext> environments = new ArrayList<EnvironmentVariableDeclarationContext>();
		public CompartmentContext compartment;
		public List<CompartmentContext> compartments = new ArrayList<CompartmentContext>();
		public ConnectionContext connection;
		public List<ConnectionContext> connections = new ArrayList<ConnectionContext>();
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public List<SubstanceDeclarationContext> substanceDeclaration() {
			return getRuleContexts(SubstanceDeclarationContext.class);
		}
		public SubstanceDeclarationContext substanceDeclaration(int i) {
			return getRuleContext(SubstanceDeclarationContext.class,i);
		}
		public List<CompartmentContext> compartment() {
			return getRuleContexts(CompartmentContext.class);
		}
		public CompartmentContext compartment(int i) {
			return getRuleContext(CompartmentContext.class,i);
		}
		public List<ConnectionContext> connection() {
			return getRuleContexts(ConnectionContext.class);
		}
		public ConnectionContext connection(int i) {
			return getRuleContext(ConnectionContext.class,i);
		}
		public List<ParameterDeclarationContext> parameterDeclaration() {
			return getRuleContexts(ParameterDeclarationContext.class);
		}
		public ParameterDeclarationContext parameterDeclaration(int i) {
			return getRuleContext(ParameterDeclarationContext.class,i);
		}
		public List<EnvironmentVariableDeclarationContext> environmentVariableDeclaration() {
			return getRuleContexts(EnvironmentVariableDeclarationContext.class);
		}
		public EnvironmentVariableDeclarationContext environmentVariableDeclaration(int i) {
			return getRuleContext(EnvironmentVariableDeclarationContext.class,i);
		}
		public BgcModelContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bgcModel; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterBgcModel(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitBgcModel(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitBgcModel(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BgcModelContext bgcModel() throws RecognitionException {
		BgcModelContext _localctx = new BgcModelContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_bgcModel);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(70);
			match(T__0);
			setState(71);
			((BgcModelContext)_localctx).name = match(ID);
			setState(72);
			match(T__1);
			setState(74); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(73);
				((BgcModelContext)_localctx).substanceDeclaration = substanceDeclaration();
				((BgcModelContext)_localctx).substanceDeclarations.add(((BgcModelContext)_localctx).substanceDeclaration);
				}
				}
				setState(76); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 960L) != 0) );
			setState(85);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__2) {
				{
				setState(78);
				match(T__2);
				setState(82);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 960L) != 0)) {
					{
					{
					setState(79);
					((BgcModelContext)_localctx).parameterDeclaration = parameterDeclaration();
					((BgcModelContext)_localctx).parameterDeclarations.add(((BgcModelContext)_localctx).parameterDeclaration);
					}
					}
					setState(84);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(94);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__3) {
				{
				setState(87);
				match(T__3);
				setState(91);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 960L) != 0)) {
					{
					{
					setState(88);
					((BgcModelContext)_localctx).environmentVariableDeclaration = environmentVariableDeclaration();
					((BgcModelContext)_localctx).environments.add(((BgcModelContext)_localctx).environmentVariableDeclaration);
					}
					}
					setState(93);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(98); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				setState(98);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__9:
				case T__10:
					{
					setState(96);
					((BgcModelContext)_localctx).compartment = compartment();
					((BgcModelContext)_localctx).compartments.add(((BgcModelContext)_localctx).compartment);
					}
					break;
				case T__16:
					{
					setState(97);
					((BgcModelContext)_localctx).connection = connection();
					((BgcModelContext)_localctx).connections.add(((BgcModelContext)_localctx).connection);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(100); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 134144L) != 0) );
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SubstanceDeclarationContext extends ParserRuleContext {
		public PrimitiveTypesContext type;
		public Token name;
		public UnitContext unit() {
			return getRuleContext(UnitContext.class,0);
		}
		public PrimitiveTypesContext primitiveTypes() {
			return getRuleContext(PrimitiveTypesContext.class,0);
		}
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public SubstanceDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_substanceDeclaration; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterSubstanceDeclaration(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitSubstanceDeclaration(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitSubstanceDeclaration(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SubstanceDeclarationContext substanceDeclaration() throws RecognitionException {
		SubstanceDeclarationContext _localctx = new SubstanceDeclarationContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_substanceDeclaration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(102);
			((SubstanceDeclarationContext)_localctx).type = primitiveTypes();
			setState(103);
			((SubstanceDeclarationContext)_localctx).name = match(ID);
			setState(104);
			unit();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParameterDeclarationContext extends ParserRuleContext {
		public PrimitiveTypesContext type;
		public Token name;
		public ArithmeticExpressionContext expression;
		public UnitContext unit() {
			return getRuleContext(UnitContext.class,0);
		}
		public PrimitiveTypesContext primitiveTypes() {
			return getRuleContext(PrimitiveTypesContext.class,0);
		}
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public ParameterDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parameterDeclaration; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterParameterDeclaration(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitParameterDeclaration(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitParameterDeclaration(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParameterDeclarationContext parameterDeclaration() throws RecognitionException {
		ParameterDeclarationContext _localctx = new ParameterDeclarationContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_parameterDeclaration);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(106);
			((ParameterDeclarationContext)_localctx).type = primitiveTypes();
			setState(107);
			((ParameterDeclarationContext)_localctx).name = match(ID);
			setState(108);
			unit();
			setState(109);
			match(T__4);
			setState(110);
			((ParameterDeclarationContext)_localctx).expression = arithmeticExpression();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EnvironmentVariableDeclarationContext extends ParserRuleContext {
		public PrimitiveTypesContext type;
		public Token name;
		public ArithmeticExpressionContext expression;
		public UnitContext unit() {
			return getRuleContext(UnitContext.class,0);
		}
		public PrimitiveTypesContext primitiveTypes() {
			return getRuleContext(PrimitiveTypesContext.class,0);
		}
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public EnvironmentVariableDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_environmentVariableDeclaration; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterEnvironmentVariableDeclaration(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitEnvironmentVariableDeclaration(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitEnvironmentVariableDeclaration(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EnvironmentVariableDeclarationContext environmentVariableDeclaration() throws RecognitionException {
		EnvironmentVariableDeclarationContext _localctx = new EnvironmentVariableDeclarationContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_environmentVariableDeclaration);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(112);
			((EnvironmentVariableDeclarationContext)_localctx).type = primitiveTypes();
			setState(113);
			((EnvironmentVariableDeclarationContext)_localctx).name = match(ID);
			setState(114);
			unit();
			setState(117);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__4) {
				{
				setState(115);
				match(T__4);
				setState(116);
				((EnvironmentVariableDeclarationContext)_localctx).expression = arithmeticExpression();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrimitiveTypesContext extends ParserRuleContext {
		public PrimitiveTypesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_primitiveTypes; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterPrimitiveTypes(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitPrimitiveTypes(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitPrimitiveTypes(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PrimitiveTypesContext primitiveTypes() throws RecognitionException {
		PrimitiveTypesContext _localctx = new PrimitiveTypesContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_primitiveTypes);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(119);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 960L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CompartmentContext extends ParserRuleContext {
		public Token name;
		public Token parent;
		public SubstanceStateContext substanceState;
		public List<SubstanceStateContext> states = new ArrayList<SubstanceStateContext>();
		public ParameterDeclarationContext parameterDeclaration;
		public List<ParameterDeclarationContext> constants = new ArrayList<ParameterDeclarationContext>();
		public EnvironmentVariableDeclarationContext environmentVariableDeclaration;
		public List<EnvironmentVariableDeclarationContext> evnironments = new ArrayList<EnvironmentVariableDeclarationContext>();
		public CalculationContext calculation;
		public List<CalculationContext> calculations = new ArrayList<CalculationContext>();
		public UpdateStateContext updateState;
		public List<UpdateStateContext> updateStates = new ArrayList<UpdateStateContext>();
		public List<TerminalNode> ID() { return getTokens(BgcDslParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(BgcDslParser.ID, i);
		}
		public List<SubstanceStateContext> substanceState() {
			return getRuleContexts(SubstanceStateContext.class);
		}
		public SubstanceStateContext substanceState(int i) {
			return getRuleContext(SubstanceStateContext.class,i);
		}
		public List<CalculationContext> calculation() {
			return getRuleContexts(CalculationContext.class);
		}
		public CalculationContext calculation(int i) {
			return getRuleContext(CalculationContext.class,i);
		}
		public List<UpdateStateContext> updateState() {
			return getRuleContexts(UpdateStateContext.class);
		}
		public UpdateStateContext updateState(int i) {
			return getRuleContext(UpdateStateContext.class,i);
		}
		public List<ParameterDeclarationContext> parameterDeclaration() {
			return getRuleContexts(ParameterDeclarationContext.class);
		}
		public ParameterDeclarationContext parameterDeclaration(int i) {
			return getRuleContext(ParameterDeclarationContext.class,i);
		}
		public List<EnvironmentVariableDeclarationContext> environmentVariableDeclaration() {
			return getRuleContexts(EnvironmentVariableDeclarationContext.class);
		}
		public EnvironmentVariableDeclarationContext environmentVariableDeclaration(int i) {
			return getRuleContext(EnvironmentVariableDeclarationContext.class,i);
		}
		public CompartmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_compartment; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterCompartment(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitCompartment(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitCompartment(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CompartmentContext compartment() throws RecognitionException {
		CompartmentContext _localctx = new CompartmentContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_compartment);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(122);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__9) {
				{
				setState(121);
				match(T__9);
				}
			}

			setState(124);
			match(T__10);
			setState(125);
			((CompartmentContext)_localctx).name = match(ID);
			setState(128);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__11) {
				{
				setState(126);
				match(T__11);
				setState(127);
				((CompartmentContext)_localctx).parent = match(ID);
				}
			}

			setState(130);
			match(T__12);
			setState(131);
			match(T__13);
			setState(133); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(132);
				((CompartmentContext)_localctx).substanceState = substanceState();
				((CompartmentContext)_localctx).states.add(((CompartmentContext)_localctx).substanceState);
				}
				}
				setState(135); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==ID );
			setState(144);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__2) {
				{
				setState(137);
				match(T__2);
				setState(141);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 960L) != 0)) {
					{
					{
					setState(138);
					((CompartmentContext)_localctx).parameterDeclaration = parameterDeclaration();
					((CompartmentContext)_localctx).constants.add(((CompartmentContext)_localctx).parameterDeclaration);
					}
					}
					setState(143);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(153);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__3) {
				{
				setState(146);
				match(T__3);
				setState(150);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 960L) != 0)) {
					{
					{
					setState(147);
					((CompartmentContext)_localctx).environmentVariableDeclaration = environmentVariableDeclaration();
					((CompartmentContext)_localctx).evnironments.add(((CompartmentContext)_localctx).environmentVariableDeclaration);
					}
					}
					setState(152);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(158);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__22 || _la==T__23) {
				{
				{
				setState(155);
				((CompartmentContext)_localctx).calculation = calculation();
				((CompartmentContext)_localctx).calculations.add(((CompartmentContext)_localctx).calculation);
				}
				}
				setState(160);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(162); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(161);
				((CompartmentContext)_localctx).updateState = updateState();
				((CompartmentContext)_localctx).updateStates.add(((CompartmentContext)_localctx).updateState);
				}
				}
				setState(164); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( _la==T__15 );
			setState(166);
			match(T__14);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SubstanceStateContext extends ParserRuleContext {
		public Token substance;
		public ArithmeticExpressionContext expression;
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public SubstanceStateContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_substanceState; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterSubstanceState(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitSubstanceState(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitSubstanceState(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SubstanceStateContext substanceState() throws RecognitionException {
		SubstanceStateContext _localctx = new SubstanceStateContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_substanceState);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(168);
			((SubstanceStateContext)_localctx).substance = match(ID);
			setState(171);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__4) {
				{
				setState(169);
				match(T__4);
				setState(170);
				((SubstanceStateContext)_localctx).expression = arithmeticExpression();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UpdateStateContext extends ParserRuleContext {
		public Token state;
		public ArithmeticExpressionContext expression;
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public UpdateStateContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_updateState; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterUpdateState(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitUpdateState(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitUpdateState(this);
			else return visitor.visitChildren(this);
		}
	}

	public final UpdateStateContext updateState() throws RecognitionException {
		UpdateStateContext _localctx = new UpdateStateContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_updateState);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(173);
			match(T__15);
			setState(174);
			((UpdateStateContext)_localctx).state = match(ID);
			setState(175);
			match(T__4);
			setState(176);
			((UpdateStateContext)_localctx).expression = arithmeticExpression();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ConnectionContext extends ParserRuleContext {
		public Token name;
		public Token ID;
		public List<Token> substances = new ArrayList<Token>();
		public Token sourceCompartment;
		public Token targetCompartment;
		public ArithmeticExpressionContext expression;
		public SubstanceExpressionContext substanceExpression;
		public List<SubstanceExpressionContext> substanceExpressions = new ArrayList<SubstanceExpressionContext>();
		public CalculationContext calculation;
		public List<CalculationContext> calculations = new ArrayList<CalculationContext>();
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public List<TerminalNode> ID() { return getTokens(BgcDslParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(BgcDslParser.ID, i);
		}
		public List<SubstanceExpressionContext> substanceExpression() {
			return getRuleContexts(SubstanceExpressionContext.class);
		}
		public SubstanceExpressionContext substanceExpression(int i) {
			return getRuleContext(SubstanceExpressionContext.class,i);
		}
		public List<CalculationContext> calculation() {
			return getRuleContexts(CalculationContext.class);
		}
		public CalculationContext calculation(int i) {
			return getRuleContext(CalculationContext.class,i);
		}
		public ConnectionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_connection; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterConnection(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitConnection(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitConnection(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ConnectionContext connection() throws RecognitionException {
		ConnectionContext _localctx = new ConnectionContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_connection);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(178);
			match(T__16);
			setState(212);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,22,_ctx) ) {
			case 1:
				{
				{
				setState(179);
				((ConnectionContext)_localctx).name = match(ID);
				setState(190);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__17) {
					{
					setState(180);
					match(T__17);
					setState(181);
					((ConnectionContext)_localctx).ID = match(ID);
					((ConnectionContext)_localctx).substances.add(((ConnectionContext)_localctx).ID);
					setState(186);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__18) {
						{
						{
						setState(182);
						match(T__18);
						setState(183);
						((ConnectionContext)_localctx).ID = match(ID);
						((ConnectionContext)_localctx).substances.add(((ConnectionContext)_localctx).ID);
						}
						}
						setState(188);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					setState(189);
					match(T__19);
					}
				}

				setState(192);
				match(T__20);
				setState(193);
				((ConnectionContext)_localctx).sourceCompartment = match(ID);
				setState(194);
				match(T__21);
				setState(195);
				((ConnectionContext)_localctx).targetCompartment = match(ID);
				}
				}
				break;
			case 2:
				{
				{
				setState(196);
				((ConnectionContext)_localctx).sourceCompartment = match(ID);
				setState(197);
				match(T__21);
				setState(198);
				((ConnectionContext)_localctx).targetCompartment = match(ID);
				setState(199);
				((ConnectionContext)_localctx).name = match(ID);
				setState(210);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if (_la==T__17) {
					{
					setState(200);
					match(T__17);
					setState(201);
					((ConnectionContext)_localctx).ID = match(ID);
					((ConnectionContext)_localctx).substances.add(((ConnectionContext)_localctx).ID);
					setState(206);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__18) {
						{
						{
						setState(202);
						match(T__18);
						setState(203);
						((ConnectionContext)_localctx).ID = match(ID);
						((ConnectionContext)_localctx).substances.add(((ConnectionContext)_localctx).ID);
						}
						}
						setState(208);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					setState(209);
					match(T__19);
					}
				}

				}
				}
				break;
			}
			setState(225);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__4:
				{
				setState(214);
				match(T__4);
				setState(215);
				((ConnectionContext)_localctx).expression = arithmeticExpression();
				}
				break;
			case T__12:
				{
				setState(216);
				match(T__12);
				setState(221);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 35184397254656L) != 0)) {
					{
					setState(219);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case ID:
						{
						setState(217);
						((ConnectionContext)_localctx).substanceExpression = substanceExpression();
						((ConnectionContext)_localctx).substanceExpressions.add(((ConnectionContext)_localctx).substanceExpression);
						}
						break;
					case T__22:
					case T__23:
						{
						setState(218);
						((ConnectionContext)_localctx).calculation = calculation();
						((ConnectionContext)_localctx).calculations.add(((ConnectionContext)_localctx).calculation);
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					}
					setState(223);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(224);
				match(T__14);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SubstanceExpressionContext extends ParserRuleContext {
		public Token substance;
		public ArithmeticExpressionContext expression;
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public SubstanceExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_substanceExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterSubstanceExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitSubstanceExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitSubstanceExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SubstanceExpressionContext substanceExpression() throws RecognitionException {
		SubstanceExpressionContext _localctx = new SubstanceExpressionContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_substanceExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(227);
			((SubstanceExpressionContext)_localctx).substance = match(ID);
			setState(228);
			match(T__4);
			setState(229);
			((SubstanceExpressionContext)_localctx).expression = arithmeticExpression();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CalculationContext extends ParserRuleContext {
		public BasicCalculationContext basicCalculation() {
			return getRuleContext(BasicCalculationContext.class,0);
		}
		public AlternativeCalculationContext alternativeCalculation() {
			return getRuleContext(AlternativeCalculationContext.class,0);
		}
		public CalculationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_calculation; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterCalculation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitCalculation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitCalculation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CalculationContext calculation() throws RecognitionException {
		CalculationContext _localctx = new CalculationContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_calculation);
		try {
			setState(233);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__22:
				enterOuterAlt(_localctx, 1);
				{
				setState(231);
				basicCalculation();
				}
				break;
			case T__23:
				enterOuterAlt(_localctx, 2);
				{
				setState(232);
				alternativeCalculation();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BasicCalculationContext extends ParserRuleContext {
		public Token name;
		public ArithmeticExpressionContext expression;
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public BasicCalculationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_basicCalculation; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterBasicCalculation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitBasicCalculation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitBasicCalculation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BasicCalculationContext basicCalculation() throws RecognitionException {
		BasicCalculationContext _localctx = new BasicCalculationContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_basicCalculation);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(235);
			match(T__22);
			setState(236);
			((BasicCalculationContext)_localctx).name = match(ID);
			setState(237);
			match(T__4);
			setState(238);
			((BasicCalculationContext)_localctx).expression = arithmeticExpression();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class AlternativeCalculationContext extends ParserRuleContext {
		public Token name;
		public ArithmeticExpressionContext expression;
		public CaseCalculationContext caseCalculation;
		public List<CaseCalculationContext> alternatives = new ArrayList<CaseCalculationContext>();
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public List<CaseCalculationContext> caseCalculation() {
			return getRuleContexts(CaseCalculationContext.class);
		}
		public CaseCalculationContext caseCalculation(int i) {
			return getRuleContext(CaseCalculationContext.class,i);
		}
		public AlternativeCalculationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_alternativeCalculation; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterAlternativeCalculation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitAlternativeCalculation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitAlternativeCalculation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final AlternativeCalculationContext alternativeCalculation() throws RecognitionException {
		AlternativeCalculationContext _localctx = new AlternativeCalculationContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_alternativeCalculation);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(240);
			match(T__23);
			setState(241);
			((AlternativeCalculationContext)_localctx).name = match(ID);
			setState(242);
			match(T__24);
			setState(243);
			((AlternativeCalculationContext)_localctx).expression = arithmeticExpression();
			setState(244);
			match(T__12);
			setState(248);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__25) {
				{
				{
				setState(245);
				((AlternativeCalculationContext)_localctx).caseCalculation = caseCalculation();
				((AlternativeCalculationContext)_localctx).alternatives.add(((AlternativeCalculationContext)_localctx).caseCalculation);
				}
				}
				setState(250);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(251);
			match(T__14);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CaseCalculationContext extends ParserRuleContext {
		public LiteralExpressionContext literalExp;
		public ArithmeticExpressionContext expression;
		public LiteralExpressionContext literalExpression() {
			return getRuleContext(LiteralExpressionContext.class,0);
		}
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public CaseCalculationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_caseCalculation; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterCaseCalculation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitCaseCalculation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitCaseCalculation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CaseCalculationContext caseCalculation() throws RecognitionException {
		CaseCalculationContext _localctx = new CaseCalculationContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_caseCalculation);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(253);
			match(T__25);
			setState(254);
			((CaseCalculationContext)_localctx).literalExp = literalExpression();
			setState(255);
			match(T__24);
			setState(256);
			((CaseCalculationContext)_localctx).expression = arithmeticExpression();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UnitContext extends ParserRuleContext {
		public UnitElementContext unitElement;
		public List<UnitElementContext> elements = new ArrayList<UnitElementContext>();
		public List<UnitElementContext> unitElement() {
			return getRuleContexts(UnitElementContext.class);
		}
		public UnitElementContext unitElement(int i) {
			return getRuleContext(UnitElementContext.class,i);
		}
		public UnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unit; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterUnit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitUnit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitUnit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final UnitContext unit() throws RecognitionException {
		UnitContext _localctx = new UnitContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_unit);
		int _la;
		try {
			setState(265);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__24:
				enterOuterAlt(_localctx, 1);
				{
				setState(258);
				match(T__24);
				setState(260); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(259);
					((UnitContext)_localctx).unitElement = unitElement();
					((UnitContext)_localctx).elements.add(((UnitContext)_localctx).unitElement);
					}
					}
					setState(262); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & 13194139795456L) != 0) );
				}
				break;
			case T__26:
				enterOuterAlt(_localctx, 2);
				{
				setState(264);
				match(T__26);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UnitElementContext extends ParserRuleContext {
		public PrefixUnitContext prefixUnit() {
			return getRuleContext(PrefixUnitContext.class,0);
		}
		public GroupUnitContext groupUnit() {
			return getRuleContext(GroupUnitContext.class,0);
		}
		public UnitElementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unitElement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterUnitElement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitUnitElement(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitUnitElement(this);
			else return visitor.visitChildren(this);
		}
	}

	public final UnitElementContext unitElement() throws RecognitionException {
		UnitElementContext _localctx = new UnitElementContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_unitElement);
		try {
			setState(269);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case CUSTOM_STRING:
			case UNIT_STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(267);
				prefixUnit();
				}
				break;
			case T__17:
				enterOuterAlt(_localctx, 2);
				{
				setState(268);
				groupUnit();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class GroupUnitContext extends ParserRuleContext {
		public UnitElementContext unitElement;
		public List<UnitElementContext> elements = new ArrayList<UnitElementContext>();
		public Token exponent;
		public List<UnitElementContext> unitElement() {
			return getRuleContexts(UnitElementContext.class);
		}
		public UnitElementContext unitElement(int i) {
			return getRuleContext(UnitElementContext.class,i);
		}
		public TerminalNode NUMBER() { return getToken(BgcDslParser.NUMBER, 0); }
		public GroupUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_groupUnit; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterGroupUnit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitGroupUnit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitGroupUnit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final GroupUnitContext groupUnit() throws RecognitionException {
		GroupUnitContext _localctx = new GroupUnitContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_groupUnit);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(271);
			match(T__17);
			setState(275);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 13194139795456L) != 0)) {
				{
				{
				setState(272);
				((GroupUnitContext)_localctx).unitElement = unitElement();
				((GroupUnitContext)_localctx).elements.add(((GroupUnitContext)_localctx).unitElement);
				}
				}
				setState(277);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(278);
			match(T__19);
			setState(281);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__27) {
				{
				setState(279);
				match(T__27);
				setState(280);
				((GroupUnitContext)_localctx).exponent = match(NUMBER);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrefixUnitContext extends ParserRuleContext {
		public Token custom;
		public Token substance;
		public Token exponent;
		public TerminalNode UNIT_STRING() { return getToken(BgcDslParser.UNIT_STRING, 0); }
		public TerminalNode CUSTOM_STRING() { return getToken(BgcDslParser.CUSTOM_STRING, 0); }
		public TerminalNode ID() { return getToken(BgcDslParser.ID, 0); }
		public TerminalNode NUMBER() { return getToken(BgcDslParser.NUMBER, 0); }
		public PrefixUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prefixUnit; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterPrefixUnit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitPrefixUnit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitPrefixUnit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PrefixUnitContext prefixUnit() throws RecognitionException {
		PrefixUnitContext _localctx = new PrefixUnitContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_prefixUnit);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(285);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case UNIT_STRING:
				{
				setState(283);
				match(UNIT_STRING);
				}
				break;
			case CUSTOM_STRING:
				{
				setState(284);
				((PrefixUnitContext)_localctx).custom = match(CUSTOM_STRING);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			setState(288);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ID) {
				{
				setState(287);
				((PrefixUnitContext)_localctx).substance = match(ID);
				}
			}

			setState(292);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__27) {
				{
				setState(290);
				match(T__27);
				setState(291);
				((PrefixUnitContext)_localctx).exponent = match(NUMBER);
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArithmeticExpressionContext extends ParserRuleContext {
		public EAdditionOperatorContext operator;
		public ArithmeticExpressionContext right;
		public MultiplicationExpressionContext multiplicationExpression() {
			return getRuleContext(MultiplicationExpressionContext.class,0);
		}
		public EAdditionOperatorContext eAdditionOperator() {
			return getRuleContext(EAdditionOperatorContext.class,0);
		}
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public ArithmeticExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arithmeticExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterArithmeticExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitArithmeticExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitArithmeticExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArithmeticExpressionContext arithmeticExpression() throws RecognitionException {
		ArithmeticExpressionContext _localctx = new ArithmeticExpressionContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_arithmeticExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(294);
			multiplicationExpression();
			setState(298);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__28 || _la==T__29) {
				{
				setState(295);
				((ArithmeticExpressionContext)_localctx).operator = eAdditionOperator();
				setState(296);
				((ArithmeticExpressionContext)_localctx).right = arithmeticExpression();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EAdditionOperatorContext extends ParserRuleContext {
		public Token ADDITION;
		public Token SUBTRACTION;
		public EAdditionOperatorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_eAdditionOperator; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterEAdditionOperator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitEAdditionOperator(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitEAdditionOperator(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EAdditionOperatorContext eAdditionOperator() throws RecognitionException {
		EAdditionOperatorContext _localctx = new EAdditionOperatorContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_eAdditionOperator);
		try {
			setState(302);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__28:
				enterOuterAlt(_localctx, 1);
				{
				setState(300);
				((EAdditionOperatorContext)_localctx).ADDITION = match(T__28);
				}
				break;
			case T__29:
				enterOuterAlt(_localctx, 2);
				{
				setState(301);
				((EAdditionOperatorContext)_localctx).SUBTRACTION = match(T__29);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class MultiplicationExpressionContext extends ParserRuleContext {
		public EMultiplicationOperatorContext operator;
		public MultiplicationExpressionContext right;
		public PowerExpressionContext powerExpression() {
			return getRuleContext(PowerExpressionContext.class,0);
		}
		public EMultiplicationOperatorContext eMultiplicationOperator() {
			return getRuleContext(EMultiplicationOperatorContext.class,0);
		}
		public MultiplicationExpressionContext multiplicationExpression() {
			return getRuleContext(MultiplicationExpressionContext.class,0);
		}
		public MultiplicationExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_multiplicationExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterMultiplicationExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitMultiplicationExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitMultiplicationExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final MultiplicationExpressionContext multiplicationExpression() throws RecognitionException {
		MultiplicationExpressionContext _localctx = new MultiplicationExpressionContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_multiplicationExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(304);
			powerExpression();
			setState(308);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 15032385536L) != 0)) {
				{
				setState(305);
				((MultiplicationExpressionContext)_localctx).operator = eMultiplicationOperator();
				setState(306);
				((MultiplicationExpressionContext)_localctx).right = multiplicationExpression();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class EMultiplicationOperatorContext extends ParserRuleContext {
		public Token MULTIPLICATION;
		public Token DIVISION;
		public Token MODULO;
		public EMultiplicationOperatorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_eMultiplicationOperator; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterEMultiplicationOperator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitEMultiplicationOperator(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitEMultiplicationOperator(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EMultiplicationOperatorContext eMultiplicationOperator() throws RecognitionException {
		EMultiplicationOperatorContext _localctx = new EMultiplicationOperatorContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_eMultiplicationOperator);
		try {
			setState(313);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__30:
				enterOuterAlt(_localctx, 1);
				{
				setState(310);
				((EMultiplicationOperatorContext)_localctx).MULTIPLICATION = match(T__30);
				}
				break;
			case T__31:
				enterOuterAlt(_localctx, 2);
				{
				setState(311);
				((EMultiplicationOperatorContext)_localctx).DIVISION = match(T__31);
				}
				break;
			case T__32:
				enterOuterAlt(_localctx, 3);
				{
				setState(312);
				((EMultiplicationOperatorContext)_localctx).MODULO = match(T__32);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PowerExpressionContext extends ParserRuleContext {
		public ValueExpressionContext right;
		public List<ValueExpressionContext> valueExpression() {
			return getRuleContexts(ValueExpressionContext.class);
		}
		public ValueExpressionContext valueExpression(int i) {
			return getRuleContext(ValueExpressionContext.class,i);
		}
		public PowerExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_powerExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterPowerExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitPowerExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitPowerExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final PowerExpressionContext powerExpression() throws RecognitionException {
		PowerExpressionContext _localctx = new PowerExpressionContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_powerExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(315);
			valueExpression();
			setState(318);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__27) {
				{
				setState(316);
				match(T__27);
				setState(317);
				((PowerExpressionContext)_localctx).right = valueExpression();
				}
			}

			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ValueExpressionContext extends ParserRuleContext {
		public ArrayExpressionContext arrayExpression() {
			return getRuleContext(ArrayExpressionContext.class,0);
		}
		public FunctionCallingExpressionContext functionCallingExpression() {
			return getRuleContext(FunctionCallingExpressionContext.class,0);
		}
		public LiteralExpressionContext literalExpression() {
			return getRuleContext(LiteralExpressionContext.class,0);
		}
		public ParenthesisExpressionContext parenthesisExpression() {
			return getRuleContext(ParenthesisExpressionContext.class,0);
		}
		public TermReferenceContext termReference() {
			return getRuleContext(TermReferenceContext.class,0);
		}
		public ValueExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_valueExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterValueExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitValueExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitValueExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ValueExpressionContext valueExpression() throws RecognitionException {
		ValueExpressionContext _localctx = new ValueExpressionContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_valueExpression);
		try {
			setState(325);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__33:
				enterOuterAlt(_localctx, 1);
				{
				setState(320);
				arrayExpression();
				}
				break;
			case T__35:
			case T__36:
			case T__37:
				enterOuterAlt(_localctx, 2);
				{
				setState(321);
				functionCallingExpression();
				}
				break;
			case T__8:
			case NUMBER:
				enterOuterAlt(_localctx, 3);
				{
				setState(322);
				literalExpression();
				}
				break;
			case T__17:
				enterOuterAlt(_localctx, 4);
				{
				setState(323);
				parenthesisExpression();
				}
				break;
			case ID:
				enterOuterAlt(_localctx, 5);
				{
				setState(324);
				termReference();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArrayExpressionContext extends ParserRuleContext {
		public ArithmeticExpressionContext arithmeticExpression;
		public List<ArithmeticExpressionContext> expressions = new ArrayList<ArithmeticExpressionContext>();
		public List<ArithmeticExpressionContext> arithmeticExpression() {
			return getRuleContexts(ArithmeticExpressionContext.class);
		}
		public ArithmeticExpressionContext arithmeticExpression(int i) {
			return getRuleContext(ArithmeticExpressionContext.class,i);
		}
		public ArrayExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arrayExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterArrayExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitArrayExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitArrayExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArrayExpressionContext arrayExpression() throws RecognitionException {
		ArrayExpressionContext _localctx = new ArrayExpressionContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_arrayExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(327);
			match(T__33);
			setState(328);
			((ArrayExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
			((ArrayExpressionContext)_localctx).expressions.add(((ArrayExpressionContext)_localctx).arithmeticExpression);
			setState(333);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__18) {
				{
				{
				setState(329);
				match(T__18);
				setState(330);
				((ArrayExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
				((ArrayExpressionContext)_localctx).expressions.add(((ArrayExpressionContext)_localctx).arithmeticExpression);
				}
				}
				setState(335);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(336);
			match(T__34);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FunctionCallingExpressionContext extends ParserRuleContext {
		public FunctionContext type;
		public ArithmeticExpressionContext arithmeticExpression;
		public List<ArithmeticExpressionContext> expressions = new ArrayList<ArithmeticExpressionContext>();
		public FunctionContext function() {
			return getRuleContext(FunctionContext.class,0);
		}
		public List<ArithmeticExpressionContext> arithmeticExpression() {
			return getRuleContexts(ArithmeticExpressionContext.class);
		}
		public ArithmeticExpressionContext arithmeticExpression(int i) {
			return getRuleContext(ArithmeticExpressionContext.class,i);
		}
		public FunctionCallingExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_functionCallingExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterFunctionCallingExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitFunctionCallingExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitFunctionCallingExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FunctionCallingExpressionContext functionCallingExpression() throws RecognitionException {
		FunctionCallingExpressionContext _localctx = new FunctionCallingExpressionContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_functionCallingExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(338);
			((FunctionCallingExpressionContext)_localctx).type = function();
			setState(339);
			match(T__17);
			setState(340);
			((FunctionCallingExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
			((FunctionCallingExpressionContext)_localctx).expressions.add(((FunctionCallingExpressionContext)_localctx).arithmeticExpression);
			setState(345);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__18) {
				{
				{
				setState(341);
				match(T__18);
				setState(342);
				((FunctionCallingExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
				((FunctionCallingExpressionContext)_localctx).expressions.add(((FunctionCallingExpressionContext)_localctx).arithmeticExpression);
				}
				}
				setState(347);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(348);
			match(T__19);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FunctionContext extends ParserRuleContext {
		public FunctionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_function; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterFunction(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitFunction(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitFunction(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FunctionContext function() throws RecognitionException {
		FunctionContext _localctx = new FunctionContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_function);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(350);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 481036337152L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LiteralExpressionContext extends ParserRuleContext {
		public LiteralContext value;
		public LiteralContext literal() {
			return getRuleContext(LiteralContext.class,0);
		}
		public LiteralExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literalExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterLiteralExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitLiteralExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitLiteralExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LiteralExpressionContext literalExpression() throws RecognitionException {
		LiteralExpressionContext _localctx = new LiteralExpressionContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_literalExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(352);
			((LiteralExpressionContext)_localctx).value = literal();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class LiteralContext extends ParserRuleContext {
		public NumberLiteralContext numberLiteral() {
			return getRuleContext(NumberLiteralContext.class,0);
		}
		public StringLiteralContext stringLiteral() {
			return getRuleContext(StringLiteralContext.class,0);
		}
		public LiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literal; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitLiteral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LiteralContext literal() throws RecognitionException {
		LiteralContext _localctx = new LiteralContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_literal);
		try {
			setState(356);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case NUMBER:
				enterOuterAlt(_localctx, 1);
				{
				setState(354);
				numberLiteral();
				}
				break;
			case T__8:
				enterOuterAlt(_localctx, 2);
				{
				setState(355);
				stringLiteral();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class NumberLiteralContext extends ParserRuleContext {
		public Token value;
		public TerminalNode NUMBER() { return getToken(BgcDslParser.NUMBER, 0); }
		public NumberLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_numberLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterNumberLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitNumberLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitNumberLiteral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NumberLiteralContext numberLiteral() throws RecognitionException {
		NumberLiteralContext _localctx = new NumberLiteralContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_numberLiteral);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(358);
			((NumberLiteralContext)_localctx).value = match(NUMBER);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class StringLiteralContext extends ParserRuleContext {
		public Token value;
		public StringLiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_stringLiteral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterStringLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitStringLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitStringLiteral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StringLiteralContext stringLiteral() throws RecognitionException {
		StringLiteralContext _localctx = new StringLiteralContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_stringLiteral);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(360);
			((StringLiteralContext)_localctx).value = match(T__8);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParenthesisExpressionContext extends ParserRuleContext {
		public ArithmeticExpressionContext expression;
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public ParenthesisExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parenthesisExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterParenthesisExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitParenthesisExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitParenthesisExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParenthesisExpressionContext parenthesisExpression() throws RecognitionException {
		ParenthesisExpressionContext _localctx = new ParenthesisExpressionContext(_ctx, getState());
		enterRule(_localctx, 62, RULE_parenthesisExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(362);
			match(T__17);
			setState(363);
			((ParenthesisExpressionContext)_localctx).expression = arithmeticExpression();
			setState(364);
			match(T__19);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TermReferenceContext extends ParserRuleContext {
		public Token sourceCompartment;
		public Token targetCompartment;
		public QualifiedNameContext reference;
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public List<TerminalNode> ID() { return getTokens(BgcDslParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(BgcDslParser.ID, i);
		}
		public TermReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_termReference; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterTermReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitTermReference(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitTermReference(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TermReferenceContext termReference() throws RecognitionException {
		TermReferenceContext _localctx = new TermReferenceContext(_ctx, getState());
		enterRule(_localctx, 64, RULE_termReference);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(368);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,45,_ctx) ) {
			case 1:
				{
				setState(366);
				((TermReferenceContext)_localctx).sourceCompartment = match(ID);
				setState(367);
				match(T__38);
				}
				break;
			}
			setState(372);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,46,_ctx) ) {
			case 1:
				{
				setState(370);
				((TermReferenceContext)_localctx).targetCompartment = match(ID);
				setState(371);
				match(T__24);
				}
				break;
			}
			setState(374);
			((TermReferenceContext)_localctx).reference = qualifiedName();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class SubtermContext extends ParserRuleContext {
		public UpdateStateContext updateState() {
			return getRuleContext(UpdateStateContext.class,0);
		}
		public ConnectionContext connection() {
			return getRuleContext(ConnectionContext.class,0);
		}
		public ParameterDeclarationContext parameterDeclaration() {
			return getRuleContext(ParameterDeclarationContext.class,0);
		}
		public CalculationContext calculation() {
			return getRuleContext(CalculationContext.class,0);
		}
		public EnvironmentVariableDeclarationContext environmentVariableDeclaration() {
			return getRuleContext(EnvironmentVariableDeclarationContext.class,0);
		}
		public SubstanceExpressionContext substanceExpression() {
			return getRuleContext(SubstanceExpressionContext.class,0);
		}
		public SubstanceStateContext substanceState() {
			return getRuleContext(SubstanceStateContext.class,0);
		}
		public SubtermContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_subterm; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterSubterm(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitSubterm(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitSubterm(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SubtermContext subterm() throws RecognitionException {
		SubtermContext _localctx = new SubtermContext(_ctx, getState());
		enterRule(_localctx, 66, RULE_subterm);
		try {
			setState(383);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,47,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(376);
				updateState();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(377);
				connection();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(378);
				parameterDeclaration();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(379);
				calculation();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(380);
				environmentVariableDeclaration();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(381);
				substanceExpression();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(382);
				substanceState();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class QualifiedNameContext extends ParserRuleContext {
		public List<TerminalNode> ID() { return getTokens(BgcDslParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(BgcDslParser.ID, i);
		}
		public QualifiedNameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_qualifiedName; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).enterQualifiedName(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof BgcDslListener ) ((BgcDslListener)listener).exitQualifiedName(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof BgcDslVisitor ) return ((BgcDslVisitor<? extends T>)visitor).visitQualifiedName(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QualifiedNameContext qualifiedName() throws RecognitionException {
		QualifiedNameContext _localctx = new QualifiedNameContext(_ctx, getState());
		enterRule(_localctx, 68, RULE_qualifiedName);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(385);
			match(ID);
			setState(390);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__39) {
				{
				{
				setState(386);
				match(T__39);
				setState(387);
				match(ID);
				}
				}
				setState(392);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public static final String _serializedATN =
		"\u0004\u00010\u018a\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007\u0015"+
		"\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002\u0018\u0007\u0018"+
		"\u0002\u0019\u0007\u0019\u0002\u001a\u0007\u001a\u0002\u001b\u0007\u001b"+
		"\u0002\u001c\u0007\u001c\u0002\u001d\u0007\u001d\u0002\u001e\u0007\u001e"+
		"\u0002\u001f\u0007\u001f\u0002 \u0007 \u0002!\u0007!\u0002\"\u0007\"\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0004\u0000K\b\u0000\u000b"+
		"\u0000\f\u0000L\u0001\u0000\u0001\u0000\u0005\u0000Q\b\u0000\n\u0000\f"+
		"\u0000T\t\u0000\u0003\u0000V\b\u0000\u0001\u0000\u0001\u0000\u0005\u0000"+
		"Z\b\u0000\n\u0000\f\u0000]\t\u0000\u0003\u0000_\b\u0000\u0001\u0000\u0001"+
		"\u0000\u0004\u0000c\b\u0000\u000b\u0000\f\u0000d\u0001\u0001\u0001\u0001"+
		"\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0003\u0003v\b\u0003\u0001\u0004\u0001\u0004\u0001\u0005"+
		"\u0003\u0005{\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0003\u0005\u0081\b\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0004\u0005"+
		"\u0086\b\u0005\u000b\u0005\f\u0005\u0087\u0001\u0005\u0001\u0005\u0005"+
		"\u0005\u008c\b\u0005\n\u0005\f\u0005\u008f\t\u0005\u0003\u0005\u0091\b"+
		"\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u0095\b\u0005\n\u0005\f\u0005"+
		"\u0098\t\u0005\u0003\u0005\u009a\b\u0005\u0001\u0005\u0005\u0005\u009d"+
		"\b\u0005\n\u0005\f\u0005\u00a0\t\u0005\u0001\u0005\u0004\u0005\u00a3\b"+
		"\u0005\u000b\u0005\f\u0005\u00a4\u0001\u0005\u0001\u0005\u0001\u0006\u0001"+
		"\u0006\u0001\u0006\u0003\u0006\u00ac\b\u0006\u0001\u0007\u0001\u0007\u0001"+
		"\u0007\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b"+
		"\u0001\b\u0005\b\u00b9\b\b\n\b\f\b\u00bc\t\b\u0001\b\u0003\b\u00bf\b\b"+
		"\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001"+
		"\b\u0001\b\u0001\b\u0001\b\u0005\b\u00cd\b\b\n\b\f\b\u00d0\t\b\u0001\b"+
		"\u0003\b\u00d3\b\b\u0003\b\u00d5\b\b\u0001\b\u0001\b\u0001\b\u0001\b\u0001"+
		"\b\u0005\b\u00dc\b\b\n\b\f\b\u00df\t\b\u0001\b\u0003\b\u00e2\b\b\u0001"+
		"\t\u0001\t\u0001\t\u0001\t\u0001\n\u0001\n\u0003\n\u00ea\b\n\u0001\u000b"+
		"\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b\u0001\f\u0001\f\u0001"+
		"\f\u0001\f\u0001\f\u0001\f\u0005\f\u00f7\b\f\n\f\f\f\u00fa\t\f\u0001\f"+
		"\u0001\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\u000e\u0001\u000e"+
		"\u0004\u000e\u0105\b\u000e\u000b\u000e\f\u000e\u0106\u0001\u000e\u0003"+
		"\u000e\u010a\b\u000e\u0001\u000f\u0001\u000f\u0003\u000f\u010e\b\u000f"+
		"\u0001\u0010\u0001\u0010\u0005\u0010\u0112\b\u0010\n\u0010\f\u0010\u0115"+
		"\t\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0003\u0010\u011a\b\u0010"+
		"\u0001\u0011\u0001\u0011\u0003\u0011\u011e\b\u0011\u0001\u0011\u0003\u0011"+
		"\u0121\b\u0011\u0001\u0011\u0001\u0011\u0003\u0011\u0125\b\u0011\u0001"+
		"\u0012\u0001\u0012\u0001\u0012\u0001\u0012\u0003\u0012\u012b\b\u0012\u0001"+
		"\u0013\u0001\u0013\u0003\u0013\u012f\b\u0013\u0001\u0014\u0001\u0014\u0001"+
		"\u0014\u0001\u0014\u0003\u0014\u0135\b\u0014\u0001\u0015\u0001\u0015\u0001"+
		"\u0015\u0003\u0015\u013a\b\u0015\u0001\u0016\u0001\u0016\u0001\u0016\u0003"+
		"\u0016\u013f\b\u0016\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0001"+
		"\u0017\u0003\u0017\u0146\b\u0017\u0001\u0018\u0001\u0018\u0001\u0018\u0001"+
		"\u0018\u0005\u0018\u014c\b\u0018\n\u0018\f\u0018\u014f\t\u0018\u0001\u0018"+
		"\u0001\u0018\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019"+
		"\u0005\u0019\u0158\b\u0019\n\u0019\f\u0019\u015b\t\u0019\u0001\u0019\u0001"+
		"\u0019\u0001\u001a\u0001\u001a\u0001\u001b\u0001\u001b\u0001\u001c\u0001"+
		"\u001c\u0003\u001c\u0165\b\u001c\u0001\u001d\u0001\u001d\u0001\u001e\u0001"+
		"\u001e\u0001\u001f\u0001\u001f\u0001\u001f\u0001\u001f\u0001 \u0001 \u0003"+
		" \u0171\b \u0001 \u0001 \u0003 \u0175\b \u0001 \u0001 \u0001!\u0001!\u0001"+
		"!\u0001!\u0001!\u0001!\u0001!\u0003!\u0180\b!\u0001\"\u0001\"\u0001\""+
		"\u0005\"\u0185\b\"\n\"\f\"\u0188\t\"\u0001\"\u0000\u0000#\u0000\u0002"+
		"\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e"+
		" \"$&(*,.02468:<>@BD\u0000\u0002\u0001\u0000\u0006\t\u0001\u0000$&\u01a0"+
		"\u0000F\u0001\u0000\u0000\u0000\u0002f\u0001\u0000\u0000\u0000\u0004j"+
		"\u0001\u0000\u0000\u0000\u0006p\u0001\u0000\u0000\u0000\bw\u0001\u0000"+
		"\u0000\u0000\nz\u0001\u0000\u0000\u0000\f\u00a8\u0001\u0000\u0000\u0000"+
		"\u000e\u00ad\u0001\u0000\u0000\u0000\u0010\u00b2\u0001\u0000\u0000\u0000"+
		"\u0012\u00e3\u0001\u0000\u0000\u0000\u0014\u00e9\u0001\u0000\u0000\u0000"+
		"\u0016\u00eb\u0001\u0000\u0000\u0000\u0018\u00f0\u0001\u0000\u0000\u0000"+
		"\u001a\u00fd\u0001\u0000\u0000\u0000\u001c\u0109\u0001\u0000\u0000\u0000"+
		"\u001e\u010d\u0001\u0000\u0000\u0000 \u010f\u0001\u0000\u0000\u0000\""+
		"\u011d\u0001\u0000\u0000\u0000$\u0126\u0001\u0000\u0000\u0000&\u012e\u0001"+
		"\u0000\u0000\u0000(\u0130\u0001\u0000\u0000\u0000*\u0139\u0001\u0000\u0000"+
		"\u0000,\u013b\u0001\u0000\u0000\u0000.\u0145\u0001\u0000\u0000\u00000"+
		"\u0147\u0001\u0000\u0000\u00002\u0152\u0001\u0000\u0000\u00004\u015e\u0001"+
		"\u0000\u0000\u00006\u0160\u0001\u0000\u0000\u00008\u0164\u0001\u0000\u0000"+
		"\u0000:\u0166\u0001\u0000\u0000\u0000<\u0168\u0001\u0000\u0000\u0000>"+
		"\u016a\u0001\u0000\u0000\u0000@\u0170\u0001\u0000\u0000\u0000B\u017f\u0001"+
		"\u0000\u0000\u0000D\u0181\u0001\u0000\u0000\u0000FG\u0005\u0001\u0000"+
		"\u0000GH\u0005-\u0000\u0000HJ\u0005\u0002\u0000\u0000IK\u0003\u0002\u0001"+
		"\u0000JI\u0001\u0000\u0000\u0000KL\u0001\u0000\u0000\u0000LJ\u0001\u0000"+
		"\u0000\u0000LM\u0001\u0000\u0000\u0000MU\u0001\u0000\u0000\u0000NR\u0005"+
		"\u0003\u0000\u0000OQ\u0003\u0004\u0002\u0000PO\u0001\u0000\u0000\u0000"+
		"QT\u0001\u0000\u0000\u0000RP\u0001\u0000\u0000\u0000RS\u0001\u0000\u0000"+
		"\u0000SV\u0001\u0000\u0000\u0000TR\u0001\u0000\u0000\u0000UN\u0001\u0000"+
		"\u0000\u0000UV\u0001\u0000\u0000\u0000V^\u0001\u0000\u0000\u0000W[\u0005"+
		"\u0004\u0000\u0000XZ\u0003\u0006\u0003\u0000YX\u0001\u0000\u0000\u0000"+
		"Z]\u0001\u0000\u0000\u0000[Y\u0001\u0000\u0000\u0000[\\\u0001\u0000\u0000"+
		"\u0000\\_\u0001\u0000\u0000\u0000][\u0001\u0000\u0000\u0000^W\u0001\u0000"+
		"\u0000\u0000^_\u0001\u0000\u0000\u0000_b\u0001\u0000\u0000\u0000`c\u0003"+
		"\n\u0005\u0000ac\u0003\u0010\b\u0000b`\u0001\u0000\u0000\u0000ba\u0001"+
		"\u0000\u0000\u0000cd\u0001\u0000\u0000\u0000db\u0001\u0000\u0000\u0000"+
		"de\u0001\u0000\u0000\u0000e\u0001\u0001\u0000\u0000\u0000fg\u0003\b\u0004"+
		"\u0000gh\u0005-\u0000\u0000hi\u0003\u001c\u000e\u0000i\u0003\u0001\u0000"+
		"\u0000\u0000jk\u0003\b\u0004\u0000kl\u0005-\u0000\u0000lm\u0003\u001c"+
		"\u000e\u0000mn\u0005\u0005\u0000\u0000no\u0003$\u0012\u0000o\u0005\u0001"+
		"\u0000\u0000\u0000pq\u0003\b\u0004\u0000qr\u0005-\u0000\u0000ru\u0003"+
		"\u001c\u000e\u0000st\u0005\u0005\u0000\u0000tv\u0003$\u0012\u0000us\u0001"+
		"\u0000\u0000\u0000uv\u0001\u0000\u0000\u0000v\u0007\u0001\u0000\u0000"+
		"\u0000wx\u0007\u0000\u0000\u0000x\t\u0001\u0000\u0000\u0000y{\u0005\n"+
		"\u0000\u0000zy\u0001\u0000\u0000\u0000z{\u0001\u0000\u0000\u0000{|\u0001"+
		"\u0000\u0000\u0000|}\u0005\u000b\u0000\u0000}\u0080\u0005-\u0000\u0000"+
		"~\u007f\u0005\f\u0000\u0000\u007f\u0081\u0005-\u0000\u0000\u0080~\u0001"+
		"\u0000\u0000\u0000\u0080\u0081\u0001\u0000\u0000\u0000\u0081\u0082\u0001"+
		"\u0000\u0000\u0000\u0082\u0083\u0005\r\u0000\u0000\u0083\u0085\u0005\u000e"+
		"\u0000\u0000\u0084\u0086\u0003\f\u0006\u0000\u0085\u0084\u0001\u0000\u0000"+
		"\u0000\u0086\u0087\u0001\u0000\u0000\u0000\u0087\u0085\u0001\u0000\u0000"+
		"\u0000\u0087\u0088\u0001\u0000\u0000\u0000\u0088\u0090\u0001\u0000\u0000"+
		"\u0000\u0089\u008d\u0005\u0003\u0000\u0000\u008a\u008c\u0003\u0004\u0002"+
		"\u0000\u008b\u008a\u0001\u0000\u0000\u0000\u008c\u008f\u0001\u0000\u0000"+
		"\u0000\u008d\u008b\u0001\u0000\u0000\u0000\u008d\u008e\u0001\u0000\u0000"+
		"\u0000\u008e\u0091\u0001\u0000\u0000\u0000\u008f\u008d\u0001\u0000\u0000"+
		"\u0000\u0090\u0089\u0001\u0000\u0000\u0000\u0090\u0091\u0001\u0000\u0000"+
		"\u0000\u0091\u0099\u0001\u0000\u0000\u0000\u0092\u0096\u0005\u0004\u0000"+
		"\u0000\u0093\u0095\u0003\u0006\u0003\u0000\u0094\u0093\u0001\u0000\u0000"+
		"\u0000\u0095\u0098\u0001\u0000\u0000\u0000\u0096\u0094\u0001\u0000\u0000"+
		"\u0000\u0096\u0097\u0001\u0000\u0000\u0000\u0097\u009a\u0001\u0000\u0000"+
		"\u0000\u0098\u0096\u0001\u0000\u0000\u0000\u0099\u0092\u0001\u0000\u0000"+
		"\u0000\u0099\u009a\u0001\u0000\u0000\u0000\u009a\u009e\u0001\u0000\u0000"+
		"\u0000\u009b\u009d\u0003\u0014\n\u0000\u009c\u009b\u0001\u0000\u0000\u0000"+
		"\u009d\u00a0\u0001\u0000\u0000\u0000\u009e\u009c\u0001\u0000\u0000\u0000"+
		"\u009e\u009f\u0001\u0000\u0000\u0000\u009f\u00a2\u0001\u0000\u0000\u0000"+
		"\u00a0\u009e\u0001\u0000\u0000\u0000\u00a1\u00a3\u0003\u000e\u0007\u0000"+
		"\u00a2\u00a1\u0001\u0000\u0000\u0000\u00a3\u00a4\u0001\u0000\u0000\u0000"+
		"\u00a4\u00a2\u0001\u0000\u0000\u0000\u00a4\u00a5\u0001\u0000\u0000\u0000"+
		"\u00a5\u00a6\u0001\u0000\u0000\u0000\u00a6\u00a7\u0005\u000f\u0000\u0000"+
		"\u00a7\u000b\u0001\u0000\u0000\u0000\u00a8\u00ab\u0005-\u0000\u0000\u00a9"+
		"\u00aa\u0005\u0005\u0000\u0000\u00aa\u00ac\u0003$\u0012\u0000\u00ab\u00a9"+
		"\u0001\u0000\u0000\u0000\u00ab\u00ac\u0001\u0000\u0000\u0000\u00ac\r\u0001"+
		"\u0000\u0000\u0000\u00ad\u00ae\u0005\u0010\u0000\u0000\u00ae\u00af\u0005"+
		"-\u0000\u0000\u00af\u00b0\u0005\u0005\u0000\u0000\u00b0\u00b1\u0003$\u0012"+
		"\u0000\u00b1\u000f\u0001\u0000\u0000\u0000\u00b2\u00d4\u0005\u0011\u0000"+
		"\u0000\u00b3\u00be\u0005-\u0000\u0000\u00b4\u00b5\u0005\u0012\u0000\u0000"+
		"\u00b5\u00ba\u0005-\u0000\u0000\u00b6\u00b7\u0005\u0013\u0000\u0000\u00b7"+
		"\u00b9\u0005-\u0000\u0000\u00b8\u00b6\u0001\u0000\u0000\u0000\u00b9\u00bc"+
		"\u0001\u0000\u0000\u0000\u00ba\u00b8\u0001\u0000\u0000\u0000\u00ba\u00bb"+
		"\u0001\u0000\u0000\u0000\u00bb\u00bd\u0001\u0000\u0000\u0000\u00bc\u00ba"+
		"\u0001\u0000\u0000\u0000\u00bd\u00bf\u0005\u0014\u0000\u0000\u00be\u00b4"+
		"\u0001\u0000\u0000\u0000\u00be\u00bf\u0001\u0000\u0000\u0000\u00bf\u00c0"+
		"\u0001\u0000\u0000\u0000\u00c0\u00c1\u0005\u0015\u0000\u0000\u00c1\u00c2"+
		"\u0005-\u0000\u0000\u00c2\u00c3\u0005\u0016\u0000\u0000\u00c3\u00d5\u0005"+
		"-\u0000\u0000\u00c4\u00c5\u0005-\u0000\u0000\u00c5\u00c6\u0005\u0016\u0000"+
		"\u0000\u00c6\u00c7\u0005-\u0000\u0000\u00c7\u00d2\u0005-\u0000\u0000\u00c8"+
		"\u00c9\u0005\u0012\u0000\u0000\u00c9\u00ce\u0005-\u0000\u0000\u00ca\u00cb"+
		"\u0005\u0013\u0000\u0000\u00cb\u00cd\u0005-\u0000\u0000\u00cc\u00ca\u0001"+
		"\u0000\u0000\u0000\u00cd\u00d0\u0001\u0000\u0000\u0000\u00ce\u00cc\u0001"+
		"\u0000\u0000\u0000\u00ce\u00cf\u0001\u0000\u0000\u0000\u00cf\u00d1\u0001"+
		"\u0000\u0000\u0000\u00d0\u00ce\u0001\u0000\u0000\u0000\u00d1\u00d3\u0005"+
		"\u0014\u0000\u0000\u00d2\u00c8\u0001\u0000\u0000\u0000\u00d2\u00d3\u0001"+
		"\u0000\u0000\u0000\u00d3\u00d5\u0001\u0000\u0000\u0000\u00d4\u00b3\u0001"+
		"\u0000\u0000\u0000\u00d4\u00c4\u0001\u0000\u0000\u0000\u00d5\u00e1\u0001"+
		"\u0000\u0000\u0000\u00d6\u00d7\u0005\u0005\u0000\u0000\u00d7\u00e2\u0003"+
		"$\u0012\u0000\u00d8\u00dd\u0005\r\u0000\u0000\u00d9\u00dc\u0003\u0012"+
		"\t\u0000\u00da\u00dc\u0003\u0014\n\u0000\u00db\u00d9\u0001\u0000\u0000"+
		"\u0000\u00db\u00da\u0001\u0000\u0000\u0000\u00dc\u00df\u0001\u0000\u0000"+
		"\u0000\u00dd\u00db\u0001\u0000\u0000\u0000\u00dd\u00de\u0001\u0000\u0000"+
		"\u0000\u00de\u00e0\u0001\u0000\u0000\u0000\u00df\u00dd\u0001\u0000\u0000"+
		"\u0000\u00e0\u00e2\u0005\u000f\u0000\u0000\u00e1\u00d6\u0001\u0000\u0000"+
		"\u0000\u00e1\u00d8\u0001\u0000\u0000\u0000\u00e2\u0011\u0001\u0000\u0000"+
		"\u0000\u00e3\u00e4\u0005-\u0000\u0000\u00e4\u00e5\u0005\u0005\u0000\u0000"+
		"\u00e5\u00e6\u0003$\u0012\u0000\u00e6\u0013\u0001\u0000\u0000\u0000\u00e7"+
		"\u00ea\u0003\u0016\u000b\u0000\u00e8\u00ea\u0003\u0018\f\u0000\u00e9\u00e7"+
		"\u0001\u0000\u0000\u0000\u00e9\u00e8\u0001\u0000\u0000\u0000\u00ea\u0015"+
		"\u0001\u0000\u0000\u0000\u00eb\u00ec\u0005\u0017\u0000\u0000\u00ec\u00ed"+
		"\u0005-\u0000\u0000\u00ed\u00ee\u0005\u0005\u0000\u0000\u00ee\u00ef\u0003"+
		"$\u0012\u0000\u00ef\u0017\u0001\u0000\u0000\u0000\u00f0\u00f1\u0005\u0018"+
		"\u0000\u0000\u00f1\u00f2\u0005-\u0000\u0000\u00f2\u00f3\u0005\u0019\u0000"+
		"\u0000\u00f3\u00f4\u0003$\u0012\u0000\u00f4\u00f8\u0005\r\u0000\u0000"+
		"\u00f5\u00f7\u0003\u001a\r\u0000\u00f6\u00f5\u0001\u0000\u0000\u0000\u00f7"+
		"\u00fa\u0001\u0000\u0000\u0000\u00f8\u00f6\u0001\u0000\u0000\u0000\u00f8"+
		"\u00f9\u0001\u0000\u0000\u0000\u00f9\u00fb\u0001\u0000\u0000\u0000\u00fa"+
		"\u00f8\u0001\u0000\u0000\u0000\u00fb\u00fc\u0005\u000f\u0000\u0000\u00fc"+
		"\u0019\u0001\u0000\u0000\u0000\u00fd\u00fe\u0005\u001a\u0000\u0000\u00fe"+
		"\u00ff\u00036\u001b\u0000\u00ff\u0100\u0005\u0019\u0000\u0000\u0100\u0101"+
		"\u0003$\u0012\u0000\u0101\u001b\u0001\u0000\u0000\u0000\u0102\u0104\u0005"+
		"\u0019\u0000\u0000\u0103\u0105\u0003\u001e\u000f\u0000\u0104\u0103\u0001"+
		"\u0000\u0000\u0000\u0105\u0106\u0001\u0000\u0000\u0000\u0106\u0104\u0001"+
		"\u0000\u0000\u0000\u0106\u0107\u0001\u0000\u0000\u0000\u0107\u010a\u0001"+
		"\u0000\u0000\u0000\u0108\u010a\u0005\u001b\u0000\u0000\u0109\u0102\u0001"+
		"\u0000\u0000\u0000\u0109\u0108\u0001\u0000\u0000\u0000\u010a\u001d\u0001"+
		"\u0000\u0000\u0000\u010b\u010e\u0003\"\u0011\u0000\u010c\u010e\u0003 "+
		"\u0010\u0000\u010d\u010b\u0001\u0000\u0000\u0000\u010d\u010c\u0001\u0000"+
		"\u0000\u0000\u010e\u001f\u0001\u0000\u0000\u0000\u010f\u0113\u0005\u0012"+
		"\u0000\u0000\u0110\u0112\u0003\u001e\u000f\u0000\u0111\u0110\u0001\u0000"+
		"\u0000\u0000\u0112\u0115\u0001\u0000\u0000\u0000\u0113\u0111\u0001\u0000"+
		"\u0000\u0000\u0113\u0114\u0001\u0000\u0000\u0000\u0114\u0116\u0001\u0000"+
		"\u0000\u0000\u0115\u0113\u0001\u0000\u0000\u0000\u0116\u0119\u0005\u0014"+
		"\u0000\u0000\u0117\u0118\u0005\u001c\u0000\u0000\u0118\u011a\u0005)\u0000"+
		"\u0000\u0119\u0117\u0001\u0000\u0000\u0000\u0119\u011a\u0001\u0000\u0000"+
		"\u0000\u011a!\u0001\u0000\u0000\u0000\u011b\u011e\u0005+\u0000\u0000\u011c"+
		"\u011e\u0005*\u0000\u0000\u011d\u011b\u0001\u0000\u0000\u0000\u011d\u011c"+
		"\u0001\u0000\u0000\u0000\u011e\u0120\u0001\u0000\u0000\u0000\u011f\u0121"+
		"\u0005-\u0000\u0000\u0120\u011f\u0001\u0000\u0000\u0000\u0120\u0121\u0001"+
		"\u0000\u0000\u0000\u0121\u0124\u0001\u0000\u0000\u0000\u0122\u0123\u0005"+
		"\u001c\u0000\u0000\u0123\u0125\u0005)\u0000\u0000\u0124\u0122\u0001\u0000"+
		"\u0000\u0000\u0124\u0125\u0001\u0000\u0000\u0000\u0125#\u0001\u0000\u0000"+
		"\u0000\u0126\u012a\u0003(\u0014\u0000\u0127\u0128\u0003&\u0013\u0000\u0128"+
		"\u0129\u0003$\u0012\u0000\u0129\u012b\u0001\u0000\u0000\u0000\u012a\u0127"+
		"\u0001\u0000\u0000\u0000\u012a\u012b\u0001\u0000\u0000\u0000\u012b%\u0001"+
		"\u0000\u0000\u0000\u012c\u012f\u0005\u001d\u0000\u0000\u012d\u012f\u0005"+
		"\u001e\u0000\u0000\u012e\u012c\u0001\u0000\u0000\u0000\u012e\u012d\u0001"+
		"\u0000\u0000\u0000\u012f\'\u0001\u0000\u0000\u0000\u0130\u0134\u0003,"+
		"\u0016\u0000\u0131\u0132\u0003*\u0015\u0000\u0132\u0133\u0003(\u0014\u0000"+
		"\u0133\u0135\u0001\u0000\u0000\u0000\u0134\u0131\u0001\u0000\u0000\u0000"+
		"\u0134\u0135\u0001\u0000\u0000\u0000\u0135)\u0001\u0000\u0000\u0000\u0136"+
		"\u013a\u0005\u001f\u0000\u0000\u0137\u013a\u0005 \u0000\u0000\u0138\u013a"+
		"\u0005!\u0000\u0000\u0139\u0136\u0001\u0000\u0000\u0000\u0139\u0137\u0001"+
		"\u0000\u0000\u0000\u0139\u0138\u0001\u0000\u0000\u0000\u013a+\u0001\u0000"+
		"\u0000\u0000\u013b\u013e\u0003.\u0017\u0000\u013c\u013d\u0005\u001c\u0000"+
		"\u0000\u013d\u013f\u0003.\u0017\u0000\u013e\u013c\u0001\u0000\u0000\u0000"+
		"\u013e\u013f\u0001\u0000\u0000\u0000\u013f-\u0001\u0000\u0000\u0000\u0140"+
		"\u0146\u00030\u0018\u0000\u0141\u0146\u00032\u0019\u0000\u0142\u0146\u0003"+
		"6\u001b\u0000\u0143\u0146\u0003>\u001f\u0000\u0144\u0146\u0003@ \u0000"+
		"\u0145\u0140\u0001\u0000\u0000\u0000\u0145\u0141\u0001\u0000\u0000\u0000"+
		"\u0145\u0142\u0001\u0000\u0000\u0000\u0145\u0143\u0001\u0000\u0000\u0000"+
		"\u0145\u0144\u0001\u0000\u0000\u0000\u0146/\u0001\u0000\u0000\u0000\u0147"+
		"\u0148\u0005\"\u0000\u0000\u0148\u014d\u0003$\u0012\u0000\u0149\u014a"+
		"\u0005\u0013\u0000\u0000\u014a\u014c\u0003$\u0012\u0000\u014b\u0149\u0001"+
		"\u0000\u0000\u0000\u014c\u014f\u0001\u0000\u0000\u0000\u014d\u014b\u0001"+
		"\u0000\u0000\u0000\u014d\u014e\u0001\u0000\u0000\u0000\u014e\u0150\u0001"+
		"\u0000\u0000\u0000\u014f\u014d\u0001\u0000\u0000\u0000\u0150\u0151\u0005"+
		"#\u0000\u0000\u01511\u0001\u0000\u0000\u0000\u0152\u0153\u00034\u001a"+
		"\u0000\u0153\u0154\u0005\u0012\u0000\u0000\u0154\u0159\u0003$\u0012\u0000"+
		"\u0155\u0156\u0005\u0013\u0000\u0000\u0156\u0158\u0003$\u0012\u0000\u0157"+
		"\u0155\u0001\u0000\u0000\u0000\u0158\u015b\u0001\u0000\u0000\u0000\u0159"+
		"\u0157\u0001\u0000\u0000\u0000\u0159\u015a\u0001\u0000\u0000\u0000\u015a"+
		"\u015c\u0001\u0000\u0000\u0000\u015b\u0159\u0001\u0000\u0000\u0000\u015c"+
		"\u015d\u0005\u0014\u0000\u0000\u015d3\u0001\u0000\u0000\u0000\u015e\u015f"+
		"\u0007\u0001\u0000\u0000\u015f5\u0001\u0000\u0000\u0000\u0160\u0161\u0003"+
		"8\u001c\u0000\u01617\u0001\u0000\u0000\u0000\u0162\u0165\u0003:\u001d"+
		"\u0000\u0163\u0165\u0003<\u001e\u0000\u0164\u0162\u0001\u0000\u0000\u0000"+
		"\u0164\u0163\u0001\u0000\u0000\u0000\u01659\u0001\u0000\u0000\u0000\u0166"+
		"\u0167\u0005)\u0000\u0000\u0167;\u0001\u0000\u0000\u0000\u0168\u0169\u0005"+
		"\t\u0000\u0000\u0169=\u0001\u0000\u0000\u0000\u016a\u016b\u0005\u0012"+
		"\u0000\u0000\u016b\u016c\u0003$\u0012\u0000\u016c\u016d\u0005\u0014\u0000"+
		"\u0000\u016d?\u0001\u0000\u0000\u0000\u016e\u016f\u0005-\u0000\u0000\u016f"+
		"\u0171\u0005\'\u0000\u0000\u0170\u016e\u0001\u0000\u0000\u0000\u0170\u0171"+
		"\u0001\u0000\u0000\u0000\u0171\u0174\u0001\u0000\u0000\u0000\u0172\u0173"+
		"\u0005-\u0000\u0000\u0173\u0175\u0005\u0019\u0000\u0000\u0174\u0172\u0001"+
		"\u0000\u0000\u0000\u0174\u0175\u0001\u0000\u0000\u0000\u0175\u0176\u0001"+
		"\u0000\u0000\u0000\u0176\u0177\u0003D\"\u0000\u0177A\u0001\u0000\u0000"+
		"\u0000\u0178\u0180\u0003\u000e\u0007\u0000\u0179\u0180\u0003\u0010\b\u0000"+
		"\u017a\u0180\u0003\u0004\u0002\u0000\u017b\u0180\u0003\u0014\n\u0000\u017c"+
		"\u0180\u0003\u0006\u0003\u0000\u017d\u0180\u0003\u0012\t\u0000\u017e\u0180"+
		"\u0003\f\u0006\u0000\u017f\u0178\u0001\u0000\u0000\u0000\u017f\u0179\u0001"+
		"\u0000\u0000\u0000\u017f\u017a\u0001\u0000\u0000\u0000\u017f\u017b\u0001"+
		"\u0000\u0000\u0000\u017f\u017c\u0001\u0000\u0000\u0000\u017f\u017d\u0001"+
		"\u0000\u0000\u0000\u017f\u017e\u0001\u0000\u0000\u0000\u0180C\u0001\u0000"+
		"\u0000\u0000\u0181\u0186\u0005-\u0000\u0000\u0182\u0183\u0005(\u0000\u0000"+
		"\u0183\u0185\u0005-\u0000\u0000\u0184\u0182\u0001\u0000\u0000\u0000\u0185"+
		"\u0188\u0001\u0000\u0000\u0000\u0186\u0184\u0001\u0000\u0000\u0000\u0186"+
		"\u0187\u0001\u0000\u0000\u0000\u0187E\u0001\u0000\u0000\u0000\u0188\u0186"+
		"\u0001\u0000\u0000\u00001LRU[^bduz\u0080\u0087\u008d\u0090\u0096\u0099"+
		"\u009e\u00a4\u00ab\u00ba\u00be\u00ce\u00d2\u00d4\u00db\u00dd\u00e1\u00e9"+
		"\u00f8\u0106\u0109\u010d\u0113\u0119\u011d\u0120\u0124\u012a\u012e\u0134"+
		"\u0139\u013e\u0145\u014d\u0159\u0164\u0170\u0174\u017f\u0186";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}