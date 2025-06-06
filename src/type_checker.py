from src.error_logger import ErrorLogger
from src.syntax import *
from src.symbol_table import SymbolTable

class SemanticError(Exception):
    """Exception raised for semantic errors in the program."""
    pass

class TypeChecker:

    def __init__(self, max_errors):
        if max_errors < 0:
            raise ValueError("max_errors must be greater than or equal to 0")
        self.logger = ErrorLogger(max_errors, "Semantic")
        self.hasMain = False

    def verify(self, ast: ASTNode) -> None:
        """
        Verifies the semantic correctness of the program.
        """
        ctx = SymbolTable[Type]()
        self.add_builtins(ctx)
        try :
            self.first_pass(ctx, ast)
            self.second_pass(ctx, ast)
        except Exception as e:
            self.logger.log(f"Unexpected error during semantic analysis: {str(e)}", -1, -1)

        if self.logger.has_errors():
            self.logger.print_errors()
            raise SemanticError("Semantic errors found.")
        else:
            print("Program is semantically valid!")

    def add_builtins(self, ctx: SymbolTable) -> None:
        """
        Adds built-in functions to the symbol table.
        """
        ctx.insert('print', FunctionType(param_types=[StringType()],
                                        return_type=UnitType()))
        ctx.insert('length', FunctionType(param_types=[ArrayType(IntType())],
                                        return_type=IntType()))
        
    def first_pass(self, ctx: SymbolTable, node: ASTNode) -> None:
        """
        First pass of semantic analysis: collects top-level declarations types
        """
        match node:
            case Program(declarations):
                for decl in declarations:
                    self.first_pass(ctx, decl)
                if not self.hasMain:
                    self.logger.log("No main function found", -1, -1)

            case FunctionDeclaration(id, _, type, _):
                if id.name == 'main':
                    self.hasMain = True
                self.insertIntoCtx(ctx, node, id, type)
                
            case TopLevelVariableDeclaration(id, type, _):
                self.insertIntoCtx(ctx, node, id, type)

            case _:
                return

    def second_pass(self, ctx: SymbolTable, program: Program) -> None:
        """
        Second pass of semantic analysis: checks the types of function bodies
        """
        for decl in program.declarations:
            self.typeof(ctx, decl)
                
    def checkEqualTypes(self, error_exp: Exp, actual_type: Type, expected_type: Type):
        """
        Checks if the actual type matches the expected type.
        """
        if actual_type == expected_type:
            return
        
        match error_exp:            
            case FunctionCall(_, _):
                self.logger.log(f"Expected function call to return type '{expected_type}', "
                        f"found type '{actual_type}' for expression \n'{error_exp}'", error_exp.lineno, error_exp.column)
                
            case Conditional(_, _, _):
                self.logger.log(f"Expected both branches to be of same type; found {actual_type} and {expected_type}, "
                        f"for expression \n'{error_exp}'", error_exp.lineno, error_exp.column)
                
            case Var(_):
                self.logger.log(f"Expected variable '{error_exp}' to be of type '{expected_type}', "
                        f"found type '{actual_type}'", error_exp.lineno, error_exp.column)

            case _: 
                self.logger.log(f"Expected two equal types; found {actual_type} and {expected_type}, "
                        f"for expression \n'{error_exp}'", error_exp.lineno, error_exp.column)
        
    def checkInstance(self, error_exp: Exp, actual_type: Type, expected_class: type) -> bool:
        """
        Checks if the actual type is an instance of the expected class.
        Returns True if it is, otherwise logs an error and returns False.
        """
        if not isinstance(actual_type, expected_class):
            self.logger.log(f"Expected a {expected_class.__name__}, found {actual_type} "
                    f"for expression \n'{error_exp}'", error_exp.lineno, error_exp.column)
            return False
        return True

    def checkBuiltInConflict(self, error_exp: Exp, var: Var):
        """
        Checks if the variable name conflicts with built-in functions.
        """
        if var.name in ['print', 'length']:
            self.logger.log(f"Variable name '{var}' conflicts with built-in function", error_exp.lineno, error_exp.column)

    def checkArguments(self, ctx: SymbolTable, error_exp: Exp, exps: List[Exp], function_type: FunctionType):
        """
        Checks if the arguments of a function call match the expected types.
        """
        expected_types = function_type.param_types
        actual_types = [self.typeof(ctx, exp) for exp in exps]
        if len(actual_types) != len(expected_types) or any(a != e for a, e in zip(actual_types, expected_types)):
            self.logger.log(
                f"expected arguments of types [{', '.join(str(t) for t in expected_types)}], "
                f"found [{', '.join(str(t) for t in actual_types)}] for expression \n'{error_exp}'",
                error_exp.lineno,
                error_exp.column
            )

    def checkParameters(self, function_id : Var, parameters: List[Var], function_type: FunctionType):
        """
        Checks if the parameters names are unique and do not conflict with built-in functions.
        """
        if function_id.name == 'main':
            # check if matches let main (x) : Unit -> Unit
            if len(parameters) != 1 or len(function_type.param_types) != 1 or \
                    function_type.param_types[0] != UnitType() or \
                    function_type.return_type != UnitType():
                self.logger.log(f"main function must have signature 'let main (x) : Unit -> Unit'", function_id.lineno, function_id.column)
                return

        if len(parameters) != len(function_type.param_types):
            self.logger.log(f"number of params does not match type in function declaration "
                    f"'{function_id}'", function_id.lineno, function_id.column)

        param_names = set()
        for param in parameters:
            if param.name != '_' and param.name in param_names:
                self.logger.log(f"duplicate parameter name '{param.name}' in function declaration "
                        f"'{function_id}'", function_id.lineno, function_id.column)
            param_names.add(param.name)

    def checkAgainst(self, ctx: SymbolTable, matched_exp: Exp, expected_type: Type) -> None:
        """
        Checks if the expression `exp` matches the expected type `type` in the given context `ctx`.
        """
        match (matched_exp, expected_type):
            case (ArrayAccess(exp1, exp2), _):
                self.checkAgainst(ctx, exp2, IntType())
                exp1Type : ArrayType = self.typeof(ctx, exp1)
                if self.checkInstance(exp1, exp1Type, ArrayType):
                    self.checkEqualTypes(matched_exp, exp1Type.type, expected_type)
            
            case (Conditional(exp1, exp2, exp3), _):
                self.checkAgainst(ctx, exp1, BoolType())
                self.checkAgainst(ctx.enter_scope(), exp2, expected_type)
                self.checkAgainst(ctx.enter_scope(), exp3, expected_type)

            case (Sequence(first, rest), _):
                self.typeof(ctx, first)
                self.checkAgainst(ctx, rest, expected_type)

            case _:
                actual_type = self.typeof(ctx, matched_exp)
                self.checkEqualTypes(matched_exp, actual_type, expected_type)

    def insertIntoCtx(self, ctx: SymbolTable, matched_exp: Exp, var: Var, type: Type) -> None:
        """
        Inserts a variable and its type into the symbol table.
        """
        name = var.name
        match matched_exp:
            case FunctionDeclaration(_, _, _, _):
                if ctx.contains(name):
                    self.logger.log(f"Multiple declarations of function '{name}'", var.lineno, var.column)
                    return

            case TopLevelVariableDeclaration(_, _, _):
                if ctx.contains(name):
                    self.logger.log(f"Multiple declarations of top-level variable '{name}'", var.lineno, var.column)
                    return
            
        if name != '_':
            ctx.insert(name, type)
        
    def typeofVar(self, ctx: SymbolTable, exp: Exp, name: str) -> Type:
        varType = ctx.lookup(name)
        if name == '_':
            self.logger.log(f"Wildcard variable '{name}' cannot be used", exp.lineno, exp.column)
        elif varType is None:
            self.logger.log(f"unresolved symbol: {name}", exp.lineno, exp.column)
        return varType
        
    def typeof(self, ctx: SymbolTable, matched_exp: Exp) -> Type:
        """
        Determines the type of the expression `matched_exp` in the given context `ctx`.
        """
        match matched_exp:        
            case IntLiteral():
                return IntType()
            
            case BoolLiteral():
                return BoolType()
            
            case UnitLiteral():
                return UnitType()
            
            case StringLiteral():
                return StringType()
            
            case ArrayCreation(type, exp1, exp2):
                self.checkAgainst(ctx, exp1, IntType())
                self.checkAgainst(ctx, exp2, type)            
                return ArrayType(type)
            
            case ArrayAccess(exp1, exp2):
                self.checkAgainst(ctx, exp2, IntType())
                exp1Type : ArrayType = self.typeof(ctx, exp1)
                if self.checkInstance(exp1, exp1Type, ArrayType):         
                    return exp1Type.type
            
            case FunctionCall(id, exps):
                if id.name == 'print':
                    if len(exps) != 1:
                        self.logger.log(f"Print function takes exactly one argument", matched_exp.lineno, matched_exp.column)
                    exp1 = exps[0]
                    self.typeof(ctx, exp1)
                    return UnitType()
                
                if id.name == 'length':
                    if len(exps) != 1:
                        self.logger.log(f"Length function takes exactly one argument", matched_exp.lineno, matched_exp.column)
                    exp1 = exps[0]
                    exp1Type = self.typeof(ctx, exp1)
                    self.checkInstance(matched_exp, exp1Type, ArrayType)
                    return IntType()
                
                funcType : FunctionType = self.typeof(ctx, id)
                if self.checkInstance(id, funcType, FunctionType):
                    self.checkArguments(ctx, matched_exp, exps, funcType)
                    return funcType.return_type
                
            case VariableDeclaration(id, type, exp):
                self.checkAgainst(ctx.enter_scope(), exp, type)
                self.insertIntoCtx(ctx, matched_exp, id, type)
                return UnitType()
            
            case TopLevelVariableDeclaration(id, type, exp):

                if isinstance(exp, Sequence):
                    self.checkAgainst(ctx, exp.first, type)
                    local_ctx = ctx.enter_scope()
                    self.checkAgainst(local_ctx, exp.rest, type)
                else:
                    self.checkAgainst(ctx.enter_scope(), exp, type)
                return UnitType()
            
            case Var(name):
                return self.typeofVar(ctx, matched_exp, name)
            
            case Conditional(exp1, exp2, exp3):
                self.checkAgainst(ctx, exp1, BoolType())
                exp2Type = self.typeof(ctx.enter_scope(), exp2)
                exp3Type = self.typeof(ctx.enter_scope(), exp3)         
                self.checkEqualTypes(matched_exp, exp2Type, exp3Type)          
                return exp2Type
            
            case WhileLoop(exp1, exp2):
                self.checkAgainst(ctx, exp1, BoolType())
                self.typeof(ctx.enter_scope(), exp2)
                return UnitType()
            
            case Assignment(lhs, exp):
                lhsType = self.typeof(ctx, lhs)
                expType = self.typeof(ctx, exp)
                self.checkEqualTypes(matched_exp, lhsType, expType)
                return UnitType()
            
            case Sequence(first, rest):
                self.typeof(ctx, first)
                return self.typeof(ctx, rest)

            case BinaryOp(left, operator, right):

                if operator in ['+', '-', '*', '/', '%', '^']:
                    self.checkAgainst(ctx, left, IntType())
                    self.checkAgainst(ctx, right, IntType())
                    return IntType()
                
                if operator in ['==', '!=', '<', '>', '<=', '>=']:
                    leftType = self.typeof(ctx, left)
                    rightType = self.typeof(ctx, right)
                    self.checkEqualTypes(matched_exp, leftType, rightType)
                    return BoolType()
                
                if operator in ['&&', '||']:
                    self.checkAgainst(ctx, left, BoolType())
                    self.checkAgainst(ctx, right, BoolType())
                    return BoolType()
                
                if operator == '++':
                    self.checkAgainst(ctx, left, StringType())
                    self.checkAgainst(ctx, right, StringType())
                    return StringType()
            
            case LogicalNegation(operand):
                self.checkAgainst(ctx, operand, BoolType())
                return BoolType()
            
            case FunctionDeclaration(id, parameters, type, body):
                self.checkBuiltInConflict(matched_exp, id)
                if not self.checkInstance(matched_exp, type, FunctionType):
                    return
                type : FunctionType = type

                self.checkParameters(id, parameters, type)

                # Augment the context with parameter types
                local_ctx = ctx.enter_scope()
                for param, param_type in zip(parameters, type.param_types):
                    self.insertIntoCtx(local_ctx, param, param, param_type)
                
                self.checkAgainst(local_ctx, body, type.return_type)

            case Group(exp):
                return self.typeof(ctx.enter_scope(), exp)
            
            case _:
                self.logger.log(f"Unknown expression type '{type(matched_exp)}'", matched_exp.lineno, matched_exp.column)