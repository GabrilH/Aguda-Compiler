from src.syntax import *
from src.symbol_table import SymbolTable

def validate(program: Program) -> None:
    """
    Validates a program by ensuring all its declarations are well-formed.
    """
    ctx = SymbolTable()
    add_builtins(ctx)
    stmts : List[Declaration] = program.declarations
    for stmt in stmts:
        if isinstance(stmt, FunctionDeclaration):
            # Validate function declarations
            typeof(ctx, stmt)
        elif isinstance(stmt, TopLevelVariableDeclaration):
            # Validate variable declarations
            typeof(ctx, stmt)
        else:
            raise TypeError(f"Invalid top-level declaration: {type(stmt)}")
    
    print("Program is semantically valid!")
        
def add_builtins(ctx: SymbolTable) -> None:
    """
    Adds built-in functions to the symbol table.
    """
    ctx.insert('print', FunctionType(param_types=[BaseType('String')],
                                    return_type=BaseType('Unit')))
    ctx.insert('length', FunctionType(param_types=[ArrayType(BaseType('Int'), 1)],
                                    return_type=BaseType('Int')))
    # for base_type in ['Int', 'Bool', 'Unit', 'String']:
    #     ctx.insert('print', FunctionType(BaseType('Unit'), [BaseType(base_type)]))
    #     ctx.insert('length', FunctionType(BaseType('Int'), [ArrayType(BaseType(base_type), 1)]))

def typeof(ctx: SymbolTable, e:Exp) -> Type:
    """
    Determines the type of an expression in the given context.
    """
    match e:
        case IntLiteral():
            return BaseType('Int')
        
        case BoolLiteral():
            return BaseType('Bool')
        
        case UnitLiteral():
            return BaseType('Unit')
        
        case StringLiteral():
            return BaseType('String')
        
        case ArrayCreation(type, exp1, exp2):
            exp1Type = typeof(ctx, exp1)
            if exp1Type != BaseType('Int'):
                raise TypeError(f"Array size must be an Int, got {exp1Type}")
            
            exp2Type = typeof(ctx, exp2)
            if exp2Type != type:
                raise TypeError(f"Array initial value must be of type {type}, got {exp2Type}")
            
            if isinstance(type, ArrayType):
                return ArrayType(type.base_type, type.dimensions + 1)
            else:
                return ArrayType(type, 1)
        
        case ArrayAccess(array, index):
            arrayType = typeof(ctx, array)
            if not isinstance(arrayType, ArrayType):
                raise TypeError(f"Array access requires an array, got {arrayType}")

            indexType = typeof(ctx, index)
            if indexType != BaseType('Int'):
                raise TypeError(f"Array index must be an Int, got {indexType}")
            
            return arrayType.base_type
        
        case FunctionCall(name, args):
            if name.name == 'print':
                if len(args) != 1:
                    raise TypeError("Print function takes exactly one argument")
                argType = typeof(ctx, args[0])
                return BaseType('Unit')
            
            if name.name == 'length':
                if len(args) != 1:
                    raise TypeError("Length function takes exactly one argument")
                argType = typeof(ctx, args[0])
                if not isinstance(argType, ArrayType):
                    raise TypeError("Length function argument must be an array")
                # TODO acho que length deve devolver um int
                # return argType.base_type
                return BaseType('Int')
            
            funcType = typeof(ctx, name)
            if not isinstance(funcType, FunctionType):
                raise TypeError(f"'{name}' is not a function")
            if len(funcType.param_types) != len(args):
                raise TypeError(f"Function '{name}' called with incorrect number of arguments")
            
            for param_type, arg in zip(funcType.param_types, args):
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
            
            # Furthermore, if the declaration appears at the left
            # of a semicolon let id : type = exp1 ; exp2, then the type of id
            # is used to validate exp2
            # TODO porque é que é necessario um caso especial para o ';' ?
            if isinstance(exp, BinaryOp) and exp.operator == ';':
                # TODO O "type of id" que é mencionado é igual ao type presente na expressão "let id : type = exp1 ; exp2" ?
                exp2Type = typeof(ctx, exp.right)
                if exp2Type != type:
                    raise TypeError(f"Expression after ';' has type {exp2Type}, expected {type}")
                
            return BaseType('Unit')
        
        case Var(name):
            varType = ctx.lookup(name)
            if varType is None:
                raise NameError(f"Variable '{name}' not defined")
            return varType
        
        case Conditional(exp1, exp2, exp3):
            exp1Type = typeof(ctx, exp1)
            if exp1Type != BaseType('Bool'):
                raise TypeError(f"Conditional expression must be a Bool, got {exp1Type}")
            
            local_ctx = ctx.enter_scope()
            exp2Type = typeof(local_ctx, exp2)
            # TODO ctx.exit_scope()
            
            local_ctx = ctx.enter_scope()
            exp3Type = typeof(local_ctx, exp3)
            # TODO ctx.exit_scope()
            
            if exp2Type != exp3Type:
                raise TypeError(f"Conditional branches have different types: {exp2Type} vs {exp3Type}")
            
            return exp2Type
        
        case WhileLoop(exp1, exp2):
            exp1Type = typeof(ctx, exp1)
            if exp1Type != BaseType('Bool'):
                raise TypeError(f"While condition must be a Bool, got {exp1Type}")
            
            # Enter a new scope for the loop body
            local_ctx = ctx.enter_scope()
            exp2Type = typeof(local_ctx, exp2)
            # TODO ctx.exit_scope()

            return exp2Type
        
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
                    raise TypeError(f"Operator '{operator}' requires Int operands")
                return BaseType('Int')
            
            if operator in ['==', '!=', '<', '>', '<=', '>=']:
                if leftType != rightType:
                    raise TypeError(f"Operator '{operator}' requires operands of the same type")
                return BaseType('Bool')
            
            if operator in ['&&', '||']:
                if leftType != BaseType('Bool') or rightType != BaseType('Bool'):
                    raise TypeError(f"Operator '{operator}' requires Bool operands")
                return BaseType('Bool')
            
            raise TypeError(f"Unknown operator '{operator}'")
        
        case LogicalNegation(operand):
            operandType = typeof(ctx, operand)
            if operandType != BaseType('Bool'):
                raise TypeError(f"Logical negation requires a Bool, got {operandType}")
            return BaseType('Bool')
        
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
                
            return BaseType('Unit')
        
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

            return BaseType('Unit')
        
        case _:
            raise TypeError(f"Unknown expression type: {type(e)}")
                
def checkAgainst(ctx: SymbolTable, exp: Exp, type: Type) -> None:
    """
    Checks if the expression `exp` matches the expected type `type` in the given context `ctx`.
    """
    actual_type = typeof(ctx, exp)
    if actual_type != type:
        raise TypeError(f"Expected type {type}, found {actual_type}, for expression '{exp}'")
    
def checkEqualTypes(type1: Type, type2: Type) -> None:
    """
    Checks if two types are equal.
    """
    if type1 != type2:
        raise TypeError(f"Expected equal types, found {type1} and {type2}")


# def checkAgainst(ctx: SymbolTable, exp: Exp, expected_type: Type) -> None:
#     """
#     Checks if the expression `exp` matches the expected type `expected_type` in the given context `ctx`.
#     """
#     match exp:
#         case Conditional(condition, then_branch, else_branch):
#             # Check the condition type
#             condition_type = typeof(ctx, condition)
#             if condition_type != BaseType('Bool'):
#                 raise TypeError(
#                     f"Expected type Bool for condition, found {condition_type}, "
#                     f"for expression '{condition}'"
#                 )
            
#             # Check both branches against the expected type
#             checkAgainst(ctx, then_branch, expected_type)
#             checkAgainst(ctx, else_branch, expected_type)

#         case BinaryOp(left, operator, right):
#             # Handle specific operators
#             if operator == ';':
#                 # Ensure the left expression has a type
#                 typeof(ctx, left)
#                 # Check the right expression against the expected type
#                 checkAgainst(ctx, right, expected_type)
#             else:
#                 # Synthesize the type and compare
#                 actual_type = typeof(ctx, exp)
#                 if actual_type != expected_type:
#                     raise TypeError(
#                         f"Expected type {expected_type}, found {actual_type}, "
#                         f"for expression '{exp}'"
#                     )

#         case Assignment(lhs, rhs):
#             # Check the type of the left-hand side
#             lhs_type = typeof(ctx, lhs)
#             # Check the right-hand side against the left-hand side's type
#             checkAgainst(ctx, rhs, lhs_type)
#             # Ensure the assignment matches the expected type
#             if lhs_type != expected_type:
#                 raise TypeError(
#                     f"Expected type {expected_type}, found {lhs_type}, "
#                     f"for assignment '{exp}'"
#                 )

#         case _:
#             # Default case: synthesize the type and compare
#             actual_type = typeof(ctx, exp)
#             if actual_type != expected_type:
#                 raise TypeError(
#                     f"Expected type {expected_type}, found {actual_type}, "
#                     f"for expression '{exp}'"
#                 )