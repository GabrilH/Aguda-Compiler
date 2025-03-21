/*
Técnicas de Compilação
Mestrado em Engenharia Informática
Faculdade de Ciências
Universidade de Lisboa
2024/2025
Vasco T. Vasconcelos

ANTLR:
    https://www.antlr.org/

Installing ANTLR:
    See book "The Definitive ANTLR 4 Reference", Section 1.1

Run as:
$ antlr4 Lang.g4
$ javac *java
$ grun Lang r -tokens < example.lang
$ grun Lang lang -gui < example.lang
*/

grammar Lang;

lang: stmt+ ;

stmt: 'print' exp
    | ID '=' exp
    ;

exp: exp '+' exp
    | ID
    | NUMBER
    ;

COMMENT : '--' .*? '\n' -> skip ;
WS : [ \t\r\n]+ -> skip ;
ID : [a-zA-Z]+ ;
NUMBER : [0-9]+ ;
