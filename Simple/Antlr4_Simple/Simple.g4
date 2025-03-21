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

exp: '-' exp
    | exp ('+'|'-') exp
    | exp ('*'|'/') exp
    | 'let' VAR '=' exp 'in' exp
    | INT
    | VAR
    | '(' exp ')'
    ;
	
COMMENT : '--' .*? '\n' -> skip ;
WS : [ \t\r\n]+ -> skip ;
VAR : [a-zA-Z]+ ;
INT : [0-9]+ ;
