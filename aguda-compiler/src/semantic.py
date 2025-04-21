# from src.syntax import *
# from src.type_checker import verify

# def validate(program: Program) -> None:
#     """
#     Validates a program by ensuring all its declarations are well-formed.
#     """
#     verify(program)
#     stmts : List[Declaration] = program.declarations
#     for stmt in stmts:
#         if isinstance(stmt, FunctionDeclaration):
#             # Validate function declarations
#             type_checker.typeof(ctx, stmt)
#         elif isinstance(stmt, TopLevelVariableDeclaration):
#             # Validate variable declarations
#             typeof(ctx, stmt)
#         else:
#             raise TypeError(f"Invalid top-level declaration: {type(stmt)}")
    
#     print("Program is semantically valid!")
        
# def add_builtins(ctx: SymbolTable) -> None:
#     """
#     Adds built-in functions to the symbol table.
#     """
#     ctx.insert('print', FunctionType(param_types=[BaseType('String')],
#                                     return_type=BaseType('Unit')))
#     ctx.insert('length', FunctionType(param_types=[ArrayType(BaseType('Int'))],
#                                     return_type=BaseType('Int')))
#     # for base_type in ['Int', 'Bool', 'Unit', 'String']:
#     #     ctx.insert('print', FunctionType(BaseType('Unit'), [BaseType(base_type)]))
#     #     ctx.insert('length', FunctionType(BaseType('Int'), [ArrayType(BaseType(base_type))]))