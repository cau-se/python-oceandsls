// Generated from Declaration.g4 by ANTLR 4.13.1
package Declaration;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class DeclarationParser extends Parser {
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
		T__38=39, T__39=40, T__40=41, T__41=42, T__42=43, T__43=44, T__44=45, 
		T__45=46, T__46=47, T__47=48, T__48=49, T__49=50, T__50=51, T__51=52, 
		T__52=53, T__53=54, T__54=55, T__55=56, T__56=57, T__57=58, T__58=59, 
		T__59=60, ELONG=61, EDOUBLE=62, EBoolean=63, ID=64, INT=65, STRING=66, 
		WS=67, ML_COMMENT=68, SL_COMMENT=69, ANY_OTHER=70;
	public static final int
		RULE_declarationModel = 0, RULE_namedElement = 1, RULE_parameterGroupDeclaration = 2, 
		RULE_parameterDeclaration = 3, RULE_featureDeclaration = 4, RULE_featureGroupDeclaration = 5, 
		RULE_eKind = 6, RULE_paramType = 7, RULE_inlineEnumerationType = 8, RULE_typeReference = 9, 
		RULE_arrayType = 10, RULE_dimension = 11, RULE_sizeDimension = 12, RULE_rangeDimension = 13, 
		RULE_declaredType = 14, RULE_rangeType = 15, RULE_enumerationType = 16, 
		RULE_enumeral = 17, RULE_unitSpecification = 18, RULE_basicUnit = 19, 
		RULE_sIUnit = 20, RULE_customUnit = 21, RULE_composedUnit = 22, RULE_ePrefix = 23, 
		RULE_eSIUnitType = 24, RULE_arithmeticExpression = 25, RULE_eAdditionOperator = 26, 
		RULE_multiplicationExpression = 27, RULE_eMultiplicationOperator = 28, 
		RULE_valueExpression = 29, RULE_literalExpression = 30, RULE_literal = 31, 
		RULE_parenthesisExpression = 32, RULE_arrayExpression = 33, RULE_namedElementReference = 34, 
		RULE_stringValue = 35, RULE_longValue = 36, RULE_doubleValue = 37, RULE_booleanValue = 38;
	private static String[] makeRuleNames() {
		return new String[] {
			"declarationModel", "namedElement", "parameterGroupDeclaration", "parameterDeclaration", 
			"featureDeclaration", "featureGroupDeclaration", "eKind", "paramType", 
			"inlineEnumerationType", "typeReference", "arrayType", "dimension", "sizeDimension", 
			"rangeDimension", "declaredType", "rangeType", "enumerationType", "enumeral", 
			"unitSpecification", "basicUnit", "sIUnit", "customUnit", "composedUnit", 
			"ePrefix", "eSIUnitType", "arithmeticExpression", "eAdditionOperator", 
			"multiplicationExpression", "eMultiplicationOperator", "valueExpression", 
			"literalExpression", "literal", "parenthesisExpression", "arrayExpression", 
			"namedElementReference", "stringValue", "longValue", "doubleValue", "booleanValue"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'model'", "'types'", "'group'", "':'", "'{'", "'}'", "'def'", 
			"','", "'='", "'required'", "'feature'", "'requires'", "'excludes'", 
			"'sub'", "'alternative'", "'multiple'", "'('", "')'", "'['", "']'", "'range'", 
			"'enum'", "'*'", "'/'", "'**'", "'noP'", "'yotta'", "'zetta'", "'exa'", 
			"'peta'", "'tera'", "'giga'", "'mega'", "'kilo'", "'hecto'", "'deca'", 
			"'deci'", "'centi'", "'mili'", "'micro'", "'nano'", "'pico'", "'femto'", 
			"'atto'", "'zepto'", "'yocto'", "'meter'", "'gram'", "'ton'", "'second'", 
			"'ampere'", "'kelvin'", "'mole'", "'candela'", "'pascal'", "'Joule'", 
			"'+'", "'-'", "'%'", "'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, "ELONG", "EDOUBLE", "EBoolean", "ID", "INT", "STRING", "WS", "ML_COMMENT", 
			"SL_COMMENT", "ANY_OTHER"
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
	public String getGrammarFileName() { return "Declaration.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public DeclarationParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DeclarationModelContext extends ParserRuleContext {
		public Token name;
		public DeclaredTypeContext declaredType;
		public List<DeclaredTypeContext> types = new ArrayList<DeclaredTypeContext>();
		public ParameterGroupDeclarationContext parameterGroupDeclaration;
		public List<ParameterGroupDeclarationContext> parameterGroupDeclarations = new ArrayList<ParameterGroupDeclarationContext>();
		public FeatureDeclarationContext featureDeclaration;
		public List<FeatureDeclarationContext> featureDeclarations = new ArrayList<FeatureDeclarationContext>();
		public TerminalNode ID() { return getToken(DeclarationParser.ID, 0); }
		public List<ParameterGroupDeclarationContext> parameterGroupDeclaration() {
			return getRuleContexts(ParameterGroupDeclarationContext.class);
		}
		public ParameterGroupDeclarationContext parameterGroupDeclaration(int i) {
			return getRuleContext(ParameterGroupDeclarationContext.class,i);
		}
		public List<FeatureDeclarationContext> featureDeclaration() {
			return getRuleContexts(FeatureDeclarationContext.class);
		}
		public FeatureDeclarationContext featureDeclaration(int i) {
			return getRuleContext(FeatureDeclarationContext.class,i);
		}
		public List<DeclaredTypeContext> declaredType() {
			return getRuleContexts(DeclaredTypeContext.class);
		}
		public DeclaredTypeContext declaredType(int i) {
			return getRuleContext(DeclaredTypeContext.class,i);
		}
		public DeclarationModelContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_declarationModel; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterDeclarationModel(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitDeclarationModel(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitDeclarationModel(this);
			else return visitor.visitChildren(this);
		}
	}

	public final DeclarationModelContext declarationModel() throws RecognitionException {
		DeclarationModelContext _localctx = new DeclarationModelContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_declarationModel);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(78);
			match(T__0);
			setState(79);
			((DeclarationModelContext)_localctx).name = match(ID);
			setState(87);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__1) {
				{
				setState(80);
				match(T__1);
				setState(84);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__20 || _la==T__21) {
					{
					{
					setState(81);
					((DeclarationModelContext)_localctx).declaredType = declaredType();
					((DeclarationModelContext)_localctx).types.add(((DeclarationModelContext)_localctx).declaredType);
					}
					}
					setState(86);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(93);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 3080L) != 0)) {
				{
				setState(91);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__2:
					{
					setState(89);
					((DeclarationModelContext)_localctx).parameterGroupDeclaration = parameterGroupDeclaration();
					((DeclarationModelContext)_localctx).parameterGroupDeclarations.add(((DeclarationModelContext)_localctx).parameterGroupDeclaration);
					}
					break;
				case T__9:
				case T__10:
					{
					setState(90);
					((DeclarationModelContext)_localctx).featureDeclaration = featureDeclaration();
					((DeclarationModelContext)_localctx).featureDeclarations.add(((DeclarationModelContext)_localctx).featureDeclaration);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(95);
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

	@SuppressWarnings("CheckReturnValue")
	public static class NamedElementContext extends ParserRuleContext {
		public ParameterDeclarationContext parameterDeclaration() {
			return getRuleContext(ParameterDeclarationContext.class,0);
		}
		public ParameterGroupDeclarationContext parameterGroupDeclaration() {
			return getRuleContext(ParameterGroupDeclarationContext.class,0);
		}
		public FeatureDeclarationContext featureDeclaration() {
			return getRuleContext(FeatureDeclarationContext.class,0);
		}
		public NamedElementContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namedElement; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterNamedElement(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitNamedElement(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitNamedElement(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NamedElementContext namedElement() throws RecognitionException {
		NamedElementContext _localctx = new NamedElementContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_namedElement);
		try {
			setState(99);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__6:
				enterOuterAlt(_localctx, 1);
				{
				setState(96);
				parameterDeclaration();
				}
				break;
			case T__2:
				enterOuterAlt(_localctx, 2);
				{
				setState(97);
				parameterGroupDeclaration();
				}
				break;
			case T__9:
			case T__10:
				enterOuterAlt(_localctx, 3);
				{
				setState(98);
				featureDeclaration();
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
	public static class ParameterGroupDeclarationContext extends ParserRuleContext {
		public ParameterGroupDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parameterGroupDeclaration; }
	 
		public ParameterGroupDeclarationContext() { }
		public void copyFrom(ParameterGroupDeclarationContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParamGroupAssignStatContext extends ParameterGroupDeclarationContext {
		public Token name;
		public Token description;
		public ParameterDeclarationContext parameterDeclaration;
		public List<ParameterDeclarationContext> parameterDeclarations = new ArrayList<ParameterDeclarationContext>();
		public TerminalNode ID() { return getToken(DeclarationParser.ID, 0); }
		public TerminalNode STRING() { return getToken(DeclarationParser.STRING, 0); }
		public List<ParameterDeclarationContext> parameterDeclaration() {
			return getRuleContexts(ParameterDeclarationContext.class);
		}
		public ParameterDeclarationContext parameterDeclaration(int i) {
			return getRuleContext(ParameterDeclarationContext.class,i);
		}
		public ParamGroupAssignStatContext(ParameterGroupDeclarationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterParamGroupAssignStat(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitParamGroupAssignStat(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitParamGroupAssignStat(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParameterGroupDeclarationContext parameterGroupDeclaration() throws RecognitionException {
		ParameterGroupDeclarationContext _localctx = new ParameterGroupDeclarationContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_parameterGroupDeclaration);
		int _la;
		try {
			_localctx = new ParamGroupAssignStatContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(101);
			match(T__2);
			setState(102);
			((ParamGroupAssignStatContext)_localctx).name = match(ID);
			setState(103);
			match(T__3);
			setState(104);
			((ParamGroupAssignStatContext)_localctx).description = match(STRING);
			setState(105);
			match(T__4);
			setState(109);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__6) {
				{
				{
				setState(106);
				((ParamGroupAssignStatContext)_localctx).parameterDeclaration = parameterDeclaration();
				((ParamGroupAssignStatContext)_localctx).parameterDeclarations.add(((ParamGroupAssignStatContext)_localctx).parameterDeclaration);
				}
				}
				setState(111);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(112);
			match(T__5);
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
		public ParameterDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parameterDeclaration; }
	 
		public ParameterDeclarationContext() { }
		public void copyFrom(ParameterDeclarationContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParamAssignStatContext extends ParameterDeclarationContext {
		public Token name;
		public ParamTypeContext type;
		public UnitSpecificationContext unit;
		public Token description;
		public ArithmeticExpressionContext defaultValue;
		public TerminalNode ID() { return getToken(DeclarationParser.ID, 0); }
		public ParamTypeContext paramType() {
			return getRuleContext(ParamTypeContext.class,0);
		}
		public UnitSpecificationContext unitSpecification() {
			return getRuleContext(UnitSpecificationContext.class,0);
		}
		public TerminalNode STRING() { return getToken(DeclarationParser.STRING, 0); }
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public ParamAssignStatContext(ParameterDeclarationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterParamAssignStat(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitParamAssignStat(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitParamAssignStat(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParameterDeclarationContext parameterDeclaration() throws RecognitionException {
		ParameterDeclarationContext _localctx = new ParameterDeclarationContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_parameterDeclaration);
		int _la;
		try {
			_localctx = new ParamAssignStatContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(114);
			match(T__6);
			setState(115);
			((ParamAssignStatContext)_localctx).name = match(ID);
			setState(116);
			((ParamAssignStatContext)_localctx).type = paramType();
			setState(117);
			match(T__3);
			setState(118);
			((ParamAssignStatContext)_localctx).unit = unitSpecification();
			setState(121);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__7) {
				{
				setState(119);
				match(T__7);
				setState(120);
				((ParamAssignStatContext)_localctx).description = match(STRING);
				}
			}

			setState(125);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__8) {
				{
				setState(123);
				match(T__8);
				setState(124);
				((ParamAssignStatContext)_localctx).defaultValue = arithmeticExpression();
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
	public static class FeatureDeclarationContext extends ParserRuleContext {
		public FeatureDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_featureDeclaration; }
	 
		public FeatureDeclarationContext() { }
		public void copyFrom(FeatureDeclarationContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FeatureAssignStatContext extends FeatureDeclarationContext {
		public Token required;
		public Token name;
		public Token description;
		public Token ID;
		public List<Token> requires = new ArrayList<Token>();
		public List<Token> excludes = new ArrayList<Token>();
		public ParameterGroupDeclarationContext parameterGroupDeclaration;
		public List<ParameterGroupDeclarationContext> parameterGroupDeclarations = new ArrayList<ParameterGroupDeclarationContext>();
		public FeatureGroupDeclarationContext featureGroupDeclaration;
		public List<FeatureGroupDeclarationContext> featureGroupDeclarations = new ArrayList<FeatureGroupDeclarationContext>();
		public List<TerminalNode> ID() { return getTokens(DeclarationParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(DeclarationParser.ID, i);
		}
		public TerminalNode STRING() { return getToken(DeclarationParser.STRING, 0); }
		public List<ParameterGroupDeclarationContext> parameterGroupDeclaration() {
			return getRuleContexts(ParameterGroupDeclarationContext.class);
		}
		public ParameterGroupDeclarationContext parameterGroupDeclaration(int i) {
			return getRuleContext(ParameterGroupDeclarationContext.class,i);
		}
		public List<FeatureGroupDeclarationContext> featureGroupDeclaration() {
			return getRuleContexts(FeatureGroupDeclarationContext.class);
		}
		public FeatureGroupDeclarationContext featureGroupDeclaration(int i) {
			return getRuleContext(FeatureGroupDeclarationContext.class,i);
		}
		public FeatureAssignStatContext(FeatureDeclarationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterFeatureAssignStat(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitFeatureAssignStat(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitFeatureAssignStat(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FeatureDeclarationContext featureDeclaration() throws RecognitionException {
		FeatureDeclarationContext _localctx = new FeatureDeclarationContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_featureDeclaration);
		int _la;
		try {
			_localctx = new FeatureAssignStatContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(128);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__9) {
				{
				setState(127);
				((FeatureAssignStatContext)_localctx).required = match(T__9);
				}
			}

			setState(130);
			match(T__10);
			setState(131);
			((FeatureAssignStatContext)_localctx).name = match(ID);
			setState(132);
			match(T__3);
			setState(133);
			((FeatureAssignStatContext)_localctx).description = match(STRING);
			setState(157);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__4) {
				{
				setState(134);
				match(T__4);
				setState(139);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__11) {
					{
					{
					setState(135);
					match(T__11);
					setState(136);
					((FeatureAssignStatContext)_localctx).ID = match(ID);
					((FeatureAssignStatContext)_localctx).requires.add(((FeatureAssignStatContext)_localctx).ID);
					}
					}
					setState(141);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(146);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__12) {
					{
					{
					setState(142);
					match(T__12);
					setState(143);
					((FeatureAssignStatContext)_localctx).ID = match(ID);
					((FeatureAssignStatContext)_localctx).excludes.add(((FeatureAssignStatContext)_localctx).ID);
					}
					}
					setState(148);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(153);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__2 || _la==T__13) {
					{
					setState(151);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case T__2:
						{
						setState(149);
						((FeatureAssignStatContext)_localctx).parameterGroupDeclaration = parameterGroupDeclaration();
						((FeatureAssignStatContext)_localctx).parameterGroupDeclarations.add(((FeatureAssignStatContext)_localctx).parameterGroupDeclaration);
						}
						break;
					case T__13:
						{
						setState(150);
						((FeatureAssignStatContext)_localctx).featureGroupDeclaration = featureGroupDeclaration();
						((FeatureAssignStatContext)_localctx).featureGroupDeclarations.add(((FeatureAssignStatContext)_localctx).featureGroupDeclaration);
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					}
					setState(155);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(156);
				match(T__5);
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
	public static class FeatureGroupDeclarationContext extends ParserRuleContext {
		public FeatureGroupDeclarationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_featureGroupDeclaration; }
	 
		public FeatureGroupDeclarationContext() { }
		public void copyFrom(FeatureGroupDeclarationContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class FeatureGroupAssignStatContext extends FeatureGroupDeclarationContext {
		public EKindContext kind;
		public FeatureDeclarationContext featureDeclaration;
		public List<FeatureDeclarationContext> featureDeclarations = new ArrayList<FeatureDeclarationContext>();
		public EKindContext eKind() {
			return getRuleContext(EKindContext.class,0);
		}
		public List<FeatureDeclarationContext> featureDeclaration() {
			return getRuleContexts(FeatureDeclarationContext.class);
		}
		public FeatureDeclarationContext featureDeclaration(int i) {
			return getRuleContext(FeatureDeclarationContext.class,i);
		}
		public FeatureGroupAssignStatContext(FeatureGroupDeclarationContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterFeatureGroupAssignStat(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitFeatureGroupAssignStat(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitFeatureGroupAssignStat(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FeatureGroupDeclarationContext featureGroupDeclaration() throws RecognitionException {
		FeatureGroupDeclarationContext _localctx = new FeatureGroupDeclarationContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_featureGroupDeclaration);
		int _la;
		try {
			_localctx = new FeatureGroupAssignStatContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(159);
			match(T__13);
			setState(160);
			((FeatureGroupAssignStatContext)_localctx).kind = eKind();
			setState(164);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__9 || _la==T__10) {
				{
				{
				setState(161);
				((FeatureGroupAssignStatContext)_localctx).featureDeclaration = featureDeclaration();
				((FeatureGroupAssignStatContext)_localctx).featureDeclarations.add(((FeatureGroupAssignStatContext)_localctx).featureDeclaration);
				}
				}
				setState(166);
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

	@SuppressWarnings("CheckReturnValue")
	public static class EKindContext extends ParserRuleContext {
		public Token alternative;
		public Token multiple;
		public EKindContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_eKind; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterEKind(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitEKind(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitEKind(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EKindContext eKind() throws RecognitionException {
		EKindContext _localctx = new EKindContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_eKind);
		try {
			setState(169);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__14:
				enterOuterAlt(_localctx, 1);
				{
				setState(167);
				((EKindContext)_localctx).alternative = match(T__14);
				}
				break;
			case T__15:
				enterOuterAlt(_localctx, 2);
				{
				setState(168);
				((EKindContext)_localctx).multiple = match(T__15);
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
	public static class ParamTypeContext extends ParserRuleContext {
		public TypeReferenceContext typeReference() {
			return getRuleContext(TypeReferenceContext.class,0);
		}
		public InlineEnumerationTypeContext inlineEnumerationType() {
			return getRuleContext(InlineEnumerationTypeContext.class,0);
		}
		public ArrayTypeContext arrayType() {
			return getRuleContext(ArrayTypeContext.class,0);
		}
		public ParamTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_paramType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterParamType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitParamType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitParamType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParamTypeContext paramType() throws RecognitionException {
		ParamTypeContext _localctx = new ParamTypeContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_paramType);
		try {
			setState(174);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,16,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(171);
				typeReference();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(172);
				inlineEnumerationType();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(173);
				arrayType();
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
	public static class InlineEnumerationTypeContext extends ParserRuleContext {
		public EnumeralContext enumeral;
		public List<EnumeralContext> values = new ArrayList<EnumeralContext>();
		public List<EnumeralContext> enumeral() {
			return getRuleContexts(EnumeralContext.class);
		}
		public EnumeralContext enumeral(int i) {
			return getRuleContext(EnumeralContext.class,i);
		}
		public InlineEnumerationTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_inlineEnumerationType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterInlineEnumerationType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitInlineEnumerationType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitInlineEnumerationType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final InlineEnumerationTypeContext inlineEnumerationType() throws RecognitionException {
		InlineEnumerationTypeContext _localctx = new InlineEnumerationTypeContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_inlineEnumerationType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(176);
			match(T__16);
			setState(177);
			((InlineEnumerationTypeContext)_localctx).enumeral = enumeral();
			((InlineEnumerationTypeContext)_localctx).values.add(((InlineEnumerationTypeContext)_localctx).enumeral);
			setState(182);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__7) {
				{
				{
				setState(178);
				match(T__7);
				setState(179);
				((InlineEnumerationTypeContext)_localctx).enumeral = enumeral();
				((InlineEnumerationTypeContext)_localctx).values.add(((InlineEnumerationTypeContext)_localctx).enumeral);
				}
				}
				setState(184);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(185);
			match(T__17);
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
	public static class TypeReferenceContext extends ParserRuleContext {
		public Token type;
		public TerminalNode ID() { return getToken(DeclarationParser.ID, 0); }
		public TypeReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_typeReference; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterTypeReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitTypeReference(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitTypeReference(this);
			else return visitor.visitChildren(this);
		}
	}

	public final TypeReferenceContext typeReference() throws RecognitionException {
		TypeReferenceContext _localctx = new TypeReferenceContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_typeReference);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(187);
			((TypeReferenceContext)_localctx).type = match(ID);
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
	public static class ArrayTypeContext extends ParserRuleContext {
		public Token type;
		public DimensionContext dimension;
		public List<DimensionContext> dimensions = new ArrayList<DimensionContext>();
		public TerminalNode ID() { return getToken(DeclarationParser.ID, 0); }
		public List<DimensionContext> dimension() {
			return getRuleContexts(DimensionContext.class);
		}
		public DimensionContext dimension(int i) {
			return getRuleContext(DimensionContext.class,i);
		}
		public ArrayTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_arrayType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterArrayType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitArrayType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitArrayType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArrayTypeContext arrayType() throws RecognitionException {
		ArrayTypeContext _localctx = new ArrayTypeContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_arrayType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(189);
			((ArrayTypeContext)_localctx).type = match(ID);
			setState(190);
			match(T__18);
			setState(191);
			((ArrayTypeContext)_localctx).dimension = dimension();
			((ArrayTypeContext)_localctx).dimensions.add(((ArrayTypeContext)_localctx).dimension);
			setState(196);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__7) {
				{
				{
				setState(192);
				match(T__7);
				setState(193);
				((ArrayTypeContext)_localctx).dimension = dimension();
				((ArrayTypeContext)_localctx).dimensions.add(((ArrayTypeContext)_localctx).dimension);
				}
				}
				setState(198);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(199);
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
	public static class DimensionContext extends ParserRuleContext {
		public SizeDimensionContext sizeDimension() {
			return getRuleContext(SizeDimensionContext.class,0);
		}
		public RangeDimensionContext rangeDimension() {
			return getRuleContext(RangeDimensionContext.class,0);
		}
		public DimensionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_dimension; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterDimension(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitDimension(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitDimension(this);
			else return visitor.visitChildren(this);
		}
	}

	public final DimensionContext dimension() throws RecognitionException {
		DimensionContext _localctx = new DimensionContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_dimension);
		try {
			setState(203);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,19,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(201);
				sizeDimension();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(202);
				rangeDimension();
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
	public static class SizeDimensionContext extends ParserRuleContext {
		public Token size;
		public TerminalNode ELONG() { return getToken(DeclarationParser.ELONG, 0); }
		public SizeDimensionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sizeDimension; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterSizeDimension(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitSizeDimension(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitSizeDimension(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SizeDimensionContext sizeDimension() throws RecognitionException {
		SizeDimensionContext _localctx = new SizeDimensionContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_sizeDimension);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(206);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELONG) {
				{
				setState(205);
				((SizeDimensionContext)_localctx).size = match(ELONG);
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
	public static class RangeDimensionContext extends ParserRuleContext {
		public Token lowerBound;
		public Token upperBound;
		public List<TerminalNode> ELONG() { return getTokens(DeclarationParser.ELONG); }
		public TerminalNode ELONG(int i) {
			return getToken(DeclarationParser.ELONG, i);
		}
		public RangeDimensionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rangeDimension; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterRangeDimension(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitRangeDimension(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitRangeDimension(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RangeDimensionContext rangeDimension() throws RecognitionException {
		RangeDimensionContext _localctx = new RangeDimensionContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_rangeDimension);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(209);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELONG) {
				{
				setState(208);
				((RangeDimensionContext)_localctx).lowerBound = match(ELONG);
				}
			}

			setState(211);
			match(T__3);
			setState(213);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELONG) {
				{
				setState(212);
				((RangeDimensionContext)_localctx).upperBound = match(ELONG);
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
	public static class DeclaredTypeContext extends ParserRuleContext {
		public RangeTypeContext rangeType() {
			return getRuleContext(RangeTypeContext.class,0);
		}
		public EnumerationTypeContext enumerationType() {
			return getRuleContext(EnumerationTypeContext.class,0);
		}
		public DeclaredTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_declaredType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterDeclaredType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitDeclaredType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitDeclaredType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final DeclaredTypeContext declaredType() throws RecognitionException {
		DeclaredTypeContext _localctx = new DeclaredTypeContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_declaredType);
		try {
			setState(217);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__20:
				enterOuterAlt(_localctx, 1);
				{
				setState(215);
				rangeType();
				}
				break;
			case T__21:
				enterOuterAlt(_localctx, 2);
				{
				setState(216);
				enumerationType();
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
	public static class RangeTypeContext extends ParserRuleContext {
		public Token name;
		public Token type;
		public LiteralContext minimum;
		public LiteralContext maximum;
		public List<TerminalNode> ID() { return getTokens(DeclarationParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(DeclarationParser.ID, i);
		}
		public List<LiteralContext> literal() {
			return getRuleContexts(LiteralContext.class);
		}
		public LiteralContext literal(int i) {
			return getRuleContext(LiteralContext.class,i);
		}
		public RangeTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rangeType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterRangeType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitRangeType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitRangeType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RangeTypeContext rangeType() throws RecognitionException {
		RangeTypeContext _localctx = new RangeTypeContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_rangeType);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(219);
			match(T__20);
			setState(220);
			((RangeTypeContext)_localctx).name = match(ID);
			setState(221);
			((RangeTypeContext)_localctx).type = match(ID);
			setState(222);
			match(T__18);
			setState(223);
			((RangeTypeContext)_localctx).minimum = literal();
			setState(224);
			match(T__3);
			setState(225);
			((RangeTypeContext)_localctx).maximum = literal();
			setState(226);
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
	public static class EnumerationTypeContext extends ParserRuleContext {
		public Token name;
		public EnumeralContext enumeral;
		public List<EnumeralContext> values = new ArrayList<EnumeralContext>();
		public TerminalNode ID() { return getToken(DeclarationParser.ID, 0); }
		public List<EnumeralContext> enumeral() {
			return getRuleContexts(EnumeralContext.class);
		}
		public EnumeralContext enumeral(int i) {
			return getRuleContext(EnumeralContext.class,i);
		}
		public EnumerationTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_enumerationType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterEnumerationType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitEnumerationType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitEnumerationType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EnumerationTypeContext enumerationType() throws RecognitionException {
		EnumerationTypeContext _localctx = new EnumerationTypeContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_enumerationType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(228);
			match(T__21);
			setState(229);
			((EnumerationTypeContext)_localctx).name = match(ID);
			setState(230);
			match(T__4);
			setState(231);
			((EnumerationTypeContext)_localctx).enumeral = enumeral();
			((EnumerationTypeContext)_localctx).values.add(((EnumerationTypeContext)_localctx).enumeral);
			setState(236);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__7) {
				{
				{
				setState(232);
				match(T__7);
				setState(233);
				((EnumerationTypeContext)_localctx).enumeral = enumeral();
				((EnumerationTypeContext)_localctx).values.add(((EnumerationTypeContext)_localctx).enumeral);
				}
				}
				setState(238);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(239);
			match(T__5);
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
	public static class EnumeralContext extends ParserRuleContext {
		public Token name;
		public Token value;
		public TerminalNode ID() { return getToken(DeclarationParser.ID, 0); }
		public TerminalNode ELONG() { return getToken(DeclarationParser.ELONG, 0); }
		public EnumeralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_enumeral; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterEnumeral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitEnumeral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitEnumeral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EnumeralContext enumeral() throws RecognitionException {
		EnumeralContext _localctx = new EnumeralContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_enumeral);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(241);
			((EnumeralContext)_localctx).name = match(ID);
			setState(244);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__8) {
				{
				setState(242);
				match(T__8);
				setState(243);
				((EnumeralContext)_localctx).value = match(ELONG);
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
	public static class UnitSpecificationContext extends ParserRuleContext {
		public ComposedUnitContext composedUnit;
		public List<ComposedUnitContext> units = new ArrayList<ComposedUnitContext>();
		public List<ComposedUnitContext> composedUnit() {
			return getRuleContexts(ComposedUnitContext.class);
		}
		public ComposedUnitContext composedUnit(int i) {
			return getRuleContext(ComposedUnitContext.class,i);
		}
		public UnitSpecificationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unitSpecification; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterUnitSpecification(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitUnitSpecification(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitUnitSpecification(this);
			else return visitor.visitChildren(this);
		}
	}

	public final UnitSpecificationContext unitSpecification() throws RecognitionException {
		UnitSpecificationContext _localctx = new UnitSpecificationContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_unitSpecification);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(246);
			((UnitSpecificationContext)_localctx).composedUnit = composedUnit();
			((UnitSpecificationContext)_localctx).units.add(((UnitSpecificationContext)_localctx).composedUnit);
			setState(251);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__22) {
				{
				{
				setState(247);
				match(T__22);
				setState(248);
				((UnitSpecificationContext)_localctx).composedUnit = composedUnit();
				((UnitSpecificationContext)_localctx).units.add(((UnitSpecificationContext)_localctx).composedUnit);
				}
				}
				setState(253);
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

	@SuppressWarnings("CheckReturnValue")
	public static class BasicUnitContext extends ParserRuleContext {
		public SIUnitContext sIUnit() {
			return getRuleContext(SIUnitContext.class,0);
		}
		public CustomUnitContext customUnit() {
			return getRuleContext(CustomUnitContext.class,0);
		}
		public UnitSpecificationContext unitSpecification() {
			return getRuleContext(UnitSpecificationContext.class,0);
		}
		public BasicUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_basicUnit; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterBasicUnit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitBasicUnit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitBasicUnit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BasicUnitContext basicUnit() throws RecognitionException {
		BasicUnitContext _localctx = new BasicUnitContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_basicUnit);
		try {
			setState(260);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__25:
			case T__26:
			case T__27:
			case T__28:
			case T__29:
			case T__30:
			case T__31:
			case T__32:
			case T__33:
			case T__34:
			case T__35:
			case T__36:
			case T__37:
			case T__38:
			case T__39:
			case T__40:
			case T__41:
			case T__42:
			case T__43:
			case T__44:
			case T__45:
			case T__46:
			case T__47:
			case T__48:
			case T__49:
			case T__50:
			case T__51:
			case T__52:
			case T__53:
			case T__54:
			case T__55:
				enterOuterAlt(_localctx, 1);
				{
				setState(254);
				sIUnit();
				}
				break;
			case STRING:
				enterOuterAlt(_localctx, 2);
				{
				setState(255);
				customUnit();
				}
				break;
			case T__16:
				enterOuterAlt(_localctx, 3);
				{
				setState(256);
				match(T__16);
				setState(257);
				unitSpecification();
				setState(258);
				match(T__17);
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
	public static class SIUnitContext extends ParserRuleContext {
		public SIUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_sIUnit; }
	 
		public SIUnitContext() { }
		public void copyFrom(SIUnitContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SiunitContext extends SIUnitContext {
		public EPrefixContext prefix;
		public ESIUnitTypeContext type;
		public ESIUnitTypeContext eSIUnitType() {
			return getRuleContext(ESIUnitTypeContext.class,0);
		}
		public EPrefixContext ePrefix() {
			return getRuleContext(EPrefixContext.class,0);
		}
		public SiunitContext(SIUnitContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterSiunit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitSiunit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitSiunit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SIUnitContext sIUnit() throws RecognitionException {
		SIUnitContext _localctx = new SIUnitContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_sIUnit);
		int _la;
		try {
			_localctx = new SiunitContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(263);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 140737421246464L) != 0)) {
				{
				setState(262);
				((SiunitContext)_localctx).prefix = ePrefix();
				}
			}

			setState(265);
			((SiunitContext)_localctx).type = eSIUnitType();
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
	public static class CustomUnitContext extends ParserRuleContext {
		public CustomUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_customUnit; }
	 
		public CustomUnitContext() { }
		public void copyFrom(CustomUnitContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CustomunitContext extends CustomUnitContext {
		public Token name;
		public TerminalNode STRING() { return getToken(DeclarationParser.STRING, 0); }
		public CustomunitContext(CustomUnitContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterCustomunit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitCustomunit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitCustomunit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final CustomUnitContext customUnit() throws RecognitionException {
		CustomUnitContext _localctx = new CustomUnitContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_customUnit);
		try {
			_localctx = new CustomunitContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(267);
			((CustomunitContext)_localctx).name = match(STRING);
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
	public static class ComposedUnitContext extends ParserRuleContext {
		public BasicUnitContext numerator;
		public BasicUnitContext denominator;
		public Token exponent;
		public List<BasicUnitContext> basicUnit() {
			return getRuleContexts(BasicUnitContext.class);
		}
		public BasicUnitContext basicUnit(int i) {
			return getRuleContext(BasicUnitContext.class,i);
		}
		public TerminalNode ELONG() { return getToken(DeclarationParser.ELONG, 0); }
		public ComposedUnitContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_composedUnit; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterComposedUnit(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitComposedUnit(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitComposedUnit(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ComposedUnitContext composedUnit() throws RecognitionException {
		ComposedUnitContext _localctx = new ComposedUnitContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_composedUnit);
		try {
			setState(277);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,30,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(269);
				((ComposedUnitContext)_localctx).numerator = basicUnit();
				setState(274);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__23:
					{
					{
					setState(270);
					match(T__23);
					setState(271);
					((ComposedUnitContext)_localctx).denominator = basicUnit();
					}
					}
					break;
				case T__24:
					{
					{
					setState(272);
					match(T__24);
					setState(273);
					((ComposedUnitContext)_localctx).exponent = match(ELONG);
					}
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(276);
				basicUnit();
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
	public static class EPrefixContext extends ParserRuleContext {
		public Token noP;
		public Token yotta;
		public Token zetta;
		public Token exa;
		public Token peta;
		public Token tera;
		public Token giga;
		public Token mega;
		public Token kilo;
		public Token hecto;
		public Token deca;
		public Token deci;
		public Token centi;
		public Token mili;
		public Token micro;
		public Token nano;
		public Token pico;
		public Token femto;
		public Token atto;
		public Token zepto;
		public Token yocto;
		public EPrefixContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_ePrefix; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterEPrefix(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitEPrefix(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitEPrefix(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EPrefixContext ePrefix() throws RecognitionException {
		EPrefixContext _localctx = new EPrefixContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_ePrefix);
		try {
			setState(300);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__25:
				enterOuterAlt(_localctx, 1);
				{
				setState(279);
				((EPrefixContext)_localctx).noP = match(T__25);
				}
				break;
			case T__26:
				enterOuterAlt(_localctx, 2);
				{
				setState(280);
				((EPrefixContext)_localctx).yotta = match(T__26);
				}
				break;
			case T__27:
				enterOuterAlt(_localctx, 3);
				{
				setState(281);
				((EPrefixContext)_localctx).zetta = match(T__27);
				}
				break;
			case T__28:
				enterOuterAlt(_localctx, 4);
				{
				setState(282);
				((EPrefixContext)_localctx).exa = match(T__28);
				}
				break;
			case T__29:
				enterOuterAlt(_localctx, 5);
				{
				setState(283);
				((EPrefixContext)_localctx).peta = match(T__29);
				}
				break;
			case T__30:
				enterOuterAlt(_localctx, 6);
				{
				setState(284);
				((EPrefixContext)_localctx).tera = match(T__30);
				}
				break;
			case T__31:
				enterOuterAlt(_localctx, 7);
				{
				setState(285);
				((EPrefixContext)_localctx).giga = match(T__31);
				}
				break;
			case T__32:
				enterOuterAlt(_localctx, 8);
				{
				setState(286);
				((EPrefixContext)_localctx).mega = match(T__32);
				}
				break;
			case T__33:
				enterOuterAlt(_localctx, 9);
				{
				setState(287);
				((EPrefixContext)_localctx).kilo = match(T__33);
				}
				break;
			case T__34:
				enterOuterAlt(_localctx, 10);
				{
				setState(288);
				((EPrefixContext)_localctx).hecto = match(T__34);
				}
				break;
			case T__35:
				enterOuterAlt(_localctx, 11);
				{
				setState(289);
				((EPrefixContext)_localctx).deca = match(T__35);
				}
				break;
			case T__36:
				enterOuterAlt(_localctx, 12);
				{
				setState(290);
				((EPrefixContext)_localctx).deci = match(T__36);
				}
				break;
			case T__37:
				enterOuterAlt(_localctx, 13);
				{
				setState(291);
				((EPrefixContext)_localctx).centi = match(T__37);
				}
				break;
			case T__38:
				enterOuterAlt(_localctx, 14);
				{
				setState(292);
				((EPrefixContext)_localctx).mili = match(T__38);
				}
				break;
			case T__39:
				enterOuterAlt(_localctx, 15);
				{
				setState(293);
				((EPrefixContext)_localctx).micro = match(T__39);
				}
				break;
			case T__40:
				enterOuterAlt(_localctx, 16);
				{
				setState(294);
				((EPrefixContext)_localctx).nano = match(T__40);
				}
				break;
			case T__41:
				enterOuterAlt(_localctx, 17);
				{
				setState(295);
				((EPrefixContext)_localctx).pico = match(T__41);
				}
				break;
			case T__42:
				enterOuterAlt(_localctx, 18);
				{
				setState(296);
				((EPrefixContext)_localctx).femto = match(T__42);
				}
				break;
			case T__43:
				enterOuterAlt(_localctx, 19);
				{
				setState(297);
				((EPrefixContext)_localctx).atto = match(T__43);
				}
				break;
			case T__44:
				enterOuterAlt(_localctx, 20);
				{
				setState(298);
				((EPrefixContext)_localctx).zepto = match(T__44);
				}
				break;
			case T__45:
				enterOuterAlt(_localctx, 21);
				{
				setState(299);
				((EPrefixContext)_localctx).yocto = match(T__45);
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
	public static class ESIUnitTypeContext extends ParserRuleContext {
		public Token meter;
		public Token gram;
		public Token ton;
		public Token second;
		public Token ampere;
		public Token kelvin;
		public Token mole;
		public Token candela;
		public Token pascal;
		public Token joule;
		public ESIUnitTypeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_eSIUnitType; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterESIUnitType(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitESIUnitType(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitESIUnitType(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ESIUnitTypeContext eSIUnitType() throws RecognitionException {
		ESIUnitTypeContext _localctx = new ESIUnitTypeContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_eSIUnitType);
		try {
			setState(312);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__46:
				enterOuterAlt(_localctx, 1);
				{
				setState(302);
				((ESIUnitTypeContext)_localctx).meter = match(T__46);
				}
				break;
			case T__47:
				enterOuterAlt(_localctx, 2);
				{
				setState(303);
				((ESIUnitTypeContext)_localctx).gram = match(T__47);
				}
				break;
			case T__48:
				enterOuterAlt(_localctx, 3);
				{
				setState(304);
				((ESIUnitTypeContext)_localctx).ton = match(T__48);
				}
				break;
			case T__49:
				enterOuterAlt(_localctx, 4);
				{
				setState(305);
				((ESIUnitTypeContext)_localctx).second = match(T__49);
				}
				break;
			case T__50:
				enterOuterAlt(_localctx, 5);
				{
				setState(306);
				((ESIUnitTypeContext)_localctx).ampere = match(T__50);
				}
				break;
			case T__51:
				enterOuterAlt(_localctx, 6);
				{
				setState(307);
				((ESIUnitTypeContext)_localctx).kelvin = match(T__51);
				}
				break;
			case T__52:
				enterOuterAlt(_localctx, 7);
				{
				setState(308);
				((ESIUnitTypeContext)_localctx).mole = match(T__52);
				}
				break;
			case T__53:
				enterOuterAlt(_localctx, 8);
				{
				setState(309);
				((ESIUnitTypeContext)_localctx).candela = match(T__53);
				}
				break;
			case T__54:
				enterOuterAlt(_localctx, 9);
				{
				setState(310);
				((ESIUnitTypeContext)_localctx).pascal = match(T__54);
				}
				break;
			case T__55:
				enterOuterAlt(_localctx, 10);
				{
				setState(311);
				((ESIUnitTypeContext)_localctx).joule = match(T__55);
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
	public static class ArithmeticExpressionContext extends ParserRuleContext {
		public MultiplicationExpressionContext left;
		public EAdditionOperatorContext op;
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
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterArithmeticExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitArithmeticExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitArithmeticExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArithmeticExpressionContext arithmeticExpression() throws RecognitionException {
		ArithmeticExpressionContext _localctx = new ArithmeticExpressionContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_arithmeticExpression);
		try {
			setState(319);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,33,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(314);
				((ArithmeticExpressionContext)_localctx).left = multiplicationExpression();
				setState(315);
				((ArithmeticExpressionContext)_localctx).op = eAdditionOperator();
				setState(316);
				((ArithmeticExpressionContext)_localctx).right = arithmeticExpression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(318);
				multiplicationExpression();
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
	public static class EAdditionOperatorContext extends ParserRuleContext {
		public EAdditionOperatorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_eAdditionOperator; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterEAdditionOperator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitEAdditionOperator(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitEAdditionOperator(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EAdditionOperatorContext eAdditionOperator() throws RecognitionException {
		EAdditionOperatorContext _localctx = new EAdditionOperatorContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_eAdditionOperator);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(321);
			_la = _input.LA(1);
			if ( !(_la==T__56 || _la==T__57) ) {
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
	public static class MultiplicationExpressionContext extends ParserRuleContext {
		public ValueExpressionContext left;
		public EMultiplicationOperatorContext op;
		public MultiplicationExpressionContext right;
		public ValueExpressionContext valueExpression() {
			return getRuleContext(ValueExpressionContext.class,0);
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
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterMultiplicationExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitMultiplicationExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitMultiplicationExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final MultiplicationExpressionContext multiplicationExpression() throws RecognitionException {
		MultiplicationExpressionContext _localctx = new MultiplicationExpressionContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_multiplicationExpression);
		try {
			setState(328);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,34,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(323);
				((MultiplicationExpressionContext)_localctx).left = valueExpression();
				setState(324);
				((MultiplicationExpressionContext)_localctx).op = eMultiplicationOperator();
				setState(325);
				((MultiplicationExpressionContext)_localctx).right = multiplicationExpression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(327);
				valueExpression();
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
	public static class EMultiplicationOperatorContext extends ParserRuleContext {
		public EMultiplicationOperatorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_eMultiplicationOperator; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterEMultiplicationOperator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitEMultiplicationOperator(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitEMultiplicationOperator(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EMultiplicationOperatorContext eMultiplicationOperator() throws RecognitionException {
		EMultiplicationOperatorContext _localctx = new EMultiplicationOperatorContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_eMultiplicationOperator);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(330);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 576460752328589312L) != 0)) ) {
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
	public static class ValueExpressionContext extends ParserRuleContext {
		public ParenthesisExpressionContext parenthesisExpression() {
			return getRuleContext(ParenthesisExpressionContext.class,0);
		}
		public NamedElementReferenceContext namedElementReference() {
			return getRuleContext(NamedElementReferenceContext.class,0);
		}
		public ArrayExpressionContext arrayExpression() {
			return getRuleContext(ArrayExpressionContext.class,0);
		}
		public LiteralExpressionContext literalExpression() {
			return getRuleContext(LiteralExpressionContext.class,0);
		}
		public ValueExpressionContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_valueExpression; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterValueExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitValueExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitValueExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ValueExpressionContext valueExpression() throws RecognitionException {
		ValueExpressionContext _localctx = new ValueExpressionContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_valueExpression);
		try {
			setState(336);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__16:
				enterOuterAlt(_localctx, 1);
				{
				setState(332);
				parenthesisExpression();
				}
				break;
			case ID:
				enterOuterAlt(_localctx, 2);
				{
				setState(333);
				namedElementReference();
				}
				break;
			case T__18:
				enterOuterAlt(_localctx, 3);
				{
				setState(334);
				arrayExpression();
				}
				break;
			case ELONG:
			case EDOUBLE:
			case EBoolean:
			case STRING:
				enterOuterAlt(_localctx, 4);
				{
				setState(335);
				literalExpression();
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
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterLiteralExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitLiteralExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitLiteralExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LiteralExpressionContext literalExpression() throws RecognitionException {
		LiteralExpressionContext _localctx = new LiteralExpressionContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_literalExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(338);
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
		public StringValueContext stringValue() {
			return getRuleContext(StringValueContext.class,0);
		}
		public LongValueContext longValue() {
			return getRuleContext(LongValueContext.class,0);
		}
		public DoubleValueContext doubleValue() {
			return getRuleContext(DoubleValueContext.class,0);
		}
		public BooleanValueContext booleanValue() {
			return getRuleContext(BooleanValueContext.class,0);
		}
		public LiteralContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_literal; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitLiteral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LiteralContext literal() throws RecognitionException {
		LiteralContext _localctx = new LiteralContext(_ctx, getState());
		enterRule(_localctx, 62, RULE_literal);
		try {
			setState(344);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(340);
				stringValue();
				}
				break;
			case ELONG:
				enterOuterAlt(_localctx, 2);
				{
				setState(341);
				longValue();
				}
				break;
			case EDOUBLE:
				enterOuterAlt(_localctx, 3);
				{
				setState(342);
				doubleValue();
				}
				break;
			case EBoolean:
				enterOuterAlt(_localctx, 4);
				{
				setState(343);
				booleanValue();
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
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterParenthesisExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitParenthesisExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitParenthesisExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParenthesisExpressionContext parenthesisExpression() throws RecognitionException {
		ParenthesisExpressionContext _localctx = new ParenthesisExpressionContext(_ctx, getState());
		enterRule(_localctx, 64, RULE_parenthesisExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(346);
			match(T__16);
			setState(347);
			((ParenthesisExpressionContext)_localctx).expression = arithmeticExpression();
			setState(348);
			match(T__17);
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
		public List<ArithmeticExpressionContext> elements = new ArrayList<ArithmeticExpressionContext>();
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
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterArrayExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitArrayExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitArrayExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArrayExpressionContext arrayExpression() throws RecognitionException {
		ArrayExpressionContext _localctx = new ArrayExpressionContext(_ctx, getState());
		enterRule(_localctx, 66, RULE_arrayExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(350);
			match(T__18);
			setState(359);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (((((_la - 17)) & ~0x3f) == 0 && ((1L << (_la - 17)) & 826832744087557L) != 0)) {
				{
				setState(351);
				((ArrayExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
				((ArrayExpressionContext)_localctx).elements.add(((ArrayExpressionContext)_localctx).arithmeticExpression);
				setState(356);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__7) {
					{
					{
					setState(352);
					match(T__7);
					setState(353);
					((ArrayExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
					((ArrayExpressionContext)_localctx).elements.add(((ArrayExpressionContext)_localctx).arithmeticExpression);
					}
					}
					setState(358);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(361);
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
	public static class NamedElementReferenceContext extends ParserRuleContext {
		public Token element;
		public Token attribute;
		public List<TerminalNode> ID() { return getTokens(DeclarationParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(DeclarationParser.ID, i);
		}
		public NamedElementReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namedElementReference; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterNamedElementReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitNamedElementReference(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitNamedElementReference(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NamedElementReferenceContext namedElementReference() throws RecognitionException {
		NamedElementReferenceContext _localctx = new NamedElementReferenceContext(_ctx, getState());
		enterRule(_localctx, 68, RULE_namedElementReference);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(363);
			((NamedElementReferenceContext)_localctx).element = match(ID);
			setState(366);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__59) {
				{
				setState(364);
				match(T__59);
				setState(365);
				((NamedElementReferenceContext)_localctx).attribute = match(ID);
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
	public static class StringValueContext extends ParserRuleContext {
		public Token value;
		public TerminalNode STRING() { return getToken(DeclarationParser.STRING, 0); }
		public StringValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_stringValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterStringValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitStringValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitStringValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StringValueContext stringValue() throws RecognitionException {
		StringValueContext _localctx = new StringValueContext(_ctx, getState());
		enterRule(_localctx, 70, RULE_stringValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(368);
			((StringValueContext)_localctx).value = match(STRING);
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
	public static class LongValueContext extends ParserRuleContext {
		public Token value;
		public TerminalNode ELONG() { return getToken(DeclarationParser.ELONG, 0); }
		public LongValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_longValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterLongValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitLongValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitLongValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LongValueContext longValue() throws RecognitionException {
		LongValueContext _localctx = new LongValueContext(_ctx, getState());
		enterRule(_localctx, 72, RULE_longValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(370);
			((LongValueContext)_localctx).value = match(ELONG);
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
	public static class DoubleValueContext extends ParserRuleContext {
		public Token value;
		public TerminalNode EDOUBLE() { return getToken(DeclarationParser.EDOUBLE, 0); }
		public DoubleValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_doubleValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterDoubleValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitDoubleValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitDoubleValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final DoubleValueContext doubleValue() throws RecognitionException {
		DoubleValueContext _localctx = new DoubleValueContext(_ctx, getState());
		enterRule(_localctx, 74, RULE_doubleValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(372);
			((DoubleValueContext)_localctx).value = match(EDOUBLE);
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
	public static class BooleanValueContext extends ParserRuleContext {
		public Token value;
		public TerminalNode EBoolean() { return getToken(DeclarationParser.EBoolean, 0); }
		public BooleanValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_booleanValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterBooleanValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitBooleanValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitBooleanValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BooleanValueContext booleanValue() throws RecognitionException {
		BooleanValueContext _localctx = new BooleanValueContext(_ctx, getState());
		enterRule(_localctx, 76, RULE_booleanValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(374);
			((BooleanValueContext)_localctx).value = match(EBoolean);
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
		"\u0004\u0001F\u0179\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007\u0015"+
		"\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002\u0018\u0007\u0018"+
		"\u0002\u0019\u0007\u0019\u0002\u001a\u0007\u001a\u0002\u001b\u0007\u001b"+
		"\u0002\u001c\u0007\u001c\u0002\u001d\u0007\u001d\u0002\u001e\u0007\u001e"+
		"\u0002\u001f\u0007\u001f\u0002 \u0007 \u0002!\u0007!\u0002\"\u0007\"\u0002"+
		"#\u0007#\u0002$\u0007$\u0002%\u0007%\u0002&\u0007&\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0005\u0000S\b\u0000\n\u0000\f\u0000V\t\u0000"+
		"\u0003\u0000X\b\u0000\u0001\u0000\u0001\u0000\u0005\u0000\\\b\u0000\n"+
		"\u0000\f\u0000_\t\u0000\u0001\u0001\u0001\u0001\u0001\u0001\u0003\u0001"+
		"d\b\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0005\u0002l\b\u0002\n\u0002\f\u0002o\t\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0003\u0003z\b\u0003\u0001\u0003\u0001\u0003"+
		"\u0003\u0003~\b\u0003\u0001\u0004\u0003\u0004\u0081\b\u0004\u0001\u0004"+
		"\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004"+
		"\u0005\u0004\u008a\b\u0004\n\u0004\f\u0004\u008d\t\u0004\u0001\u0004\u0001"+
		"\u0004\u0005\u0004\u0091\b\u0004\n\u0004\f\u0004\u0094\t\u0004\u0001\u0004"+
		"\u0001\u0004\u0005\u0004\u0098\b\u0004\n\u0004\f\u0004\u009b\t\u0004\u0001"+
		"\u0004\u0003\u0004\u009e\b\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0005"+
		"\u0005\u00a3\b\u0005\n\u0005\f\u0005\u00a6\t\u0005\u0001\u0006\u0001\u0006"+
		"\u0003\u0006\u00aa\b\u0006\u0001\u0007\u0001\u0007\u0001\u0007\u0003\u0007"+
		"\u00af\b\u0007\u0001\b\u0001\b\u0001\b\u0001\b\u0005\b\u00b5\b\b\n\b\f"+
		"\b\u00b8\t\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\n\u0001\n\u0001\n\u0001"+
		"\n\u0001\n\u0005\n\u00c3\b\n\n\n\f\n\u00c6\t\n\u0001\n\u0001\n\u0001\u000b"+
		"\u0001\u000b\u0003\u000b\u00cc\b\u000b\u0001\f\u0003\f\u00cf\b\f\u0001"+
		"\r\u0003\r\u00d2\b\r\u0001\r\u0001\r\u0003\r\u00d6\b\r\u0001\u000e\u0001"+
		"\u000e\u0003\u000e\u00da\b\u000e\u0001\u000f\u0001\u000f\u0001\u000f\u0001"+
		"\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001\u000f\u0001"+
		"\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0005"+
		"\u0010\u00eb\b\u0010\n\u0010\f\u0010\u00ee\t\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0011\u0001\u0011\u0001\u0011\u0003\u0011\u00f5\b\u0011\u0001\u0012"+
		"\u0001\u0012\u0001\u0012\u0005\u0012\u00fa\b\u0012\n\u0012\f\u0012\u00fd"+
		"\t\u0012\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0001"+
		"\u0013\u0003\u0013\u0105\b\u0013\u0001\u0014\u0003\u0014\u0108\b\u0014"+
		"\u0001\u0014\u0001\u0014\u0001\u0015\u0001\u0015\u0001\u0016\u0001\u0016"+
		"\u0001\u0016\u0001\u0016\u0001\u0016\u0003\u0016\u0113\b\u0016\u0001\u0016"+
		"\u0003\u0016\u0116\b\u0016\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017"+
		"\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017"+
		"\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017"+
		"\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017\u0003\u0017"+
		"\u012d\b\u0017\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018"+
		"\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0003\u0018"+
		"\u0139\b\u0018\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019"+
		"\u0003\u0019\u0140\b\u0019\u0001\u001a\u0001\u001a\u0001\u001b\u0001\u001b"+
		"\u0001\u001b\u0001\u001b\u0001\u001b\u0003\u001b\u0149\b\u001b\u0001\u001c"+
		"\u0001\u001c\u0001\u001d\u0001\u001d\u0001\u001d\u0001\u001d\u0003\u001d"+
		"\u0151\b\u001d\u0001\u001e\u0001\u001e\u0001\u001f\u0001\u001f\u0001\u001f"+
		"\u0001\u001f\u0003\u001f\u0159\b\u001f\u0001 \u0001 \u0001 \u0001 \u0001"+
		"!\u0001!\u0001!\u0001!\u0005!\u0163\b!\n!\f!\u0166\t!\u0003!\u0168\b!"+
		"\u0001!\u0001!\u0001\"\u0001\"\u0001\"\u0003\"\u016f\b\"\u0001#\u0001"+
		"#\u0001$\u0001$\u0001%\u0001%\u0001&\u0001&\u0001&\u0000\u0000\'\u0000"+
		"\u0002\u0004\u0006\b\n\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c"+
		"\u001e \"$&(*,.02468:<>@BDFHJL\u0000\u0002\u0001\u00009:\u0002\u0000\u0017"+
		"\u0018;;\u019b\u0000N\u0001\u0000\u0000\u0000\u0002c\u0001\u0000\u0000"+
		"\u0000\u0004e\u0001\u0000\u0000\u0000\u0006r\u0001\u0000\u0000\u0000\b"+
		"\u0080\u0001\u0000\u0000\u0000\n\u009f\u0001\u0000\u0000\u0000\f\u00a9"+
		"\u0001\u0000\u0000\u0000\u000e\u00ae\u0001\u0000\u0000\u0000\u0010\u00b0"+
		"\u0001\u0000\u0000\u0000\u0012\u00bb\u0001\u0000\u0000\u0000\u0014\u00bd"+
		"\u0001\u0000\u0000\u0000\u0016\u00cb\u0001\u0000\u0000\u0000\u0018\u00ce"+
		"\u0001\u0000\u0000\u0000\u001a\u00d1\u0001\u0000\u0000\u0000\u001c\u00d9"+
		"\u0001\u0000\u0000\u0000\u001e\u00db\u0001\u0000\u0000\u0000 \u00e4\u0001"+
		"\u0000\u0000\u0000\"\u00f1\u0001\u0000\u0000\u0000$\u00f6\u0001\u0000"+
		"\u0000\u0000&\u0104\u0001\u0000\u0000\u0000(\u0107\u0001\u0000\u0000\u0000"+
		"*\u010b\u0001\u0000\u0000\u0000,\u0115\u0001\u0000\u0000\u0000.\u012c"+
		"\u0001\u0000\u0000\u00000\u0138\u0001\u0000\u0000\u00002\u013f\u0001\u0000"+
		"\u0000\u00004\u0141\u0001\u0000\u0000\u00006\u0148\u0001\u0000\u0000\u0000"+
		"8\u014a\u0001\u0000\u0000\u0000:\u0150\u0001\u0000\u0000\u0000<\u0152"+
		"\u0001\u0000\u0000\u0000>\u0158\u0001\u0000\u0000\u0000@\u015a\u0001\u0000"+
		"\u0000\u0000B\u015e\u0001\u0000\u0000\u0000D\u016b\u0001\u0000\u0000\u0000"+
		"F\u0170\u0001\u0000\u0000\u0000H\u0172\u0001\u0000\u0000\u0000J\u0174"+
		"\u0001\u0000\u0000\u0000L\u0176\u0001\u0000\u0000\u0000NO\u0005\u0001"+
		"\u0000\u0000OW\u0005@\u0000\u0000PT\u0005\u0002\u0000\u0000QS\u0003\u001c"+
		"\u000e\u0000RQ\u0001\u0000\u0000\u0000SV\u0001\u0000\u0000\u0000TR\u0001"+
		"\u0000\u0000\u0000TU\u0001\u0000\u0000\u0000UX\u0001\u0000\u0000\u0000"+
		"VT\u0001\u0000\u0000\u0000WP\u0001\u0000\u0000\u0000WX\u0001\u0000\u0000"+
		"\u0000X]\u0001\u0000\u0000\u0000Y\\\u0003\u0004\u0002\u0000Z\\\u0003\b"+
		"\u0004\u0000[Y\u0001\u0000\u0000\u0000[Z\u0001\u0000\u0000\u0000\\_\u0001"+
		"\u0000\u0000\u0000][\u0001\u0000\u0000\u0000]^\u0001\u0000\u0000\u0000"+
		"^\u0001\u0001\u0000\u0000\u0000_]\u0001\u0000\u0000\u0000`d\u0003\u0006"+
		"\u0003\u0000ad\u0003\u0004\u0002\u0000bd\u0003\b\u0004\u0000c`\u0001\u0000"+
		"\u0000\u0000ca\u0001\u0000\u0000\u0000cb\u0001\u0000\u0000\u0000d\u0003"+
		"\u0001\u0000\u0000\u0000ef\u0005\u0003\u0000\u0000fg\u0005@\u0000\u0000"+
		"gh\u0005\u0004\u0000\u0000hi\u0005B\u0000\u0000im\u0005\u0005\u0000\u0000"+
		"jl\u0003\u0006\u0003\u0000kj\u0001\u0000\u0000\u0000lo\u0001\u0000\u0000"+
		"\u0000mk\u0001\u0000\u0000\u0000mn\u0001\u0000\u0000\u0000np\u0001\u0000"+
		"\u0000\u0000om\u0001\u0000\u0000\u0000pq\u0005\u0006\u0000\u0000q\u0005"+
		"\u0001\u0000\u0000\u0000rs\u0005\u0007\u0000\u0000st\u0005@\u0000\u0000"+
		"tu\u0003\u000e\u0007\u0000uv\u0005\u0004\u0000\u0000vy\u0003$\u0012\u0000"+
		"wx\u0005\b\u0000\u0000xz\u0005B\u0000\u0000yw\u0001\u0000\u0000\u0000"+
		"yz\u0001\u0000\u0000\u0000z}\u0001\u0000\u0000\u0000{|\u0005\t\u0000\u0000"+
		"|~\u00032\u0019\u0000}{\u0001\u0000\u0000\u0000}~\u0001\u0000\u0000\u0000"+
		"~\u0007\u0001\u0000\u0000\u0000\u007f\u0081\u0005\n\u0000\u0000\u0080"+
		"\u007f\u0001\u0000\u0000\u0000\u0080\u0081\u0001\u0000\u0000\u0000\u0081"+
		"\u0082\u0001\u0000\u0000\u0000\u0082\u0083\u0005\u000b\u0000\u0000\u0083"+
		"\u0084\u0005@\u0000\u0000\u0084\u0085\u0005\u0004\u0000\u0000\u0085\u009d"+
		"\u0005B\u0000\u0000\u0086\u008b\u0005\u0005\u0000\u0000\u0087\u0088\u0005"+
		"\f\u0000\u0000\u0088\u008a\u0005@\u0000\u0000\u0089\u0087\u0001\u0000"+
		"\u0000\u0000\u008a\u008d\u0001\u0000\u0000\u0000\u008b\u0089\u0001\u0000"+
		"\u0000\u0000\u008b\u008c\u0001\u0000\u0000\u0000\u008c\u0092\u0001\u0000"+
		"\u0000\u0000\u008d\u008b\u0001\u0000\u0000\u0000\u008e\u008f\u0005\r\u0000"+
		"\u0000\u008f\u0091\u0005@\u0000\u0000\u0090\u008e\u0001\u0000\u0000\u0000"+
		"\u0091\u0094\u0001\u0000\u0000\u0000\u0092\u0090\u0001\u0000\u0000\u0000"+
		"\u0092\u0093\u0001\u0000\u0000\u0000\u0093\u0099\u0001\u0000\u0000\u0000"+
		"\u0094\u0092\u0001\u0000\u0000\u0000\u0095\u0098\u0003\u0004\u0002\u0000"+
		"\u0096\u0098\u0003\n\u0005\u0000\u0097\u0095\u0001\u0000\u0000\u0000\u0097"+
		"\u0096\u0001\u0000\u0000\u0000\u0098\u009b\u0001\u0000\u0000\u0000\u0099"+
		"\u0097\u0001\u0000\u0000\u0000\u0099\u009a\u0001\u0000\u0000\u0000\u009a"+
		"\u009c\u0001\u0000\u0000\u0000\u009b\u0099\u0001\u0000\u0000\u0000\u009c"+
		"\u009e\u0005\u0006\u0000\u0000\u009d\u0086\u0001\u0000\u0000\u0000\u009d"+
		"\u009e\u0001\u0000\u0000\u0000\u009e\t\u0001\u0000\u0000\u0000\u009f\u00a0"+
		"\u0005\u000e\u0000\u0000\u00a0\u00a4\u0003\f\u0006\u0000\u00a1\u00a3\u0003"+
		"\b\u0004\u0000\u00a2\u00a1\u0001\u0000\u0000\u0000\u00a3\u00a6\u0001\u0000"+
		"\u0000\u0000\u00a4\u00a2\u0001\u0000\u0000\u0000\u00a4\u00a5\u0001\u0000"+
		"\u0000\u0000\u00a5\u000b\u0001\u0000\u0000\u0000\u00a6\u00a4\u0001\u0000"+
		"\u0000\u0000\u00a7\u00aa\u0005\u000f\u0000\u0000\u00a8\u00aa\u0005\u0010"+
		"\u0000\u0000\u00a9\u00a7\u0001\u0000\u0000\u0000\u00a9\u00a8\u0001\u0000"+
		"\u0000\u0000\u00aa\r\u0001\u0000\u0000\u0000\u00ab\u00af\u0003\u0012\t"+
		"\u0000\u00ac\u00af\u0003\u0010\b\u0000\u00ad\u00af\u0003\u0014\n\u0000"+
		"\u00ae\u00ab\u0001\u0000\u0000\u0000\u00ae\u00ac\u0001\u0000\u0000\u0000"+
		"\u00ae\u00ad\u0001\u0000\u0000\u0000\u00af\u000f\u0001\u0000\u0000\u0000"+
		"\u00b0\u00b1\u0005\u0011\u0000\u0000\u00b1\u00b6\u0003\"\u0011\u0000\u00b2"+
		"\u00b3\u0005\b\u0000\u0000\u00b3\u00b5\u0003\"\u0011\u0000\u00b4\u00b2"+
		"\u0001\u0000\u0000\u0000\u00b5\u00b8\u0001\u0000\u0000\u0000\u00b6\u00b4"+
		"\u0001\u0000\u0000\u0000\u00b6\u00b7\u0001\u0000\u0000\u0000\u00b7\u00b9"+
		"\u0001\u0000\u0000\u0000\u00b8\u00b6\u0001\u0000\u0000\u0000\u00b9\u00ba"+
		"\u0005\u0012\u0000\u0000\u00ba\u0011\u0001\u0000\u0000\u0000\u00bb\u00bc"+
		"\u0005@\u0000\u0000\u00bc\u0013\u0001\u0000\u0000\u0000\u00bd\u00be\u0005"+
		"@\u0000\u0000\u00be\u00bf\u0005\u0013\u0000\u0000\u00bf\u00c4\u0003\u0016"+
		"\u000b\u0000\u00c0\u00c1\u0005\b\u0000\u0000\u00c1\u00c3\u0003\u0016\u000b"+
		"\u0000\u00c2\u00c0\u0001\u0000\u0000\u0000\u00c3\u00c6\u0001\u0000\u0000"+
		"\u0000\u00c4\u00c2\u0001\u0000\u0000\u0000\u00c4\u00c5\u0001\u0000\u0000"+
		"\u0000\u00c5\u00c7\u0001\u0000\u0000\u0000\u00c6\u00c4\u0001\u0000\u0000"+
		"\u0000\u00c7\u00c8\u0005\u0014\u0000\u0000\u00c8\u0015\u0001\u0000\u0000"+
		"\u0000\u00c9\u00cc\u0003\u0018\f\u0000\u00ca\u00cc\u0003\u001a\r\u0000"+
		"\u00cb\u00c9\u0001\u0000\u0000\u0000\u00cb\u00ca\u0001\u0000\u0000\u0000"+
		"\u00cc\u0017\u0001\u0000\u0000\u0000\u00cd\u00cf\u0005=\u0000\u0000\u00ce"+
		"\u00cd\u0001\u0000\u0000\u0000\u00ce\u00cf\u0001\u0000\u0000\u0000\u00cf"+
		"\u0019\u0001\u0000\u0000\u0000\u00d0\u00d2\u0005=\u0000\u0000\u00d1\u00d0"+
		"\u0001\u0000\u0000\u0000\u00d1\u00d2\u0001\u0000\u0000\u0000\u00d2\u00d3"+
		"\u0001\u0000\u0000\u0000\u00d3\u00d5\u0005\u0004\u0000\u0000\u00d4\u00d6"+
		"\u0005=\u0000\u0000\u00d5\u00d4\u0001\u0000\u0000\u0000\u00d5\u00d6\u0001"+
		"\u0000\u0000\u0000\u00d6\u001b\u0001\u0000\u0000\u0000\u00d7\u00da\u0003"+
		"\u001e\u000f\u0000\u00d8\u00da\u0003 \u0010\u0000\u00d9\u00d7\u0001\u0000"+
		"\u0000\u0000\u00d9\u00d8\u0001\u0000\u0000\u0000\u00da\u001d\u0001\u0000"+
		"\u0000\u0000\u00db\u00dc\u0005\u0015\u0000\u0000\u00dc\u00dd\u0005@\u0000"+
		"\u0000\u00dd\u00de\u0005@\u0000\u0000\u00de\u00df\u0005\u0013\u0000\u0000"+
		"\u00df\u00e0\u0003>\u001f\u0000\u00e0\u00e1\u0005\u0004\u0000\u0000\u00e1"+
		"\u00e2\u0003>\u001f\u0000\u00e2\u00e3\u0005\u0014\u0000\u0000\u00e3\u001f"+
		"\u0001\u0000\u0000\u0000\u00e4\u00e5\u0005\u0016\u0000\u0000\u00e5\u00e6"+
		"\u0005@\u0000\u0000\u00e6\u00e7\u0005\u0005\u0000\u0000\u00e7\u00ec\u0003"+
		"\"\u0011\u0000\u00e8\u00e9\u0005\b\u0000\u0000\u00e9\u00eb\u0003\"\u0011"+
		"\u0000\u00ea\u00e8\u0001\u0000\u0000\u0000\u00eb\u00ee\u0001\u0000\u0000"+
		"\u0000\u00ec\u00ea\u0001\u0000\u0000\u0000\u00ec\u00ed\u0001\u0000\u0000"+
		"\u0000\u00ed\u00ef\u0001\u0000\u0000\u0000\u00ee\u00ec\u0001\u0000\u0000"+
		"\u0000\u00ef\u00f0\u0005\u0006\u0000\u0000\u00f0!\u0001\u0000\u0000\u0000"+
		"\u00f1\u00f4\u0005@\u0000\u0000\u00f2\u00f3\u0005\t\u0000\u0000\u00f3"+
		"\u00f5\u0005=\u0000\u0000\u00f4\u00f2\u0001\u0000\u0000\u0000\u00f4\u00f5"+
		"\u0001\u0000\u0000\u0000\u00f5#\u0001\u0000\u0000\u0000\u00f6\u00fb\u0003"+
		",\u0016\u0000\u00f7\u00f8\u0005\u0017\u0000\u0000\u00f8\u00fa\u0003,\u0016"+
		"\u0000\u00f9\u00f7\u0001\u0000\u0000\u0000\u00fa\u00fd\u0001\u0000\u0000"+
		"\u0000\u00fb\u00f9\u0001\u0000\u0000\u0000\u00fb\u00fc\u0001\u0000\u0000"+
		"\u0000\u00fc%\u0001\u0000\u0000\u0000\u00fd\u00fb\u0001\u0000\u0000\u0000"+
		"\u00fe\u0105\u0003(\u0014\u0000\u00ff\u0105\u0003*\u0015\u0000\u0100\u0101"+
		"\u0005\u0011\u0000\u0000\u0101\u0102\u0003$\u0012\u0000\u0102\u0103\u0005"+
		"\u0012\u0000\u0000\u0103\u0105\u0001\u0000\u0000\u0000\u0104\u00fe\u0001"+
		"\u0000\u0000\u0000\u0104\u00ff\u0001\u0000\u0000\u0000\u0104\u0100\u0001"+
		"\u0000\u0000\u0000\u0105\'\u0001\u0000\u0000\u0000\u0106\u0108\u0003."+
		"\u0017\u0000\u0107\u0106\u0001\u0000\u0000\u0000\u0107\u0108\u0001\u0000"+
		"\u0000\u0000\u0108\u0109\u0001\u0000\u0000\u0000\u0109\u010a\u00030\u0018"+
		"\u0000\u010a)\u0001\u0000\u0000\u0000\u010b\u010c\u0005B\u0000\u0000\u010c"+
		"+\u0001\u0000\u0000\u0000\u010d\u0112\u0003&\u0013\u0000\u010e\u010f\u0005"+
		"\u0018\u0000\u0000\u010f\u0113\u0003&\u0013\u0000\u0110\u0111\u0005\u0019"+
		"\u0000\u0000\u0111\u0113\u0005=\u0000\u0000\u0112\u010e\u0001\u0000\u0000"+
		"\u0000\u0112\u0110\u0001\u0000\u0000\u0000\u0113\u0116\u0001\u0000\u0000"+
		"\u0000\u0114\u0116\u0003&\u0013\u0000\u0115\u010d\u0001\u0000\u0000\u0000"+
		"\u0115\u0114\u0001\u0000\u0000\u0000\u0116-\u0001\u0000\u0000\u0000\u0117"+
		"\u012d\u0005\u001a\u0000\u0000\u0118\u012d\u0005\u001b\u0000\u0000\u0119"+
		"\u012d\u0005\u001c\u0000\u0000\u011a\u012d\u0005\u001d\u0000\u0000\u011b"+
		"\u012d\u0005\u001e\u0000\u0000\u011c\u012d\u0005\u001f\u0000\u0000\u011d"+
		"\u012d\u0005 \u0000\u0000\u011e\u012d\u0005!\u0000\u0000\u011f\u012d\u0005"+
		"\"\u0000\u0000\u0120\u012d\u0005#\u0000\u0000\u0121\u012d\u0005$\u0000"+
		"\u0000\u0122\u012d\u0005%\u0000\u0000\u0123\u012d\u0005&\u0000\u0000\u0124"+
		"\u012d\u0005\'\u0000\u0000\u0125\u012d\u0005(\u0000\u0000\u0126\u012d"+
		"\u0005)\u0000\u0000\u0127\u012d\u0005*\u0000\u0000\u0128\u012d\u0005+"+
		"\u0000\u0000\u0129\u012d\u0005,\u0000\u0000\u012a\u012d\u0005-\u0000\u0000"+
		"\u012b\u012d\u0005.\u0000\u0000\u012c\u0117\u0001\u0000\u0000\u0000\u012c"+
		"\u0118\u0001\u0000\u0000\u0000\u012c\u0119\u0001\u0000\u0000\u0000\u012c"+
		"\u011a\u0001\u0000\u0000\u0000\u012c\u011b\u0001\u0000\u0000\u0000\u012c"+
		"\u011c\u0001\u0000\u0000\u0000\u012c\u011d\u0001\u0000\u0000\u0000\u012c"+
		"\u011e\u0001\u0000\u0000\u0000\u012c\u011f\u0001\u0000\u0000\u0000\u012c"+
		"\u0120\u0001\u0000\u0000\u0000\u012c\u0121\u0001\u0000\u0000\u0000\u012c"+
		"\u0122\u0001\u0000\u0000\u0000\u012c\u0123\u0001\u0000\u0000\u0000\u012c"+
		"\u0124\u0001\u0000\u0000\u0000\u012c\u0125\u0001\u0000\u0000\u0000\u012c"+
		"\u0126\u0001\u0000\u0000\u0000\u012c\u0127\u0001\u0000\u0000\u0000\u012c"+
		"\u0128\u0001\u0000\u0000\u0000\u012c\u0129\u0001\u0000\u0000\u0000\u012c"+
		"\u012a\u0001\u0000\u0000\u0000\u012c\u012b\u0001\u0000\u0000\u0000\u012d"+
		"/\u0001\u0000\u0000\u0000\u012e\u0139\u0005/\u0000\u0000\u012f\u0139\u0005"+
		"0\u0000\u0000\u0130\u0139\u00051\u0000\u0000\u0131\u0139\u00052\u0000"+
		"\u0000\u0132\u0139\u00053\u0000\u0000\u0133\u0139\u00054\u0000\u0000\u0134"+
		"\u0139\u00055\u0000\u0000\u0135\u0139\u00056\u0000\u0000\u0136\u0139\u0005"+
		"7\u0000\u0000\u0137\u0139\u00058\u0000\u0000\u0138\u012e\u0001\u0000\u0000"+
		"\u0000\u0138\u012f\u0001\u0000\u0000\u0000\u0138\u0130\u0001\u0000\u0000"+
		"\u0000\u0138\u0131\u0001\u0000\u0000\u0000\u0138\u0132\u0001\u0000\u0000"+
		"\u0000\u0138\u0133\u0001\u0000\u0000\u0000\u0138\u0134\u0001\u0000\u0000"+
		"\u0000\u0138\u0135\u0001\u0000\u0000\u0000\u0138\u0136\u0001\u0000\u0000"+
		"\u0000\u0138\u0137\u0001\u0000\u0000\u0000\u01391\u0001\u0000\u0000\u0000"+
		"\u013a\u013b\u00036\u001b\u0000\u013b\u013c\u00034\u001a\u0000\u013c\u013d"+
		"\u00032\u0019\u0000\u013d\u0140\u0001\u0000\u0000\u0000\u013e\u0140\u0003"+
		"6\u001b\u0000\u013f\u013a\u0001\u0000\u0000\u0000\u013f\u013e\u0001\u0000"+
		"\u0000\u0000\u01403\u0001\u0000\u0000\u0000\u0141\u0142\u0007\u0000\u0000"+
		"\u0000\u01425\u0001\u0000\u0000\u0000\u0143\u0144\u0003:\u001d\u0000\u0144"+
		"\u0145\u00038\u001c\u0000\u0145\u0146\u00036\u001b\u0000\u0146\u0149\u0001"+
		"\u0000\u0000\u0000\u0147\u0149\u0003:\u001d\u0000\u0148\u0143\u0001\u0000"+
		"\u0000\u0000\u0148\u0147\u0001\u0000\u0000\u0000\u01497\u0001\u0000\u0000"+
		"\u0000\u014a\u014b\u0007\u0001\u0000\u0000\u014b9\u0001\u0000\u0000\u0000"+
		"\u014c\u0151\u0003@ \u0000\u014d\u0151\u0003D\"\u0000\u014e\u0151\u0003"+
		"B!\u0000\u014f\u0151\u0003<\u001e\u0000\u0150\u014c\u0001\u0000\u0000"+
		"\u0000\u0150\u014d\u0001\u0000\u0000\u0000\u0150\u014e\u0001\u0000\u0000"+
		"\u0000\u0150\u014f\u0001\u0000\u0000\u0000\u0151;\u0001\u0000\u0000\u0000"+
		"\u0152\u0153\u0003>\u001f\u0000\u0153=\u0001\u0000\u0000\u0000\u0154\u0159"+
		"\u0003F#\u0000\u0155\u0159\u0003H$\u0000\u0156\u0159\u0003J%\u0000\u0157"+
		"\u0159\u0003L&\u0000\u0158\u0154\u0001\u0000\u0000\u0000\u0158\u0155\u0001"+
		"\u0000\u0000\u0000\u0158\u0156\u0001\u0000\u0000\u0000\u0158\u0157\u0001"+
		"\u0000\u0000\u0000\u0159?\u0001\u0000\u0000\u0000\u015a\u015b\u0005\u0011"+
		"\u0000\u0000\u015b\u015c\u00032\u0019\u0000\u015c\u015d\u0005\u0012\u0000"+
		"\u0000\u015dA\u0001\u0000\u0000\u0000\u015e\u0167\u0005\u0013\u0000\u0000"+
		"\u015f\u0164\u00032\u0019\u0000\u0160\u0161\u0005\b\u0000\u0000\u0161"+
		"\u0163\u00032\u0019\u0000\u0162\u0160\u0001\u0000\u0000\u0000\u0163\u0166"+
		"\u0001\u0000\u0000\u0000\u0164\u0162\u0001\u0000\u0000\u0000\u0164\u0165"+
		"\u0001\u0000\u0000\u0000\u0165\u0168\u0001\u0000\u0000\u0000\u0166\u0164"+
		"\u0001\u0000\u0000\u0000\u0167\u015f\u0001\u0000\u0000\u0000\u0167\u0168"+
		"\u0001\u0000\u0000\u0000\u0168\u0169\u0001\u0000\u0000\u0000\u0169\u016a"+
		"\u0005\u0014\u0000\u0000\u016aC\u0001\u0000\u0000\u0000\u016b\u016e\u0005"+
		"@\u0000\u0000\u016c\u016d\u0005<\u0000\u0000\u016d\u016f\u0005@\u0000"+
		"\u0000\u016e\u016c\u0001\u0000\u0000\u0000\u016e\u016f\u0001\u0000\u0000"+
		"\u0000\u016fE\u0001\u0000\u0000\u0000\u0170\u0171\u0005B\u0000\u0000\u0171"+
		"G\u0001\u0000\u0000\u0000\u0172\u0173\u0005=\u0000\u0000\u0173I\u0001"+
		"\u0000\u0000\u0000\u0174\u0175\u0005>\u0000\u0000\u0175K\u0001\u0000\u0000"+
		"\u0000\u0176\u0177\u0005?\u0000\u0000\u0177M\u0001\u0000\u0000\u0000("+
		"TW[]cmy}\u0080\u008b\u0092\u0097\u0099\u009d\u00a4\u00a9\u00ae\u00b6\u00c4"+
		"\u00cb\u00ce\u00d1\u00d5\u00d9\u00ec\u00f4\u00fb\u0104\u0107\u0112\u0115"+
		"\u012c\u0138\u013f\u0148\u0150\u0158\u0164\u0167\u016e";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}