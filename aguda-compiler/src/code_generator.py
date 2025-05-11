from src.syntax import *
import subprocess
import os
from typing import Dict, List, Set, Tuple
from src.error_logger import ErrorLogger

class CodeGenerationError(Exception):
    """Custom exception for code generation errors."""
    pass

class Emitter:
    def __init__(self):
        self.code = []
        self.counter = 0

    def emit(self, code: str):
        self.code.append(code)

class CodeGenerator:
    def __init__(self, max_errors):
        self.logger = ErrorLogger(max_errors, "Code Generation")
        self.emitter = Emitter()

    def get_llvm_type(self, aguda_type: Type) -> str:
        """Convert AGUDA type to LLVM type."""
        match aguda_type:
            case BaseType(name="Int"):
                return "i32"
            case BaseType(name="Bool"):
                return "i1"
            case BaseType(name="Unit"):
                return "void"
            case FunctionType(return_type, param_types):
                param_types_llvm = [self.get_llvm_type(param) for param in param_types]
                return f"{self.get_llvm_type(return_type)} ({', '.join(param_types_llvm)})"
            case _:
                self.logger.log(f"Unsupported type: {aguda_type}", -1, -1)
    
    def generate_exp(self, matched_exp: Exp):
        """
        Generate LLVM code for an expression.
        """
        match matched_exp:
            case IntLiteral():
                self.emitter.emit(f"%int_literal_{self.counter} = i32 {matched_exp.value}")
            case BoolLiteral():
                self.emitter.emit(f"%bool_literal_{self.counter} = i1 {matched_exp.value}")
            case UnitLiteral():
                self.emitter.emit(f"%unit_literal_{self.counter} = i32 0")
            case FunctionCall(id, exps):
                pass
            case VariableDeclaration(id, type, exp):
                pass
            case Var(name):
                pass
            case Conditional(cond, then_branch, else_branch):
                pass
            case WhileLoop(cond, body):
                pass
            case Assignment(lhs, rhs):
                pass
            case Sequence(first, rest):
                pass
            case BinaryOp(op, left, right):
                pass
            case LogicalNegation(operand):
                pass
            case Group(exp):
                return self.generate_exp(exp)
            case _:
                self.logger.log(f"Non-implemented expression type: {type(matched_exp).__name__}", matched_exp.lineno, matched_exp.column)           

    def generate(self, program: Program) -> Emitter:
        """Generate LLVM IR code from the AST."""
        
        self.emitter.emit("; LLVM IR generated from AGUDA")
        
        for decl in program.declarations:
            match decl:
                case FunctionDeclaration(name, parameters, type, body):
                    self.generate_function(name, parameters, type, body)
                case TopLevelVariableDeclaration(name, type, value):
                    self.generate_top_level_variable(name, type, value)
                case _:
                    self.logger.log(f"Non-implemented top-level declaration type: {type(decl).__name__}", decl.lineno, decl.column)
        
        # Check if there were any errors
        if self.logger.has_errors():
            self.logger.print_errors()
            raise CodeGenerationError("Code generation failed due to unsupported features")
        
        return self.emitter
