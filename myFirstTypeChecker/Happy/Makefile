all: typeCheck

Lexer: Lexer.x
	alex Lexer.x

Parser: Parser.y
	happy Parser.y

typeCheck: Lexer Parser Syntax.hs TypeChecker.hs Main.hs
	ghc --make Main

clean:
	rm -f Main Parser.hs Lexer.hs *.o *.hi *~ *# .#*
