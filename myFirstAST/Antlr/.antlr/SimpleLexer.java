// Generated from /Users/vv/workspace/tcomp/src/myFirstAST/Antlr/Simple.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.Lexer;
import org.antlr.v4.runtime.CharStream;
import org.antlr.v4.runtime.Token;
import org.antlr.v4.runtime.TokenStream;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.misc.*;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue", "this-escape"})
public class SimpleLexer extends Lexer {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, T__4=5, COMMENT=6, WS=7, VAR=8, INT=9, 
		MUL=10, DIV=11, ADD=12, SUB=13;
	public static String[] channelNames = {
		"DEFAULT_TOKEN_CHANNEL", "HIDDEN"
	};

	public static String[] modeNames = {
		"DEFAULT_MODE"
	};

	private static String[] makeRuleNames() {
		return new String[] {
			"T__0", "T__1", "T__2", "T__3", "T__4", "COMMENT", "WS", "VAR", "INT", 
			"MUL", "DIV", "ADD", "SUB"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'let'", "'='", "'in'", "'('", "')'", null, null, null, null, "'*'", 
			"'/'", "'+'", "'-'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, null, "COMMENT", "WS", "VAR", "INT", "MUL", 
			"DIV", "ADD", "SUB"
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


	public SimpleLexer(CharStream input) {
		super(input);
		_interp = new LexerATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@Override
	public String getGrammarFileName() { return "Simple.g4"; }

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
		"\u0004\u0000\rN\u0006\uffff\uffff\u0002\u0000\u0007\u0000\u0002\u0001"+
		"\u0007\u0001\u0002\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004"+
		"\u0007\u0004\u0002\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007"+
		"\u0007\u0007\u0002\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b"+
		"\u0007\u000b\u0002\f\u0007\f\u0001\u0000\u0001\u0000\u0001\u0000\u0001"+
		"\u0000\u0001\u0001\u0001\u0001\u0001\u0002\u0001\u0002\u0001\u0002\u0001"+
		"\u0003\u0001\u0003\u0001\u0004\u0001\u0004\u0001\u0005\u0001\u0005\u0001"+
		"\u0005\u0001\u0005\u0005\u0005-\b\u0005\n\u0005\f\u00050\t\u0005\u0001"+
		"\u0005\u0001\u0005\u0001\u0005\u0001\u0005\u0001\u0006\u0004\u00067\b"+
		"\u0006\u000b\u0006\f\u00068\u0001\u0006\u0001\u0006\u0001\u0007\u0004"+
		"\u0007>\b\u0007\u000b\u0007\f\u0007?\u0001\b\u0004\bC\b\b\u000b\b\f\b"+
		"D\u0001\t\u0001\t\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001\f\u0001"+
		"\f\u0001.\u0000\r\u0001\u0001\u0003\u0002\u0005\u0003\u0007\u0004\t\u0005"+
		"\u000b\u0006\r\u0007\u000f\b\u0011\t\u0013\n\u0015\u000b\u0017\f\u0019"+
		"\r\u0001\u0000\u0003\u0003\u0000\t\n\r\r  \u0002\u0000AZaz\u0001\u0000"+
		"09Q\u0000\u0001\u0001\u0000\u0000\u0000\u0000\u0003\u0001\u0000\u0000"+
		"\u0000\u0000\u0005\u0001\u0000\u0000\u0000\u0000\u0007\u0001\u0000\u0000"+
		"\u0000\u0000\t\u0001\u0000\u0000\u0000\u0000\u000b\u0001\u0000\u0000\u0000"+
		"\u0000\r\u0001\u0000\u0000\u0000\u0000\u000f\u0001\u0000\u0000\u0000\u0000"+
		"\u0011\u0001\u0000\u0000\u0000\u0000\u0013\u0001\u0000\u0000\u0000\u0000"+
		"\u0015\u0001\u0000\u0000\u0000\u0000\u0017\u0001\u0000\u0000\u0000\u0000"+
		"\u0019\u0001\u0000\u0000\u0000\u0001\u001b\u0001\u0000\u0000\u0000\u0003"+
		"\u001f\u0001\u0000\u0000\u0000\u0005!\u0001\u0000\u0000\u0000\u0007$\u0001"+
		"\u0000\u0000\u0000\t&\u0001\u0000\u0000\u0000\u000b(\u0001\u0000\u0000"+
		"\u0000\r6\u0001\u0000\u0000\u0000\u000f=\u0001\u0000\u0000\u0000\u0011"+
		"B\u0001\u0000\u0000\u0000\u0013F\u0001\u0000\u0000\u0000\u0015H\u0001"+
		"\u0000\u0000\u0000\u0017J\u0001\u0000\u0000\u0000\u0019L\u0001\u0000\u0000"+
		"\u0000\u001b\u001c\u0005l\u0000\u0000\u001c\u001d\u0005e\u0000\u0000\u001d"+
		"\u001e\u0005t\u0000\u0000\u001e\u0002\u0001\u0000\u0000\u0000\u001f \u0005"+
		"=\u0000\u0000 \u0004\u0001\u0000\u0000\u0000!\"\u0005i\u0000\u0000\"#"+
		"\u0005n\u0000\u0000#\u0006\u0001\u0000\u0000\u0000$%\u0005(\u0000\u0000"+
		"%\b\u0001\u0000\u0000\u0000&\'\u0005)\u0000\u0000\'\n\u0001\u0000\u0000"+
		"\u0000()\u0005-\u0000\u0000)*\u0005-\u0000\u0000*.\u0001\u0000\u0000\u0000"+
		"+-\t\u0000\u0000\u0000,+\u0001\u0000\u0000\u0000-0\u0001\u0000\u0000\u0000"+
		"./\u0001\u0000\u0000\u0000.,\u0001\u0000\u0000\u0000/1\u0001\u0000\u0000"+
		"\u00000.\u0001\u0000\u0000\u000012\u0005\n\u0000\u000023\u0001\u0000\u0000"+
		"\u000034\u0006\u0005\u0000\u00004\f\u0001\u0000\u0000\u000057\u0007\u0000"+
		"\u0000\u000065\u0001\u0000\u0000\u000078\u0001\u0000\u0000\u000086\u0001"+
		"\u0000\u0000\u000089\u0001\u0000\u0000\u00009:\u0001\u0000\u0000\u0000"+
		":;\u0006\u0006\u0000\u0000;\u000e\u0001\u0000\u0000\u0000<>\u0007\u0001"+
		"\u0000\u0000=<\u0001\u0000\u0000\u0000>?\u0001\u0000\u0000\u0000?=\u0001"+
		"\u0000\u0000\u0000?@\u0001\u0000\u0000\u0000@\u0010\u0001\u0000\u0000"+
		"\u0000AC\u0007\u0002\u0000\u0000BA\u0001\u0000\u0000\u0000CD\u0001\u0000"+
		"\u0000\u0000DB\u0001\u0000\u0000\u0000DE\u0001\u0000\u0000\u0000E\u0012"+
		"\u0001\u0000\u0000\u0000FG\u0005*\u0000\u0000G\u0014\u0001\u0000\u0000"+
		"\u0000HI\u0005/\u0000\u0000I\u0016\u0001\u0000\u0000\u0000JK\u0005+\u0000"+
		"\u0000K\u0018\u0001\u0000\u0000\u0000LM\u0005-\u0000\u0000M\u001a\u0001"+
		"\u0000\u0000\u0000\u0005\u0000.8?D\u0001\u0006\u0000\u0000";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}