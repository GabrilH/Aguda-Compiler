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
    'unit': 'UNIT',
    'true': 'TRUE',
    'false': 'FALSE',
    'null': 'NULL',
    'new': 'NEW',
    'length': 'LENGTH', #TODO maybe remove
    'print': 'PRINT', #TODO maybe remove
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
    'BAR'
] + list(reserved.values())

# Token regular expressions
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'
t_POWER = r'\^'
t_EQUALS = r'='
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

# Identifier rule
def t_ID(t):
    r'[a-zA-Z][a-zA-Z_0-9\']*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

# Integer literal rule
def t_INT_LITERAL(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

# String literal rule
def t_STRING_LITERAL(t):
    r'"([^"\\n]*)"'
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

# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()