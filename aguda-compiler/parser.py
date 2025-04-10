import ply.yacc as yacc
import syntax as s
from lexer import tokens

# Define operator precedence and associativity
# https://introcs.cs.princeton.edu/java/11precedence/
precedence = (
    ('right', 'SEMICOLON'),
    ('right', 'ASSIGN'),
    ('right', 'ARROW'),
    ('nonassoc', 'WHILE', 'IF'),
    ('right', 'THEN', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOT_EQUALS'),
    ('left', 'LESS', 'LESS_EQUAL', 'GREATER', 'GREATER_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'POWER'),
    ('right', 'UMINUS', 'NOT')
)

# Grammar rules

def p_program(t):
    '''program : declarations'''
    t[0] = s.Program(t[1])

def p_declarations(t):
    '''declarations : declaration declarations_tail'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = [t[1]] + t[2]

def p_declarations_tail(t):
    '''declarations_tail : declaration declarations_tail
                         | empty'''
    if len(t) == 3:
        t[0] = [t[1]] + t[2]
    else:
        t[0] = []

def p_declaration(t):
    '''declaration : variable_declaration
                   | function_declaration'''
    t[0] = t[1]

def p_function_declaration(t):
    '''function_declaration : LET ID LPAREN parameters RPAREN COLON function_type ASSIGN exp'''
    t[0] = s.FunctionDeclaration(t[2], t[4], t[7], t[9])

def p_parameters(t):
    '''parameters : variable parameters_tail'''
    t[0] = [t[1]] + t[2]

def p_parameters_tail(t):
    '''parameters_tail : COMMA variable parameters_tail
                       | empty'''
    if len(t) == 4:
        t[0] = [t[2]] + t[3]
    else:
        t[0] = []

# There is an intentional shift/reduce conflict involving `array_suffix`
# when parsing `type` and `array_creation`, both with `LBRACKET` as lookahead.
# code e.g. new Int[] [n | new Int [n | 0]]
# 
# After the reading 'Int', the parser resolves the conflict by shifting
# to parse `array_suffix` as part of `type`, and then it will parse the rest
def p_type(t):
    '''
    type : INT_TYPE
         | STRING_TYPE
         | UNIT_TYPE
         | BOOL_TYPE
         | array_type
    '''
    t[0] = t[1]

def p_array_type(t):
    'array_type : type LBRACKET RBRACKET '
    t[0] = s.ArrayType(t[1],0)

# def p_type(t):
#     '''type : base_type array_suffix'''
#     if t[2] > 0:
#         t[0] = s.ArrayType(t[1], t[2])
#     else:
#         t[0] = t[1]

# def p_base_type(t):
#     '''base_type : INT_TYPE
#                  | BOOL_TYPE
#                  | UNIT_TYPE
#                  | STRING_TYPE'''
#     t[0] = s.BaseType(t[1])

# def p_array_suffix(t):
#     '''array_suffix : LBRACKET RBRACKET array_suffix
#                     | empty'''
#     if len(t) == 4:
#         t[0] = 1 + t[3] # count the number of brackets
#     else:
#         t[0] = 0

def p_function_type(t):
    '''function_type : type ARROW type
                     | LPAREN type function_type_tail RPAREN ARROW type'''
    if len(t) == 4:
        t[0] = s.FunctionType([t[1]], t[3])
    else:
        t[0] = s.FunctionType([t[2]] + t[3], t[5])

def p_function_type_tail(t):
    '''function_type_tail : COMMA type function_type_tail
                          | empty'''
    if len(t) == 4:
        t[0] = [t[2]] + t[3]
    else:
        t[0] = []

def p_exp(t):
    '''exp : variable
            | literal
            | binary_exp
            | unary_exp
            | function_call
            | assignment
            | variable_declaration
            | if_then_else
            | if_then
            | while_loop
            | array_creation
            | array_access
            | group'''
    t[0] = t[1]

def p_variable(t):
    '''variable : ID
                | UNDERSCORE'''
    t[0] = s.Var(t[1])

def p_literal(t):
    '''literal : INT_LITERAL
               | TRUE
               | FALSE
               | NULL
               | UNIT
               | STRING_LITERAL'''
    if t[1] == 'true':
        t[0] = s.BoolLiteral(True)
    elif t[1] == 'false':
        t[0] = s.BoolLiteral(False)
    elif t[1] == 'null':
        t[0] = s.NullLiteral()
    elif t[1] == 'unit':
        t[0] = s.UnitLiteral()
    elif isinstance(t[1], int):
        t[0] = s.IntLiteral(t[1])
    else:
        t[0] = s.StringLiteral(t[1])

def p_binary_exp(t):
    '''binary_exp : exp PLUS exp
                    | exp MINUS exp
                    | exp TIMES exp
                    | exp DIVIDE exp
                    | exp MOD exp
                    | exp POWER exp
                    | exp EQUALS exp
                    | exp NOT_EQUALS exp
                    | exp LESS exp
                    | exp LESS_EQUAL exp
                    | exp GREATER exp
                    | exp GREATER_EQUAL exp
                    | exp AND exp
                    | exp OR exp
                    | exp SEMICOLON exp'''
    t[0] = s.BinaryOp(t[1], t[2], t[3])

def p_unary_exp(t):
    '''unary_exp : MINUS exp %prec UMINUS
                 | NOT exp'''
    if t[1] == '-':
        t[0] = s.BinaryOp(s.IntLiteral(0), '-', t[2])
    else:
        t[0] = s.LogicalNegation(t[2])

def p_function_call(t):
    '''function_call : variable LPAREN arguments RPAREN'''
    t[0] = s.FunctionCall(t[1], t[3])

def p_arguments(t):
    '''arguments : exp arguments_tail'''
    t[0] = [t[1]] + t[2]

def p_arguments_tail(t):
    '''arguments_tail : COMMA exp arguments_tail
                      | empty'''
    if len(t) == 4:
        t[0] = [t[2]] + t[3]
    else:
        t[0] = []

def p_assignment(t):
    '''assignment : SET lhs ASSIGN exp'''
    t[0] = s.Assignment(t[2], t[4])

def p_lhs(t):
    '''lhs : variable
           | array_access'''
    t[0] = t[1]

def p_array_access(t):
    '''array_access : lhs LBRACKET exp RBRACKET'''
    t[0] = s.ArrayAccess(t[1], t[3])

def p_variable_declaration(t):
    '''variable_declaration : LET variable COLON type ASSIGN exp'''
    t[0] = s.VariableDeclaration(t[2], t[4], t[6])

def p_if_then_else(t):
    '''if_then_else : IF exp THEN exp ELSE exp %prec IF'''
    t[0] = s.Conditional(t[2], t[4], t[6])

def p_if_then(t):
    '''if_then : IF exp THEN exp %prec IF'''
    t[0] = s.Conditional(t[2], t[4], s.UnitLiteral())

# def p_conditional(t):
#     '''conditional : IF exp THEN exp conditional_else %prec IF'''
#     t[0] = s.Conditional(t[2], t[4], t[5])

# def p_conditional_else(t):
#     '''conditional_else : ELSE exp
#                         | empty'''
#     if len(t) == 3:
#         t[0] = t[2]
#     else:
#         t[0] = s.UnitLiteral()

def p_while_loop(t):
    '''while_loop : WHILE exp DO exp %prec WHILE'''
    t[0] = s.WhileLoop(t[2], t[4])

# There is an intentional shift/reduce conflict involving `array_suffix`
# when parsing `type` and `array_creation`, both with `LBRACKET` as lookahead.
# code e.g. new Int[] [n | new Int [n | 0]]
# 
# After the reading 'Int', the parser resolves the conflict by shifting
# to parse `array_suffix` as part of `type`, and then it will parse the rest
def p_array_creation(t):
    '''array_creation : NEW type LBRACKET exp BAR exp RBRACKET'''
    t[0] = s.ArrayCreation(t[2], t[4], t[6])

# def p_array_initializer(t):
#     '''array_initializer : LBRACKET array_initializer_tail RBRACKET'''
#     t[0] = t[2]

def p_group(t):
    '''group : LPAREN exp RPAREN'''
    t[0] = t[2]

def p_empty(t):
    '''empty :'''
    t[0] = []

def find_column(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = (token.lexpos - last_cr)
    return column

def p_error(p):
    if p:
        col = find_column(p.lexer.lexdata, p)
        print(f"Syntactic error: at line {p.lineno}, column {col}: Unexpected token '{p.value}'")
    else:
        print("Syntactic error: at EOF")

parser = yacc.yacc()

if __name__ == '__main__':
    with open("aguda-compiler/tests/powers.agu", 'r') as f:
        data = f.read()

    result = parser.parse(data)
    print(result)