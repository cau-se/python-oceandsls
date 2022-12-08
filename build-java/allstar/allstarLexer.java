// Generated from java-escape by ANTLR 4.11.1
package allstar;
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class allstarLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.11.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, ID=4, NUM=5, INT=6;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "ID", "NUM", "INT", "EXP", "DIG"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "';'", "'('", "')'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, "ID", "NUM", "INT"
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


	public allstarLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "allstar.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public String[] getChannelNames() { return channelNames; }

	@Override
	public String[] getModeNames() { return modeNames; }

	@Override
	public ATN getATN() { return _ATN; }

	public static final String _serializedATN =
		"\u0004\u0000\u0006J\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0001\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0002"+
		"\u0001\u0002\u0001\u0003\u0004\u0003\u0019\b\u0003\u000b\u0003\f\u0003"+
		"\u001a\u0001\u0004\u0003\u0004\u001e\b\u0004\u0001\u0004\u0001\u0004\u0004"+
		"\u0004\"\b\u0004\u000b\u0004\f\u0004#\u0001\u0004\u0004\u0004\'\b\u0004"+
		"\u000b\u0004\f\u0004(\u0001\u0004\u0001\u0004\u0005\u0004-\b\u0004\n\u0004"+
		"\f\u00040\t\u0004\u0003\u00042\b\u0004\u0001\u0004\u0003\u00045\b\u0004"+
		"\u0003\u00047\b\u0004\u0001\u0005\u0001\u0005\u0001\u0005\u0005\u0005"+
		"<\b\u0005\n\u0005\f\u0005?\t\u0005\u0003\u0005A\b\u0005\u0001\u0006\u0001"+
		"\u0006\u0003\u0006E\b\u0006\u0001\u0006\u0001\u0006\u0001\u0007\u0001"+
		"\u0007\u0000\u0000\b\u0001\u0001\u0003\u0002\u0005\u0003\u0007\u0004\t"+
		"\u0005\u000b\u0006\r\u0000\u000f\u0000\u0001\u0000\u0005\u0002\u0000A"+
		"Zaz\u0001\u000019\u0002\u0000EEee\u0002\u0000++--\u0001\u000009R\u0000"+
		"\u0001\u0001\u0000\u0000\u0000\u0000\u0003\u0001\u0000\u0000\u0000\u0000"+
		"\u0005\u0001\u0000\u0000\u0000\u0000\u0007\u0001\u0000\u0000\u0000\u0000"+
		"\t\u0001\u0000\u0000\u0000\u0000\u000b\u0001\u0000\u0000\u0000\u0001\u0011"+
		"\u0001\u0000\u0000\u0000\u0003\u0013\u0001\u0000\u0000\u0000\u0005\u0015"+
		"\u0001\u0000\u0000\u0000\u0007\u0018\u0001\u0000\u0000\u0000\t\u001d\u0001"+
		"\u0000\u0000\u0000\u000b@\u0001\u0000\u0000\u0000\rB\u0001\u0000\u0000"+
		"\u0000\u000fH\u0001\u0000\u0000\u0000\u0011\u0012\u0005;\u0000\u0000\u0012"+
		"\u0002\u0001\u0000\u0000\u0000\u0013\u0014\u0005(\u0000\u0000\u0014\u0004"+
		"\u0001\u0000\u0000\u0000\u0015\u0016\u0005)\u0000\u0000\u0016\u0006\u0001"+
		"\u0000\u0000\u0000\u0017\u0019\u0007\u0000\u0000\u0000\u0018\u0017\u0001"+
		"\u0000\u0000\u0000\u0019\u001a\u0001\u0000\u0000\u0000\u001a\u0018\u0001"+
		"\u0000\u0000\u0000\u001a\u001b\u0001\u0000\u0000\u0000\u001b\b\u0001\u0000"+
		"\u0000\u0000\u001c\u001e\u0005-\u0000\u0000\u001d\u001c\u0001\u0000\u0000"+
		"\u0000\u001d\u001e\u0001\u0000\u0000\u0000\u001e6\u0001\u0000\u0000\u0000"+
		"\u001f!\u0005.\u0000\u0000 \"\u0003\u000f\u0007\u0000! \u0001\u0000\u0000"+
		"\u0000\"#\u0001\u0000\u0000\u0000#!\u0001\u0000\u0000\u0000#$\u0001\u0000"+
		"\u0000\u0000$7\u0001\u0000\u0000\u0000%\'\u0003\u000f\u0007\u0000&%\u0001"+
		"\u0000\u0000\u0000\'(\u0001\u0000\u0000\u0000(&\u0001\u0000\u0000\u0000"+
		"()\u0001\u0000\u0000\u0000)1\u0001\u0000\u0000\u0000*.\u0005.\u0000\u0000"+
		"+-\u0003\u000f\u0007\u0000,+\u0001\u0000\u0000\u0000-0\u0001\u0000\u0000"+
		"\u0000.,\u0001\u0000\u0000\u0000./\u0001\u0000\u0000\u0000/2\u0001\u0000"+
		"\u0000\u00000.\u0001\u0000\u0000\u00001*\u0001\u0000\u0000\u000012\u0001"+
		"\u0000\u0000\u000024\u0001\u0000\u0000\u000035\u0003\r\u0006\u000043\u0001"+
		"\u0000\u0000\u000045\u0001\u0000\u0000\u000057\u0001\u0000\u0000\u0000"+
		"6\u001f\u0001\u0000\u0000\u00006&\u0001\u0000\u0000\u00007\n\u0001\u0000"+
		"\u0000\u00008A\u00050\u0000\u00009=\u0007\u0001\u0000\u0000:<\u0003\u000f"+
		"\u0007\u0000;:\u0001\u0000\u0000\u0000<?\u0001\u0000\u0000\u0000=;\u0001"+
		"\u0000\u0000\u0000=>\u0001\u0000\u0000\u0000>A\u0001\u0000\u0000\u0000"+
		"?=\u0001\u0000\u0000\u0000@8\u0001\u0000\u0000\u0000@9\u0001\u0000\u0000"+
		"\u0000A\f\u0001\u0000\u0000\u0000BD\u0007\u0002\u0000\u0000CE\u0007\u0003"+
		"\u0000\u0000DC\u0001\u0000\u0000\u0000DE\u0001\u0000\u0000\u0000EF\u0001"+
		"\u0000\u0000\u0000FG\u0003\u000b\u0005\u0000G\u000e\u0001\u0000\u0000"+
		"\u0000HI\u0007\u0004\u0000\u0000I\u0010\u0001\u0000\u0000\u0000\f\u0000"+
		"\u001a\u001d#(.146=@D\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}