import ply.lex as lex

# Reserved keywords
reserved = {
    'let': 'LET',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'set': 'SET',
    'unit': 'UNIT_LITERAL',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'new': 'NEW',
    'Int': 'INT_TYPE',
    'Bool': 'BOOL_TYPE',
    'Unit': 'UNIT_TYPE',
    'String': 'STRING_TYPE'
}

# Token names
tokens = [
    'ID', 'INT_LITERAL', 'STRING_LITERAL',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD', 'POWER',
    'EQUALS', 'NOT_EQUALS', 'LESS', 'LESS_EQUAL', 'GREATER', 'GREATER_EQUAL',
    'AND', 'OR', 'NOT', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'COMMA', 'SEMICOLON',
    'BAR', 'ARROW', 'COLON', 'UNDERSCORE', 'ASSIGN'
] + list(reserved.values())

# Token regular expressions
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_POWER = r'\^'
t_EQUALS = r'=='
t_NOT_EQUALS = r'!='
t_LESS = r'<'
t_LESS_EQUAL = r'<='
t_GREATER = r'>'
t_GREATER_EQUAL = r'>='
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COMMA = r','
t_SEMICOLON = r';'
t_BAR = r'\|'
t_ARROW = r'->'
t_COLON = r':'
t_UNDERSCORE = r'_'
t_ASSIGN = r'='

# Identifier rule
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9\']*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Integer literal rule
def t_INT_LITERAL(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# String literal rule
def t_STRING_LITERAL(t):
    r'"([^"\\]|\\.)*"'
    t.value = t.value[1:-1]  # Remove surrounding quotes
    return t

# Ignored characters (whitespace)
t_ignore = " \t"

# Comment rule
t_ignore_COMMENT = r'\-\-.*'

# Newline rule
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = (token.lexpos - last_cr)
    return column

# Error handling rule
def t_error(t):
    col = find_column(t.lexer.lexdata, t)
    print(f"Lexical error: Illegal character '{t.value[0]}' at line {t.lexer.lineno}, column {col}")
    t.lexer.skip(1)

lexer = lex.lex()

# if __name__ == '__main__':
#     import sys

#     # lexer.input(sys.stdin.read())
#     with open("aguda-compiler/tests/collatz.agu") as f:
#         lexer.input(f.read())

#     while True:
#         tok = lexer.token()
#         if not tok: 
#             break      # No more input
#         print(tok)