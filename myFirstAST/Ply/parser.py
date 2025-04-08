"""
A parser for the Simple programming language

Author: Técnicas de Compilação
        Mestrado em Engenharia Informática
        Faculdade de Ciências
        Universidade de Lisboa
        2024/2025
        Alcides Fonseca
        Vasco T. Vasconcelos
"""

# 1. Lexer

reserved = {
    'let' : 'LET',
    'in' : 'IN'
    }

tokens = [
    'ID','NUMBER',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN'
    ] + list(reserved.values())

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQUALS  = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LET     = r'let'
t_IN      = r'in'

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

t_ignore_COMMENT = r'\-\-.*'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# 2. Parser

import syntax as s

precedence = (
    ('left','PLUS','MINUS'),
    ('left','TIMES','DIVIDE'),
    ('right','UMINUS'),
    ('right','IN'),
    )

def p_exp_let(t):
    'exp : LET ID EQUALS exp IN exp'
    t[0] = s.Let(t[2], t[4], t[6])

def p_exp_binop(t):
    '''exp : exp PLUS exp
                  | exp MINUS exp
                  | exp TIMES exp
                  | exp DIVIDE exp'''
    t[0] = s.Op(t[1], t[2], t[3])

def p_exp_uminus(t):
    'exp : MINUS exp %prec UMINUS'
    t[0] = s.Op(s.Int(0), t[1], t[2])

def p_exp_group(t):
    'exp : LPAREN exp RPAREN'
    t[0] = t[2]

def p_exp_number(t):
    'exp : NUMBER'
    t[0] = s.Int(t[1])

def p_exp_id(t):
    'exp : ID'
    t[0] = s.Var(t[1])

def p_error(t):
    print("Syntax error at '%s'" % t.value)

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()
