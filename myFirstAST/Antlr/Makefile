all: simple

SimpleParser.java: Simple.g4
	/opt/homebrew/bin/antlr -no-listener -visitor Simple.g4

simple: SimpleParser.java Calc.java
	javac Calc.java

clean:
	rm -f SimpleLexer.interp SimpleListener.java Simple.tokens SimpleLexer.java SimpleParser.java Simple.interp SimpleBaseListener.java SimpleVisitor.java SimpleBaseVisitor.java SimpleLexer.tokens *class