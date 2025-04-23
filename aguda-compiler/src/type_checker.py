from src.syntax import *
from src.symbol_table import SymbolTable

MAX_ERRORS = 5
logger = None

class SemanticError(Exception):
    """Exception raised for semantic errors in the program."""
    pass

class ErrorLogger:
    def __init__(self):
        self.messages = []

    def log(self, message: str, lineno: int, column: int):
        self.messages.append(f"Error: ({lineno}, {column}) {message}")

    def print_errors(self):
        for error in self.messages[:MAX_ERRORS]:
            print(error)
        if len(self.messages) > MAX_ERRORS:
            print(f"...and {len(self.messages) - MAX_ERRORS} more errors.")

    def has_errors(self) -> bool:
        return len(self.messages) > 0

    def reset(self):
        self.messages = []

    def get_errors(self):
        return self.messages
                
def checkEqualTypes(error_exp: Exp, actual_type: Type, expected_type: Type):
    """
    Checks if the actual type matches the expected type.
    """
    if actual_type == expected_type:
        return
    
    match error_exp:            
        case FunctionCall(_, _):
            logger.log(f"Expected function call to return type '{expected_type}', "
                    f"found type '{actual_type}' for expression \n'{error_exp}'", error_exp.lineno, error_exp.column)
            
        case Conditional(_, _, _):
            logger.log(f"Expected both branches to be of same type; found {actual_type} and {expected_type}, "
                    f"for expression \n'{error_exp}'", error_exp.lineno, error_exp.column)
            
        case Var(_):
            logger.log(f"Expected variable '{error_exp}' to be of type '{expected_type}', "
                    f"found type '{actual_type}'", error_exp.lineno, error_exp.column)

        case _: 
            logger.log(f"Expected two equal types; found {actual_type} and {expected_type}, "
                    f"for expression \n'{error_exp}'", error_exp.lineno, error_exp.column)
    
def checkInstance(error_exp: Exp, actual_type: Type, expected_class: type) -> bool:
    """
    Checks if the actual type is an instance of the expected class.
    Returns True if it is, otherwise logs an error and returns False.
    """
    if not isinstance(actual_type, expected_class):
        logger.log(f"Expected a {expected_class.__name__}, found {actual_type} "
                   f"for expression \n'{error_exp}'", error_exp.lineno, error_exp.column)
        return False
    return True

def checkBuiltInConflict(error_exp: Exp, var: Var):
    """
    Checks if the variable name conflicts with built-in functions.
    """
    if var.name in ['print', 'length']:
        logger.log(f"Variable name '{var}' conflicts with built-in function", error_exp.lineno, error_exp.column)

def checkArguments(ctx: SymbolTable, error_exp: Exp, exps: List[Exp], function_type: FunctionType):
    """
    Checks if the arguments of a function call match the expected types.
    """
    expected_types = function_type.param_types
    actual_types = [typeof(ctx, exp) for exp in exps]
    if len(actual_types) != len(expected_types) or any(a != e for a, e in zip(actual_types, expected_types)):
        logger.log(
            f"expected arguments of types [{', '.join(str(t) for t in expected_types)}], "
            f"found [{', '.join(str(t) for t in actual_types)}] for expression \n'{error_exp}'",
            error_exp.lineno,
            error_exp.column
        )

def checkParameters(error_exp : Exp, parameters: List[Var], function_type: FunctionType):
    """
    Checks if the parameters names are unique and do not conflict with built-in functions.
    """
    if len(parameters) != len(function_type.param_types):
        logger.log(f"number of params does not match type in function declaration "
                   f"'{error_exp}'", error_exp.lineno, error_exp.column)

    param_names = set()
    for param in parameters:
        if param.name != '_' and param.name in param_names:
            logger.log(f"duplicate parameter name '{param.name}' in function declaration "
                       f"'{error_exp}'", error_exp.lineno, error_exp.column)
        param_names.add(param.name)

def checkAgainst(ctx: SymbolTable, matched_exp: Exp, expected_type: Type) -> None:
    """
    Checks if the expression `exp` matches the expected type `type` in the given context `ctx`.
    """
    match (matched_exp, expected_type):
        case (IntLiteral(), BaseType('Int')):
            pass
        case (BoolLiteral(), BaseType('Bool')):
            pass
        case (UnitLiteral(), BaseType('Unit')):
            pass
        case (StringLiteral(), BaseType('String')):
            pass

        case (ArrayCreation(type, exp1, exp2), ArrayType()):
            checkAgainst(ctx, exp1, BaseType('Int'))
            checkAgainst(ctx, exp2, type)

        case (ArrayAccess(exp1, exp2), _):
            checkAgainst(ctx, exp2, BaseType('Int'))
            exp1Type : ArrayType = typeof(ctx, exp1)
            if checkInstance(exp1, exp1Type, ArrayType):
                checkEqualTypes(matched_exp, exp1Type.type, expected_type)

        case (FunctionCall(id, exps), _):
            match (id.name, expected_type):
                case ('print', BaseType('Unit')):
                    if len(exps) != 1:
                        logger.log(f"Print function takes exactly one argument", matched_exp.lineno, matched_exp.column)
                    else:
                        exp1 = exps[0]
                        typeof(ctx, exp1)

                case ('length', BaseType('Int')):
                    if len(exps) != 1:
                        logger.log(f"Length function takes exactly one argument", matched_exp.lineno, matched_exp.column)
                    else:
                        exp1 = exps[0]
                        exp1Type = typeof(ctx, exp1)
                        checkInstance(matched_exp, exp1Type, ArrayType)

                case ('length', _) | ('print', _):
                    logger.log(f"Expected type '{expected_type}', found type '{typeof(ctx, matched_exp)}' "
                               f"for expression \n'{matched_exp}'", matched_exp.lineno, matched_exp.column)

                case _:
                    funcType : FunctionType = typeof(ctx, id)
                    if checkInstance(id, funcType, FunctionType):
                        checkArguments(ctx, matched_exp, exps, funcType)
                        checkEqualTypes(matched_exp, funcType.return_type, expected_type)

        case (VariableDeclaration(id, type, exp),BaseType('Unit')) | (TopLevelVariableDeclaration(id, type, exp),BaseType('Unit')):
            checkAgainst(ctx, exp, type)
            insertIntoCtx(ctx, id, type)

        case (Var(name),_):
            actual_type = typeofVar(ctx, matched_exp, name)
            checkEqualTypes(matched_exp, actual_type, expected_type)
        
        case (Conditional(exp1, exp2, exp3), _):
            checkAgainst(ctx, exp1, BaseType('Bool'))
            checkAgainst(ctx, exp2, expected_type)
            checkAgainst(ctx, exp3, expected_type)

        case (WhileLoop(exp1, exp2), BaseType('Unit')):
            checkAgainst(ctx, exp1, BaseType('Bool'))
            typeof(ctx.enter_scope(), exp2)

        case (Assignment(lhs, exp), BaseType('Unit')):
            lhsType = typeof(ctx, lhs)
            checkAgainst(ctx, exp, lhsType)

        case (Sequence(first, rest), _):
            typeof(ctx, first)
            checkAgainst(ctx, rest, expected_type)

        case (BinaryOp(left, operator, right), _):

            if operator in ['+', '-', '*', '/', '%', '^']:
                checkAgainst(ctx, left, BaseType('Int'))
                checkAgainst(ctx, right, BaseType('Int'))
                checkEqualTypes(matched_exp, BaseType('Int'), expected_type)
            
            if operator in ['==', '!=', '<', '>', '<=', '>=']:
                leftType = typeof(ctx, left)
                rightType = typeof(ctx, right)
                checkEqualTypes(matched_exp, leftType, rightType)
                checkEqualTypes(matched_exp, BaseType('Bool'), expected_type)
            
            if operator in ['&&', '||']:
                checkAgainst(ctx, left, BaseType('Bool'))
                checkAgainst(ctx, right, BaseType('Bool'))
                checkEqualTypes(matched_exp, BaseType('Bool'), expected_type)

        case (LogicalNegation(operand), BaseType('Bool')):
            checkAgainst(ctx, operand, BaseType('Bool'))

        case (Group(exp), _):
            checkAgainst(ctx, exp, expected_type)

        case _:
            logger.log(f"Expected type '{expected_type}', found type '{typeof(ctx, matched_exp)}' "
                       f"for expression \n'{matched_exp}'", matched_exp.lineno, matched_exp.column)

def insertIntoCtx(ctx: SymbolTable, var: Var, type: Type) -> None:
    """
    Inserts a variable and its type into the symbol table.
    """
    name = var.name
    if name != '_':
        ctx.insert(name, type)
    
def typeofVar(ctx: SymbolTable, exp: Exp, name: str) -> Type:
    varType = ctx.lookup(name)
    if varType is None:
        logger.log(f"unresolved symbol: {name}", exp.lineno, exp.column)
    return varType
    
def typeof(ctx: SymbolTable, matched_exp: Exp) -> Type:
    """
    Determines the type of the expression `matched_exp` in the given context `ctx`.
    """
    match matched_exp:        
        case IntLiteral():
            return BaseType('Int')
        
        case BoolLiteral():
            return BaseType('Bool')
        
        case UnitLiteral():
            return BaseType('Unit')
        
        case StringLiteral():
            return BaseType('String')
        
        case ArrayCreation(type, exp1, exp2):
            checkAgainst(ctx, exp1, BaseType('Int'))
            checkAgainst(ctx, exp2, type)            
            return ArrayType(type)
        
        case ArrayAccess(exp1, exp2):
            checkAgainst(ctx, exp2, BaseType('Int'))
            exp1Type : ArrayType = typeof(ctx, exp1)
            if checkInstance(exp1, exp1Type, ArrayType):         
                return exp1Type.type
        
        case FunctionCall(id, exps):
            if id.name == 'print':
                if len(exps) != 1:
                    logger.log(f"Print function takes exactly one argument", matched_exp.lineno, matched_exp.column)
                exp1 = exps[0]
                typeof(ctx, exp1)
                return BaseType('Unit')
            
            if id.name == 'length':
                if len(exps) != 1:
                    logger.log(f"Length function takes exactly one argument", matched_exp.lineno, matched_exp.column)
                exp1 = exps[0]
                exp1Type = typeof(ctx, exp1)
                checkInstance(matched_exp, exp1Type, ArrayType)
                return BaseType('Int')
            
            funcType : FunctionType = typeof(ctx, id)
            if checkInstance(id, funcType, FunctionType):
                checkArguments(ctx, matched_exp, exps, funcType)
                return funcType.return_type
            
        case VariableDeclaration(id, type, exp) | TopLevelVariableDeclaration(id, type, exp):   
            checkAgainst(ctx, exp, type)
            insertIntoCtx(ctx, id, type)
            return BaseType('Unit')
        
        case Var(name):
            return typeofVar(ctx, matched_exp, name)
        
        case Conditional(exp1, exp2, exp3):
            checkAgainst(ctx, exp1, BaseType('Bool'))
            exp2Type = typeof(ctx.enter_scope(), exp2)
            exp3Type = typeof(ctx.enter_scope(), exp3)         
            checkEqualTypes(matched_exp, exp2Type, exp3Type)          
            return exp2Type
        
        case WhileLoop(exp1, exp2):
            checkAgainst(ctx, exp1, BaseType('Bool'))
            typeof(ctx.enter_scope(), exp2)
            return BaseType('Unit')
        
        case Assignment(lhs, exp):
            lhsType = typeof(ctx, lhs)
            expType = typeof(ctx, exp)
            checkEqualTypes(matched_exp, lhsType, expType)
            return BaseType('Unit')
        
        case Sequence(first, rest):
            typeof(ctx, first)
            return typeof(ctx, rest)

        case BinaryOp(left, operator, right):

            if operator in ['+', '-', '*', '/', '%', '^']:
                checkAgainst(ctx, left, BaseType('Int'))
                checkAgainst(ctx, right, BaseType('Int'))
                return BaseType('Int')
            
            if operator in ['==', '!=', '<', '>', '<=', '>=']:
                leftType = typeof(ctx, left)
                rightType = typeof(ctx, right)
                checkEqualTypes(matched_exp, leftType, rightType)
                return BaseType('Bool')
            
            if operator in ['&&', '||']:
                checkAgainst(ctx, left, BaseType('Bool'))
                checkAgainst(ctx, right, BaseType('Bool'))
                return BaseType('Bool')
            
            if operator == '++':
                checkAgainst(ctx, left, BaseType('String'))
                checkAgainst(ctx, right, BaseType('String'))
                return BaseType('String')
        
        case LogicalNegation(operand):
            checkAgainst(ctx, operand, BaseType('Bool'))
            return BaseType('Bool')
        
        case FunctionDeclaration(id, parameters, type, body):
            checkBuiltInConflict(matched_exp, id)
            if not checkInstance(matched_exp, type, FunctionType):
                return
            type : FunctionType = type

            checkParameters(id, parameters, type)
            insertIntoCtx(ctx, id, type)

            # Augment the context with parameter types
            local_ctx = ctx.enter_scope()
            for param, param_type in zip(parameters, type.param_types):
                insertIntoCtx(local_ctx, param, param_type)
            
            checkAgainst(local_ctx, body, type.return_type)

        case Group(exp):
            return typeof(ctx.enter_scope(), exp)
        
        case _:
            logger.log(f"Unknown expression type '{type(matched_exp)}'", matched_exp.lineno, matched_exp.column)
        
def second_pass(ctx: SymbolTable, program: Program) -> None:
    """
    Second pass of semantic analysis: checks the types of function bodies
    """
    for decl in program.declarations:
        typeof(ctx, decl)
    
def first_pass(ctx: SymbolTable, node: ASTNode) -> None:
    """
    First pass of semantic analysis: collects top-level declarations types
    """
    match node:
        case Program(declarations):
            for decl in declarations:
                first_pass(ctx, decl)

        case FunctionDeclaration(id, _, type, _):
            checkBuiltInConflict(node, id)
            insertIntoCtx(ctx, id, type)

        case TopLevelVariableDeclaration(id, type, _):
            insertIntoCtx(ctx, id, type)
            
        case _:
            return


def add_builtins(ctx: SymbolTable) -> None:
    """
    Adds built-in functions to the symbol table.
    """
    ctx.insert('print', FunctionType(param_types=[BaseType('String')],
                                    return_type=BaseType('Unit')))
    ctx.insert('length', FunctionType(param_types=[ArrayType(BaseType('Int'))],
                                    return_type=BaseType('Int')))
    
def verify(ast: ASTNode) -> None:
    """
    Verifies the semantic correctness of the program.
    """
    global logger
    logger = ErrorLogger()

    ctx = SymbolTable()
    add_builtins(ctx)
    try :
        first_pass(ctx, ast)
        second_pass(ctx, ast)
    except Exception as e:
        logger.log(f"Unexpected error during semantic analysis: {str(e)}", -1, -1)

    if logger.has_errors():
        logger.print_errors()
        raise SemanticError("Semantic errors found.")
    else:
        print("Program is semantically valid!")