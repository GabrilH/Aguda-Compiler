all: simple

SimpleParser.java: Simple.g4
	/opt/homebrew/bin/antlr Simple.g4

simple: SimpleParser.java Simple.java
	javac Simple.java

clean:
	rm -f SimpleLexer.interp SimpleListener.java Simple.tokens SimpleLexer.java SimpleParser.java Simple.interp SimpleBaseListener.java SimpleLexer.tokens *class