# Lexer first

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
    'length': 'LENGTH',
    'print': 'PRINT',
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

# Build the lexer
import ply.lex as lex
lexer = lex.lex()

# 2. Parser

import syntax as s

# Define operator precedence and associativity
# https://introcs.cs.princeton.edu/java/11precedence/
precedence = (
    ('rigth', 'SEMICOLON'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOT_EQUALS'),
    ('left', 'LESS', 'LESS_EQUAL', 'GREATER', 'GREATER_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'POWER'),
    ('right', 'UMINUS', 'NOT'),
)

# Grammar rules

def p_program(t):
    '''program : declarations'''
    t[0] = s.Program(t[1])

def p_declarations(t):
    '''declarations : declaration
                    | declaration declarations'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[2]]

def p_declaration(t):
    '''declaration : variable_declaration
                   | function_declaration'''
    t[0] = t[1]

def p_variable_declaration(t):
    '''variable_declaration : LET ID COLON type EQUALS expression'''
    t[0] = s.VariableDeclaration(t[2], t[4], t[6])

def p_function_declaration(t):
    '''function_declaration : LET ID LPAREN function_parameters RPAREN COLON function_type EQUALS expression'''
    t[0] = s.FunctionDeclaration(t[2], t[4], t[7], t[9], t[11])

def p_function_parameters(t):
    '''function_parameters : ID
                           | ID COMMA function_parameters'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

def p_type(t):
    '''type : INT_TYPE
            | BOOL_TYPE
            | UNIT_TYPE
            | STRING_TYPE
            | type LBRACKET RBRACKET'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = s.ArrayType(t[1])

def p_function_type(t):
    '''function_type : type ARROW type
                     | LPAREN function_type_multi RPAREN ARROW type'''
    if len(t) == 4:
        t[0] = s.FunctionType(t[1], t[3])
    else:
        t[0] = s.FunctionType(t[2], t[5])

def p_function_type_multi(t):
    '''function_type_multi : type
                           | type COMMA function_type_multi'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

#TODO possivelmente dá para meter p_exp_ antes
# de cada produção e separar
# TODO adicionar aqui os unários + variable_declaration
def p_expression(t):
    '''expression : binary_expression
                  | assignment
                  | conditional
                  | while_loop
                  | function_call
                  | array_creation
                  | array_access
                  | literal
                  | variable
                  | LPAREN expression RPAREN'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = t[2]

#TODO mesmo que o anterior
def p_binary_expression(t):
    '''binary_expression : expression PLUS expression
                        | expression MINUS expression
                        | expression TIMES expression
                        | expression DIVIDE expression
                        | expression MOD expression
                        | expression POWER expression
                        | expression EQUALS expression
                        | expression NOT_EQUALS expression
                        | expression LESS expression
                        | expression LESS_EQUAL expression
                        | expression GREATER expression
                        | expression GREATER_EQUAL expression
                        | expression AND expression
                        | expression OR expression'''
    t[0] = s.BinaryOp(t[1], t[2], t[3])

#TODO -1 deve-se transformar em 0-1, mas e o NOT?
def p_unary_expression(t):
    '''unary_expression : MINUS expression %prec UMINUS
                        | NOT expression'''
    t[0] = s.UnaryOp(t[1], t[2])

def p_assignment(t):
    '''assignment : variable EQUALS expression
                  | array_access EQUALS expression'''
    t[0] = s.Assignment(t[1], t[3])

def p_conditional(t):
    '''conditional : IF expression THEN expression ELSE expression
                   | IF expression THEN expression'''
    if len(t) == 5:
        #TODO é assim que se referencia o UNIT?
        # provavelmente não, e UNIT tem que ser do tipo expression algures
        t[0] = s.Conditional(t[2], t[4], "UNIT")
    else:
        t[0] = s.Conditional(t[2], t[4], t[6])

def p_while_loop(t):
    '''while_loop : WHILE expression DO expression'''
    t[0] = s.WhileLoop(t[2], t[4])

def p_function_call(t):
    '''function_call : ID LPAREN function_call_args RPAREN'''
    t[0] = s.FunctionCall(t[1], t[3])

def p_function_call_args(t):
    '''function_call_args : expression
                          | expression COMMA function_call_args'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

def p_array_creation(t):
    '''array_creation : NEW type LBRACKET expression BAR expression RBRACKET'''
    t[0] = s.ArrayCreation(t[2], t[4], t[6])

def p_array_access(t):
    '''array_access : expression LBRACKET expression RBRACKET'''
    t[0] = s.ArrayAccess(t[1], t[3])

def p_literal(t):
    '''literal : INT_LITERAL
               | TRUE
               | FALSE
               | NULL
               | STRING_LITERAL'''
    if t[1] == 'true':
        t[0] = s.BoolLiteral(True)
    elif t[1] == 'false':
        t[0] = s.BoolLiteral(False)
    elif t[1] == 'null':
        t[0] = s.NullLiteral()
    elif isinstance(t[1], int):
        t[0] = s.IntLiteral(t[1])
    else:
        t[0] = s.StringLiteral(t[1])

def p_variable(t):
    '''variable : ID'''
    t[0] = s.Variable(t[1])

def p_error(t):
    print(f"Syntax error at '{t.value}' on line {t.lineno}")

# Build the parser
import ply.yacc as yacc
parser = yacc.yacc()

