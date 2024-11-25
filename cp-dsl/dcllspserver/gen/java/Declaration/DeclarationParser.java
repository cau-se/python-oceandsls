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
		RULE_parameterDeclaration = 3, RULE_featureDeclaration = 4, RULE_featureReference = 5, 
		RULE_featureGroupDeclaration = 6, RULE_eKind = 7, RULE_paramType = 8, 
		RULE_inlineEnumerationType = 9, RULE_typeReference = 10, RULE_arrayType = 11, 
		RULE_dimension = 12, RULE_sizeDimension = 13, RULE_rangeDimension = 14, 
		RULE_declaredType = 15, RULE_rangeType = 16, RULE_enumerationType = 17, 
		RULE_enumeral = 18, RULE_unitSpecification = 19, RULE_basicUnit = 20, 
		RULE_sIUnit = 21, RULE_customUnit = 22, RULE_composedUnit = 23, RULE_ePrefix = 24, 
		RULE_eSIUnitType = 25, RULE_arithmeticExpression = 26, RULE_eAdditionOperator = 27, 
		RULE_multiplicationExpression = 28, RULE_eMultiplicationOperator = 29, 
		RULE_valueExpression = 30, RULE_literalExpression = 31, RULE_literal = 32, 
		RULE_parenthesisExpression = 33, RULE_arrayExpression = 34, RULE_namedElementReference = 35, 
		RULE_stringValue = 36, RULE_longValue = 37, RULE_doubleValue = 38, RULE_booleanValue = 39;
	private static String[] makeRuleNames() {
		return new String[] {
			"declarationModel", "namedElement", "parameterGroupDeclaration", "parameterDeclaration", 
			"featureDeclaration", "featureReference", "featureGroupDeclaration", 
			"eKind", "paramType", "inlineEnumerationType", "typeReference", "arrayType", 
			"dimension", "sizeDimension", "rangeDimension", "declaredType", "rangeType", 
			"enumerationType", "enumeral", "unitSpecification", "basicUnit", "sIUnit", 
			"customUnit", "composedUnit", "ePrefix", "eSIUnitType", "arithmeticExpression", 
			"eAdditionOperator", "multiplicationExpression", "eMultiplicationOperator", 
			"valueExpression", "literalExpression", "literal", "parenthesisExpression", 
			"arrayExpression", "namedElementReference", "stringValue", "longValue", 
			"doubleValue", "booleanValue"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'model'", "'types'", "'group'", "':'", "'{'", "'}'", "'def'", 
			"','", "'='", "'required'", "'feature'", "'requires'", "'excludes'", 
			"'.'", "'sub'", "'alternative'", "'multiple'", "'('", "')'", "'['", "']'", 
			"'range'", "'enum'", "'*'", "'/'", "'**'", "'noP'", "'yotta'", "'zetta'", 
			"'exa'", "'peta'", "'tera'", "'giga'", "'mega'", "'kilo'", "'hecto'", 
			"'deca'", "'deci'", "'centi'", "'mili'", "'micro'", "'nano'", "'pico'", 
			"'femto'", "'atto'", "'zepto'", "'yocto'", "'meter'", "'gram'", "'ton'", 
			"'second'", "'ampere'", "'kelvin'", "'mole'", "'candela'", "'pascal'", 
			"'Joule'", "'+'", "'-'", "'%'"
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
			setState(80);
			match(T__0);
			setState(81);
			((DeclarationModelContext)_localctx).name = match(ID);
			setState(89);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__1) {
				{
				setState(82);
				match(T__1);
				setState(86);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__21 || _la==T__22) {
					{
					{
					setState(83);
					((DeclarationModelContext)_localctx).declaredType = declaredType();
					((DeclarationModelContext)_localctx).types.add(((DeclarationModelContext)_localctx).declaredType);
					}
					}
					setState(88);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(95);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 3080L) != 0)) {
				{
				setState(93);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__2:
					{
					setState(91);
					((DeclarationModelContext)_localctx).parameterGroupDeclaration = parameterGroupDeclaration();
					((DeclarationModelContext)_localctx).parameterGroupDeclarations.add(((DeclarationModelContext)_localctx).parameterGroupDeclaration);
					}
					break;
				case T__9:
				case T__10:
					{
					setState(92);
					((DeclarationModelContext)_localctx).featureDeclaration = featureDeclaration();
					((DeclarationModelContext)_localctx).featureDeclarations.add(((DeclarationModelContext)_localctx).featureDeclaration);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(97);
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
			setState(101);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__6:
				enterOuterAlt(_localctx, 1);
				{
				setState(98);
				parameterDeclaration();
				}
				break;
			case T__2:
				enterOuterAlt(_localctx, 2);
				{
				setState(99);
				parameterGroupDeclaration();
				}
				break;
			case T__9:
			case T__10:
				enterOuterAlt(_localctx, 3);
				{
				setState(100);
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
			setState(103);
			match(T__2);
			setState(104);
			((ParamGroupAssignStatContext)_localctx).name = match(ID);
			setState(105);
			match(T__3);
			setState(106);
			((ParamGroupAssignStatContext)_localctx).description = match(STRING);
			setState(107);
			match(T__4);
			setState(111);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__6) {
				{
				{
				setState(108);
				((ParamGroupAssignStatContext)_localctx).parameterDeclaration = parameterDeclaration();
				((ParamGroupAssignStatContext)_localctx).parameterDeclarations.add(((ParamGroupAssignStatContext)_localctx).parameterDeclaration);
				}
				}
				setState(113);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(114);
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
			setState(116);
			match(T__6);
			setState(117);
			((ParamAssignStatContext)_localctx).name = match(ID);
			setState(118);
			((ParamAssignStatContext)_localctx).type = paramType();
			setState(119);
			match(T__3);
			setState(120);
			((ParamAssignStatContext)_localctx).unit = unitSpecification();
			setState(123);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__7) {
				{
				setState(121);
				match(T__7);
				setState(122);
				((ParamAssignStatContext)_localctx).description = match(STRING);
				}
			}

			setState(127);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__8) {
				{
				setState(125);
				match(T__8);
				setState(126);
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
		public FeatureReferenceContext featureReference;
		public List<FeatureReferenceContext> requires = new ArrayList<FeatureReferenceContext>();
		public List<FeatureReferenceContext> excludes = new ArrayList<FeatureReferenceContext>();
		public ParameterGroupDeclarationContext parameterGroupDeclaration;
		public List<ParameterGroupDeclarationContext> parameterGroupDeclarations = new ArrayList<ParameterGroupDeclarationContext>();
		public FeatureGroupDeclarationContext featureGroupDeclaration;
		public List<FeatureGroupDeclarationContext> featureGroupDeclarations = new ArrayList<FeatureGroupDeclarationContext>();
		public TerminalNode ID() { return getToken(DeclarationParser.ID, 0); }
		public TerminalNode STRING() { return getToken(DeclarationParser.STRING, 0); }
		public List<FeatureReferenceContext> featureReference() {
			return getRuleContexts(FeatureReferenceContext.class);
		}
		public FeatureReferenceContext featureReference(int i) {
			return getRuleContext(FeatureReferenceContext.class,i);
		}
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
			setState(130);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__9) {
				{
				setState(129);
				((FeatureAssignStatContext)_localctx).required = match(T__9);
				}
			}

			setState(132);
			match(T__10);
			setState(133);
			((FeatureAssignStatContext)_localctx).name = match(ID);
			setState(134);
			match(T__3);
			setState(135);
			((FeatureAssignStatContext)_localctx).description = match(STRING);
			setState(173);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__4) {
				{
				setState(136);
				match(T__4);
				setState(148);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__11) {
					{
					{
					setState(137);
					match(T__11);
					setState(138);
					((FeatureAssignStatContext)_localctx).featureReference = featureReference();
					((FeatureAssignStatContext)_localctx).requires.add(((FeatureAssignStatContext)_localctx).featureReference);
					setState(143);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__7) {
						{
						{
						setState(139);
						match(T__7);
						setState(140);
						((FeatureAssignStatContext)_localctx).featureReference = featureReference();
						((FeatureAssignStatContext)_localctx).requires.add(((FeatureAssignStatContext)_localctx).featureReference);
						}
						}
						setState(145);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
					}
					setState(150);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(162);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__12) {
					{
					{
					setState(151);
					match(T__12);
					setState(152);
					((FeatureAssignStatContext)_localctx).featureReference = featureReference();
					((FeatureAssignStatContext)_localctx).excludes.add(((FeatureAssignStatContext)_localctx).featureReference);
					setState(157);
					_errHandler.sync(this);
					_la = _input.LA(1);
					while (_la==T__7) {
						{
						{
						setState(153);
						match(T__7);
						setState(154);
						((FeatureAssignStatContext)_localctx).featureReference = featureReference();
						((FeatureAssignStatContext)_localctx).excludes.add(((FeatureAssignStatContext)_localctx).featureReference);
						}
						}
						setState(159);
						_errHandler.sync(this);
						_la = _input.LA(1);
					}
					}
					}
					setState(164);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(169);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__2 || _la==T__14) {
					{
					setState(167);
					_errHandler.sync(this);
					switch (_input.LA(1)) {
					case T__2:
						{
						setState(165);
						((FeatureAssignStatContext)_localctx).parameterGroupDeclaration = parameterGroupDeclaration();
						((FeatureAssignStatContext)_localctx).parameterGroupDeclarations.add(((FeatureAssignStatContext)_localctx).parameterGroupDeclaration);
						}
						break;
					case T__14:
						{
						setState(166);
						((FeatureAssignStatContext)_localctx).featureGroupDeclaration = featureGroupDeclaration();
						((FeatureAssignStatContext)_localctx).featureGroupDeclarations.add(((FeatureAssignStatContext)_localctx).featureGroupDeclaration);
						}
						break;
					default:
						throw new NoViableAltException(this);
					}
					}
					setState(171);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(172);
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
	public static class FeatureReferenceContext extends ParserRuleContext {
		public Token ID;
		public List<Token> elements = new ArrayList<Token>();
		public List<TerminalNode> ID() { return getTokens(DeclarationParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(DeclarationParser.ID, i);
		}
		public FeatureReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_featureReference; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).enterFeatureReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof DeclarationListener ) ((DeclarationListener)listener).exitFeatureReference(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof DeclarationVisitor ) return ((DeclarationVisitor<? extends T>)visitor).visitFeatureReference(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FeatureReferenceContext featureReference() throws RecognitionException {
		FeatureReferenceContext _localctx = new FeatureReferenceContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_featureReference);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(175);
			((FeatureReferenceContext)_localctx).ID = match(ID);
			((FeatureReferenceContext)_localctx).elements.add(((FeatureReferenceContext)_localctx).ID);
			setState(180);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__13) {
				{
				{
				setState(176);
				match(T__13);
				setState(177);
				((FeatureReferenceContext)_localctx).ID = match(ID);
				((FeatureReferenceContext)_localctx).elements.add(((FeatureReferenceContext)_localctx).ID);
				}
				}
				setState(182);
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
		enterRule(_localctx, 12, RULE_featureGroupDeclaration);
		int _la;
		try {
			_localctx = new FeatureGroupAssignStatContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(183);
			match(T__14);
			setState(184);
			((FeatureGroupAssignStatContext)_localctx).kind = eKind();
			setState(188);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__9 || _la==T__10) {
				{
				{
				setState(185);
				((FeatureGroupAssignStatContext)_localctx).featureDeclaration = featureDeclaration();
				((FeatureGroupAssignStatContext)_localctx).featureDeclarations.add(((FeatureGroupAssignStatContext)_localctx).featureDeclaration);
				}
				}
				setState(190);
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
		enterRule(_localctx, 14, RULE_eKind);
		try {
			setState(193);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__15:
				enterOuterAlt(_localctx, 1);
				{
				setState(191);
				((EKindContext)_localctx).alternative = match(T__15);
				}
				break;
			case T__16:
				enterOuterAlt(_localctx, 2);
				{
				setState(192);
				((EKindContext)_localctx).multiple = match(T__16);
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
		enterRule(_localctx, 16, RULE_paramType);
		try {
			setState(198);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,19,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(195);
				typeReference();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(196);
				inlineEnumerationType();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(197);
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
		enterRule(_localctx, 18, RULE_inlineEnumerationType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(200);
			match(T__17);
			setState(201);
			((InlineEnumerationTypeContext)_localctx).enumeral = enumeral();
			((InlineEnumerationTypeContext)_localctx).values.add(((InlineEnumerationTypeContext)_localctx).enumeral);
			setState(206);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__7) {
				{
				{
				setState(202);
				match(T__7);
				setState(203);
				((InlineEnumerationTypeContext)_localctx).enumeral = enumeral();
				((InlineEnumerationTypeContext)_localctx).values.add(((InlineEnumerationTypeContext)_localctx).enumeral);
				}
				}
				setState(208);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(209);
			match(T__18);
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
		enterRule(_localctx, 20, RULE_typeReference);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(211);
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
		enterRule(_localctx, 22, RULE_arrayType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(213);
			((ArrayTypeContext)_localctx).type = match(ID);
			setState(214);
			match(T__19);
			setState(215);
			((ArrayTypeContext)_localctx).dimension = dimension();
			((ArrayTypeContext)_localctx).dimensions.add(((ArrayTypeContext)_localctx).dimension);
			setState(220);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__7) {
				{
				{
				setState(216);
				match(T__7);
				setState(217);
				((ArrayTypeContext)_localctx).dimension = dimension();
				((ArrayTypeContext)_localctx).dimensions.add(((ArrayTypeContext)_localctx).dimension);
				}
				}
				setState(222);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(223);
			match(T__20);
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
		enterRule(_localctx, 24, RULE_dimension);
		try {
			setState(227);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,22,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(225);
				sizeDimension();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(226);
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
		enterRule(_localctx, 26, RULE_sizeDimension);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(230);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELONG) {
				{
				setState(229);
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
		enterRule(_localctx, 28, RULE_rangeDimension);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(233);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELONG) {
				{
				setState(232);
				((RangeDimensionContext)_localctx).lowerBound = match(ELONG);
				}
			}

			setState(235);
			match(T__3);
			setState(237);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==ELONG) {
				{
				setState(236);
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
		enterRule(_localctx, 30, RULE_declaredType);
		try {
			setState(241);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__21:
				enterOuterAlt(_localctx, 1);
				{
				setState(239);
				rangeType();
				}
				break;
			case T__22:
				enterOuterAlt(_localctx, 2);
				{
				setState(240);
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
		enterRule(_localctx, 32, RULE_rangeType);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(243);
			match(T__21);
			setState(244);
			((RangeTypeContext)_localctx).name = match(ID);
			setState(245);
			((RangeTypeContext)_localctx).type = match(ID);
			setState(246);
			match(T__19);
			setState(247);
			((RangeTypeContext)_localctx).minimum = literal();
			setState(248);
			match(T__3);
			setState(249);
			((RangeTypeContext)_localctx).maximum = literal();
			setState(250);
			match(T__20);
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
		enterRule(_localctx, 34, RULE_enumerationType);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(252);
			match(T__22);
			setState(253);
			((EnumerationTypeContext)_localctx).name = match(ID);
			setState(254);
			match(T__4);
			setState(255);
			((EnumerationTypeContext)_localctx).enumeral = enumeral();
			((EnumerationTypeContext)_localctx).values.add(((EnumerationTypeContext)_localctx).enumeral);
			setState(260);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__7) {
				{
				{
				setState(256);
				match(T__7);
				setState(257);
				((EnumerationTypeContext)_localctx).enumeral = enumeral();
				((EnumerationTypeContext)_localctx).values.add(((EnumerationTypeContext)_localctx).enumeral);
				}
				}
				setState(262);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(263);
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
		enterRule(_localctx, 36, RULE_enumeral);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(265);
			((EnumeralContext)_localctx).name = match(ID);
			setState(268);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__8) {
				{
				setState(266);
				match(T__8);
				setState(267);
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
		enterRule(_localctx, 38, RULE_unitSpecification);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(270);
			((UnitSpecificationContext)_localctx).composedUnit = composedUnit();
			((UnitSpecificationContext)_localctx).units.add(((UnitSpecificationContext)_localctx).composedUnit);
			setState(275);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__23) {
				{
				{
				setState(271);
				match(T__23);
				setState(272);
				((UnitSpecificationContext)_localctx).composedUnit = composedUnit();
				((UnitSpecificationContext)_localctx).units.add(((UnitSpecificationContext)_localctx).composedUnit);
				}
				}
				setState(277);
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
		enterRule(_localctx, 40, RULE_basicUnit);
		try {
			setState(284);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
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
			case T__56:
				enterOuterAlt(_localctx, 1);
				{
				setState(278);
				sIUnit();
				}
				break;
			case STRING:
				enterOuterAlt(_localctx, 2);
				{
				setState(279);
				customUnit();
				}
				break;
			case T__17:
				enterOuterAlt(_localctx, 3);
				{
				setState(280);
				match(T__17);
				setState(281);
				unitSpecification();
				setState(282);
				match(T__18);
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
		enterRule(_localctx, 42, RULE_sIUnit);
		int _la;
		try {
			_localctx = new SiunitContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(287);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 281474842492928L) != 0)) {
				{
				setState(286);
				((SiunitContext)_localctx).prefix = ePrefix();
				}
			}

			setState(289);
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
		enterRule(_localctx, 44, RULE_customUnit);
		try {
			_localctx = new CustomunitContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(291);
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
		enterRule(_localctx, 46, RULE_composedUnit);
		try {
			setState(301);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,33,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(293);
				((ComposedUnitContext)_localctx).numerator = basicUnit();
				setState(298);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__24:
					{
					{
					setState(294);
					match(T__24);
					setState(295);
					((ComposedUnitContext)_localctx).denominator = basicUnit();
					}
					}
					break;
				case T__25:
					{
					{
					setState(296);
					match(T__25);
					setState(297);
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
				setState(300);
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
		enterRule(_localctx, 48, RULE_ePrefix);
		try {
			setState(324);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__26:
				enterOuterAlt(_localctx, 1);
				{
				setState(303);
				((EPrefixContext)_localctx).noP = match(T__26);
				}
				break;
			case T__27:
				enterOuterAlt(_localctx, 2);
				{
				setState(304);
				((EPrefixContext)_localctx).yotta = match(T__27);
				}
				break;
			case T__28:
				enterOuterAlt(_localctx, 3);
				{
				setState(305);
				((EPrefixContext)_localctx).zetta = match(T__28);
				}
				break;
			case T__29:
				enterOuterAlt(_localctx, 4);
				{
				setState(306);
				((EPrefixContext)_localctx).exa = match(T__29);
				}
				break;
			case T__30:
				enterOuterAlt(_localctx, 5);
				{
				setState(307);
				((EPrefixContext)_localctx).peta = match(T__30);
				}
				break;
			case T__31:
				enterOuterAlt(_localctx, 6);
				{
				setState(308);
				((EPrefixContext)_localctx).tera = match(T__31);
				}
				break;
			case T__32:
				enterOuterAlt(_localctx, 7);
				{
				setState(309);
				((EPrefixContext)_localctx).giga = match(T__32);
				}
				break;
			case T__33:
				enterOuterAlt(_localctx, 8);
				{
				setState(310);
				((EPrefixContext)_localctx).mega = match(T__33);
				}
				break;
			case T__34:
				enterOuterAlt(_localctx, 9);
				{
				setState(311);
				((EPrefixContext)_localctx).kilo = match(T__34);
				}
				break;
			case T__35:
				enterOuterAlt(_localctx, 10);
				{
				setState(312);
				((EPrefixContext)_localctx).hecto = match(T__35);
				}
				break;
			case T__36:
				enterOuterAlt(_localctx, 11);
				{
				setState(313);
				((EPrefixContext)_localctx).deca = match(T__36);
				}
				break;
			case T__37:
				enterOuterAlt(_localctx, 12);
				{
				setState(314);
				((EPrefixContext)_localctx).deci = match(T__37);
				}
				break;
			case T__38:
				enterOuterAlt(_localctx, 13);
				{
				setState(315);
				((EPrefixContext)_localctx).centi = match(T__38);
				}
				break;
			case T__39:
				enterOuterAlt(_localctx, 14);
				{
				setState(316);
				((EPrefixContext)_localctx).mili = match(T__39);
				}
				break;
			case T__40:
				enterOuterAlt(_localctx, 15);
				{
				setState(317);
				((EPrefixContext)_localctx).micro = match(T__40);
				}
				break;
			case T__41:
				enterOuterAlt(_localctx, 16);
				{
				setState(318);
				((EPrefixContext)_localctx).nano = match(T__41);
				}
				break;
			case T__42:
				enterOuterAlt(_localctx, 17);
				{
				setState(319);
				((EPrefixContext)_localctx).pico = match(T__42);
				}
				break;
			case T__43:
				enterOuterAlt(_localctx, 18);
				{
				setState(320);
				((EPrefixContext)_localctx).femto = match(T__43);
				}
				break;
			case T__44:
				enterOuterAlt(_localctx, 19);
				{
				setState(321);
				((EPrefixContext)_localctx).atto = match(T__44);
				}
				break;
			case T__45:
				enterOuterAlt(_localctx, 20);
				{
				setState(322);
				((EPrefixContext)_localctx).zepto = match(T__45);
				}
				break;
			case T__46:
				enterOuterAlt(_localctx, 21);
				{
				setState(323);
				((EPrefixContext)_localctx).yocto = match(T__46);
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
		enterRule(_localctx, 50, RULE_eSIUnitType);
		try {
			setState(336);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__47:
				enterOuterAlt(_localctx, 1);
				{
				setState(326);
				((ESIUnitTypeContext)_localctx).meter = match(T__47);
				}
				break;
			case T__48:
				enterOuterAlt(_localctx, 2);
				{
				setState(327);
				((ESIUnitTypeContext)_localctx).gram = match(T__48);
				}
				break;
			case T__49:
				enterOuterAlt(_localctx, 3);
				{
				setState(328);
				((ESIUnitTypeContext)_localctx).ton = match(T__49);
				}
				break;
			case T__50:
				enterOuterAlt(_localctx, 4);
				{
				setState(329);
				((ESIUnitTypeContext)_localctx).second = match(T__50);
				}
				break;
			case T__51:
				enterOuterAlt(_localctx, 5);
				{
				setState(330);
				((ESIUnitTypeContext)_localctx).ampere = match(T__51);
				}
				break;
			case T__52:
				enterOuterAlt(_localctx, 6);
				{
				setState(331);
				((ESIUnitTypeContext)_localctx).kelvin = match(T__52);
				}
				break;
			case T__53:
				enterOuterAlt(_localctx, 7);
				{
				setState(332);
				((ESIUnitTypeContext)_localctx).mole = match(T__53);
				}
				break;
			case T__54:
				enterOuterAlt(_localctx, 8);
				{
				setState(333);
				((ESIUnitTypeContext)_localctx).candela = match(T__54);
				}
				break;
			case T__55:
				enterOuterAlt(_localctx, 9);
				{
				setState(334);
				((ESIUnitTypeContext)_localctx).pascal = match(T__55);
				}
				break;
			case T__56:
				enterOuterAlt(_localctx, 10);
				{
				setState(335);
				((ESIUnitTypeContext)_localctx).joule = match(T__56);
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
		enterRule(_localctx, 52, RULE_arithmeticExpression);
		try {
			setState(343);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,36,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(338);
				((ArithmeticExpressionContext)_localctx).left = multiplicationExpression();
				setState(339);
				((ArithmeticExpressionContext)_localctx).op = eAdditionOperator();
				setState(340);
				((ArithmeticExpressionContext)_localctx).right = arithmeticExpression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(342);
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
		enterRule(_localctx, 54, RULE_eAdditionOperator);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(345);
			_la = _input.LA(1);
			if ( !(_la==T__57 || _la==T__58) ) {
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
		enterRule(_localctx, 56, RULE_multiplicationExpression);
		try {
			setState(352);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,37,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(347);
				((MultiplicationExpressionContext)_localctx).left = valueExpression();
				setState(348);
				((MultiplicationExpressionContext)_localctx).op = eMultiplicationOperator();
				setState(349);
				((MultiplicationExpressionContext)_localctx).right = multiplicationExpression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(351);
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
		enterRule(_localctx, 58, RULE_eMultiplicationOperator);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(354);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 1152921504657178624L) != 0)) ) {
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
		enterRule(_localctx, 60, RULE_valueExpression);
		try {
			setState(360);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__17:
				enterOuterAlt(_localctx, 1);
				{
				setState(356);
				parenthesisExpression();
				}
				break;
			case ID:
				enterOuterAlt(_localctx, 2);
				{
				setState(357);
				namedElementReference();
				}
				break;
			case T__19:
				enterOuterAlt(_localctx, 3);
				{
				setState(358);
				arrayExpression();
				}
				break;
			case ELONG:
			case EDOUBLE:
			case EBoolean:
			case STRING:
				enterOuterAlt(_localctx, 4);
				{
				setState(359);
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
		enterRule(_localctx, 62, RULE_literalExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(362);
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
		enterRule(_localctx, 64, RULE_literal);
		try {
			setState(368);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(364);
				stringValue();
				}
				break;
			case ELONG:
				enterOuterAlt(_localctx, 2);
				{
				setState(365);
				longValue();
				}
				break;
			case EDOUBLE:
				enterOuterAlt(_localctx, 3);
				{
				setState(366);
				doubleValue();
				}
				break;
			case EBoolean:
				enterOuterAlt(_localctx, 4);
				{
				setState(367);
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
		enterRule(_localctx, 66, RULE_parenthesisExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(370);
			match(T__17);
			setState(371);
			((ParenthesisExpressionContext)_localctx).expression = arithmeticExpression();
			setState(372);
			match(T__18);
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
		enterRule(_localctx, 68, RULE_arrayExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(374);
			match(T__19);
			setState(383);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (((((_la - 18)) & ~0x3f) == 0 && ((1L << (_la - 18)) & 413416372043781L) != 0)) {
				{
				setState(375);
				((ArrayExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
				((ArrayExpressionContext)_localctx).elements.add(((ArrayExpressionContext)_localctx).arithmeticExpression);
				setState(380);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__7) {
					{
					{
					setState(376);
					match(T__7);
					setState(377);
					((ArrayExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
					((ArrayExpressionContext)_localctx).elements.add(((ArrayExpressionContext)_localctx).arithmeticExpression);
					}
					}
					setState(382);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(385);
			match(T__20);
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
		public Token ID;
		public List<Token> elements = new ArrayList<Token>();
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
		enterRule(_localctx, 70, RULE_namedElementReference);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(387);
			((NamedElementReferenceContext)_localctx).ID = match(ID);
			((NamedElementReferenceContext)_localctx).elements.add(((NamedElementReferenceContext)_localctx).ID);
			setState(392);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__13) {
				{
				{
				setState(388);
				match(T__13);
				setState(389);
				((NamedElementReferenceContext)_localctx).ID = match(ID);
				((NamedElementReferenceContext)_localctx).elements.add(((NamedElementReferenceContext)_localctx).ID);
				}
				}
				setState(394);
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
		enterRule(_localctx, 72, RULE_stringValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(395);
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
		enterRule(_localctx, 74, RULE_longValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(397);
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
		enterRule(_localctx, 76, RULE_doubleValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(399);
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
		enterRule(_localctx, 78, RULE_booleanValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(401);
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
		"\u0004\u0001F\u0194\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
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
		"#\u0007#\u0002$\u0007$\u0002%\u0007%\u0002&\u0007&\u0002\'\u0007\'\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0005\u0000U\b\u0000\n\u0000"+
		"\f\u0000X\t\u0000\u0003\u0000Z\b\u0000\u0001\u0000\u0001\u0000\u0005\u0000"+
		"^\b\u0000\n\u0000\f\u0000a\t\u0000\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0003\u0001f\b\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001\u0002"+
		"\u0001\u0002\u0001\u0002\u0005\u0002n\b\u0002\n\u0002\f\u0002q\t\u0002"+
		"\u0001\u0002\u0001\u0002\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0001\u0003\u0003\u0003|\b\u0003\u0001\u0003"+
		"\u0001\u0003\u0003\u0003\u0080\b\u0003\u0001\u0004\u0003\u0004\u0083\b"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0005\u0004\u008e\b\u0004\n"+
		"\u0004\f\u0004\u0091\t\u0004\u0005\u0004\u0093\b\u0004\n\u0004\f\u0004"+
		"\u0096\t\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0005\u0004"+
		"\u009c\b\u0004\n\u0004\f\u0004\u009f\t\u0004\u0005\u0004\u00a1\b\u0004"+
		"\n\u0004\f\u0004\u00a4\t\u0004\u0001\u0004\u0001\u0004\u0005\u0004\u00a8"+
		"\b\u0004\n\u0004\f\u0004\u00ab\t\u0004\u0001\u0004\u0003\u0004\u00ae\b"+
		"\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u00b3\b\u0005\n"+
		"\u0005\f\u0005\u00b6\t\u0005\u0001\u0006\u0001\u0006\u0001\u0006\u0005"+
		"\u0006\u00bb\b\u0006\n\u0006\f\u0006\u00be\t\u0006\u0001\u0007\u0001\u0007"+
		"\u0003\u0007\u00c2\b\u0007\u0001\b\u0001\b\u0001\b\u0003\b\u00c7\b\b\u0001"+
		"\t\u0001\t\u0001\t\u0001\t\u0005\t\u00cd\b\t\n\t\f\t\u00d0\t\t\u0001\t"+
		"\u0001\t\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001\u000b\u0001\u000b"+
		"\u0001\u000b\u0005\u000b\u00db\b\u000b\n\u000b\f\u000b\u00de\t\u000b\u0001"+
		"\u000b\u0001\u000b\u0001\f\u0001\f\u0003\f\u00e4\b\f\u0001\r\u0003\r\u00e7"+
		"\b\r\u0001\u000e\u0003\u000e\u00ea\b\u000e\u0001\u000e\u0001\u000e\u0003"+
		"\u000e\u00ee\b\u000e\u0001\u000f\u0001\u000f\u0003\u000f\u00f2\b\u000f"+
		"\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0010\u0001\u0010\u0001\u0010\u0001\u0011\u0001\u0011\u0001\u0011"+
		"\u0001\u0011\u0001\u0011\u0001\u0011\u0005\u0011\u0103\b\u0011\n\u0011"+
		"\f\u0011\u0106\t\u0011\u0001\u0011\u0001\u0011\u0001\u0012\u0001\u0012"+
		"\u0001\u0012\u0003\u0012\u010d\b\u0012\u0001\u0013\u0001\u0013\u0001\u0013"+
		"\u0005\u0013\u0112\b\u0013\n\u0013\f\u0013\u0115\t\u0013\u0001\u0014\u0001"+
		"\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0003\u0014\u011d"+
		"\b\u0014\u0001\u0015\u0003\u0015\u0120\b\u0015\u0001\u0015\u0001\u0015"+
		"\u0001\u0016\u0001\u0016\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017"+
		"\u0001\u0017\u0003\u0017\u012b\b\u0017\u0001\u0017\u0003\u0017\u012e\b"+
		"\u0017\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001"+
		"\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001"+
		"\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001"+
		"\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0003\u0018\u0145\b\u0018\u0001"+
		"\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001"+
		"\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0003\u0019\u0151\b\u0019\u0001"+
		"\u001a\u0001\u001a\u0001\u001a\u0001\u001a\u0001\u001a\u0003\u001a\u0158"+
		"\b\u001a\u0001\u001b\u0001\u001b\u0001\u001c\u0001\u001c\u0001\u001c\u0001"+
		"\u001c\u0001\u001c\u0003\u001c\u0161\b\u001c\u0001\u001d\u0001\u001d\u0001"+
		"\u001e\u0001\u001e\u0001\u001e\u0001\u001e\u0003\u001e\u0169\b\u001e\u0001"+
		"\u001f\u0001\u001f\u0001 \u0001 \u0001 \u0001 \u0003 \u0171\b \u0001!"+
		"\u0001!\u0001!\u0001!\u0001\"\u0001\"\u0001\"\u0001\"\u0005\"\u017b\b"+
		"\"\n\"\f\"\u017e\t\"\u0003\"\u0180\b\"\u0001\"\u0001\"\u0001#\u0001#\u0001"+
		"#\u0005#\u0187\b#\n#\f#\u018a\t#\u0001$\u0001$\u0001%\u0001%\u0001&\u0001"+
		"&\u0001\'\u0001\'\u0001\'\u0000\u0000(\u0000\u0002\u0004\u0006\b\n\f\u000e"+
		"\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e \"$&(*,.02468:<>@BDF"+
		"HJLN\u0000\u0002\u0001\u0000:;\u0002\u0000\u0018\u0019<<\u01b8\u0000P"+
		"\u0001\u0000\u0000\u0000\u0002e\u0001\u0000\u0000\u0000\u0004g\u0001\u0000"+
		"\u0000\u0000\u0006t\u0001\u0000\u0000\u0000\b\u0082\u0001\u0000\u0000"+
		"\u0000\n\u00af\u0001\u0000\u0000\u0000\f\u00b7\u0001\u0000\u0000\u0000"+
		"\u000e\u00c1\u0001\u0000\u0000\u0000\u0010\u00c6\u0001\u0000\u0000\u0000"+
		"\u0012\u00c8\u0001\u0000\u0000\u0000\u0014\u00d3\u0001\u0000\u0000\u0000"+
		"\u0016\u00d5\u0001\u0000\u0000\u0000\u0018\u00e3\u0001\u0000\u0000\u0000"+
		"\u001a\u00e6\u0001\u0000\u0000\u0000\u001c\u00e9\u0001\u0000\u0000\u0000"+
		"\u001e\u00f1\u0001\u0000\u0000\u0000 \u00f3\u0001\u0000\u0000\u0000\""+
		"\u00fc\u0001\u0000\u0000\u0000$\u0109\u0001\u0000\u0000\u0000&\u010e\u0001"+
		"\u0000\u0000\u0000(\u011c\u0001\u0000\u0000\u0000*\u011f\u0001\u0000\u0000"+
		"\u0000,\u0123\u0001\u0000\u0000\u0000.\u012d\u0001\u0000\u0000\u00000"+
		"\u0144\u0001\u0000\u0000\u00002\u0150\u0001\u0000\u0000\u00004\u0157\u0001"+
		"\u0000\u0000\u00006\u0159\u0001\u0000\u0000\u00008\u0160\u0001\u0000\u0000"+
		"\u0000:\u0162\u0001\u0000\u0000\u0000<\u0168\u0001\u0000\u0000\u0000>"+
		"\u016a\u0001\u0000\u0000\u0000@\u0170\u0001\u0000\u0000\u0000B\u0172\u0001"+
		"\u0000\u0000\u0000D\u0176\u0001\u0000\u0000\u0000F\u0183\u0001\u0000\u0000"+
		"\u0000H\u018b\u0001\u0000\u0000\u0000J\u018d\u0001\u0000\u0000\u0000L"+
		"\u018f\u0001\u0000\u0000\u0000N\u0191\u0001\u0000\u0000\u0000PQ\u0005"+
		"\u0001\u0000\u0000QY\u0005@\u0000\u0000RV\u0005\u0002\u0000\u0000SU\u0003"+
		"\u001e\u000f\u0000TS\u0001\u0000\u0000\u0000UX\u0001\u0000\u0000\u0000"+
		"VT\u0001\u0000\u0000\u0000VW\u0001\u0000\u0000\u0000WZ\u0001\u0000\u0000"+
		"\u0000XV\u0001\u0000\u0000\u0000YR\u0001\u0000\u0000\u0000YZ\u0001\u0000"+
		"\u0000\u0000Z_\u0001\u0000\u0000\u0000[^\u0003\u0004\u0002\u0000\\^\u0003"+
		"\b\u0004\u0000][\u0001\u0000\u0000\u0000]\\\u0001\u0000\u0000\u0000^a"+
		"\u0001\u0000\u0000\u0000_]\u0001\u0000\u0000\u0000_`\u0001\u0000\u0000"+
		"\u0000`\u0001\u0001\u0000\u0000\u0000a_\u0001\u0000\u0000\u0000bf\u0003"+
		"\u0006\u0003\u0000cf\u0003\u0004\u0002\u0000df\u0003\b\u0004\u0000eb\u0001"+
		"\u0000\u0000\u0000ec\u0001\u0000\u0000\u0000ed\u0001\u0000\u0000\u0000"+
		"f\u0003\u0001\u0000\u0000\u0000gh\u0005\u0003\u0000\u0000hi\u0005@\u0000"+
		"\u0000ij\u0005\u0004\u0000\u0000jk\u0005B\u0000\u0000ko\u0005\u0005\u0000"+
		"\u0000ln\u0003\u0006\u0003\u0000ml\u0001\u0000\u0000\u0000nq\u0001\u0000"+
		"\u0000\u0000om\u0001\u0000\u0000\u0000op\u0001\u0000\u0000\u0000pr\u0001"+
		"\u0000\u0000\u0000qo\u0001\u0000\u0000\u0000rs\u0005\u0006\u0000\u0000"+
		"s\u0005\u0001\u0000\u0000\u0000tu\u0005\u0007\u0000\u0000uv\u0005@\u0000"+
		"\u0000vw\u0003\u0010\b\u0000wx\u0005\u0004\u0000\u0000x{\u0003&\u0013"+
		"\u0000yz\u0005\b\u0000\u0000z|\u0005B\u0000\u0000{y\u0001\u0000\u0000"+
		"\u0000{|\u0001\u0000\u0000\u0000|\u007f\u0001\u0000\u0000\u0000}~\u0005"+
		"\t\u0000\u0000~\u0080\u00034\u001a\u0000\u007f}\u0001\u0000\u0000\u0000"+
		"\u007f\u0080\u0001\u0000\u0000\u0000\u0080\u0007\u0001\u0000\u0000\u0000"+
		"\u0081\u0083\u0005\n\u0000\u0000\u0082\u0081\u0001\u0000\u0000\u0000\u0082"+
		"\u0083\u0001\u0000\u0000\u0000\u0083\u0084\u0001\u0000\u0000\u0000\u0084"+
		"\u0085\u0005\u000b\u0000\u0000\u0085\u0086\u0005@\u0000\u0000\u0086\u0087"+
		"\u0005\u0004\u0000\u0000\u0087\u00ad\u0005B\u0000\u0000\u0088\u0094\u0005"+
		"\u0005\u0000\u0000\u0089\u008a\u0005\f\u0000\u0000\u008a\u008f\u0003\n"+
		"\u0005\u0000\u008b\u008c\u0005\b\u0000\u0000\u008c\u008e\u0003\n\u0005"+
		"\u0000\u008d\u008b\u0001\u0000\u0000\u0000\u008e\u0091\u0001\u0000\u0000"+
		"\u0000\u008f\u008d\u0001\u0000\u0000\u0000\u008f\u0090\u0001\u0000\u0000"+
		"\u0000\u0090\u0093\u0001\u0000\u0000\u0000\u0091\u008f\u0001\u0000\u0000"+
		"\u0000\u0092\u0089\u0001\u0000\u0000\u0000\u0093\u0096\u0001\u0000\u0000"+
		"\u0000\u0094\u0092\u0001\u0000\u0000\u0000\u0094\u0095\u0001\u0000\u0000"+
		"\u0000\u0095\u00a2\u0001\u0000\u0000\u0000\u0096\u0094\u0001\u0000\u0000"+
		"\u0000\u0097\u0098\u0005\r\u0000\u0000\u0098\u009d\u0003\n\u0005\u0000"+
		"\u0099\u009a\u0005\b\u0000\u0000\u009a\u009c\u0003\n\u0005\u0000\u009b"+
		"\u0099\u0001\u0000\u0000\u0000\u009c\u009f\u0001\u0000\u0000\u0000\u009d"+
		"\u009b\u0001\u0000\u0000\u0000\u009d\u009e\u0001\u0000\u0000\u0000\u009e"+
		"\u00a1\u0001\u0000\u0000\u0000\u009f\u009d\u0001\u0000\u0000\u0000\u00a0"+
		"\u0097\u0001\u0000\u0000\u0000\u00a1\u00a4\u0001\u0000\u0000\u0000\u00a2"+
		"\u00a0\u0001\u0000\u0000\u0000\u00a2\u00a3\u0001\u0000\u0000\u0000\u00a3"+
		"\u00a9\u0001\u0000\u0000\u0000\u00a4\u00a2\u0001\u0000\u0000\u0000\u00a5"+
		"\u00a8\u0003\u0004\u0002\u0000\u00a6\u00a8\u0003\f\u0006\u0000\u00a7\u00a5"+
		"\u0001\u0000\u0000\u0000\u00a7\u00a6\u0001\u0000\u0000\u0000\u00a8\u00ab"+
		"\u0001\u0000\u0000\u0000\u00a9\u00a7\u0001\u0000\u0000\u0000\u00a9\u00aa"+
		"\u0001\u0000\u0000\u0000\u00aa\u00ac\u0001\u0000\u0000\u0000\u00ab\u00a9"+
		"\u0001\u0000\u0000\u0000\u00ac\u00ae\u0005\u0006\u0000\u0000\u00ad\u0088"+
		"\u0001\u0000\u0000\u0000\u00ad\u00ae\u0001\u0000\u0000\u0000\u00ae\t\u0001"+
		"\u0000\u0000\u0000\u00af\u00b4\u0005@\u0000\u0000\u00b0\u00b1\u0005\u000e"+
		"\u0000\u0000\u00b1\u00b3\u0005@\u0000\u0000\u00b2\u00b0\u0001\u0000\u0000"+
		"\u0000\u00b3\u00b6\u0001\u0000\u0000\u0000\u00b4\u00b2\u0001\u0000\u0000"+
		"\u0000\u00b4\u00b5\u0001\u0000\u0000\u0000\u00b5\u000b\u0001\u0000\u0000"+
		"\u0000\u00b6\u00b4\u0001\u0000\u0000\u0000\u00b7\u00b8\u0005\u000f\u0000"+
		"\u0000\u00b8\u00bc\u0003\u000e\u0007\u0000\u00b9\u00bb\u0003\b\u0004\u0000"+
		"\u00ba\u00b9\u0001\u0000\u0000\u0000\u00bb\u00be\u0001\u0000\u0000\u0000"+
		"\u00bc\u00ba\u0001\u0000\u0000\u0000\u00bc\u00bd\u0001\u0000\u0000\u0000"+
		"\u00bd\r\u0001\u0000\u0000\u0000\u00be\u00bc\u0001\u0000\u0000\u0000\u00bf"+
		"\u00c2\u0005\u0010\u0000\u0000\u00c0\u00c2\u0005\u0011\u0000\u0000\u00c1"+
		"\u00bf\u0001\u0000\u0000\u0000\u00c1\u00c0\u0001\u0000\u0000\u0000\u00c2"+
		"\u000f\u0001\u0000\u0000\u0000\u00c3\u00c7\u0003\u0014\n\u0000\u00c4\u00c7"+
		"\u0003\u0012\t\u0000\u00c5\u00c7\u0003\u0016\u000b\u0000\u00c6\u00c3\u0001"+
		"\u0000\u0000\u0000\u00c6\u00c4\u0001\u0000\u0000\u0000\u00c6\u00c5\u0001"+
		"\u0000\u0000\u0000\u00c7\u0011\u0001\u0000\u0000\u0000\u00c8\u00c9\u0005"+
		"\u0012\u0000\u0000\u00c9\u00ce\u0003$\u0012\u0000\u00ca\u00cb\u0005\b"+
		"\u0000\u0000\u00cb\u00cd\u0003$\u0012\u0000\u00cc\u00ca\u0001\u0000\u0000"+
		"\u0000\u00cd\u00d0\u0001\u0000\u0000\u0000\u00ce\u00cc\u0001\u0000\u0000"+
		"\u0000\u00ce\u00cf\u0001\u0000\u0000\u0000\u00cf\u00d1\u0001\u0000\u0000"+
		"\u0000\u00d0\u00ce\u0001\u0000\u0000\u0000\u00d1\u00d2\u0005\u0013\u0000"+
		"\u0000\u00d2\u0013\u0001\u0000\u0000\u0000\u00d3\u00d4\u0005@\u0000\u0000"+
		"\u00d4\u0015\u0001\u0000\u0000\u0000\u00d5\u00d6\u0005@\u0000\u0000\u00d6"+
		"\u00d7\u0005\u0014\u0000\u0000\u00d7\u00dc\u0003\u0018\f\u0000\u00d8\u00d9"+
		"\u0005\b\u0000\u0000\u00d9\u00db\u0003\u0018\f\u0000\u00da\u00d8\u0001"+
		"\u0000\u0000\u0000\u00db\u00de\u0001\u0000\u0000\u0000\u00dc\u00da\u0001"+
		"\u0000\u0000\u0000\u00dc\u00dd\u0001\u0000\u0000\u0000\u00dd\u00df\u0001"+
		"\u0000\u0000\u0000\u00de\u00dc\u0001\u0000\u0000\u0000\u00df\u00e0\u0005"+
		"\u0015\u0000\u0000\u00e0\u0017\u0001\u0000\u0000\u0000\u00e1\u00e4\u0003"+
		"\u001a\r\u0000\u00e2\u00e4\u0003\u001c\u000e\u0000\u00e3\u00e1\u0001\u0000"+
		"\u0000\u0000\u00e3\u00e2\u0001\u0000\u0000\u0000\u00e4\u0019\u0001\u0000"+
		"\u0000\u0000\u00e5\u00e7\u0005=\u0000\u0000\u00e6\u00e5\u0001\u0000\u0000"+
		"\u0000\u00e6\u00e7\u0001\u0000\u0000\u0000\u00e7\u001b\u0001\u0000\u0000"+
		"\u0000\u00e8\u00ea\u0005=\u0000\u0000\u00e9\u00e8\u0001\u0000\u0000\u0000"+
		"\u00e9\u00ea\u0001\u0000\u0000\u0000\u00ea\u00eb\u0001\u0000\u0000\u0000"+
		"\u00eb\u00ed\u0005\u0004\u0000\u0000\u00ec\u00ee\u0005=\u0000\u0000\u00ed"+
		"\u00ec\u0001\u0000\u0000\u0000\u00ed\u00ee\u0001\u0000\u0000\u0000\u00ee"+
		"\u001d\u0001\u0000\u0000\u0000\u00ef\u00f2\u0003 \u0010\u0000\u00f0\u00f2"+
		"\u0003\"\u0011\u0000\u00f1\u00ef\u0001\u0000\u0000\u0000\u00f1\u00f0\u0001"+
		"\u0000\u0000\u0000\u00f2\u001f\u0001\u0000\u0000\u0000\u00f3\u00f4\u0005"+
		"\u0016\u0000\u0000\u00f4\u00f5\u0005@\u0000\u0000\u00f5\u00f6\u0005@\u0000"+
		"\u0000\u00f6\u00f7\u0005\u0014\u0000\u0000\u00f7\u00f8\u0003@ \u0000\u00f8"+
		"\u00f9\u0005\u0004\u0000\u0000\u00f9\u00fa\u0003@ \u0000\u00fa\u00fb\u0005"+
		"\u0015\u0000\u0000\u00fb!\u0001\u0000\u0000\u0000\u00fc\u00fd\u0005\u0017"+
		"\u0000\u0000\u00fd\u00fe\u0005@\u0000\u0000\u00fe\u00ff\u0005\u0005\u0000"+
		"\u0000\u00ff\u0104\u0003$\u0012\u0000\u0100\u0101\u0005\b\u0000\u0000"+
		"\u0101\u0103\u0003$\u0012\u0000\u0102\u0100\u0001\u0000\u0000\u0000\u0103"+
		"\u0106\u0001\u0000\u0000\u0000\u0104\u0102\u0001\u0000\u0000\u0000\u0104"+
		"\u0105\u0001\u0000\u0000\u0000\u0105\u0107\u0001\u0000\u0000\u0000\u0106"+
		"\u0104\u0001\u0000\u0000\u0000\u0107\u0108\u0005\u0006\u0000\u0000\u0108"+
		"#\u0001\u0000\u0000\u0000\u0109\u010c\u0005@\u0000\u0000\u010a\u010b\u0005"+
		"\t\u0000\u0000\u010b\u010d\u0005=\u0000\u0000\u010c\u010a\u0001\u0000"+
		"\u0000\u0000\u010c\u010d\u0001\u0000\u0000\u0000\u010d%\u0001\u0000\u0000"+
		"\u0000\u010e\u0113\u0003.\u0017\u0000\u010f\u0110\u0005\u0018\u0000\u0000"+
		"\u0110\u0112\u0003.\u0017\u0000\u0111\u010f\u0001\u0000\u0000\u0000\u0112"+
		"\u0115\u0001\u0000\u0000\u0000\u0113\u0111\u0001\u0000\u0000\u0000\u0113"+
		"\u0114\u0001\u0000\u0000\u0000\u0114\'\u0001\u0000\u0000\u0000\u0115\u0113"+
		"\u0001\u0000\u0000\u0000\u0116\u011d\u0003*\u0015\u0000\u0117\u011d\u0003"+
		",\u0016\u0000\u0118\u0119\u0005\u0012\u0000\u0000\u0119\u011a\u0003&\u0013"+
		"\u0000\u011a\u011b\u0005\u0013\u0000\u0000\u011b\u011d\u0001\u0000\u0000"+
		"\u0000\u011c\u0116\u0001\u0000\u0000\u0000\u011c\u0117\u0001\u0000\u0000"+
		"\u0000\u011c\u0118\u0001\u0000\u0000\u0000\u011d)\u0001\u0000\u0000\u0000"+
		"\u011e\u0120\u00030\u0018\u0000\u011f\u011e\u0001\u0000\u0000\u0000\u011f"+
		"\u0120\u0001\u0000\u0000\u0000\u0120\u0121\u0001\u0000\u0000\u0000\u0121"+
		"\u0122\u00032\u0019\u0000\u0122+\u0001\u0000\u0000\u0000\u0123\u0124\u0005"+
		"B\u0000\u0000\u0124-\u0001\u0000\u0000\u0000\u0125\u012a\u0003(\u0014"+
		"\u0000\u0126\u0127\u0005\u0019\u0000\u0000\u0127\u012b\u0003(\u0014\u0000"+
		"\u0128\u0129\u0005\u001a\u0000\u0000\u0129\u012b\u0005=\u0000\u0000\u012a"+
		"\u0126\u0001\u0000\u0000\u0000\u012a\u0128\u0001\u0000\u0000\u0000\u012b"+
		"\u012e\u0001\u0000\u0000\u0000\u012c\u012e\u0003(\u0014\u0000\u012d\u0125"+
		"\u0001\u0000\u0000\u0000\u012d\u012c\u0001\u0000\u0000\u0000\u012e/\u0001"+
		"\u0000\u0000\u0000\u012f\u0145\u0005\u001b\u0000\u0000\u0130\u0145\u0005"+
		"\u001c\u0000\u0000\u0131\u0145\u0005\u001d\u0000\u0000\u0132\u0145\u0005"+
		"\u001e\u0000\u0000\u0133\u0145\u0005\u001f\u0000\u0000\u0134\u0145\u0005"+
		" \u0000\u0000\u0135\u0145\u0005!\u0000\u0000\u0136\u0145\u0005\"\u0000"+
		"\u0000\u0137\u0145\u0005#\u0000\u0000\u0138\u0145\u0005$\u0000\u0000\u0139"+
		"\u0145\u0005%\u0000\u0000\u013a\u0145\u0005&\u0000\u0000\u013b\u0145\u0005"+
		"\'\u0000\u0000\u013c\u0145\u0005(\u0000\u0000\u013d\u0145\u0005)\u0000"+
		"\u0000\u013e\u0145\u0005*\u0000\u0000\u013f\u0145\u0005+\u0000\u0000\u0140"+
		"\u0145\u0005,\u0000\u0000\u0141\u0145\u0005-\u0000\u0000\u0142\u0145\u0005"+
		".\u0000\u0000\u0143\u0145\u0005/\u0000\u0000\u0144\u012f\u0001\u0000\u0000"+
		"\u0000\u0144\u0130\u0001\u0000\u0000\u0000\u0144\u0131\u0001\u0000\u0000"+
		"\u0000\u0144\u0132\u0001\u0000\u0000\u0000\u0144\u0133\u0001\u0000\u0000"+
		"\u0000\u0144\u0134\u0001\u0000\u0000\u0000\u0144\u0135\u0001\u0000\u0000"+
		"\u0000\u0144\u0136\u0001\u0000\u0000\u0000\u0144\u0137\u0001\u0000\u0000"+
		"\u0000\u0144\u0138\u0001\u0000\u0000\u0000\u0144\u0139\u0001\u0000\u0000"+
		"\u0000\u0144\u013a\u0001\u0000\u0000\u0000\u0144\u013b\u0001\u0000\u0000"+
		"\u0000\u0144\u013c\u0001\u0000\u0000\u0000\u0144\u013d\u0001\u0000\u0000"+
		"\u0000\u0144\u013e\u0001\u0000\u0000\u0000\u0144\u013f\u0001\u0000\u0000"+
		"\u0000\u0144\u0140\u0001\u0000\u0000\u0000\u0144\u0141\u0001\u0000\u0000"+
		"\u0000\u0144\u0142\u0001\u0000\u0000\u0000\u0144\u0143\u0001\u0000\u0000"+
		"\u0000\u01451\u0001\u0000\u0000\u0000\u0146\u0151\u00050\u0000\u0000\u0147"+
		"\u0151\u00051\u0000\u0000\u0148\u0151\u00052\u0000\u0000\u0149\u0151\u0005"+
		"3\u0000\u0000\u014a\u0151\u00054\u0000\u0000\u014b\u0151\u00055\u0000"+
		"\u0000\u014c\u0151\u00056\u0000\u0000\u014d\u0151\u00057\u0000\u0000\u014e"+
		"\u0151\u00058\u0000\u0000\u014f\u0151\u00059\u0000\u0000\u0150\u0146\u0001"+
		"\u0000\u0000\u0000\u0150\u0147\u0001\u0000\u0000\u0000\u0150\u0148\u0001"+
		"\u0000\u0000\u0000\u0150\u0149\u0001\u0000\u0000\u0000\u0150\u014a\u0001"+
		"\u0000\u0000\u0000\u0150\u014b\u0001\u0000\u0000\u0000\u0150\u014c\u0001"+
		"\u0000\u0000\u0000\u0150\u014d\u0001\u0000\u0000\u0000\u0150\u014e\u0001"+
		"\u0000\u0000\u0000\u0150\u014f\u0001\u0000\u0000\u0000\u01513\u0001\u0000"+
		"\u0000\u0000\u0152\u0153\u00038\u001c\u0000\u0153\u0154\u00036\u001b\u0000"+
		"\u0154\u0155\u00034\u001a\u0000\u0155\u0158\u0001\u0000\u0000\u0000\u0156"+
		"\u0158\u00038\u001c\u0000\u0157\u0152\u0001\u0000\u0000\u0000\u0157\u0156"+
		"\u0001\u0000\u0000\u0000\u01585\u0001\u0000\u0000\u0000\u0159\u015a\u0007"+
		"\u0000\u0000\u0000\u015a7\u0001\u0000\u0000\u0000\u015b\u015c\u0003<\u001e"+
		"\u0000\u015c\u015d\u0003:\u001d\u0000\u015d\u015e\u00038\u001c\u0000\u015e"+
		"\u0161\u0001\u0000\u0000\u0000\u015f\u0161\u0003<\u001e\u0000\u0160\u015b"+
		"\u0001\u0000\u0000\u0000\u0160\u015f\u0001\u0000\u0000\u0000\u01619\u0001"+
		"\u0000\u0000\u0000\u0162\u0163\u0007\u0001\u0000\u0000\u0163;\u0001\u0000"+
		"\u0000\u0000\u0164\u0169\u0003B!\u0000\u0165\u0169\u0003F#\u0000\u0166"+
		"\u0169\u0003D\"\u0000\u0167\u0169\u0003>\u001f\u0000\u0168\u0164\u0001"+
		"\u0000\u0000\u0000\u0168\u0165\u0001\u0000\u0000\u0000\u0168\u0166\u0001"+
		"\u0000\u0000\u0000\u0168\u0167\u0001\u0000\u0000\u0000\u0169=\u0001\u0000"+
		"\u0000\u0000\u016a\u016b\u0003@ \u0000\u016b?\u0001\u0000\u0000\u0000"+
		"\u016c\u0171\u0003H$\u0000\u016d\u0171\u0003J%\u0000\u016e\u0171\u0003"+
		"L&\u0000\u016f\u0171\u0003N\'\u0000\u0170\u016c\u0001\u0000\u0000\u0000"+
		"\u0170\u016d\u0001\u0000\u0000\u0000\u0170\u016e\u0001\u0000\u0000\u0000"+
		"\u0170\u016f\u0001\u0000\u0000\u0000\u0171A\u0001\u0000\u0000\u0000\u0172"+
		"\u0173\u0005\u0012\u0000\u0000\u0173\u0174\u00034\u001a\u0000\u0174\u0175"+
		"\u0005\u0013\u0000\u0000\u0175C\u0001\u0000\u0000\u0000\u0176\u017f\u0005"+
		"\u0014\u0000\u0000\u0177\u017c\u00034\u001a\u0000\u0178\u0179\u0005\b"+
		"\u0000\u0000\u0179\u017b\u00034\u001a\u0000\u017a\u0178\u0001\u0000\u0000"+
		"\u0000\u017b\u017e\u0001\u0000\u0000\u0000\u017c\u017a\u0001\u0000\u0000"+
		"\u0000\u017c\u017d\u0001\u0000\u0000\u0000\u017d\u0180\u0001\u0000\u0000"+
		"\u0000\u017e\u017c\u0001\u0000\u0000\u0000\u017f\u0177\u0001\u0000\u0000"+
		"\u0000\u017f\u0180\u0001\u0000\u0000\u0000\u0180\u0181\u0001\u0000\u0000"+
		"\u0000\u0181\u0182\u0005\u0015\u0000\u0000\u0182E\u0001\u0000\u0000\u0000"+
		"\u0183\u0188\u0005@\u0000\u0000\u0184\u0185\u0005\u000e\u0000\u0000\u0185"+
		"\u0187\u0005@\u0000\u0000\u0186\u0184\u0001\u0000\u0000\u0000\u0187\u018a"+
		"\u0001\u0000\u0000\u0000\u0188\u0186\u0001\u0000\u0000\u0000\u0188\u0189"+
		"\u0001\u0000\u0000\u0000\u0189G\u0001\u0000\u0000\u0000\u018a\u0188\u0001"+
		"\u0000\u0000\u0000\u018b\u018c\u0005B\u0000\u0000\u018cI\u0001\u0000\u0000"+
		"\u0000\u018d\u018e\u0005=\u0000\u0000\u018eK\u0001\u0000\u0000\u0000\u018f"+
		"\u0190\u0005>\u0000\u0000\u0190M\u0001\u0000\u0000\u0000\u0191\u0192\u0005"+
		"?\u0000\u0000\u0192O\u0001\u0000\u0000\u0000+VY]_eo{\u007f\u0082\u008f"+
		"\u0094\u009d\u00a2\u00a7\u00a9\u00ad\u00b4\u00bc\u00c1\u00c6\u00ce\u00dc"+
		"\u00e3\u00e6\u00e9\u00ed\u00f1\u0104\u010c\u0113\u011c\u011f\u012a\u012d"+
		"\u0144\u0150\u0157\u0160\u0168\u0170\u017c\u017f\u0188";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}