import ply.yacc as yacc
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
    '''function_declaration : LET ID LPAREN parameters RPAREN COLON function_type EQUALS exp'''
    t[0] = s.FunctionDeclaration(t[2], t[4], t[7], t[9])

def p_parameters(t):
    '''parameters : ID parameters_tail'''
    t[0] = [t[1]] + t[2]

def p_parameters_tail(t):
    '''parameters_tail : COMMA ID parameters_tail
                       | empty'''
    if len(t) == 4:
        t[0] = [t[2]] + t[3]
    else:
        t[0] = []

def p_type(t):
    '''type : base_type array_suffix'''
    t[0] = t[1] + t[2]

def p_base_type(t):
    '''base_type : INT_TYPE
                 | BOOL_TYPE
                 | UNIT_TYPE
                 | STRING_TYPE'''
    t[0] = t[1]

# TODO  t[0] = t[1] + t[2] + t[3] provavelmente nao correto
def p_array_suffix(t):
    '''array_suffix : LBRACKET RBRACKET array_suffix
                    | empty'''
    if len(t) == 4:
        t[0] = t[1] + t[2] + t[3]
    else:
        t[0] = ''

# TODO meter FunctionType no syntax?
def p_function_type(t):
    '''function_type : type ARROW type
                     | LPAREN type function_type_tail RPAREN ARROW type'''
    if len(t) == 4:
        t[0] = s.FunctionType(t[1], t[3])
    else:
        t[0] = s.FunctionType(t[2], t[5])

def p_function_type_tail(t):
    '''function_type_tail : COMMA type function_type_tail
                          | empty'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = t[1] + [t[3]]

def p_exp(t):
    '''exp : variable
            | literal
            | binary_exp
            | unary_exp
            | function_call
            | assignment
            | variable_declaration
            | conditional
            | while_loop
            | array_creation
            | array_access
            | group'''
    t[0] = t[1]

def p_variable(t):
    '''variable : ID'''
    t[0] = s.Var(t[1])

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
                    | exp OR exp'''
    t[0] = s.BinaryOp(t[1], t[2], t[3])

#TODO mudar UnaryOp para NegationOp ou algo assim
def p_unary_exp(t):
    '''unary_exp : MINUS exp %prec UMINUS
                 | NOT exp'''
    if t[1] == '-':
        t[0] = s.BinaryOp(s.IntLiteral(0), '-', t[2])
    else:
        t[0] = s.UnaryOp(t[1], t[2])

def p_function_call(t):
    '''function_call : ID LPAREN arguments RPAREN'''
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
    '''assignment : lhs EQUALS exp'''
    t[0] = s.Assignment(t[1], t[3])

def p_lhs(t):
    '''lhs : variable
           | array_access'''
    t[0] = t[1]

def p_array_access(t):
    '''array_access : lhs LBRACKET exp RBRACKET'''
    t[0] = s.ArrayAccess(t[1], t[3])

def p_variable_declaration(t):
    '''variable_declaration : LET ID COLON type EQUALS exp'''
    t[0] = s.VariableDeclaration(t[2], t[4], t[6])

# TODO fiquei aqui, necessario left factoring e ver se é None que se usa
def p_conditional(t):
    '''conditional : IF expression THEN expression ELSE expression
                   | IF expression THEN expression'''
    if len(t) == 6:
        t[0] = s.Conditional(t[2], t[4], None)
    else:
        t[0] = s.Conditional(t[2], t[4], t[6])

def p_while_loop(t):
    '''while_loop : WHILE exp DO exp'''
    t[0] = s.WhileLoop(t[2], t[4])

def p_array_creation(t):
    '''array_creation : NEW type LBRACKET exp BAR exp RBRACKET'''
    t[0] = s.ArrayCreation(t[2], t[4], t[6])

def p_empty(t):
    '''empty :'''
    t[0] = []

def p_error(t):
    print(f"Syntax error at '{t.value}' on line {t.lineno}")

parser = yacc.yacc()