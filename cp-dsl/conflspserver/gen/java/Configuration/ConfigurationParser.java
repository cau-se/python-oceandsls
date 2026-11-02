// Generated from Configuration.g4 by ANTLR 4.13.1
package Configuration;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class ConfigurationParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, T__5=6, T__6=7, T__7=8, T__8=9, 
		T__9=10, T__10=11, T__11=12, T__12=13, T__13=14, T__14=15, T__15=16, T__16=17, 
		T__17=18, T__18=19, T__19=20, T__20=21, ELONG=22, EDOUBLE=23, EBoolean=24, 
		ID=25, INT=26, STRING=27, WS=28, ML_COMMENT=29, SL_COMMENT=30, ANY_OTHER=31;
	public static final int
		RULE_configurationModel = 0, RULE_include = 1, RULE_featureActivation = 2, 
		RULE_featureConfiguration = 3, RULE_parameterGroup = 4, RULE_parameterAssignment = 5, 
		RULE_selector = 6, RULE_elementSelector = 7, RULE_rangeSelector = 8, RULE_unitSpecification = 9, 
		RULE_unitFactor = 10, RULE_qualifiedName = 11, RULE_arithmeticExpression = 12, 
		RULE_eAdditionOperator = 13, RULE_multiplicationExpression = 14, RULE_eMultiplicationOperator = 15, 
		RULE_valueExpression = 16, RULE_literalExpression = 17, RULE_literal = 18, 
		RULE_parenthesisExpression = 19, RULE_arrayExpression = 20, RULE_namedElementReference = 21, 
		RULE_stringValue = 22, RULE_longValue = 23, RULE_doubleValue = 24, RULE_booleanValue = 25;
	private static String[] makeRuleNames() {
		return new String[] {
			"configurationModel", "include", "featureActivation", "featureConfiguration", 
			"parameterGroup", "parameterAssignment", "selector", "elementSelector", 
			"rangeSelector", "unitSpecification", "unitFactor", "qualifiedName", 
			"arithmeticExpression", "eAdditionOperator", "multiplicationExpression", 
			"eMultiplicationOperator", "valueExpression", "literalExpression", "literal", 
			"parenthesisExpression", "arrayExpression", "namedElementReference", 
			"stringValue", "longValue", "doubleValue", "booleanValue"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'configuration'", "':'", "'activate'", "','", "'include'", "'!'", 
			"'feature'", "'{'", "'}'", "'group'", "'['", "']'", "'('", "')'", "'*'", 
			"'/'", "'^'", "'.'", "'+'", "'-'", "'%'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, null, null, null, null, null, null, 
			null, null, null, null, null, null, null, null, null, null, "ELONG", 
			"EDOUBLE", "EBoolean", "ID", "INT", "STRING", "WS", "ML_COMMENT", "SL_COMMENT", 
			"ANY_OTHER"
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
	public String getGrammarFileName() { return "Configuration.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public ConfigurationParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ConfigurationModelContext extends ParserRuleContext {
		public Token name;
		public Token declarationModel;
		public IncludeContext include;
		public List<IncludeContext> includes = new ArrayList<IncludeContext>();
		public FeatureActivationContext featureActivation;
		public List<FeatureActivationContext> featureActivations = new ArrayList<FeatureActivationContext>();
		public ParameterGroupContext parameterGroup;
		public List<ParameterGroupContext> parameterGroups = new ArrayList<ParameterGroupContext>();
		public FeatureConfigurationContext featureConfiguration;
		public List<FeatureConfigurationContext> featureConfigurations = new ArrayList<FeatureConfigurationContext>();
		public List<TerminalNode> ID() { return getTokens(ConfigurationParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(ConfigurationParser.ID, i);
		}
		public List<IncludeContext> include() {
			return getRuleContexts(IncludeContext.class);
		}
		public IncludeContext include(int i) {
			return getRuleContext(IncludeContext.class,i);
		}
		public List<FeatureActivationContext> featureActivation() {
			return getRuleContexts(FeatureActivationContext.class);
		}
		public FeatureActivationContext featureActivation(int i) {
			return getRuleContext(FeatureActivationContext.class,i);
		}
		public List<ParameterGroupContext> parameterGroup() {
			return getRuleContexts(ParameterGroupContext.class);
		}
		public ParameterGroupContext parameterGroup(int i) {
			return getRuleContext(ParameterGroupContext.class,i);
		}
		public List<FeatureConfigurationContext> featureConfiguration() {
			return getRuleContexts(FeatureConfigurationContext.class);
		}
		public FeatureConfigurationContext featureConfiguration(int i) {
			return getRuleContext(FeatureConfigurationContext.class,i);
		}
		public ConfigurationModelContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_configurationModel; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterConfigurationModel(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitConfigurationModel(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitConfigurationModel(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ConfigurationModelContext configurationModel() throws RecognitionException {
		ConfigurationModelContext _localctx = new ConfigurationModelContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_configurationModel);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(52);
			match(T__0);
			setState(53);
			((ConfigurationModelContext)_localctx).name = match(ID);
			setState(54);
			match(T__1);
			setState(55);
			((ConfigurationModelContext)_localctx).declarationModel = match(ID);
			setState(59);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__4) {
				{
				{
				setState(56);
				((ConfigurationModelContext)_localctx).include = include();
				((ConfigurationModelContext)_localctx).includes.add(((ConfigurationModelContext)_localctx).include);
				}
				}
				setState(61);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(71);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__2) {
				{
				setState(62);
				match(T__2);
				setState(63);
				((ConfigurationModelContext)_localctx).featureActivation = featureActivation();
				((ConfigurationModelContext)_localctx).featureActivations.add(((ConfigurationModelContext)_localctx).featureActivation);
				setState(68);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(64);
					match(T__3);
					setState(65);
					((ConfigurationModelContext)_localctx).featureActivation = featureActivation();
					((ConfigurationModelContext)_localctx).featureActivations.add(((ConfigurationModelContext)_localctx).featureActivation);
					}
					}
					setState(70);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(77);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__6 || _la==T__9) {
				{
				setState(75);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__9:
					{
					setState(73);
					((ConfigurationModelContext)_localctx).parameterGroup = parameterGroup();
					((ConfigurationModelContext)_localctx).parameterGroups.add(((ConfigurationModelContext)_localctx).parameterGroup);
					}
					break;
				case T__6:
					{
					setState(74);
					((ConfigurationModelContext)_localctx).featureConfiguration = featureConfiguration();
					((ConfigurationModelContext)_localctx).featureConfigurations.add(((ConfigurationModelContext)_localctx).featureConfiguration);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(79);
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
	public static class IncludeContext extends ParserRuleContext {
		public QualifiedNameContext importedNamespace;
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public IncludeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_include; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterInclude(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitInclude(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitInclude(this);
			else return visitor.visitChildren(this);
		}
	}

	public final IncludeContext include() throws RecognitionException {
		IncludeContext _localctx = new IncludeContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_include);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(80);
			match(T__4);
			setState(81);
			((IncludeContext)_localctx).importedNamespace = qualifiedName();
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
	public static class FeatureActivationContext extends ParserRuleContext {
		public Token deactivated;
		public Token declaration;
		public TerminalNode ID() { return getToken(ConfigurationParser.ID, 0); }
		public FeatureActivationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_featureActivation; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterFeatureActivation(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitFeatureActivation(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitFeatureActivation(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FeatureActivationContext featureActivation() throws RecognitionException {
		FeatureActivationContext _localctx = new FeatureActivationContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_featureActivation);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(84);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__5) {
				{
				setState(83);
				((FeatureActivationContext)_localctx).deactivated = match(T__5);
				}
			}

			setState(86);
			((FeatureActivationContext)_localctx).declaration = match(ID);
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
	public static class FeatureConfigurationContext extends ParserRuleContext {
		public Token declaration;
		public FeatureActivationContext featureActivation;
		public List<FeatureActivationContext> featureActivations = new ArrayList<FeatureActivationContext>();
		public ParameterGroupContext parameterGroup;
		public List<ParameterGroupContext> parameterGroups = new ArrayList<ParameterGroupContext>();
		public FeatureConfigurationContext featureConfiguration;
		public List<FeatureConfigurationContext> featureConfigurations = new ArrayList<FeatureConfigurationContext>();
		public TerminalNode ID() { return getToken(ConfigurationParser.ID, 0); }
		public List<FeatureActivationContext> featureActivation() {
			return getRuleContexts(FeatureActivationContext.class);
		}
		public FeatureActivationContext featureActivation(int i) {
			return getRuleContext(FeatureActivationContext.class,i);
		}
		public List<ParameterGroupContext> parameterGroup() {
			return getRuleContexts(ParameterGroupContext.class);
		}
		public ParameterGroupContext parameterGroup(int i) {
			return getRuleContext(ParameterGroupContext.class,i);
		}
		public List<FeatureConfigurationContext> featureConfiguration() {
			return getRuleContexts(FeatureConfigurationContext.class);
		}
		public FeatureConfigurationContext featureConfiguration(int i) {
			return getRuleContext(FeatureConfigurationContext.class,i);
		}
		public FeatureConfigurationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_featureConfiguration; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterFeatureConfiguration(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitFeatureConfiguration(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitFeatureConfiguration(this);
			else return visitor.visitChildren(this);
		}
	}

	public final FeatureConfigurationContext featureConfiguration() throws RecognitionException {
		FeatureConfigurationContext _localctx = new FeatureConfigurationContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_featureConfiguration);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(88);
			match(T__6);
			setState(89);
			((FeatureConfigurationContext)_localctx).declaration = match(ID);
			setState(90);
			match(T__7);
			setState(100);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__2) {
				{
				setState(91);
				match(T__2);
				setState(92);
				((FeatureConfigurationContext)_localctx).featureActivation = featureActivation();
				((FeatureConfigurationContext)_localctx).featureActivations.add(((FeatureConfigurationContext)_localctx).featureActivation);
				setState(97);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(93);
					match(T__3);
					setState(94);
					((FeatureConfigurationContext)_localctx).featureActivation = featureActivation();
					((FeatureConfigurationContext)_localctx).featureActivations.add(((FeatureConfigurationContext)_localctx).featureActivation);
					}
					}
					setState(99);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(106);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__6 || _la==T__9) {
				{
				setState(104);
				_errHandler.sync(this);
				switch (_input.LA(1)) {
				case T__9:
					{
					setState(102);
					((FeatureConfigurationContext)_localctx).parameterGroup = parameterGroup();
					((FeatureConfigurationContext)_localctx).parameterGroups.add(((FeatureConfigurationContext)_localctx).parameterGroup);
					}
					break;
				case T__6:
					{
					setState(103);
					((FeatureConfigurationContext)_localctx).featureConfiguration = featureConfiguration();
					((FeatureConfigurationContext)_localctx).featureConfigurations.add(((FeatureConfigurationContext)_localctx).featureConfiguration);
					}
					break;
				default:
					throw new NoViableAltException(this);
				}
				}
				setState(108);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(109);
			match(T__8);
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
	public static class ParameterGroupContext extends ParserRuleContext {
		public Token declaration;
		public ParameterAssignmentContext parameterAssignment;
		public List<ParameterAssignmentContext> parameters = new ArrayList<ParameterAssignmentContext>();
		public TerminalNode ID() { return getToken(ConfigurationParser.ID, 0); }
		public List<ParameterAssignmentContext> parameterAssignment() {
			return getRuleContexts(ParameterAssignmentContext.class);
		}
		public ParameterAssignmentContext parameterAssignment(int i) {
			return getRuleContext(ParameterAssignmentContext.class,i);
		}
		public ParameterGroupContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parameterGroup; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterParameterGroup(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitParameterGroup(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitParameterGroup(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParameterGroupContext parameterGroup() throws RecognitionException {
		ParameterGroupContext _localctx = new ParameterGroupContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_parameterGroup);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(111);
			match(T__9);
			setState(112);
			((ParameterGroupContext)_localctx).declaration = match(ID);
			setState(113);
			match(T__7);
			setState(117);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==ID) {
				{
				{
				setState(114);
				((ParameterGroupContext)_localctx).parameterAssignment = parameterAssignment();
				((ParameterGroupContext)_localctx).parameters.add(((ParameterGroupContext)_localctx).parameterAssignment);
				}
				}
				setState(119);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			setState(120);
			match(T__8);
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
	public static class ParameterAssignmentContext extends ParserRuleContext {
		public QualifiedNameContext declaration;
		public SelectorContext selector;
		public List<SelectorContext> selectors = new ArrayList<SelectorContext>();
		public ArithmeticExpressionContext value;
		public UnitSpecificationContext unit;
		public QualifiedNameContext qualifiedName() {
			return getRuleContext(QualifiedNameContext.class,0);
		}
		public ArithmeticExpressionContext arithmeticExpression() {
			return getRuleContext(ArithmeticExpressionContext.class,0);
		}
		public List<SelectorContext> selector() {
			return getRuleContexts(SelectorContext.class);
		}
		public SelectorContext selector(int i) {
			return getRuleContext(SelectorContext.class,i);
		}
		public UnitSpecificationContext unitSpecification() {
			return getRuleContext(UnitSpecificationContext.class,0);
		}
		public ParameterAssignmentContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parameterAssignment; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterParameterAssignment(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitParameterAssignment(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitParameterAssignment(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParameterAssignmentContext parameterAssignment() throws RecognitionException {
		ParameterAssignmentContext _localctx = new ParameterAssignmentContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_parameterAssignment);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(122);
			((ParameterAssignmentContext)_localctx).declaration = qualifiedName();
			setState(145);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__10:
				{
				setState(123);
				match(T__10);
				setState(124);
				((ParameterAssignmentContext)_localctx).selector = selector();
				((ParameterAssignmentContext)_localctx).selectors.add(((ParameterAssignmentContext)_localctx).selector);
				setState(129);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(125);
					match(T__3);
					setState(126);
					((ParameterAssignmentContext)_localctx).selector = selector();
					((ParameterAssignmentContext)_localctx).selectors.add(((ParameterAssignmentContext)_localctx).selector);
					}
					}
					setState(131);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(132);
				match(T__11);
				}
				break;
			case T__12:
				{
				setState(134);
				match(T__12);
				setState(135);
				((ParameterAssignmentContext)_localctx).selector = selector();
				((ParameterAssignmentContext)_localctx).selectors.add(((ParameterAssignmentContext)_localctx).selector);
				setState(140);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(136);
					match(T__3);
					setState(137);
					((ParameterAssignmentContext)_localctx).selector = selector();
					((ParameterAssignmentContext)_localctx).selectors.add(((ParameterAssignmentContext)_localctx).selector);
					}
					}
					setState(142);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				setState(143);
				match(T__13);
				}
				break;
			case T__1:
				break;
			default:
				break;
			}
			setState(147);
			match(T__1);
			setState(148);
			((ParameterAssignmentContext)_localctx).value = arithmeticExpression();
			setState(150);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,14,_ctx) ) {
			case 1:
				{
				setState(149);
				((ParameterAssignmentContext)_localctx).unit = unitSpecification();
				}
				break;
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
	public static class SelectorContext extends ParserRuleContext {
		public ElementSelectorContext elementSelector() {
			return getRuleContext(ElementSelectorContext.class,0);
		}
		public RangeSelectorContext rangeSelector() {
			return getRuleContext(RangeSelectorContext.class,0);
		}
		public SelectorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_selector; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterSelector(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitSelector(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitSelector(this);
			else return visitor.visitChildren(this);
		}
	}

	public final SelectorContext selector() throws RecognitionException {
		SelectorContext _localctx = new SelectorContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_selector);
		try {
			setState(154);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,15,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(152);
				elementSelector();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(153);
				rangeSelector();
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
	public static class ElementSelectorContext extends ParserRuleContext {
		public Token element;
		public TerminalNode ELONG() { return getToken(ConfigurationParser.ELONG, 0); }
		public ElementSelectorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_elementSelector; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterElementSelector(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitElementSelector(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitElementSelector(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ElementSelectorContext elementSelector() throws RecognitionException {
		ElementSelectorContext _localctx = new ElementSelectorContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_elementSelector);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(156);
			((ElementSelectorContext)_localctx).element = match(ELONG);
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
	public static class RangeSelectorContext extends ParserRuleContext {
		public Token lowerBound;
		public Token upperBound;
		public List<TerminalNode> ELONG() { return getTokens(ConfigurationParser.ELONG); }
		public TerminalNode ELONG(int i) {
			return getToken(ConfigurationParser.ELONG, i);
		}
		public RangeSelectorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_rangeSelector; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterRangeSelector(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitRangeSelector(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitRangeSelector(this);
			else return visitor.visitChildren(this);
		}
	}

	public final RangeSelectorContext rangeSelector() throws RecognitionException {
		RangeSelectorContext _localctx = new RangeSelectorContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_rangeSelector);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(158);
			((RangeSelectorContext)_localctx).lowerBound = match(ELONG);
			setState(159);
			match(T__1);
			setState(160);
			((RangeSelectorContext)_localctx).upperBound = match(ELONG);
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
		public List<UnitFactorContext> unitFactor() {
			return getRuleContexts(UnitFactorContext.class);
		}
		public UnitFactorContext unitFactor(int i) {
			return getRuleContext(UnitFactorContext.class,i);
		}
		public UnitSpecificationContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unitSpecification; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterUnitSpecification(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitUnitSpecification(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitUnitSpecification(this);
			else return visitor.visitChildren(this);
		}
	}

	public final UnitSpecificationContext unitSpecification() throws RecognitionException {
		UnitSpecificationContext _localctx = new UnitSpecificationContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_unitSpecification);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(162);
			unitFactor();
			setState(167);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__14 || _la==T__15) {
				{
				{
				setState(163);
				_la = _input.LA(1);
				if ( !(_la==T__14 || _la==T__15) ) {
				_errHandler.recoverInline(this);
				}
				else {
					if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
					_errHandler.reportMatch(this);
					consume();
				}
				setState(164);
				unitFactor();
				}
				}
				setState(169);
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
	public static class UnitFactorContext extends ParserRuleContext {
		public TerminalNode ID() { return getToken(ConfigurationParser.ID, 0); }
		public TerminalNode ELONG() { return getToken(ConfigurationParser.ELONG, 0); }
		public UnitFactorContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unitFactor; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterUnitFactor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitUnitFactor(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitUnitFactor(this);
			else return visitor.visitChildren(this);
		}
	}

	public final UnitFactorContext unitFactor() throws RecognitionException {
		UnitFactorContext _localctx = new UnitFactorContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_unitFactor);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(170);
			match(ID);
			setState(173);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if (_la==T__16) {
				{
				setState(171);
				match(T__16);
				setState(172);
				match(ELONG);
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
	public static class QualifiedNameContext extends ParserRuleContext {
		public List<TerminalNode> ID() { return getTokens(ConfigurationParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(ConfigurationParser.ID, i);
		}
		public QualifiedNameContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_qualifiedName; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterQualifiedName(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitQualifiedName(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitQualifiedName(this);
			else return visitor.visitChildren(this);
		}
	}

	public final QualifiedNameContext qualifiedName() throws RecognitionException {
		QualifiedNameContext _localctx = new QualifiedNameContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_qualifiedName);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(175);
			match(ID);
			setState(180);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__17) {
				{
				{
				setState(176);
				match(T__17);
				setState(177);
				match(ID);
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterArithmeticExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitArithmeticExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitArithmeticExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArithmeticExpressionContext arithmeticExpression() throws RecognitionException {
		ArithmeticExpressionContext _localctx = new ArithmeticExpressionContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_arithmeticExpression);
		try {
			setState(188);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,19,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(183);
				((ArithmeticExpressionContext)_localctx).left = multiplicationExpression();
				setState(184);
				((ArithmeticExpressionContext)_localctx).op = eAdditionOperator();
				setState(185);
				((ArithmeticExpressionContext)_localctx).right = arithmeticExpression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(187);
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterEAdditionOperator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitEAdditionOperator(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitEAdditionOperator(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EAdditionOperatorContext eAdditionOperator() throws RecognitionException {
		EAdditionOperatorContext _localctx = new EAdditionOperatorContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_eAdditionOperator);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(190);
			_la = _input.LA(1);
			if ( !(_la==T__18 || _la==T__19) ) {
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterMultiplicationExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitMultiplicationExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitMultiplicationExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final MultiplicationExpressionContext multiplicationExpression() throws RecognitionException {
		MultiplicationExpressionContext _localctx = new MultiplicationExpressionContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_multiplicationExpression);
		try {
			setState(197);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,20,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(192);
				((MultiplicationExpressionContext)_localctx).left = valueExpression();
				setState(193);
				((MultiplicationExpressionContext)_localctx).op = eMultiplicationOperator();
				setState(194);
				((MultiplicationExpressionContext)_localctx).right = multiplicationExpression();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(196);
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterEMultiplicationOperator(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitEMultiplicationOperator(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitEMultiplicationOperator(this);
			else return visitor.visitChildren(this);
		}
	}

	public final EMultiplicationOperatorContext eMultiplicationOperator() throws RecognitionException {
		EMultiplicationOperatorContext _localctx = new EMultiplicationOperatorContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_eMultiplicationOperator);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(199);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 2195456L) != 0)) ) {
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterValueExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitValueExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitValueExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ValueExpressionContext valueExpression() throws RecognitionException {
		ValueExpressionContext _localctx = new ValueExpressionContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_valueExpression);
		try {
			setState(205);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__12:
				enterOuterAlt(_localctx, 1);
				{
				setState(201);
				parenthesisExpression();
				}
				break;
			case ID:
				enterOuterAlt(_localctx, 2);
				{
				setState(202);
				namedElementReference();
				}
				break;
			case T__10:
				enterOuterAlt(_localctx, 3);
				{
				setState(203);
				arrayExpression();
				}
				break;
			case ELONG:
			case EDOUBLE:
			case EBoolean:
			case STRING:
				enterOuterAlt(_localctx, 4);
				{
				setState(204);
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterLiteralExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitLiteralExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitLiteralExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LiteralExpressionContext literalExpression() throws RecognitionException {
		LiteralExpressionContext _localctx = new LiteralExpressionContext(_ctx, getState());
		enterRule(_localctx, 34, RULE_literalExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(207);
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterLiteral(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitLiteral(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitLiteral(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LiteralContext literal() throws RecognitionException {
		LiteralContext _localctx = new LiteralContext(_ctx, getState());
		enterRule(_localctx, 36, RULE_literal);
		try {
			setState(213);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case STRING:
				enterOuterAlt(_localctx, 1);
				{
				setState(209);
				stringValue();
				}
				break;
			case ELONG:
				enterOuterAlt(_localctx, 2);
				{
				setState(210);
				longValue();
				}
				break;
			case EDOUBLE:
				enterOuterAlt(_localctx, 3);
				{
				setState(211);
				doubleValue();
				}
				break;
			case EBoolean:
				enterOuterAlt(_localctx, 4);
				{
				setState(212);
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterParenthesisExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitParenthesisExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitParenthesisExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ParenthesisExpressionContext parenthesisExpression() throws RecognitionException {
		ParenthesisExpressionContext _localctx = new ParenthesisExpressionContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_parenthesisExpression);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(215);
			match(T__12);
			setState(216);
			((ParenthesisExpressionContext)_localctx).expression = arithmeticExpression();
			setState(217);
			match(T__13);
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
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterArrayExpression(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitArrayExpression(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitArrayExpression(this);
			else return visitor.visitChildren(this);
		}
	}

	public final ArrayExpressionContext arrayExpression() throws RecognitionException {
		ArrayExpressionContext _localctx = new ArrayExpressionContext(_ctx, getState());
		enterRule(_localctx, 40, RULE_arrayExpression);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(219);
			match(T__10);
			setState(228);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 197142528L) != 0)) {
				{
				setState(220);
				((ArrayExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
				((ArrayExpressionContext)_localctx).elements.add(((ArrayExpressionContext)_localctx).arithmeticExpression);
				setState(225);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==T__3) {
					{
					{
					setState(221);
					match(T__3);
					setState(222);
					((ArrayExpressionContext)_localctx).arithmeticExpression = arithmeticExpression();
					((ArrayExpressionContext)_localctx).elements.add(((ArrayExpressionContext)_localctx).arithmeticExpression);
					}
					}
					setState(227);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
			}

			setState(230);
			match(T__11);
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
		public List<TerminalNode> ID() { return getTokens(ConfigurationParser.ID); }
		public TerminalNode ID(int i) {
			return getToken(ConfigurationParser.ID, i);
		}
		public NamedElementReferenceContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_namedElementReference; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterNamedElementReference(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitNamedElementReference(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitNamedElementReference(this);
			else return visitor.visitChildren(this);
		}
	}

	public final NamedElementReferenceContext namedElementReference() throws RecognitionException {
		NamedElementReferenceContext _localctx = new NamedElementReferenceContext(_ctx, getState());
		enterRule(_localctx, 42, RULE_namedElementReference);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(232);
			((NamedElementReferenceContext)_localctx).ID = match(ID);
			((NamedElementReferenceContext)_localctx).elements.add(((NamedElementReferenceContext)_localctx).ID);
			setState(237);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==T__17) {
				{
				{
				setState(233);
				match(T__17);
				setState(234);
				((NamedElementReferenceContext)_localctx).ID = match(ID);
				((NamedElementReferenceContext)_localctx).elements.add(((NamedElementReferenceContext)_localctx).ID);
				}
				}
				setState(239);
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
		public TerminalNode STRING() { return getToken(ConfigurationParser.STRING, 0); }
		public StringValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_stringValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterStringValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitStringValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitStringValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final StringValueContext stringValue() throws RecognitionException {
		StringValueContext _localctx = new StringValueContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_stringValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(240);
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
		public TerminalNode ELONG() { return getToken(ConfigurationParser.ELONG, 0); }
		public LongValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_longValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterLongValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitLongValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitLongValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final LongValueContext longValue() throws RecognitionException {
		LongValueContext _localctx = new LongValueContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_longValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(242);
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
		public TerminalNode EDOUBLE() { return getToken(ConfigurationParser.EDOUBLE, 0); }
		public DoubleValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_doubleValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterDoubleValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitDoubleValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitDoubleValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final DoubleValueContext doubleValue() throws RecognitionException {
		DoubleValueContext _localctx = new DoubleValueContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_doubleValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(244);
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
		public TerminalNode EBoolean() { return getToken(ConfigurationParser.EBoolean, 0); }
		public BooleanValueContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_booleanValue; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).enterBooleanValue(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof ConfigurationListener ) ((ConfigurationListener)listener).exitBooleanValue(this);
		}
		@Override
		public <T> T accept(ParseTreeVisitor<? extends T> visitor) {
			if ( visitor instanceof ConfigurationVisitor ) return ((ConfigurationVisitor<? extends T>)visitor).visitBooleanValue(this);
			else return visitor.visitChildren(this);
		}
	}

	public final BooleanValueContext booleanValue() throws RecognitionException {
		BooleanValueContext _localctx = new BooleanValueContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_booleanValue);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(246);
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
		"\u0004\u0001\u001f\u00f9\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001"+
		"\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004"+
		"\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007"+
		"\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b"+
		"\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007"+
		"\u000f\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007"+
		"\u0012\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007"+
		"\u0015\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002\u0018\u0007"+
		"\u0018\u0002\u0019\u0007\u0019\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0000\u0005\u0000:\b\u0000\n\u0000\f\u0000=\t\u0000\u0001"+
		"\u0000\u0001\u0000\u0001\u0000\u0001\u0000\u0005\u0000C\b\u0000\n\u0000"+
		"\f\u0000F\t\u0000\u0003\u0000H\b\u0000\u0001\u0000\u0001\u0000\u0005\u0000"+
		"L\b\u0000\n\u0000\f\u0000O\t\u0000\u0001\u0001\u0001\u0001\u0001\u0001"+
		"\u0001\u0002\u0003\u0002U\b\u0002\u0001\u0002\u0001\u0002\u0001\u0003"+
		"\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003\u0001\u0003"+
		"\u0005\u0003`\b\u0003\n\u0003\f\u0003c\t\u0003\u0003\u0003e\b\u0003\u0001"+
		"\u0003\u0001\u0003\u0005\u0003i\b\u0003\n\u0003\f\u0003l\t\u0003\u0001"+
		"\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0005"+
		"\u0004t\b\u0004\n\u0004\f\u0004w\t\u0004\u0001\u0004\u0001\u0004\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u0080"+
		"\b\u0005\n\u0005\f\u0005\u0083\t\u0005\u0001\u0005\u0001\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005\u008b\b\u0005\n\u0005"+
		"\f\u0005\u008e\t\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0092\b\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0097\b\u0005\u0001\u0006"+
		"\u0001\u0006\u0003\u0006\u009b\b\u0006\u0001\u0007\u0001\u0007\u0001\b"+
		"\u0001\b\u0001\b\u0001\b\u0001\t\u0001\t\u0001\t\u0005\t\u00a6\b\t\n\t"+
		"\f\t\u00a9\t\t\u0001\n\u0001\n\u0001\n\u0003\n\u00ae\b\n\u0001\u000b\u0001"+
		"\u000b\u0001\u000b\u0005\u000b\u00b3\b\u000b\n\u000b\f\u000b\u00b6\t\u000b"+
		"\u0001\f\u0001\f\u0001\f\u0001\f\u0001\f\u0003\f\u00bd\b\f\u0001\r\u0001"+
		"\r\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000e\u0003\u000e"+
		"\u00c6\b\u000e\u0001\u000f\u0001\u000f\u0001\u0010\u0001\u0010\u0001\u0010"+
		"\u0001\u0010\u0003\u0010\u00ce\b\u0010\u0001\u0011\u0001\u0011\u0001\u0012"+
		"\u0001\u0012\u0001\u0012\u0001\u0012\u0003\u0012\u00d6\b\u0012\u0001\u0013"+
		"\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0014\u0001\u0014\u0001\u0014"+
		"\u0001\u0014\u0005\u0014\u00e0\b\u0014\n\u0014\f\u0014\u00e3\t\u0014\u0003"+
		"\u0014\u00e5\b\u0014\u0001\u0014\u0001\u0014\u0001\u0015\u0001\u0015\u0001"+
		"\u0015\u0005\u0015\u00ec\b\u0015\n\u0015\f\u0015\u00ef\t\u0015\u0001\u0016"+
		"\u0001\u0016\u0001\u0017\u0001\u0017\u0001\u0018\u0001\u0018\u0001\u0019"+
		"\u0001\u0019\u0001\u0019\u0000\u0000\u001a\u0000\u0002\u0004\u0006\b\n"+
		"\f\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e \"$&(*,.02\u0000"+
		"\u0003\u0001\u0000\u000f\u0010\u0001\u0000\u0013\u0014\u0002\u0000\u000f"+
		"\u0010\u0015\u0015\u00fd\u00004\u0001\u0000\u0000\u0000\u0002P\u0001\u0000"+
		"\u0000\u0000\u0004T\u0001\u0000\u0000\u0000\u0006X\u0001\u0000\u0000\u0000"+
		"\bo\u0001\u0000\u0000\u0000\nz\u0001\u0000\u0000\u0000\f\u009a\u0001\u0000"+
		"\u0000\u0000\u000e\u009c\u0001\u0000\u0000\u0000\u0010\u009e\u0001\u0000"+
		"\u0000\u0000\u0012\u00a2\u0001\u0000\u0000\u0000\u0014\u00aa\u0001\u0000"+
		"\u0000\u0000\u0016\u00af\u0001\u0000\u0000\u0000\u0018\u00bc\u0001\u0000"+
		"\u0000\u0000\u001a\u00be\u0001\u0000\u0000\u0000\u001c\u00c5\u0001\u0000"+
		"\u0000\u0000\u001e\u00c7\u0001\u0000\u0000\u0000 \u00cd\u0001\u0000\u0000"+
		"\u0000\"\u00cf\u0001\u0000\u0000\u0000$\u00d5\u0001\u0000\u0000\u0000"+
		"&\u00d7\u0001\u0000\u0000\u0000(\u00db\u0001\u0000\u0000\u0000*\u00e8"+
		"\u0001\u0000\u0000\u0000,\u00f0\u0001\u0000\u0000\u0000.\u00f2\u0001\u0000"+
		"\u0000\u00000\u00f4\u0001\u0000\u0000\u00002\u00f6\u0001\u0000\u0000\u0000"+
		"45\u0005\u0001\u0000\u000056\u0005\u0019\u0000\u000067\u0005\u0002\u0000"+
		"\u00007;\u0005\u0019\u0000\u00008:\u0003\u0002\u0001\u000098\u0001\u0000"+
		"\u0000\u0000:=\u0001\u0000\u0000\u0000;9\u0001\u0000\u0000\u0000;<\u0001"+
		"\u0000\u0000\u0000<G\u0001\u0000\u0000\u0000=;\u0001\u0000\u0000\u0000"+
		">?\u0005\u0003\u0000\u0000?D\u0003\u0004\u0002\u0000@A\u0005\u0004\u0000"+
		"\u0000AC\u0003\u0004\u0002\u0000B@\u0001\u0000\u0000\u0000CF\u0001\u0000"+
		"\u0000\u0000DB\u0001\u0000\u0000\u0000DE\u0001\u0000\u0000\u0000EH\u0001"+
		"\u0000\u0000\u0000FD\u0001\u0000\u0000\u0000G>\u0001\u0000\u0000\u0000"+
		"GH\u0001\u0000\u0000\u0000HM\u0001\u0000\u0000\u0000IL\u0003\b\u0004\u0000"+
		"JL\u0003\u0006\u0003\u0000KI\u0001\u0000\u0000\u0000KJ\u0001\u0000\u0000"+
		"\u0000LO\u0001\u0000\u0000\u0000MK\u0001\u0000\u0000\u0000MN\u0001\u0000"+
		"\u0000\u0000N\u0001\u0001\u0000\u0000\u0000OM\u0001\u0000\u0000\u0000"+
		"PQ\u0005\u0005\u0000\u0000QR\u0003\u0016\u000b\u0000R\u0003\u0001\u0000"+
		"\u0000\u0000SU\u0005\u0006\u0000\u0000TS\u0001\u0000\u0000\u0000TU\u0001"+
		"\u0000\u0000\u0000UV\u0001\u0000\u0000\u0000VW\u0005\u0019\u0000\u0000"+
		"W\u0005\u0001\u0000\u0000\u0000XY\u0005\u0007\u0000\u0000YZ\u0005\u0019"+
		"\u0000\u0000Zd\u0005\b\u0000\u0000[\\\u0005\u0003\u0000\u0000\\a\u0003"+
		"\u0004\u0002\u0000]^\u0005\u0004\u0000\u0000^`\u0003\u0004\u0002\u0000"+
		"_]\u0001\u0000\u0000\u0000`c\u0001\u0000\u0000\u0000a_\u0001\u0000\u0000"+
		"\u0000ab\u0001\u0000\u0000\u0000be\u0001\u0000\u0000\u0000ca\u0001\u0000"+
		"\u0000\u0000d[\u0001\u0000\u0000\u0000de\u0001\u0000\u0000\u0000ej\u0001"+
		"\u0000\u0000\u0000fi\u0003\b\u0004\u0000gi\u0003\u0006\u0003\u0000hf\u0001"+
		"\u0000\u0000\u0000hg\u0001\u0000\u0000\u0000il\u0001\u0000\u0000\u0000"+
		"jh\u0001\u0000\u0000\u0000jk\u0001\u0000\u0000\u0000km\u0001\u0000\u0000"+
		"\u0000lj\u0001\u0000\u0000\u0000mn\u0005\t\u0000\u0000n\u0007\u0001\u0000"+
		"\u0000\u0000op\u0005\n\u0000\u0000pq\u0005\u0019\u0000\u0000qu\u0005\b"+
		"\u0000\u0000rt\u0003\n\u0005\u0000sr\u0001\u0000\u0000\u0000tw\u0001\u0000"+
		"\u0000\u0000us\u0001\u0000\u0000\u0000uv\u0001\u0000\u0000\u0000vx\u0001"+
		"\u0000\u0000\u0000wu\u0001\u0000\u0000\u0000xy\u0005\t\u0000\u0000y\t"+
		"\u0001\u0000\u0000\u0000z\u0091\u0003\u0016\u000b\u0000{|\u0005\u000b"+
		"\u0000\u0000|\u0081\u0003\f\u0006\u0000}~\u0005\u0004\u0000\u0000~\u0080"+
		"\u0003\f\u0006\u0000\u007f}\u0001\u0000\u0000\u0000\u0080\u0083\u0001"+
		"\u0000\u0000\u0000\u0081\u007f\u0001\u0000\u0000\u0000\u0081\u0082\u0001"+
		"\u0000\u0000\u0000\u0082\u0084\u0001\u0000\u0000\u0000\u0083\u0081\u0001"+
		"\u0000\u0000\u0000\u0084\u0085\u0005\f\u0000\u0000\u0085\u0092\u0001\u0000"+
		"\u0000\u0000\u0086\u0087\u0005\r\u0000\u0000\u0087\u008c\u0003\f\u0006"+
		"\u0000\u0088\u0089\u0005\u0004\u0000\u0000\u0089\u008b\u0003\f\u0006\u0000"+
		"\u008a\u0088\u0001\u0000\u0000\u0000\u008b\u008e\u0001\u0000\u0000\u0000"+
		"\u008c\u008a\u0001\u0000\u0000\u0000\u008c\u008d\u0001\u0000\u0000\u0000"+
		"\u008d\u008f\u0001\u0000\u0000\u0000\u008e\u008c\u0001\u0000\u0000\u0000"+
		"\u008f\u0090\u0005\u000e\u0000\u0000\u0090\u0092\u0001\u0000\u0000\u0000"+
		"\u0091{\u0001\u0000\u0000\u0000\u0091\u0086\u0001\u0000\u0000\u0000\u0091"+
		"\u0092\u0001\u0000\u0000\u0000\u0092\u0093\u0001\u0000\u0000\u0000\u0093"+
		"\u0094\u0005\u0002\u0000\u0000\u0094\u0096\u0003\u0018\f\u0000\u0095\u0097"+
		"\u0003\u0012\t\u0000\u0096\u0095\u0001\u0000\u0000\u0000\u0096\u0097\u0001"+
		"\u0000\u0000\u0000\u0097\u000b\u0001\u0000\u0000\u0000\u0098\u009b\u0003"+
		"\u000e\u0007\u0000\u0099\u009b\u0003\u0010\b\u0000\u009a\u0098\u0001\u0000"+
		"\u0000\u0000\u009a\u0099\u0001\u0000\u0000\u0000\u009b\r\u0001\u0000\u0000"+
		"\u0000\u009c\u009d\u0005\u0016\u0000\u0000\u009d\u000f\u0001\u0000\u0000"+
		"\u0000\u009e\u009f\u0005\u0016\u0000\u0000\u009f\u00a0\u0005\u0002\u0000"+
		"\u0000\u00a0\u00a1\u0005\u0016\u0000\u0000\u00a1\u0011\u0001\u0000\u0000"+
		"\u0000\u00a2\u00a7\u0003\u0014\n\u0000\u00a3\u00a4\u0007\u0000\u0000\u0000"+
		"\u00a4\u00a6\u0003\u0014\n\u0000\u00a5\u00a3\u0001\u0000\u0000\u0000\u00a6"+
		"\u00a9\u0001\u0000\u0000\u0000\u00a7\u00a5\u0001\u0000\u0000\u0000\u00a7"+
		"\u00a8\u0001\u0000\u0000\u0000\u00a8\u0013\u0001\u0000\u0000\u0000\u00a9"+
		"\u00a7\u0001\u0000\u0000\u0000\u00aa\u00ad\u0005\u0019\u0000\u0000\u00ab"+
		"\u00ac\u0005\u0011\u0000\u0000\u00ac\u00ae\u0005\u0016\u0000\u0000\u00ad"+
		"\u00ab\u0001\u0000\u0000\u0000\u00ad\u00ae\u0001\u0000\u0000\u0000\u00ae"+
		"\u0015\u0001\u0000\u0000\u0000\u00af\u00b4\u0005\u0019\u0000\u0000\u00b0"+
		"\u00b1\u0005\u0012\u0000\u0000\u00b1\u00b3\u0005\u0019\u0000\u0000\u00b2"+
		"\u00b0\u0001\u0000\u0000\u0000\u00b3\u00b6\u0001\u0000\u0000\u0000\u00b4"+
		"\u00b2\u0001\u0000\u0000\u0000\u00b4\u00b5\u0001\u0000\u0000\u0000\u00b5"+
		"\u0017\u0001\u0000\u0000\u0000\u00b6\u00b4\u0001\u0000\u0000\u0000\u00b7"+
		"\u00b8\u0003\u001c\u000e\u0000\u00b8\u00b9\u0003\u001a\r\u0000\u00b9\u00ba"+
		"\u0003\u0018\f\u0000\u00ba\u00bd\u0001\u0000\u0000\u0000\u00bb\u00bd\u0003"+
		"\u001c\u000e\u0000\u00bc\u00b7\u0001\u0000\u0000\u0000\u00bc\u00bb\u0001"+
		"\u0000\u0000\u0000\u00bd\u0019\u0001\u0000\u0000\u0000\u00be\u00bf\u0007"+
		"\u0001\u0000\u0000\u00bf\u001b\u0001\u0000\u0000\u0000\u00c0\u00c1\u0003"+
		" \u0010\u0000\u00c1\u00c2\u0003\u001e\u000f\u0000\u00c2\u00c3\u0003\u001c"+
		"\u000e\u0000\u00c3\u00c6\u0001\u0000\u0000\u0000\u00c4\u00c6\u0003 \u0010"+
		"\u0000\u00c5\u00c0\u0001\u0000\u0000\u0000\u00c5\u00c4\u0001\u0000\u0000"+
		"\u0000\u00c6\u001d\u0001\u0000\u0000\u0000\u00c7\u00c8\u0007\u0002\u0000"+
		"\u0000\u00c8\u001f\u0001\u0000\u0000\u0000\u00c9\u00ce\u0003&\u0013\u0000"+
		"\u00ca\u00ce\u0003*\u0015\u0000\u00cb\u00ce\u0003(\u0014\u0000\u00cc\u00ce"+
		"\u0003\"\u0011\u0000\u00cd\u00c9\u0001\u0000\u0000\u0000\u00cd\u00ca\u0001"+
		"\u0000\u0000\u0000\u00cd\u00cb\u0001\u0000\u0000\u0000\u00cd\u00cc\u0001"+
		"\u0000\u0000\u0000\u00ce!\u0001\u0000\u0000\u0000\u00cf\u00d0\u0003$\u0012"+
		"\u0000\u00d0#\u0001\u0000\u0000\u0000\u00d1\u00d6\u0003,\u0016\u0000\u00d2"+
		"\u00d6\u0003.\u0017\u0000\u00d3\u00d6\u00030\u0018\u0000\u00d4\u00d6\u0003"+
		"2\u0019\u0000\u00d5\u00d1\u0001\u0000\u0000\u0000\u00d5\u00d2\u0001\u0000"+
		"\u0000\u0000\u00d5\u00d3\u0001\u0000\u0000\u0000\u00d5\u00d4\u0001\u0000"+
		"\u0000\u0000\u00d6%\u0001\u0000\u0000\u0000\u00d7\u00d8\u0005\r\u0000"+
		"\u0000\u00d8\u00d9\u0003\u0018\f\u0000\u00d9\u00da\u0005\u000e\u0000\u0000"+
		"\u00da\'\u0001\u0000\u0000\u0000\u00db\u00e4\u0005\u000b\u0000\u0000\u00dc"+
		"\u00e1\u0003\u0018\f\u0000\u00dd\u00de\u0005\u0004\u0000\u0000\u00de\u00e0"+
		"\u0003\u0018\f\u0000\u00df\u00dd\u0001\u0000\u0000\u0000\u00e0\u00e3\u0001"+
		"\u0000\u0000\u0000\u00e1\u00df\u0001\u0000\u0000\u0000\u00e1\u00e2\u0001"+
		"\u0000\u0000\u0000\u00e2\u00e5\u0001\u0000\u0000\u0000\u00e3\u00e1\u0001"+
		"\u0000\u0000\u0000\u00e4\u00dc\u0001\u0000\u0000\u0000\u00e4\u00e5\u0001"+
		"\u0000\u0000\u0000\u00e5\u00e6\u0001\u0000\u0000\u0000\u00e6\u00e7\u0005"+
		"\f\u0000\u0000\u00e7)\u0001\u0000\u0000\u0000\u00e8\u00ed\u0005\u0019"+
		"\u0000\u0000\u00e9\u00ea\u0005\u0012\u0000\u0000\u00ea\u00ec\u0005\u0019"+
		"\u0000\u0000\u00eb\u00e9\u0001\u0000\u0000\u0000\u00ec\u00ef\u0001\u0000"+
		"\u0000\u0000\u00ed\u00eb\u0001\u0000\u0000\u0000\u00ed\u00ee\u0001\u0000"+
		"\u0000\u0000\u00ee+\u0001\u0000\u0000\u0000\u00ef\u00ed\u0001\u0000\u0000"+
		"\u0000\u00f0\u00f1\u0005\u001b\u0000\u0000\u00f1-\u0001\u0000\u0000\u0000"+
		"\u00f2\u00f3\u0005\u0016\u0000\u0000\u00f3/\u0001\u0000\u0000\u0000\u00f4"+
		"\u00f5\u0005\u0017\u0000\u0000\u00f51\u0001\u0000\u0000\u0000\u00f6\u00f7"+
		"\u0005\u0018\u0000\u0000\u00f73\u0001\u0000\u0000\u0000\u001a;DGKMTad"+
		"hju\u0081\u008c\u0091\u0096\u009a\u00a7\u00ad\u00b4\u00bc\u00c5\u00cd"+
		"\u00d5\u00e1\u00e4\u00ed";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}