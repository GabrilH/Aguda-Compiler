__copyright__ = """
    Técnicas de Compilação
    Mestrado em Engenharia Informática
    Faculdade de Ciências
    Universidade de Lisboa
    2024/2025"""
__author__ = "Vasco Vasconcelos"

# Run as
#   $ python3 calc.py < example.lang

# To install ply use pip.

# For further info about ply, refer to https://ply.readthedocs.io/en/latest/ply.html

# The list of tokens
tokens = (
    'VAR', 'NUMBER', 'PRINT',
    'PLUS','MINUS','TIMES','DIVIDE','EQUALS',
    'LPAREN','RPAREN',
    )

# Regular expressions for the various tokens
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

reserved = {
    'print' : 'PRINT'
}

def t_VAR(t):
    r'[a-zA-Z_][a-zA-Z_0-9_\']*'
    t.type = reserved.get(t.value,'VAR')    # Check for reserved words
    return t
    
t_ignore = " \t\n"

t_ignore_COMMENT = r'--.*'
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    
# Build the lexer
import ply.lex as lex
lexer = lex.lex()

if __name__ == '__main__':
    import sys

    lexer.input(sys.stdin.read())
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)
