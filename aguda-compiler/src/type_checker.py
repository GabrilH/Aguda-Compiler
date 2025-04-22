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

    def log(self, message: str, lineno: int, column: int) -> None:
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
                
def checkAgainst(ctx: SymbolTable, match_exp: Exp, expected_type: Type) -> None:
    """
    Checks if the expression `exp` matches the expected type `type` in the given context `ctx`.
    """
    match (match_exp, expected_type):
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
            checkInstance(ctx, exp1, ArrayType)
            checkAgainst(ctx, exp2, BaseType('Int'))
            actual_type = typeof(ctx, exp1).type
            checkEqualTypes(match_exp, actual_type, expected_type)

        case (FunctionCall(id, exps), _):
            if id.name == 'print':
                if len(exps) != 1:
                    logger.log(f"Print function takes exactly one argument", match_exp.lineno, match_exp.column)
                else:
                    exp1 = exps[0]
                    typeof(ctx, exp1)
                checkEqualTypes(match_exp, BaseType('Unit'), expected_type)
            
            elif id.name == 'length':
                if len(exps) != 1:
                    logger.log(f"Length function takes exactly one argument", match_exp.lineno, match_exp.column)
                else:
                    checkInstance(ctx, exps[0], ArrayType)
                checkEqualTypes(match_exp, BaseType('Int'), expected_type)
            
            else:
                funcType = typeof(ctx, id)
                checkInstance(ctx, id, FunctionType)
                checkArguments(ctx, match_exp, exps, funcType)
                checkEqualTypes(match_exp, funcType.return_type, expected_type)

        case (VariableDeclaration(id, type, exp),BaseType('Unit')) | (TopLevelVariableDeclaration(id, type, exp),BaseType('Unit')):
            checkAgainst(ctx, exp, type)
            checkBuiltInConflict(match_exp, id.name)
            insertIntoCtx(ctx, id.name, type)

        case (Var(name),_):
            actual_type = typeofVar(ctx, match_exp, name)
            checkEqualTypes(match_exp, actual_type, expected_type)
        
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
                checkEqualTypes(match_exp, BaseType('Int'), expected_type)
            
            if operator in ['==', '!=', '<', '>', '<=', '>=']:
                leftType = typeof(ctx, left)
                rightType = typeof(ctx, right)
                checkEqualTypes(match_exp, leftType, rightType)
                checkEqualTypes(match_exp, BaseType('Bool'), expected_type)
            
            if operator in ['&&', '||']:
                checkAgainst(ctx, left, BaseType('Bool'))
                checkAgainst(ctx, right, BaseType('Bool'))
                checkEqualTypes(match_exp, BaseType('Bool'), expected_type)

        case (LogicalNegation(operand), BaseType('Bool')):
            checkAgainst(ctx, operand, BaseType('Bool'))

        case (Group(exp), _):
            checkAgainst(ctx, exp, expected_type)

        case _:
            logger.log(f"Expected type '{expected_type}', found type '{typeof(ctx, match_exp)}' for expression \n'{match_exp}'", match_exp.lineno, match_exp.column)
            # actual_type = typeof(ctx, match_exp)
            # checkEqualTypes(match_exp, actual_type, expected_type)
        
def checkArguments(ctx: SymbolTable, matched_exp: Exp, exps: List[Exp], function_type: FunctionType) -> None:
    """
    Checks if the arguments `exps` match the expected types in `expected_types`.
    """
    expected_types = function_type.param_types
    if len(exps) != len(expected_types):
        logger.log(f"Function call '{matched_exp}' has {len(exps)} arguments, expected {len(expected_types)}", matched_exp.lineno, matched_exp.column)
    else:
        for exp, expected_type in zip(exps, expected_types):
            checkAgainst(ctx, exp, expected_type)
    
def checkEqualTypes(exp: Exp, actual_type: Type, expected_type: Type) -> None:
    """
    Checks if two types are equal or compatible.
    """
    # TODO deve receber exp ou n?
    if actual_type != expected_type:
        logger.log(f"Expected two equal types; found {expected_type} and {actual_type}, for expression \n'{exp}'", exp.lineno, exp.column)
    
def checkInstance(ctx: SymbolTable, exp: Exp, expected_class: type) -> None:
    """
    Checks if the expression `exp` is an instance of the expected class `expected_class`.
    """
    actual_type = typeof(ctx, exp)
    if not isinstance(actual_type, expected_class):
        logger.log(f"Expected instance of {expected_class}, found {actual_type}, for expression \n'{exp}'", exp.lineno, exp.column)

def checkBuiltInConflict(exp: Exp, name: str) -> None:
    """
    Checks if the name conflicts with built-in functions.
    """
    if name in ['print', 'length']:
        logger.log(f"Name '{name}' conflicts with built-in function", exp.lineno, exp.column)

def insertIntoCtx(ctx: SymbolTable, name: str, type: Type) -> None:
    if name != '_':
        ctx.insert(name, type)
    
def typeofVar(ctx: SymbolTable, exp: Exp, name: str) -> Type:
    # TODO deve receber exp ou n?
    varType = ctx.lookup(name)
    if varType is None:
        logger.log(f"unresolved symbol: {name}", exp.lineno, exp.column)
    return varType
    
def typeof(ctx: SymbolTable, match_exp: Exp) -> Type:
    """
    Determines the type of the expression `match_exp` in the given context `ctx`.
    """
    match match_exp:        
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
            exp1Type = typeof(ctx, exp1)
            checkInstance(ctx, exp1, ArrayType)
            checkAgainst(ctx, exp2, BaseType('Int'))            
            return exp1Type.type
        
        case FunctionCall(id, exps):
            if id.name == 'print':
                if len(exps) != 1:
                    logger.log(f"Print function takes exactly one argument", match_exp.lineno, match_exp.column)
                exp1 = exps[0]
                typeof(ctx, exp1)
                return BaseType('Unit')
            
            if id.name == 'length':
                if len(exps) != 1:
                    logger.log(f"Length function takes exactly one argument", match_exp.lineno, match_exp.column)
                exp1 = exps[0]
                checkInstance(ctx, exp1, ArrayType)
                return BaseType('Int')
            
            funcType = typeof(ctx, id)
            checkInstance(ctx, id, FunctionType)
            checkArguments(ctx, match_exp, exps, funcType)
            
            return funcType.return_type
            
        case VariableDeclaration(id, type, exp) | TopLevelVariableDeclaration(id, type, exp):           
            checkAgainst(ctx, exp, type)
            checkBuiltInConflict(match_exp, id.name)
            insertIntoCtx(ctx, id.name, type)
            # TODO Furthermore, if the declaration appears at the left
            # of a semicolon let id : type = exp1 ; exp2, then the type of id
            # is used to validate exp2
            return BaseType('Unit')
        
        case Var(name):
            return typeofVar(ctx, match_exp, name)
        
        case Conditional(exp1, exp2, exp3):
            checkAgainst(ctx, exp1, BaseType('Bool'))
            exp2Type = typeof(ctx.enter_scope(), exp2)
            exp3Type = typeof(ctx.enter_scope(), exp3)         
            checkEqualTypes(match_exp, exp2Type, exp3Type)          
            return exp2Type
        
        case WhileLoop(exp1, exp2):
            checkAgainst(ctx, exp1, BaseType('Bool'))
            typeof(ctx.enter_scope(), exp2)
            return BaseType('Unit')
        
        case Assignment(lhs, exp):
            lhsType = typeof(ctx, lhs)
            expType = typeof(ctx, exp)
            checkEqualTypes(match_exp, lhsType, expType)
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
                checkEqualTypes(match_exp, leftType, rightType)
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
            checkBuiltInConflict(match_exp, id.name)
            checkInstance(ctx, id, FunctionType)
            if len(parameters) != len(type.param_types):
                logger.log(f"number of params does not match type in function declaration '{id.name}'", match_exp.lineno, match_exp.column)
            insertIntoCtx(ctx, id.name, type)

            # Check for duplicate parameter names (except for '_')
            param_names = set()
            for param in parameters:
                if param.name != '_' and param.name in param_names:
                    logger.log(f"Duplicate parameter name '{param.name}' in function '{id.name}'", match_exp.lineno, match_exp.column)
                param_names.add(param.name)

            # Augment the context with parameter types
            local_ctx = ctx.enter_scope()
            for param, param_type in zip(parameters, type.param_types):
                insertIntoCtx(local_ctx, param.name, param_type)
            
            checkAgainst(local_ctx, body, type.return_type)

        case Group(exp):
            return typeof(ctx.enter_scope(), exp)
        
        case _:
            logger.log(f"Unknown expression type '{type(match_exp)}'", match_exp.lineno, match_exp.column)
        
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
            checkBuiltInConflict(node, id.name)
            insertIntoCtx(ctx, id.name, type)

        case TopLevelVariableDeclaration(id, type, _):
            checkBuiltInConflict(node, id.name)
            insertIntoCtx(ctx, id.name, type)
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
    add_builtins(ctx)  # Add built-in functions to the context
    try :
        first_pass(ctx, ast)  # first pass
        second_pass(ctx, ast)  # second pass
    except Exception as e:
        logger.log(f"Unexpected error during semantic analysis: {str(e)}", -1, -1)

    if logger.has_errors():
        logger.print_errors()
        raise SemanticError("Semantic errors found.")
    else:
        print("Program is semantically valid!")