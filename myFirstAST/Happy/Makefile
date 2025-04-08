all: calc

Lexer.hs: Lexer.x
	alex Lexer.x

Parser.hs: Parser.y
	happy Parser.y

calc: Lexer.hs Parser.hs Syntax.hs Calc.hs
	ghc --make Calc

clean:
	rm -f Calc Parser.hs Lexer.hs *.o *.hi *~ *# .#*
