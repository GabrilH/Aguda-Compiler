from src.syntax import *
from src.error_logger import ErrorLogger
from llvmlite import ir
from llvmlite.ir import Constant
from typing import Dict, Tuple, Optional, List

class CodeGenerationError(Exception):
    """Custom exception for code generation errors."""
    pass

class CodeGenerator:
    def __init__(self, max_errors):
        self.logger = ErrorLogger(max_errors, "Code Generation")
        self.module = ir.Module()
        self.builder = None
        self.current_function = None
        self.symbol_table : Dict[str, Tuple[Type, ir.Value]] = {}  # Maps variable names to (type, value) pairs
        self.function_types : Dict[str, FunctionType] = {}  # Maps function names to their types
        self.label_counter = 0
        self.register_counter = 0

    def get_llvm_type(self, aguda_type: Type) -> ir.Type:
        """Convert AGUDA type to LLVM type."""
        match aguda_type:
            case BaseType('Int'):
                return ir.IntType(32)
            case BaseType("Bool"):
                return ir.IntType(1)
            case BaseType("Unit"):
                return ir.IntType(1)
            case FunctionType():
                param_types = [self.get_llvm_type(t) for t in aguda_type.param_types]
                return_type = self.get_llvm_type(aguda_type.return_type)
                return ir.FunctionType(return_type, param_types)
            case _:
                self.logger.log(f"Unsupported type: {aguda_type}", aguda_type.lineno, aguda_type.column)

    def fresh_label(self) -> str:
        """Generate a fresh label name."""
        label = f"label_{self.label_counter}"
        self.label_counter += 1
        return label

    def fresh_register(self) -> str:
        """Generate a fresh register name."""
        reg = f"%r{self.register_counter}"
        self.register_counter += 1
        return reg

    def expGen(self, exp: Exp) -> Tuple[List[str], str]:
        """
        Generate LLVM code for an expression.
        Returns a tuple of (code, value) where code is a list of LLVM instructions
        and value is the register containing the result.
        """
        match exp:
            case IntLiteral(value):
                return [], str(value)
            case BoolLiteral(value):
                return [], "1" if value else "0"
            case UnitLiteral():
                # TODO: not sure of Unit value
                return [], "1"
            case Var(name):
                var_info = self.symbol_table.get(name)
                if not var_info:
                    self.logger.log(f"Undefined variable: {name}", exp.lineno, exp.column)
                var_type, var_value = var_info
                reg = self.fresh_register()
                return [f"{reg} = load {self.get_llvm_type(var_type)}, {var_value}"], reg
            
            case VariableDeclaration(id, type, value):
                #TODO
                pass
            case BinaryOp(left, operator, right):
                code1, val1 = self.expGen(left)
                code2, val2 = self.expGen(right)
                reg = self.fresh_register()

                if operator in ['+', '-', '*', '/', '%']:
                    op_map = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'sdiv', '%': 'srem'}
                    code = code1 + code2 + [f"{reg} = {op_map[operator]} i32 {val1}, {val2}"]
                elif operator in ['==', '!=', '<', '<=', '>', '>=']:
                    # TODO it's possible to compare bool values
                    op_map = {'==': 'eq', '!=': 'ne', '<': 'slt', '<=': 'sle', '>': 'sgt', '>=': 'sge'}
                    code = code1 + code2 + [f"{reg} = icmp {op_map[operator]} i32 {val1}, {val2}"]
                else:
                    #TODO power operator
                    self.logger.log(f"Unsupported binary operator: {operator}", exp.lineno, exp.column)

            case FunctionCall(id, arguments):
                arg_codes = []
                arg_values = []
                for arg in arguments:
                    code, val = self.expGen(arg)
                    arg_codes.extend(code)
                    arg_values.append(val)
                
                # Get function type
                func_type = self.function_types.get(id.name)
                if not func_type:
                    self.logger.log(f"Undefined function: {id.name}", id.lineno, id.column)
                
                # Generate call
                reg = self.fresh_register()
                arg_str = ", ".join(f"{self.get_llvm_type(t)} {v}" for t, v in zip(func_type.param_types, arg_values))
                code = arg_codes + [f"{reg} = call {self.get_llvm_type(func_type.return_type)} @{id.name}({arg_str})"]
                return code, reg
            
        if isinstance(exp, Conditional):
            # Generate labels
            then_label = self.fresh_label()
            else_label = self.fresh_label()
            end_label = self.fresh_label()
            
            # Generate condition code
            cond_code = self.condGen(exp.condition, then_label, else_label)
            
            # Generate then branch
            then_code, then_val = self.expGen(exp.then_branch)
            then_code.append(f"br label %{end_label}")
            
            # Generate else branch
            else_code, else_val = self.expGen(exp.else_branch)
            else_code.append(f"br label %{end_label}")
            
            # Combine all code
            reg = self.fresh_register()
            code = (cond_code + 
                   [f"{then_label}:"] + then_code +
                   [f"{else_label}:"] + else_code +
                   [f"{end_label}:",
                    f"{reg} = phi i32 [{then_val}, %{then_label}], [{else_val}, %{else_label}]"])
            
            return code, reg
        elif isinstance(exp, WhileLoop):
            # Generate labels
            start_label = self.fresh_label()
            body_label = self.fresh_label()
            end_label = self.fresh_label()
            
            # Generate condition code
            cond_code = self.condGen(exp.condition, body_label, end_label)
            
            # Generate body code
            body_code, _ = self.expGen(exp.body)
            body_code.append(f"br label %{start_label}")
            
            # Combine all code
            code = ([f"br label %{start_label}",
                    f"{start_label}:"] + 
                   cond_code +
                   [f"{body_label}:"] + body_code +
                   [f"{end_label}:",
                    "ret i32 1"])  # Return unit value
            
            return code, "1"  # Return unit value
        elif isinstance(exp, Sequence):
            code1, _ = self.expGen(exp.first)
            code2, val2 = self.expGen(exp.rest)
            return code1 + code2, val2
        elif isinstance(exp, Assignment):
            # Generate code for the right-hand side
            code, val = self.expGen(exp.exp)
            
            if isinstance(exp.lhs, Var):
                var_info = self.symbol_table.get(exp.lhs.name)
                if not var_info:
                    raise CodeGenerationError(f"Undefined variable: {exp.lhs.name}")
                var_type, var_value = var_info
                code.append(f"store {self.get_llvm_type(var_type)} {val}, {var_value}")
            else:
                raise CodeGenerationError("Array assignments not supported yet")
            
            return code, "1"  # Return unit value
        else:
            raise CodeGenerationError(f"Unsupported expression type: {type(exp)}")

    def condGen(self, exp: Exp, true_label: str, false_label: str) -> List[str]:
        """
        Generate LLVM code for a conditional expression.
        Returns a list of LLVM instructions that branch to true_label or false_label.
        """
        if isinstance(exp, BoolLiteral):
            return [f"br i1 {1 if exp.value else 0}, label %{true_label}, label %{false_label}"]
        elif isinstance(exp, BinaryOp) and exp.operator in ['&&', '||']:
            if exp.operator == '&&':
                mid_label = self.fresh_label()
                code1 = self.condGen(exp.left, mid_label, false_label)
                code2 = self.condGen(exp.right, true_label, false_label)
                return code1 + [f"{mid_label}:"] + code2
            else:  # ||
                mid_label = self.fresh_label()
                code1 = self.condGen(exp.left, true_label, mid_label)
                code2 = self.condGen(exp.right, true_label, false_label)
                return code1 + [f"{mid_label}:"] + code2
        else:
            # For other expressions, evaluate and branch based on result
            code, val = self.expGen(exp)
            return code + [f"br i1 {val}, label %{true_label}, label %{false_label}"]

    def first_pass(self, program: Program):
        """
        First pass over the AST to collect function types and global variables.
        """
        for decl in program.declarations:
            if isinstance(decl, FunctionDeclaration):
                self.function_types[decl.name.name] = decl.type
            elif isinstance(decl, TopLevelVariableDeclaration):
                if not isinstance(decl.value, (IntLiteral, BoolLiteral, UnitLiteral)):
                    raise CodeGenerationError("Top-level variable declarations must be initialized with literals")
                # Create global variable
                var_type = self.get_llvm_type(decl.type)
                var = ir.GlobalVariable(self.module, var_type, decl.name.name)
                var.initializer = self.get_llvm_constant(decl.value, decl.type)
                self.symbol_table[decl.name.name] = (decl.type, var)

    def get_llvm_constant(self, value: Exp, type: Type) -> Constant:
        """Convert an AGUDA literal to an LLVM constant."""
        if isinstance(value, IntLiteral):
            return Constant(ir.IntType(32), value.value)
        elif isinstance(value, BoolLiteral):
            return Constant(ir.IntType(1), 1 if value.value else 0)
        elif isinstance(value, UnitLiteral):
            return Constant(ir.IntType(32), 1)
        else:
            raise CodeGenerationError(f"Unsupported constant type: {type(value)}")

    def second_pass(self, program: Program):
        """
        Second pass over the AST to generate LLVM code.
        """
        # Generate code for each function
        for decl in program.declarations:
            if isinstance(decl, FunctionDeclaration):
                self.generate_function(decl)

    def generate_function(self, func_decl: FunctionDeclaration):
        """Generate LLVM code for a function declaration."""
        # Create function
        func_type = self.get_llvm_type(func_decl.type)
        func = ir.Function(self.module, func_type, func_decl.name.name)
        
        # Set up basic block
        entry_block = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(entry_block)
        self.current_function = func
        
        # Add parameters to symbol table
        for param, arg in zip(func_decl.parameters, func.args):
            param_type = func_decl.type.param_types[func.args.index(arg)]
            # Allocate space for parameter
            param_ptr = self.builder.alloca(self.get_llvm_type(param_type))
            self.builder.store(arg, param_ptr)
            self.symbol_table[param.name] = (param_type, param_ptr)
        
        # Generate function body
        code, value = self.expGen(func_decl.body)
        
        # Add all instructions to the basic block
        for instr in code:
            self.builder.insert_into_block(entry_block, instr)
        
        # Return the value
        if isinstance(func_decl.type.return_type, BaseType) and func_decl.type.return_type.name == "unit":
            self.builder.ret_void()
        else:
            self.builder.ret(value)
        
        # Clean up
        self.builder = None
        self.current_function = None
        # Clear local variables from symbol table
        self.symbol_table = {k: v for k, v in self.symbol_table.items() 
                           if isinstance(v[1], ir.GlobalVariable)}

    def generate(self, program: Program) -> str:
        """Generate LLVM IR code from the AST."""
        self.first_pass(program)
        self.second_pass(program)
        
        # Check if there were any errors
        if self.logger.has_errors():
            self.logger.print_errors()
            raise CodeGenerationError("Code generation failed due to unsupported features")
        
        return str(self.module)