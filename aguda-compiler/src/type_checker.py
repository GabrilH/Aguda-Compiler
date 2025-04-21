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
    
def typeofVar(ctx: SymbolTable, name: str) -> Type:
    varType = ctx.lookup(name)
    if varType is None:
        raise NameError(f"Variable '{name}' not defined")
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
                    raise TypeError("Print function takes exactly one argument")
                exp1 = exps[0]
                typeof(ctx, exp1)
                return BaseType('Unit')
            
            if id.name == 'length':
                if len(exps) != 1:
                    raise TypeError("Length function takes exactly one argument")
                exp1 = exps[0]
                exp1Type = checkInstance(ctx, exp1, ArrayType)
                return BaseType('Int')
            
            funcType = typeof(ctx, id)
            if not isinstance(funcType, FunctionType):
                raise TypeError(f"'{id}' is not a function")
            if len(funcType.param_types) != len(exps):
                raise TypeError(f"Function '{id}' called with incorrect number of arguments")
            
            for param_type, arg in zip(funcType.param_types, exps):
                arg_type = typeof(ctx, arg)
                if param_type != arg_type:
                    raise TypeError(f"Function '{name}' called with incorrect argument types: expected {param_type}, got {arg_type}")
            
            return funcType.return_type
            
        case VariableDeclaration(name, type, exp):
            expType = typeof(ctx, exp)
            if expType != type:
                raise TypeError(f"Variable '{name}' declared with type {type}, but assigned {expType}")
            
            # No variable may be named as print or length
            if name.name in ['print', 'length']:
                raise NameError(f"Variable name '{name}' conflicts with built-in function")
            
            # Insert the variable into the context only if it is not '_' (wildcard)
            if name.name != '_':
                ctx.insert(name.name, type)
                
            return BaseType('Unit')
        
        case Var(name):
            return typeofVar(ctx, name)
        
        case Conditional(exp1, exp2, exp3):
            exp1Type = typeof(ctx, exp1)
            if exp1Type != BaseType('Bool'):
                raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Conditional expression must be a Bool, got {exp1Type}")
            
            local_ctx = ctx.enter_scope()
            exp2Type = typeof(local_ctx, exp2)
            # TODO ctx.exit_scope()
            
            local_ctx = ctx.enter_scope()
            exp3Type = typeof(local_ctx, exp3)
            # TODO ctx.exit_scope()
            
            if exp2Type != exp3Type:
                raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Conditional branches must have the same type, got {exp2Type} and {exp3Type} for expression '{exp}'")
            
            return exp2Type
        
        case WhileLoop(exp1, exp2):
            exp1Type = typeof(ctx, exp1)
            if exp1Type != BaseType('Bool'):
                raise TypeError(f"While condition must be a Bool, got {exp1Type}")
            
            # Enter a new scope for the loop body
            local_ctx = ctx.enter_scope()
            typeof(local_ctx, exp2)
            
            return BaseType('Unit')
        
        case Assignment(lhs, exp):
            lhsType = typeof(ctx, lhs)
            expType = typeof(ctx, exp)
            if lhsType != expType:
                raise TypeError(f"Assignment type mismatch: {lhsType} vs {expType}")

            return BaseType('Unit')
        
        case Sequence(first, rest):
            typeof(ctx, first)
            return typeof(ctx, rest)

        case BinaryOp(left, operator, right):
            leftType = typeof(ctx, left)
            rightType = typeof(ctx, right)
            
            if operator in ['+', '-', '*', '/', '%', '^']:
                if leftType != BaseType('Int') or rightType != BaseType('Int'):
                    raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Operator '{operator}' requires Int operands")
                return BaseType('Int')
            
            if operator in ['==', '!=', '<', '>', '<=', '>=']:
                if leftType != rightType:
                    raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Operator '{operator}' requires operands of the same type")
                return BaseType('Bool')
            
            if operator in ['&&', '||']:
                if leftType != BaseType('Bool') or rightType != BaseType('Bool'):
                    raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Operator '{operator}' requires Bool operands")
                return BaseType('Bool')
            
            raise TypeError(f"Error: ({exp.lineno}, {exp.column}) Unknown operator '{operator}'")
        
        case LogicalNegation(operand):
            operandType = typeof(ctx, operand)
            if operandType != BaseType('Bool'):
                raise TypeError(f"Logical negation requires a Bool, got {operandType}")
            return BaseType('Bool')
        
        case FunctionDeclaration(name, parameters, type, body):
            # No function may be named as print or length
            if name.name in ['print', 'length']:
                raise NameError(f"Function name '{name}' conflicts with built-in function")

            if not isinstance(type, FunctionType):
                raise TypeError(f"Function '{name}' must have a function type, got {type}")
            
            if len(parameters) != len(type.param_types):
                raise TypeError(f"Function '{name}' declared with incorrect number of parameters")
            
            # Allow mutually recursive declarations
            # Only insert if name != UNDERSCORE
            if name.name != '_':
                ctx.insert(name.name, type)

            # Check for duplicate parameter names (except for '_')
            param_names = set()
            for param in parameters:
                if param.name != '_' and param.name in param_names:
                    raise NameError(f"Duplicate parameter name '{param.name}' in function '{name}'")
                param_names.add(param.name)

            # Augment the context with parameter types
            local_ctx = ctx.enter_scope()
            for param, param_type in zip(parameters, type.param_types):
                local_ctx.insert(param.name, param_type)
            
            # Check the body of the function
            body_type = typeof(local_ctx, body)
            if body_type != type.return_type:
                raise TypeError(f"Function '{name}' body has type {body_type}, expected {type.return_type}")

            # Exit the local context TODO: is this needed?
            # TODO ctx.exit_scope()

        case TopLevelVariableDeclaration(name, type, exp):
            # No variable may be named as print or length
            if name.name in ['print', 'length']:
                raise NameError(f"Variable name '{name}' conflicts with built-in function")
            
            # Check the type of the expression against the declared type
            expType = typeof(ctx, exp)
            if expType != type:
                raise TypeError(f"Top-level variable '{name}' declared with type {type}, but assigned {expType}")
            
            # Insert the variable into the context only if it is not '_' (wildcard)
            if name.name != '_':
                ctx.insert(name.name, type)
        
        case _:
            raise TypeError(f"Unknown AST node type: {type(exp)}")
        
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

        case FunctionDeclaration(name, _, type, _):
            if name.name in ['print', 'length']:
                raise NameError(f"Function name '{name}' conflicts with built-in function")

            if name.name != '_':
                ctx.insert(name.name, type)

        case TopLevelVariableDeclaration(name, type, _):
            if name.name in ['print', 'length']:
                raise NameError(f"Variable name '{name}' conflicts with built-in function")

            if name.name != '_':
                ctx.insert(name.name, type)

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