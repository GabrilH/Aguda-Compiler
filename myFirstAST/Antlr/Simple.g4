/*
A parser for the Simple programming language

Usage:
$ antlr4 Simple.g4
$ javac *java
$ grun Simple r -tokens < ../example.simple
$ grun Simple exp -gui < ../example.simple

Author: Técnicas de Compilação
        Mestrado em Engenharia Informática
        Faculdade de Ciências
        Universidade de Lisboa
        2024/2025
        Alcides Fonseca
        Vasco T. Vasconcelos
*/

grammar Simple;

exp: '-' exp                               # UnMinus
    | <assoc=left> exp op=('*'|'/') exp    # MultDiv
    | <assoc=left> exp op=('+'|'-') exp    # AddSub
    | 'let' VAR '=' exp 'in' exp           # Let
    | INT                                  # Int
    | VAR                                  # Var
    | '(' exp ')'                          # Parens
    ;
	
COMMENT : '--' .*? '\n' -> skip ;
WS : [ \t\r\n]+ -> skip ;
VAR : [a-zA-Z]+ ;
INT : [0-9]+ ;
// token names for the operator literals so that, later, we
// can reference token names as Java constants in the visitor.
MUL : '*' ;
DIV : '/' ;
ADD : '+' ;
SUB : '-' ;