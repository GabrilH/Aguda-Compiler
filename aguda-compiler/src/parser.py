import ply.yacc as yacc
import src.syntax as s
from src.lexer import lexer, tokens

# Define operator precedence and associativity
# https://introcs.cs.princeton.edu/java/11precedence/
precedence = (
    ('right', 'ASSIGN', 'SEMICOLON'),
    ('right', 'ARROW'),
    ('nonassoc', 'WHILE', 'IF', 'DO'),
    ('right', 'THEN', 'ELSE'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUALS', 'NOT_EQUALS'),
    ('left', 'LESS', 'LESS_EQUAL', 'GREATER', 'GREATER_EQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'POWER'),
    ('right', 'UMINUS', 'NOT'),
    ('left', 'LBRACKET')
)

# Grammar rules

def p_program(t):
    '''program : top_level_declarations'''
    # TODO adicionar se for preciso
    # program = s.Program(t[1])
    # program.lineno = t[1][0].lineno if t[1] else 1
    # program.column = t[1][0].column if t[1] else 1
    # t[0] = program
    t[0] = s.Program(t[1])

def p_top_level_declarations(t):
    '''top_level_declarations : top_level_declaration top_level_declarations_tail'''
    if len(t) == 2:
        t[0] = [t[1]]
    else:
        t[0] = [t[1]] + t[2]

def p_top_level_declarations_tail(t):
    '''top_level_declarations_tail : top_level_declaration top_level_declarations_tail
                                   | empty'''
    if len(t) == 3:
        t[0] = [t[1]] + t[2]
    else:
        t[0] = []

def p_top_level_declaration(t):
    '''top_level_declaration : top_level_variable_declaration
                             | top_level_function_declaration'''
    t[0] = t[1]

def p_top_level_variable_declaration(t):
    '''top_level_variable_declaration : LET variable COLON type ASSIGN sequence'''
    tl_var_decl = s.TopLevelVariableDeclaration(t[2], t[4], t[6])
    tl_var_decl.lineno = t.lineno(1)
    tl_var_decl.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = tl_var_decl

def p_top_level_function_declaration(t):
    '''top_level_function_declaration : LET variable LPAREN parameters RPAREN COLON type ASSIGN sequence'''
    func_decl = s.FunctionDeclaration(t[2], t[4], t[7], t[9])
    func_decl.lineno = t.lineno(1)
    func_decl.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = func_decl

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

def p_type(t):
    '''
    type : base_type
         | array_type
         | function_type
    '''
    t[0] = t[1]

def p_base_type(t):
    '''
    base_type : INT_TYPE
              | STRING_TYPE
              | UNIT_TYPE
              | BOOL_TYPE
    '''
    base_type = s.BaseType(t[1])
    base_type.lineno = t.lineno(1)
    base_type.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = base_type

def p_array_type(t):
    'array_type : type LBRACKET RBRACKET'
    array_type = s.ArrayType(t[1])
    array_type.lineno = t[1].lineno
    array_type.column = t[1].column
    t[0] = array_type

def p_function_type(t):
    '''function_type : type ARROW type
                     | LPAREN type function_type_tail RPAREN ARROW type'''
    if len(t) == 4:
        func_type = s.FunctionType([t[1]], t[3])
        func_type.lineno = t.lineno(2)
        func_type.column = find_column(t.lexer.lexdata, t.slice[2])
        t[0] = func_type
    else:
        func_type = s.FunctionType([t[2]] + t[3], t[6])
        func_type.lineno = t.lineno(5)
        func_type.column = find_column(t.lexer.lexdata, t.slice[5])
        t[0] = func_type

def p_function_type_tail(t):
    '''function_type_tail : COMMA type function_type_tail
                          | empty'''
    if len(t) == 4:
        t[0] = [t[2]] + t[3]
    else:
        t[0] = []

def p_sequence(t):
    '''sequence : exp sequence_tail'''
    if not t[2]:
        t[0] = t[1]
    else:
        sequence = s.Sequence(t[1], t[2])
        sequence.lineno = t[1].lineno
        sequence.column = t[1].column
        t[0] = sequence

def p_sequence_tail(t):
    '''sequence_tail : SEMICOLON sequence
                     | empty'''
    if len(t) == 3:
        t[0] = t[2]
    else:
        t[0] = None

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
    variable = s.Var(t[1])
    variable.lineno = t.lineno(1)
    variable.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = variable

def p_literal(t):
    '''literal : INT_LITERAL
               | TRUE
               | FALSE
               | UNIT_LITERAL
               | STRING_LITERAL'''
    if t[1] == 'true':
        literal = s.BoolLiteral(True)
    elif t[1] == 'false':
        literal = s.BoolLiteral(False)
    elif t[1] == 'unit':
        literal = s.UnitLiteral()
    elif isinstance(t[1], int):
        literal = s.IntLiteral(t[1])
    else:
        literal = s.StringLiteral(t[1])

    literal.lineno = t.lineno(1)
    literal.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = literal

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
                    | exp OR exp
                    | exp AND exp'''
    binOp = s.BinaryOp(t[1], t[2], t[3])
    binOp.lineno = t.lineno(2)
    binOp.column = find_column(t.lexer.lexdata, t.slice[2])
    t[0] = binOp

def p_unary_exp(t):
    '''unary_exp : MINUS exp %prec UMINUS
                 | NOT exp'''
    if t[1] == '-':
        unary_exp = s.BinaryOp(s.IntLiteral(0), '-', t[2])
        unary_exp.lineno = t.lineno(1)
        unary_exp.column = find_column(t.lexer.lexdata, t.slice[1])
        t[0] = s.BinaryOp(s.IntLiteral(0), '-', t[2])
    else:
        unary_exp = s.LogicalNegation(t[2])
        unary_exp.lineno = t.lineno(1)
        unary_exp.column = find_column(t.lexer.lexdata, t.slice[1])

    t[0] = unary_exp

def p_function_call(t):
    '''function_call : variable LPAREN arguments RPAREN'''
    func_call = s.FunctionCall(t[1], t[3])
    func_call.lineno = t[1].lineno
    func_call.column = t[1].column
    t[0] = func_call

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
    assign = s.Assignment(t[2], t[4])
    assign.lineno = t.lineno(1)
    assign.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = assign

def p_lhs(t):
    '''lhs : variable
           | array_access'''
    t[0] = t[1]

def p_variable_declaration(t):
    '''variable_declaration : LET variable COLON type ASSIGN exp'''
    var_decl = s.VariableDeclaration(t[2], t[4], t[6])
    var_decl.lineno = t.lineno(1)
    var_decl.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = var_decl

def p_if_then_else(t):
    '''if_then_else : IF exp THEN exp ELSE exp'''
    cond = s.Conditional(t[2], t[4], t[6])
    cond.lineno = t.lineno(1)
    cond.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = cond

def p_if_then(t):
    '''if_then : IF exp THEN exp'''
    cond = s.Conditional(t[2], t[4], s.UnitLiteral())
    cond.lineno = t.lineno(1)
    cond.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = cond

def p_while_loop(t):
    '''while_loop : WHILE exp DO exp'''
    while_loop = s.WhileLoop(t[2], t[4])
    while_loop.lineno = t.lineno(1)
    while_loop.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = while_loop

def p_array_creation(t):
    '''array_creation : NEW type LBRACKET exp BAR exp RBRACKET'''
    array_creation = s.ArrayCreation(t[2], t[4], t[6])
    array_creation.lineno = t.lineno(1)
    array_creation.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = array_creation

def p_array_access(t):
    '''array_access : lhs LBRACKET exp RBRACKET'''
    array_access = s.ArrayAccess(t[1], t[3])
    array_access.lineno = t.lineno(2)
    array_access.column = find_column(t.lexer.lexdata, t.slice[2])
    t[0] = array_access

def p_group(t):
    '''group : LPAREN sequence RPAREN'''
    group = s.Group(t[2])
    group.lineno = t.lineno(1)
    group.column = find_column(t.lexer.lexdata, t.slice[1])
    t[0] = group

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

def reset_parser():

    if hasattr(parser, 'symstack'):
        parser.symstack.clear()
    if hasattr(parser, 'statestack'):
        parser.statestack.clear()
    if hasattr(lexer, 'lineno'):
        lexer.lineno = 1

parser = yacc.yacc()

# if __name__ == '__main__':
#     with open("test/valid/56334_bubbleSort/bubbleSort.agu", 'r') as f:
#         data = f.read()

#     ast = parser.parse(data)
#     print(ast)