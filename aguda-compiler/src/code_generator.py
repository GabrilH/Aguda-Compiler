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

    def fresh_cond_labels(self) -> Tuple[str, str, str]:
        """Generate a set of related labels for a conditional expression."""
        cond_num = self.label_counter
        self.label_counter += 1
        then_label = f"cond_{cond_num}_then"
        else_label = f"cond_{cond_num}_else"
        end_label = f"cond_{cond_num}_end"
        return then_label, else_label, end_label

    def fresh_while_labels(self) -> Tuple[str, str, str]:
        """Generate a set of related labels for a while loop."""
        loop_num = self.label_counter
        self.label_counter += 1
        start_label = f"while_{loop_num}_start"
        body_label = f"while_{loop_num}_body"
        end_label = f"while_{loop_num}_end"
        return start_label, body_label, end_label

    def expGen(self, exp: Exp) -> ir.Value:
        """
        Generate LLVM code for an expression.
        Returns the LLVM value containing the result.
        """
        match exp:
            case IntLiteral(value):
                return ir.Constant(ir.IntType(32), value)
            case BoolLiteral(value):
                return ir.Constant(ir.IntType(1), 1 if value else 0)
            case UnitLiteral():
                return ir.Constant(ir.IntType(32), 1)
            case Var(name):
                var_info = self.symbol_table.get(name)
                if not var_info:
                    self.logger.log(f"Undefined variable: {name}", exp.lineno, exp.column)
                var_type, var_value = var_info
                return self.builder.load(var_value)
            
            case VariableDeclaration(id, type, value):
                # Allocate space for the variable
                var_type = self.get_llvm_type(type)
                var_ptr = self.builder.alloca(var_type)
                
                # Store the initial value
                if value is not None:
                    val = self.expGen(value)
                    self.builder.store(val, var_ptr)
                
                # Add to symbol table
                self.symbol_table[id.name] = (type, var_ptr)
                
                # Return unit value for variable declaration
                return ir.Constant(ir.IntType(32), 1)
            
            case BinaryOp(left, operator, right):
                val1 = self.expGen(left)
                val2 = self.expGen(right)

                if operator in ['+', '-', '*', '/', '%']:
                    op_map = {
                        '+': self.builder.add,
                        '-': self.builder.sub,
                        '*': self.builder.mul,
                        '/': self.builder.sdiv,
                        '%': self.builder.srem
                    }
                    return op_map[operator](val1, val2)
                elif operator in ['==', '!=', '<', '<=', '>', '>=']:
                    # TODO it's possible to compare bool values
                    op_map = {
                        '==': 'eq', '!=': 'ne', '<': 'slt', '<=': 'sle', '>': 'sgt', '>=': 'sge'
                    }
                    return self.builder.icmp_signed(op_map[operator], val1, val2)
                else:
                    #TODO power operator
                    self.logger.log(f"Unsupported binary operator: {operator}", exp.lineno, exp.column)

            case FunctionCall(id, arguments):
                arg_values = [self.expGen(arg) for arg in arguments]
                
                # Get function type
                func_type = self.function_types.get(id.name)
                if not func_type:
                    self.logger.log(f"Undefined function: {id.name}", id.lineno, id.column)
                
                # Get function from module
                func = self.module.get_global(id.name)
                if not func:
                    self.logger.log(f"Function not found in module: {id.name}", id.lineno, id.column)
                
                return self.builder.call(func, arg_values)
            
            case Conditional(condition, then_branch, else_branch):
                # Generate labels
                then_label, else_label, end_label = self.fresh_cond_labels()
                
                # Create blocks ahead of time
                then_block = self.current_function.append_basic_block(then_label)
                else_block = self.current_function.append_basic_block(else_label)
                
                # Generate condition code that will branch to the appropriate block
                self.condGen(condition, then_label, else_label)
                
                # Generate then branch
                self.builder.position_at_end(then_block)
                then_val = self.expGen(then_branch)
                then_block_end = self.builder.block
                
                # Create end block
                end_block = self.current_function.append_basic_block(end_label)
                self.builder.branch(end_block)
                
                # Generate else branch
                self.builder.position_at_end(else_block)
                else_val = self.expGen(else_branch)
                else_block_end = self.builder.block
                self.builder.branch(end_block)

                # Position at end block and create phi node
                self.builder.position_at_end(end_block)
                phi = self.builder.phi(then_val.type)
                phi.add_incoming(then_val, then_block_end)
                phi.add_incoming(else_val, else_block_end)
                
                return phi
            
            case WhileLoop(condition, body):
                # Generate labels
                start_label, body_label, end_label = self.fresh_while_labels()
                
                # Create all blocks ahead of time
                start_block = self.current_function.append_basic_block(start_label)
                body_block = self.current_function.append_basic_block(body_label)
                end_block = self.current_function.append_basic_block(end_label)
                
                # Branch to start block
                self.builder.branch(start_block)
                
                # Generate start block with condition
                self.builder.position_at_end(start_block)
                self.condGen(condition, body_label, end_label)
                
                # Generate body block
                self.builder.position_at_end(body_block)
                self.expGen(body)
                self.builder.branch(start_block)
                
                # Position at end block
                self.builder.position_at_end(end_block)
                
                # Return unit value
                return ir.Constant(ir.IntType(32), 1)
            
            case Sequence(first, rest):
                self.expGen(first)
                return self.expGen(rest)
            
            case Assignment(lhs, exp):
                # Generate code for the right-hand side
                val = self.expGen(exp)

                if isinstance(lhs, Var):
                    var_info = self.symbol_table.get(lhs.name)
                    if not var_info:
                        self.logger.log(f"Undefined variable: {lhs.name}", lhs.lineno, lhs.column)
                    var_type, var_value = var_info
                    self.builder.store(val, var_value)
                else:
                    self.logger.log(f"Array assignments not supported yet", lhs.lineno, lhs.column)
                
                return ir.Constant(ir.IntType(32), 1)  # Return unit value
            
            case _:
                self.logger.log(f"Unsupported expression type: {type(exp)}", exp.lineno, exp.column)

    def condGen(self, exp: Exp, true_label: str, false_label: str):
        """
        Generate LLVM code for a conditional expression.
        Branches to true_label or false_label based on the condition.
        """
        # Find existing blocks or create new ones
        true_blocks = [b for b in self.current_function.basic_blocks if b.name == true_label]
        false_blocks = [b for b in self.current_function.basic_blocks if b.name == false_label]
        
        true_block = true_blocks[0] if true_blocks else self.current_function.append_basic_block(true_label)
        false_block = false_blocks[0] if false_blocks else self.current_function.append_basic_block(false_label)
        
        match exp:
            case BoolLiteral(value):
                if value:
                    self.builder.branch(true_block)
                else:
                    self.builder.branch(false_block)
                    
            case BinaryOp(left, '&&', right):
                mid_label = self.fresh_label()
                mid_block = self.current_function.append_basic_block(mid_label)
                
                # Generate left operand, will branch to mid_block if true, false_block if false
                self.condGen(left, mid_label, false_label)
                
                # Generate right operand in mid_block
                self.builder.position_at_end(mid_block)
                self.condGen(right, true_label, false_label)
            
            case BinaryOp(left, '||', right):
                mid_label = self.fresh_label()
                mid_block = self.current_function.append_basic_block(mid_label)
                
                # Generate left operand, will branch to true_block if true, mid_block if false
                self.condGen(left, true_label, mid_label)
                
                # Generate right operand in mid_block
                self.builder.position_at_end(mid_block)
                self.condGen(right, true_label, false_label)
            
            # case LogicalNegation(operand):
            #     return self.condGen(operand, false_label, true_label)

            # TODO: binop comparable
            
            case _:
                # For other expressions, evaluate and branch based on result
                val = self.expGen(exp)
                self.builder.cbranch(val, true_block, false_block)

    def first_pass(self, program: Program):
        """
        First pass over the AST to collect function types and global variables.z
        """
        # Create our print function
        print_type = FunctionType([BaseType("Int")], BaseType("Unit"))  # We'll handle type checking in expGen
        print_func = ir.Function(self.module, self.get_llvm_type(print_type), "print")
        print_func.linkage = "external"
        
        # Add function type to our dictionary
        self.function_types["print"] = print_type

        for decl in program.declarations:
            match decl:
                case FunctionDeclaration(id, _, type, _):
                    self.function_types[id.name] = type
                case TopLevelVariableDeclaration(id, type, value):
                    if not isinstance(value, (IntLiteral, BoolLiteral, UnitLiteral)):
                        self.logger.log(f"Top-level variable declarations must be initialized with literals", decl.lineno, decl.column)
                    else:
                        var_type = self.get_llvm_type(type)
                        var = ir.GlobalVariable(self.module, var_type, id.name)
                        var.initializer = self.get_llvm_constant(value, type)
                        self.symbol_table[id.name] = (type, var)

    def get_llvm_constant(self, value: Exp, type: Type) -> Constant:
        """Convert an AGUDA literal to an LLVM constant."""
        match value:
            case IntLiteral(value):
                return Constant(ir.IntType(32), value.value)
            case BoolLiteral(value):
                return Constant(ir.IntType(1), 1 if value.value else 0)
            case UnitLiteral():
                return Constant(ir.IntType(32), 1)
            case _:
                self.logger.log(f"Unsupported constant type: {type(value)}", value.lineno, value.column)

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
        func = ir.Function(self.module, func_type, func_decl.id.name)
        
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
        value = self.expGen(func_decl.body)
        
        # Return the value
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
            raise CodeGenerationError("Code generation failed due to errors")
        
        return str(self.module)