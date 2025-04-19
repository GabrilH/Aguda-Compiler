from src.syntax import *
from symtable import SymbolTable

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
        
        case Var(name):
            varType = ctx.lookup(name)
            if varType is None:
                raise NameError(f"Variable '{name}' not defined")
            return varType
        
        case ArrayCreation(type, exp1, exp2):

            exp1Type = typeof(ctx, exp1)
            if exp1Type != BaseType('Int'):
                raise TypeError(f"Array size must be an Int, got {exp1Type}")
            
            arrayType = typeof(ctx, type)
            exp2Type = typeof(ctx, exp2)
            if arrayType != exp2Type:
                raise TypeError(f"Array type mismatch: {arrayType} vs {exp2Type}")
            
            if isinstance(type, ArrayType):
                return ArrayType(type.base_type, type.dimensions + 1)
            else:
                return ArrayType(type, 1)
        
        case ArrayAccess(array, index):

            arrayType = typeof(ctx, array)
            if isinstance(arrayType, ArrayType):
                raise TypeError(f"Array access requires an array, got {arrayType}")

            indexType = typeof(ctx, index)
            if indexType != BaseType('Int'):
                raise TypeError(f"Array index must be an Int, got {indexType}")
            
            return arrayType.base_type
        
        case FunctionCall(name, args):
            if name == 'print':
                if len(args) != 1:
                    raise TypeError("Print function takes exactly one argument")
                argType = typeof(ctx, args[0])
                if argType is None:
                    raise TypeError("Print function argument cannot be None")
                return BaseType('Unit')
            
            if name == 'length':
                if len(args) != 1:
                    raise TypeError("Length function takes exactly one argument")
                argType = typeof(ctx, args[0])
                if not isinstance(argType, ArrayType):
                    raise TypeError("Length function argument must be an array")
                # TODO acho que length deve devolver um int
                # return BaseType('Int')
                return argType.base_type
            
            funcType = typeof(ctx, name)
            if not isinstance(funcType, FunctionType):
                raise TypeError(f"'{name}' is not a function")
            if len(funcType.param_types) != len(args):
                raise TypeError(f"Function '{name}' called with incorrect number of arguments")
            if funcType.param_types != args:
                raise TypeError(f"Function '{name}' called with incorrect argument types")
            
            return funcType.return_type
            
        case VariableDeclaration(name, type, exp):

            expType = typeof(ctx, exp)
            if expType != type:
                raise TypeError(f"Variable '{name}' declared with type {type}, but assigned {expType}")
            
            # Furthermore, if the declaration appears at the left
            # of a semicolon let id : type = exp1 ; exp2, then the type of id
            # is used to validate exp2
            if isinstance(exp, BinaryOp) and exp.operator == ';':
                # TODO O "type of id" que é mencionado é igual ao type presente na expressão "let id : type = exp1 ; exp2" ?
                exp2Type = typeof(ctx, exp.right)
                if exp2Type != type:
                    raise TypeError(f"Expression after ';' has type {exp2Type}, expected {type}")
                
                
                    
            


        

def checkAgainst(ctx: SymbolTable, exp: Exp, type: Type) -> tuple[SymbolTable, Exp, Type]:
    pass