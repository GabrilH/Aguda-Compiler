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

def p_variable_declaration(t):
    '''variable_declaration : LET ID COLON type EQUALS expression'''
    t[0] = s.VariableDeclaration(t[2], t[4], t[6])

def p_function_declaration(t):
    '''function_declaration : LET ID LPAREN parameters RPAREN COLON function_type EQUALS expression'''
    t[0] = s.FunctionDeclaration(t[2], t[4], t[7], t[9])

# TODO refazer com o Mistral (é suposto ser só ID COMMA ID COMMA ID ...)
# perguntar se vale a pena criar Parameters no syntax
def p_parameters(t):
    '''parameters : ID COLON type parameters_tail'''
    t[0] = s.Parameters([(t[1], t[3])] + t[4].params)

def p_parameters_tail(t):
    '''parameters_tail : COMMA ID COLON type parameters_tail
                       | empty'''
    if len(t) == 5:
        t[0] = s.Parameters([(t[2], t[4])] + t[5].params)
    else:
        t[0] = s.Parameters([])

# TODO tem left recursion e o else está estranho
# vale a pena criar um syntax para Type?
def p_type(t):
    '''type : INT_TYPE
            | BOOL_TYPE
            | UNIT_TYPE
            | STRING_TYPE
            | type LBRACKET RBRACKET'''
    if len(t) == 2:
        t[0] = t[1]
    else:
        t[0] = f"{t[1]}[]"

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

#TODO -1 deve-se transformar em 0-1, mas e o NOT? maybe criar s.Negatation?
def p_unary_expression(t):
    '''unary_expression : MINUS expression %prec UMINUS
                        | NOT expression'''
    t[0] = s.UnaryOp(t[1], t[2])

def p_assignment(t):
    '''assignment : variable EQUALS expression
                  | array_access EQUALS expression'''
    t[0] = s.Assignment(t[1], t[3])

#TODO fazer left refactor
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
    '''function_call : ID LPAREN arguments RPAREN'''
    t[0] = s.FunctionCall(t[1], t[3])

def p_arguments(t):
    '''arguments : expression arguments_tail'''
    t[0] = [t[1]] + t[2]

def p_arguments_tail(t):
    '''arguments_tail : COMMA expression arguments_tail
                      | empty'''
    if len(t) == 4:
        t[0] = [t[2]] + t[3]
    else:
        t[0] = []

def p_array_creation(t):
    '''array_creation : NEW type LBRACKET expression BAR expression RBRACKET'''
    t[0] = s.ArrayCreation(t[2], t[4], t[6])

# TODO o primeiro expression tem que ser um ID ou ArrayAccess
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
    t[0] = s.Var(t[1])

def p_empty(t):
    '''empty :'''
    t[0] = []

def p_error(t):
    print(f"Syntax error at '{t.value}' on line {t.lineno}")

parser = yacc.yacc()