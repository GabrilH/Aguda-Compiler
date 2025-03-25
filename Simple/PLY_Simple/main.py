"""
A parser for the Simple programming language

Usage:
  $ pip3 install ply
  $ python3 main.py < ../example.simple


Author: Técnicas de Compilação
        Mestrado em Engenharia Informática
        Faculdade de Ciências
        Universidade de Lisboa
        2024/2025
        Alcides Fonseca
        Vasco T. Vasconcelos
"""

# Lexer first

reserved = {
    'let' : 'LET',
    'in' : 'IN'
    }

tokens = [
    'ID','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN'
    ] + list(reserved.values())

# Regras para identificar os tokens

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LET     = r'let'
t_IN      = r'in'

# Para regras mais complexas

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

t_ignore = " \t"


# qualquer comentario de linha (. não reconhece \n)
t_ignore_COMMENT = r'\-\-.*'

# para controlar as linhas de posição do codigo
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# Parsing second

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    ('right','IN'),
    )

# tem sempre que começar com p - produção mas pode ser p_exp_let
def p_expression_let(t):
    'expression : LET ID EQUALS expression IN expression'

def p_expression_binop(t):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''

def p_expression_uminus(t):
    'expression : MINUS expression %prec UMINUS'

def p_expression_group(t):
    'expression : LPAREN expression RPAREN'

def p_expression_number(t):
    'expression : NUMBER'

def p_expression_id(t):
    'expression : ID'

def p_error(t):
    print("Syntax error at '%s'" % t.value)

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()

# A little main

if __name__ == '__main__':
    import sys
    print(parser.parse(sys.stdin.read()))
    # expect None
