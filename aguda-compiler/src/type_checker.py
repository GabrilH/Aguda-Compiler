from src.syntax import *
from src.symbol_table import SymbolTable
                
def checkAgainst(ctx: SymbolTable, exp: Exp, expected_type: Type) -> Type:
    """
    Checks if the expression `exp` matches the expected type `type` in the given context `ctx`.
    """
    actual_type = typeof(ctx, exp)
    return checkEqualTypes(exp, actual_type, expected_type)
    
def checkEqualTypes(exp: Exp, actual_type: Type, expected_type: Type) -> Type:
    """
    Checks if two types are equal or compatible.
    """
    if actual_type != expected_type:
        raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Expected two equal types, found {expected_type} and {actual_type}, for expression '{exp}'")
    return actual_type
    
def checkInstance(ctx: SymbolTable, exp: Exp, expected_class: type) -> Type:
    """
    Checks if the expression `exp` is an instance of the expected class `expected_class`.
    """
    actual_type = typeof(ctx, exp)
    if not isinstance(actual_type, expected_class):
        raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Expected instance of {expected_class}, found {actual_type}, for expression '{exp}'")
    return actual_type

def checkBuiltInConflict(exp: Exp, name: str) -> None:
    """
    Checks if the name conflicts with built-in functions.
    """
    if name in ['print', 'length']:
        raise NameError(f"Error: ({exp.lineno}, {exp.column}) Name '{name}' conflicts with built-in function")

def insertIntoCtx(ctx: SymbolTable, name: str, type: Type) -> None:
    if name != '_':
        ctx.insert(name, type)
    
def typeofVar(ctx: SymbolTable, exp: Exp, name: str) -> Type:
    varType = ctx.lookup(name)
    if varType is None:
        raise NameError(f"Error: ({exp.lineno}, {exp.column}) Variable '{name}' not found in the current context")
    return varType
    
def typeof(ctx: SymbolTable, exp: Exp) -> Type:
    """
    Determines the type of the expression `exp` in the given context `ctx`.
    """
    match exp:        
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
            arrayType : ArrayType = checkInstance(ctx, exp1, ArrayType)
            checkAgainst(ctx, exp2, BaseType('Int'))            
            return arrayType.type
        
        case FunctionCall(id, exps):
            if id.name == 'print':
                if len(exps) != 1:
                    raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Print function takes exactly one argument")
                exp1 = exps[0]
                typeof(ctx, exp1)
                return BaseType('Unit')
            
            if id.name == 'length':
                if len(exps) != 1:
                    raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Length function takes exactly one argument")
                exp1 = exps[0]
                checkInstance(ctx, exp1, ArrayType)
                return BaseType('Int')
            
            funcType : FunctionType = checkInstance(ctx, id, FunctionType)
            if len(funcType.param_types) != len(exps):
                raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Function '{id}' called with incorrect number of arguments")
            
            for param_type, arg in zip(funcType.param_types, exps):
                checkAgainst(ctx, arg, param_type)
            
            return funcType.return_type
            
        case VariableDeclaration(id, type, exp) | TopLevelVariableDeclaration(id, type, exp):           
            checkAgainst(ctx, exp, type)
            checkBuiltInConflict(exp, id.name)          
            insertIntoCtx(ctx, id.name, type)
            # TODO Furthermore, if the declaration appears at the left
            # of a semicolon let id : type = exp1 ; exp2, then the type of id
            # is used to validate exp2
            return BaseType('Unit')
        
        case Var(name):
            return typeofVar(ctx, exp, name)
        
        case Conditional(exp1, exp2, exp3):
            checkAgainst(ctx, exp1, BaseType('Bool'))
            exp2Type = typeof(ctx.enter_scope(), exp2)
            exp3Type = typeof(ctx.enter_scope(), exp3)         
            checkEqualTypes(exp, exp2Type, exp3Type)          
            return exp2Type
        
        case WhileLoop(exp1, exp2):
            checkAgainst(ctx, exp1, BaseType('Bool'))
            typeof(ctx.enter_scope(), exp2)
            return BaseType('Unit')
        
        case Assignment(lhs, exp):
            lhsType = typeof(ctx, lhs)
            expType = typeof(ctx, exp)
            checkEqualTypes(exp, lhsType, expType)
            return BaseType('Unit')
        
        case Sequence(first, rest):
            typeof(ctx, first)
            return typeof(ctx, rest)

        case BinaryOp(left, operator, right):
            leftType = typeof(ctx, left)
            rightType = typeof(ctx, right)
            checkEqualTypes(exp, leftType, rightType)
            
            if operator in ['+', '-', '*', '/', '%', '^']:
                checkEqualTypes(exp, leftType, BaseType('Int'))
                return BaseType('Int')
            
            if operator in ['==', '!=', '<', '>', '<=', '>=']:
                return BaseType('Bool')
            
            if operator in ['&&', '||']:
                checkEqualTypes(exp, leftType, BaseType('Bool'))
                return BaseType('Bool')
        
        case LogicalNegation(operand):
            checkAgainst(ctx, operand, BaseType('Bool'))
            return BaseType('Bool')
        
        case FunctionDeclaration(id, parameters, type, body):
            checkBuiltInConflict(exp, id.name)
            checkInstance(ctx, id, FunctionType)
            if len(parameters) != len(type.param_types):
                raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Function '{id}' declared with incorrect number of parameters")
            insertIntoCtx(ctx, id.name, type)

            # Check for duplicate parameter names (except for '_')
            param_names = set()
            for param in parameters:
                if param.name != '_' and param.name in param_names:
                    raise NameError(f"Error: ({exp.lineno}, {exp.column}) Duplicate parameter name '{param.name}' in function '{id.name}'")
                param_names.add(param.name)

            # Augment the context with parameter types
            local_ctx = ctx.enter_scope()
            for param, param_type in zip(parameters, type.param_types):
                insertIntoCtx(local_ctx, param.name, param_type)
            
            checkAgainst(local_ctx, body, type.return_type)
        
        case _:
            raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Unknown expression type '{type(exp)}'")
        
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
            if id.name != '_':
                ctx.insert(id.name, type)

        case TopLevelVariableDeclaration(id, type, _):
            checkBuiltInConflict(node, id.name)
            if id.name != '_':
                ctx.insert(id.name, type)
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
    ctx = SymbolTable()
    add_builtins(ctx)  # Add built-in functions to the context
    first_pass(ctx, ast)  # first pass
    second_pass(ctx, ast)  # second pass
    print("Program is semantically valid!")