// Generated from /home/sgu/IdeaProjects/python-oceandsls/tdd-dsl/tddLSPServer/grammars/Typing.g4 by ANTLR 4.12.0
package grammars;

import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class TypingLexer extends Lexer {
    public static final int
            T__0 = 1, T__1 = 2, T__2 = 3, T__3 = 4, T__4 = 5, T__5 = 6, T__6 = 7, T__7 = 8, T__8 = 9,
            T__9 = 10, T__10 = 11, ID = 12, STRING = 13, COMMENT = 14, INT = 15, NUM = 16, DP = 17,
            TDD_COMMENT = 18, NEWLINE = 19, WS = 20;
    public static final String[] ruleNames = makeRuleNames();
    /**
     * @deprecated Use {@link #VOCABULARY} instead.
     */
    @Deprecated
    public static final String[] tokenNames;
    public static final String _serializedATN =
            "\u0004\u0000\u0014\u00d4\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002" +
                    "\u0001\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002" +
                    "\u0004\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002" +
                    "\u0007\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002" +
                    "\u000b\u0007\u000b\u0002\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e" +
                    "\u0002\u000f\u0007\u000f\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011" +
                    "\u0002\u0012\u0007\u0012\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014" +
                    "\u0002\u0015\u0007\u0015\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017" +
                    "\u0001\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002" +
                    "\u0001\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005" +
                    "\u0001\u0006\u0001\u0006\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001" +
                    "\t\u0001\t\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0005\u000bJ\b\u000b" +
                    "\n\u000b\f\u000bM\t\u000b\u0001\f\u0001\f\u0001\f\u0005\fR\b\f\n\f\f\f" +
                    "U\t\f\u0001\f\u0001\f\u0001\r\u0001\r\u0001\r\u0005\r\\\b\r\n\r\f\r_\t" +
                    "\r\u0001\r\u0001\r\u0001\u000e\u0001\u000e\u0001\u000e\u0001\u000f\u0001" +
                    "\u000f\u0001\u000f\u0005\u000fi\b\u000f\n\u000f\f\u000fl\t\u000f\u0003" +
                    "\u000fn\b\u000f\u0001\u0010\u0003\u0010q\b\u0010\u0001\u0010\u0001\u0010" +
                    "\u0004\u0010u\b\u0010\u000b\u0010\f\u0010v\u0001\u0010\u0004\u0010z\b" +
                    "\u0010\u000b\u0010\f\u0010{\u0001\u0010\u0001\u0010\u0005\u0010\u0080" +
                    "\b\u0010\n\u0010\f\u0010\u0083\t\u0010\u0003\u0010\u0085\b\u0010\u0001" +
                    "\u0010\u0003\u0010\u0088\b\u0010\u0003\u0010\u008a\b\u0010\u0001\u0011" +
                    "\u0003\u0011\u008d\b\u0011\u0001\u0011\u0001\u0011\u0004\u0011\u0091\b" +
                    "\u0011\u000b\u0011\f\u0011\u0092\u0001\u0011\u0004\u0011\u0096\b\u0011" +
                    "\u000b\u0011\f\u0011\u0097\u0001\u0011\u0001\u0011\u0005\u0011\u009c\b" +
                    "\u0011\n\u0011\f\u0011\u009f\t\u0011\u0003\u0011\u00a1\b\u0011\u0001\u0011" +
                    "\u0003\u0011\u00a4\b\u0011\u0003\u0011\u00a6\b\u0011\u0001\u0012\u0001" +
                    "\u0012\u0003\u0012\u00aa\b\u0012\u0001\u0012\u0004\u0012\u00ad\b\u0012" +
                    "\u000b\u0012\f\u0012\u00ae\u0001\u0013\u0001\u0013\u0003\u0013\u00b3\b" +
                    "\u0013\u0001\u0013\u0004\u0013\u00b6\b\u0013\u000b\u0013\f\u0013\u00b7" +
                    "\u0001\u0014\u0001\u0014\u0001\u0015\u0001\u0015\u0001\u0015\u0001\u0015" +
                    "\u0005\u0015\u00c0\b\u0015\n\u0015\f\u0015\u00c3\t\u0015\u0001\u0015\u0001" +
                    "\u0015\u0001\u0015\u0001\u0015\u0001\u0016\u0003\u0016\u00ca\b\u0016\u0001" +
                    "\u0016\u0001\u0016\u0001\u0017\u0004\u0017\u00cf\b\u0017\u000b\u0017\f" +
                    "\u0017\u00d0\u0001\u0017\u0001\u0017\u0003S]\u00c1\u0000\u0018\u0001\u0001" +
                    "\u0003\u0002\u0005\u0003\u0007\u0004\t\u0005\u000b\u0006\r\u0007\u000f" +
                    "\b\u0011\t\u0013\n\u0015\u000b\u0017\f\u0019\r\u001b\u000e\u001d\u0000" +
                    "\u001f\u000f!\u0010#\u0011%\u0000\'\u0000)\u0000+\u0012-\u0013/\u0014" +
                    "\u0001\u0000\b\u0002\u0000AZaz\u0004\u000009AZ__az\u0007\u0000\"\"\'\'" +
                    "\\\\bbnnrrtt\u0001\u000019\u0002\u0000EEee\u0002\u0000++--\u0001\u0000" +
                    "09\u0002\u0000\t\t  \u00eb\u0000\u0001\u0001\u0000\u0000\u0000\u0000\u0003" +
                    "\u0001\u0000\u0000\u0000\u0000\u0005\u0001\u0000\u0000\u0000\u0000\u0007" +
                    "\u0001\u0000\u0000\u0000\u0000\t\u0001\u0000\u0000\u0000\u0000\u000b\u0001" +
                    "\u0000\u0000\u0000\u0000\r\u0001\u0000\u0000\u0000\u0000\u000f\u0001\u0000" +
                    "\u0000\u0000\u0000\u0011\u0001\u0000\u0000\u0000\u0000\u0013\u0001\u0000" +
                    "\u0000\u0000\u0000\u0015\u0001\u0000\u0000\u0000\u0000\u0017\u0001\u0000" +
                    "\u0000\u0000\u0000\u0019\u0001\u0000\u0000\u0000\u0000\u001b\u0001\u0000" +
                    "\u0000\u0000\u0000\u001f\u0001\u0000\u0000\u0000\u0000!\u0001\u0000\u0000" +
                    "\u0000\u0000#\u0001\u0000\u0000\u0000\u0000+\u0001\u0000\u0000\u0000\u0000" +
                    "-\u0001\u0000\u0000\u0000\u0000/\u0001\u0000\u0000\u0000\u00011\u0001" +
                    "\u0000\u0000\u0000\u00033\u0001\u0000\u0000\u0000\u00055\u0001\u0000\u0000" +
                    "\u0000\u00077\u0001\u0000\u0000\u0000\t9\u0001\u0000\u0000\u0000\u000b" +
                    ";\u0001\u0000\u0000\u0000\r=\u0001\u0000\u0000\u0000\u000f?\u0001\u0000" +
                    "\u0000\u0000\u0011A\u0001\u0000\u0000\u0000\u0013C\u0001\u0000\u0000\u0000" +
                    "\u0015E\u0001\u0000\u0000\u0000\u0017G\u0001\u0000\u0000\u0000\u0019N" +
                    "\u0001\u0000\u0000\u0000\u001bX\u0001\u0000\u0000\u0000\u001db\u0001\u0000" +
                    "\u0000\u0000\u001fm\u0001\u0000\u0000\u0000!p\u0001\u0000\u0000\u0000" +
                    "#\u008c\u0001\u0000\u0000\u0000%\u00a7\u0001\u0000\u0000\u0000\'\u00b0" +
                    "\u0001\u0000\u0000\u0000)\u00b9\u0001\u0000\u0000\u0000+\u00bb\u0001\u0000" +
                    "\u0000\u0000-\u00c9\u0001\u0000\u0000\u0000/\u00ce\u0001\u0000\u0000\u0000" +
                    "12\u0005(\u0000\u00002\u0002\u0001\u0000\u0000\u000034\u0005,\u0000\u0000" +
                    "4\u0004\u0001\u0000\u0000\u000056\u0005)\u0000\u00006\u0006\u0001\u0000" +
                    "\u0000\u000078\u0005=\u0000\u00008\b\u0001\u0000\u0000\u00009:\u0005[" +
                    "\u0000\u0000:\n\u0001\u0000\u0000\u0000;<\u0005]\u0000\u0000<\f\u0001" +
                    "\u0000\u0000\u0000=>\u0005:\u0000\u0000>\u000e\u0001\u0000\u0000\u0000" +
                    "?@\u0005*\u0000\u0000@\u0010\u0001\u0000\u0000\u0000AB\u0005/\u0000\u0000" +
                    "B\u0012\u0001\u0000\u0000\u0000CD\u0005+\u0000\u0000D\u0014\u0001\u0000" +
                    "\u0000\u0000EF\u0005-\u0000\u0000F\u0016\u0001\u0000\u0000\u0000GK\u0007" +
                    "\u0000\u0000\u0000HJ\u0007\u0001\u0000\u0000IH\u0001\u0000\u0000\u0000" +
                    "JM\u0001\u0000\u0000\u0000KI\u0001\u0000\u0000\u0000KL\u0001\u0000\u0000" +
                    "\u0000L\u0018\u0001\u0000\u0000\u0000MK\u0001\u0000\u0000\u0000NS\u0005" +
                    "\'\u0000\u0000OR\u0003\u001d\u000e\u0000PR\t\u0000\u0000\u0000QO\u0001" +
                    "\u0000\u0000\u0000QP\u0001\u0000\u0000\u0000RU\u0001\u0000\u0000\u0000" +
                    "ST\u0001\u0000\u0000\u0000SQ\u0001\u0000\u0000\u0000TV\u0001\u0000\u0000" +
                    "\u0000US\u0001\u0000\u0000\u0000VW\u0005\'\u0000\u0000W\u001a\u0001\u0000" +
                    "\u0000\u0000X]\u0005#\u0000\u0000Y\\\u0003\u001d\u000e\u0000Z\\\t\u0000" +
                    "\u0000\u0000[Y\u0001\u0000\u0000\u0000[Z\u0001\u0000\u0000\u0000\\_\u0001" +
                    "\u0000\u0000\u0000]^\u0001\u0000\u0000\u0000][\u0001\u0000\u0000\u0000" +
                    "^`\u0001\u0000\u0000\u0000_]\u0001\u0000\u0000\u0000`a\u0003-\u0016\u0000" +
                    "a\u001c\u0001\u0000\u0000\u0000bc\u0005\\\u0000\u0000cd\u0007\u0002\u0000" +
                    "\u0000d\u001e\u0001\u0000\u0000\u0000en\u00050\u0000\u0000fj\u0007\u0003" +
                    "\u0000\u0000gi\u0003)\u0014\u0000hg\u0001\u0000\u0000\u0000il\u0001\u0000" +
                    "\u0000\u0000jh\u0001\u0000\u0000\u0000jk\u0001\u0000\u0000\u0000kn\u0001" +
                    "\u0000\u0000\u0000lj\u0001\u0000\u0000\u0000me\u0001\u0000\u0000\u0000" +
                    "mf\u0001\u0000\u0000\u0000n \u0001\u0000\u0000\u0000oq\u0005-\u0000\u0000" +
                    "po\u0001\u0000\u0000\u0000pq\u0001\u0000\u0000\u0000q\u0089\u0001\u0000" +
                    "\u0000\u0000rt\u0005.\u0000\u0000su\u0003)\u0014\u0000ts\u0001\u0000\u0000" +
                    "\u0000uv\u0001\u0000\u0000\u0000vt\u0001\u0000\u0000\u0000vw\u0001\u0000" +
                    "\u0000\u0000w\u008a\u0001\u0000\u0000\u0000xz\u0003)\u0014\u0000yx\u0001" +
                    "\u0000\u0000\u0000z{\u0001\u0000\u0000\u0000{y\u0001\u0000\u0000\u0000" +
                    "{|\u0001\u0000\u0000\u0000|\u0084\u0001\u0000\u0000\u0000}\u0081\u0005" +
                    ".\u0000\u0000~\u0080\u0003)\u0014\u0000\u007f~\u0001\u0000\u0000\u0000" +
                    "\u0080\u0083\u0001\u0000\u0000\u0000\u0081\u007f\u0001\u0000\u0000\u0000" +
                    "\u0081\u0082\u0001\u0000\u0000\u0000\u0082\u0085\u0001\u0000\u0000\u0000" +
                    "\u0083\u0081\u0001\u0000\u0000\u0000\u0084}\u0001\u0000\u0000\u0000\u0084" +
                    "\u0085\u0001\u0000\u0000\u0000\u0085\u0087\u0001\u0000\u0000\u0000\u0086" +
                    "\u0088\u0003%\u0012\u0000\u0087\u0086\u0001\u0000\u0000\u0000\u0087\u0088" +
                    "\u0001\u0000\u0000\u0000\u0088\u008a\u0001\u0000\u0000\u0000\u0089r\u0001" +
                    "\u0000\u0000\u0000\u0089y\u0001\u0000\u0000\u0000\u008a\"\u0001\u0000" +
                    "\u0000\u0000\u008b\u008d\u0005-\u0000\u0000\u008c\u008b\u0001\u0000\u0000" +
                    "\u0000\u008c\u008d\u0001\u0000\u0000\u0000\u008d\u00a5\u0001\u0000\u0000" +
                    "\u0000\u008e\u0090\u0005.\u0000\u0000\u008f\u0091\u0003)\u0014\u0000\u0090" +
                    "\u008f\u0001\u0000\u0000\u0000\u0091\u0092\u0001\u0000\u0000\u0000\u0092" +
                    "\u0090\u0001\u0000\u0000\u0000\u0092\u0093\u0001\u0000\u0000\u0000\u0093" +
                    "\u00a6\u0001\u0000\u0000\u0000\u0094\u0096\u0003)\u0014\u0000\u0095\u0094" +
                    "\u0001\u0000\u0000\u0000\u0096\u0097\u0001\u0000\u0000\u0000\u0097\u0095" +
                    "\u0001\u0000\u0000\u0000\u0097\u0098\u0001\u0000\u0000\u0000\u0098\u00a0" +
                    "\u0001\u0000\u0000\u0000\u0099\u009d\u0005.\u0000\u0000\u009a\u009c\u0003" +
                    ")\u0014\u0000\u009b\u009a\u0001\u0000\u0000\u0000\u009c\u009f\u0001\u0000" +
                    "\u0000\u0000\u009d\u009b\u0001\u0000\u0000\u0000\u009d\u009e\u0001\u0000" +
                    "\u0000\u0000\u009e\u00a1\u0001\u0000\u0000\u0000\u009f\u009d\u0001\u0000" +
                    "\u0000\u0000\u00a0\u0099\u0001\u0000\u0000\u0000\u00a0\u00a1\u0001\u0000" +
                    "\u0000\u0000\u00a1\u00a3\u0001\u0000\u0000\u0000\u00a2\u00a4\u0003\'\u0013" +
                    "\u0000\u00a3\u00a2\u0001\u0000\u0000\u0000\u00a3\u00a4\u0001\u0000\u0000" +
                    "\u0000\u00a4\u00a6\u0001\u0000\u0000\u0000\u00a5\u008e\u0001\u0000\u0000" +
                    "\u0000\u00a5\u0095\u0001\u0000\u0000\u0000\u00a6$\u0001\u0000\u0000\u0000" +
                    "\u00a7\u00a9\u0007\u0004\u0000\u0000\u00a8\u00aa\u0007\u0005\u0000\u0000" +
                    "\u00a9\u00a8\u0001\u0000\u0000\u0000\u00a9\u00aa\u0001\u0000\u0000\u0000" +
                    "\u00aa\u00ac\u0001\u0000\u0000\u0000\u00ab\u00ad\u0003)\u0014\u0000\u00ac" +
                    "\u00ab\u0001\u0000\u0000\u0000\u00ad\u00ae\u0001\u0000\u0000\u0000\u00ae" +
                    "\u00ac\u0001\u0000\u0000\u0000\u00ae\u00af\u0001\u0000\u0000\u0000\u00af" +
                    "&\u0001\u0000\u0000\u0000\u00b0\u00b2\u0005D\u0000\u0000\u00b1\u00b3\u0007" +
                    "\u0005\u0000\u0000\u00b2\u00b1\u0001\u0000\u0000\u0000\u00b2\u00b3\u0001" +
                    "\u0000\u0000\u0000\u00b3\u00b5\u0001\u0000\u0000\u0000\u00b4\u00b6\u0003" +
                    ")\u0014\u0000\u00b5\u00b4\u0001\u0000\u0000\u0000\u00b6\u00b7\u0001\u0000" +
                    "\u0000\u0000\u00b7\u00b5\u0001\u0000\u0000\u0000\u00b7\u00b8\u0001\u0000" +
                    "\u0000\u0000\u00b8(\u0001\u0000\u0000\u0000\u00b9\u00ba\u0007\u0006\u0000" +
                    "\u0000\u00ba*\u0001\u0000\u0000\u0000\u00bb\u00bc\u0005/\u0000\u0000\u00bc" +
                    "\u00bd\u0005/\u0000\u0000\u00bd\u00c1\u0001\u0000\u0000\u0000\u00be\u00c0" +
                    "\t\u0000\u0000\u0000\u00bf\u00be\u0001\u0000\u0000\u0000\u00c0\u00c3\u0001" +
                    "\u0000\u0000\u0000\u00c1\u00c2\u0001\u0000\u0000\u0000\u00c1\u00bf\u0001" +
                    "\u0000\u0000\u0000\u00c2\u00c4\u0001\u0000\u0000\u0000\u00c3\u00c1\u0001" +
                    "\u0000\u0000\u0000\u00c4\u00c5\u0003-\u0016\u0000\u00c5\u00c6\u0001\u0000" +
                    "\u0000\u0000\u00c6\u00c7\u0006\u0015\u0000\u0000\u00c7,\u0001\u0000\u0000" +
                    "\u0000\u00c8\u00ca\u0005\r\u0000\u0000\u00c9\u00c8\u0001\u0000\u0000\u0000" +
                    "\u00c9\u00ca\u0001\u0000\u0000\u0000\u00ca\u00cb\u0001\u0000\u0000\u0000" +
                    "\u00cb\u00cc\u0005\n\u0000\u0000\u00cc.\u0001\u0000\u0000\u0000\u00cd" +
                    "\u00cf\u0007\u0007\u0000\u0000\u00ce\u00cd\u0001\u0000\u0000\u0000\u00cf" +
                    "\u00d0\u0001\u0000\u0000\u0000\u00d0\u00ce\u0001\u0000\u0000\u0000\u00d0" +
                    "\u00d1\u0001\u0000\u0000\u0000\u00d1\u00d2\u0001\u0000\u0000\u0000\u00d2" +
                    "\u00d3\u0006\u0017\u0000\u0000\u00d30\u0001\u0000\u0000\u0000\u001d\u0000" +
                    "KQS[]jmpv{\u0081\u0084\u0087\u0089\u008c\u0092\u0097\u009d\u00a0\u00a3" +
                    "\u00a5\u00a9\u00ae\u00b2\u00b7\u00c1\u00c9\u00d0\u0001\u0000\u0001\u0000";
    public static final ATN _ATN =
            new ATNDeserializer().deserialize(_serializedATN.toCharArray());
    protected static final DFA[] _decisionToDFA;
    protected static final PredictionContextCache _sharedContextCache =
            new PredictionContextCache();
    private static final String[] _LITERAL_NAMES = makeLiteralNames();
    private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
    public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);
    public static String[] channelNames = {
            "DEFAULT_TOKEN_CHANNEL", "HIDDEN"
    };
    public static String[] modeNames = {
            "DEFAULT_MODE"
    };

    static {
        RuntimeMetaData.checkVersion("4.12.0", RuntimeMetaData.VERSION);
    }

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

    static {
        _decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
        for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
            _decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
        }
    }

    public TypingLexer(CharStream input) {
        super(input);
        _interp = new LexerATNSimulator(this, _ATN, _decisionToDFA, _sharedContextCache);
    }

    private static String[] makeRuleNames() {
        return new String[]{
                "T__0", "T__1", "T__2", "T__3", "T__4", "T__5", "T__6", "T__7", "T__8",
                "T__9", "T__10", "ID", "STRING", "COMMENT", "ESC", "INT", "NUM", "DP",
                "EXP", "DEXP", "DIG", "TDD_COMMENT", "NEWLINE", "WS"
        };
    }

    private static String[] makeLiteralNames() {
        return new String[]{
                null, "'('", "','", "')'", "'='", "'['", "']'", "':'", "'*'", "'/'",
                "'+'", "'-'"
        };
    }

    private static String[] makeSymbolicNames() {
        return new String[]{
                null, null, null, null, null, null, null, null, null, null, null, null,
                "ID", "STRING", "COMMENT", "INT", "NUM", "DP", "TDD_COMMENT", "NEWLINE",
                "WS"
        };
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
    public String getGrammarFileName() {
        return "Typing.g4";
    }

    @Override
    public String[] getRuleNames() {
        return ruleNames;
    }

    @Override
    public String getSerializedATN() {
        return _serializedATN;
    }

    @Override
    public String[] getChannelNames() {
        return channelNames;
    }

    @Override
    public String[] getModeNames() {
        return modeNames;
    }

    @Override
    public ATN getATN() {
        return _ATN;
    }
}