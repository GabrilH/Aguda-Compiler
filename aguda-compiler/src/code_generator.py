from src.syntax import *
from src.symbol_table import SymbolTable
from llvmlite import ir
from typing import Dict, Tuple, Optional

class CodeGenerationError(Exception):
    """Custom exception for code generation errors."""
    pass

class CodeGenerator:
    def __init__(self):
        self.module = ir.Module()
        self.builder : Optional[ir.IRBuilder] = None
        self.current_function : Optional[ir.Function] = None
        self.label_counter = 0

    def generate(self, program: Program) -> str:
        """Generate LLVM IR code from the AST."""
        ctx = SymbolTable[ir.Value]()
        self.add_builtins(ctx)	
        self.first_pass(ctx, program)
        self.second_pass(ctx, program)
        return str(self.module)
    
    def add_builtins(self, ctx: SymbolTable):
        """
        Adds built-in functions to the module.
        """
        # Print function
        print_type = FunctionType([BaseType("Int")], BaseType("Unit")) # Input type is bypassed in expGen
        print_func = ir.Function(self.module, self.get_llvm_type(print_type), "print")
        print_func.linkage = "external"
        ctx.insert("print", print_func)

        # Power function
        power_type = FunctionType([BaseType("Int"), BaseType("Int")], BaseType("Int"))
        power_func = ir.Function(self.module, self.get_llvm_type(power_type), "_power")
        power_func.linkage = "external"
        ctx.insert("_power", power_func)

    def first_pass(self, ctx: SymbolTable, program: Program):
        """
        First pass over the AST to collect function types and global variables.
        """
        for decl in program.declarations:
            match decl:
                case FunctionDeclaration(id, _, type, _):
                    func_type = self.get_llvm_type(type)
                    func = ir.Function(self.module, func_type, id.name)
                    ctx.insert(id.name, func)
                case TopLevelVariableDeclaration(id, type, value):
                    if isinstance(value, (IntLiteral, BoolLiteral, UnitLiteral)):
                        var_type = self.get_llvm_type(type)
                        var = ir.GlobalVariable(self.module, var_type, id.name)
                        var.initializer = self.expGen(ctx, value)
                        ctx.insert(id.name, var)
                    else:
                        raise CodeGenerationError(f"Top-level variable declarations must be initialized with literals ({decl.lineno}, {decl.column})")

    def second_pass(self, ctx: SymbolTable, program: Program):
        """
        Second pass over the AST to generate LLVM code.
        """
        for decl in program.declarations:
            if isinstance(decl, FunctionDeclaration):
                self.generate_function(ctx, decl)

    def generate_function(self, ctx: SymbolTable, func_decl: FunctionDeclaration):
        """Generate LLVM code for a function declaration."""
        func = ctx.lookup(func_decl.id.name)
        # Set up basic block
        entry_block = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(entry_block)
        self.current_function = func
        
        # Enter a new scope for function parameters and body
        local_ctx = ctx.enter_scope()
        
        # Add parameters to symbol table
        for param, arg in zip(func_decl.parameters, func.args):
            param_type = func_decl.type.param_types[func.args.index(arg)]
            # Allocate space for parameter
            param_ptr = self.builder.alloca(self.get_llvm_type(param_type))
            self.builder.store(arg, param_ptr)
            local_ctx.insert(param.name, param_ptr)
        
        # Generate function body
        value = self.expGen(local_ctx, func_decl.body)
        
        # Return the value
        self.builder.ret(value)
        
        self.builder = None
        self.current_function = None
        
    def expGen(self, ctx: SymbolTable, exp: Exp) -> ir.Value:
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
                var_value = ctx.lookup(name)
                return self.builder.load(var_value)
            
            case VariableDeclaration(id, type, value):
                # Allocate space for the variable
                var_type = self.get_llvm_type(type)
                var_ptr = self.builder.alloca(var_type)
                
                # Store the initial value
                val = self.expGen(ctx.enter_scope(),value)
                self.builder.store(val, var_ptr)
                
                # Add to symbol table
                ctx.insert(id.name, var_ptr)
                
                # Return unit value for variable declaration
                return ir.Constant(ir.IntType(32), 1)
            
            case BinaryOp(left, op, right):
                # Handle short-circuit boolean operations using condGen
                if op in ['&&', '||']:
                    return self.short_circuit_expGen(ctx, exp)
                
                # For other binary operators, evaluate both sides first (left then right)
                val1 = self.expGen(ctx, left)
                val2 = self.expGen(ctx, right)

                match op:
                    case '+':
                        return self.builder.add(val1, val2)
                    case '-':
                        return self.builder.sub(val1, val2)
                    case '*':
                        return self.builder.mul(val1, val2)
                    case '/':
                        return self.builder.sdiv(val1, val2)
                    case '%':
                        return self.builder.srem(val1, val2)
                    case '^':
                        power_func = self.module.get_global('_power')
                        return self.builder.call(power_func, [val1, val2])
                    case '==' | '!=' | '<' | '<=' | '>' | '>=':
                        return self.builder.icmp_signed(op, val1, val2)
                    case _:
                        raise CodeGenerationError(f"Unsupported binary operator: {op} ({exp.lineno}, {exp.column})")

            case FunctionCall(id, arguments):
                arg_values = [self.expGen(ctx, arg) for arg in arguments]
                func = ctx.lookup(id.name)
                
                # Special handling for print function: convert bool to int
                if id.name == "print" and arg_values[0].type == ir.IntType(1):
                        arg_values[0] = self.builder.zext(arg_values[0], ir.IntType(32))
                
                return self.builder.call(func, arg_values)
            
            case Conditional(condition, then_branch, else_branch):
                # Generate labels
                then_label, else_label, end_label = self.fresh_cond_labels()
                
                # Create blocks ahead of time
                then_block = self.current_function.append_basic_block(then_label)
                else_block = self.current_function.append_basic_block(else_label)
                end_block = self.current_function.append_basic_block(end_label)
                
                # Generate condition code that will branch to the appropriate block
                self.condGen(ctx, condition, then_label, else_label)
                
                # Generate then branch
                self.builder.position_at_end(then_block)
                then_val = self.expGen(ctx.enter_scope(), then_branch)
                then_block_end = self.builder.block
                
                self.builder.branch(end_block)
                
                # Generate else branch
                self.builder.position_at_end(else_block)
                # Enter a new scope for the else branch
                else_val = self.expGen(ctx.enter_scope(), else_branch)
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
                self.condGen(ctx, condition, body_label, end_label)
                
                # Generate body block
                self.builder.position_at_end(body_block)
                # Enter a new scope for the loop body
                self.expGen(ctx.enter_scope(), body)
                # Exit loop body scope
                self.builder.branch(start_block)
                
                # Position at end block
                self.builder.position_at_end(end_block)
                
                # Return unit value
                return ir.Constant(ir.IntType(32), 1)
            
            case Sequence(first, rest):
                self.expGen(ctx, first)
                return self.expGen(ctx, rest)
            
            case Assignment(lhs, exp):
                # Generate code for the right-hand side
                val = self.expGen(ctx, exp)

                if isinstance(lhs, Var):
                    var_ptr = ctx.lookup(lhs.name)
                    self.builder.store(val, var_ptr)
                else:
                    raise CodeGenerationError(f"Array assignments not supported ({lhs.lineno}, {lhs.column})")
                
                return ir.Constant(ir.IntType(32), 1)  # Return unit value
            
            case LogicalNegation(operand):
                # For logical negation, delegate to short-circuit implementation
                return self.short_circuit_expGen(ctx, exp)
            
            case Group(exp):
                return self.expGen(ctx, exp)
            
            case _:
                raise CodeGenerationError(f"Not implemented: Generating code for ({exp.lineno}, {exp.column}) expression  '{exp}'")

    def short_circuit_expGen(self, ctx: SymbolTable, exp: Exp) -> ir.Value:
        """
        Generate LLVM IR code for short-circuit boolean expressions.
        Returns a boolean value using proper short-circuit evaluation.
        """
        # Create result variable to store the boolean result
        result_ptr = self.builder.alloca(ir.IntType(1))
        
        # Create blocks for the final result
        end_label = self.fresh_label()
        end_block = self.current_function.append_basic_block(end_label)
        
        match exp:
            case BinaryOp(left, '&&', right):
                # For AND, create blocks to evaluate right operand if left is true
                true_label = self.fresh_label()
                false_label = self.fresh_label()
                
                true_block = self.current_function.append_basic_block(true_label)
                false_block = self.current_function.append_basic_block(false_label)
                
                # Use condGen to implement short-circuit evaluation
                self.condGen(ctx, left, true_label, false_label)
                
                # If left is true, evaluate right operand
                self.builder.position_at_end(true_block)
                right_val = self.expGen(ctx, right)
                self.builder.store(right_val, result_ptr)
                self.builder.branch(end_block)
                
                # If left is false, result is false without evaluating right
                self.builder.position_at_end(false_block)
                self.builder.store(ir.Constant(ir.IntType(1), 0), result_ptr)
                self.builder.branch(end_block)
                
            case BinaryOp(left, '||', right):
                # For OR, create blocks to evaluate right operand if left is false
                true_label = self.fresh_label()
                false_label = self.fresh_label()
                
                true_block = self.current_function.append_basic_block(true_label)
                false_block = self.current_function.append_basic_block(false_label)
                
                # Use condGen to implement short-circuit evaluation
                self.condGen(ctx, left, true_label, false_label)
                
                # If left is true, result is true without evaluating right
                self.builder.position_at_end(true_block)
                self.builder.store(ir.Constant(ir.IntType(1), 1), result_ptr)
                self.builder.branch(end_block)
                
                # If left is false, evaluate right operand
                self.builder.position_at_end(false_block)
                right_val = self.expGen(ctx, right)
                self.builder.store(right_val, result_ptr)
                self.builder.branch(end_block)
                
            case LogicalNegation(operand):
                # Implement logical negation with short-circuit
                operand_val = self.expGen(ctx, operand)
                self.builder.store(self.builder.not_(operand_val), result_ptr)
                self.builder.branch(end_block)
                
            case _:
                raise CodeGenerationError(f"Unexpected expression in short_circuit_expGen: {exp}")
        
        # Continue from the end block
        self.builder.position_at_end(end_block)
        return self.builder.load(result_ptr)

    def condGen(self, ctx: SymbolTable, exp: Exp, true_label: str, false_label: str):
        """
        Generate LLVM code for a conditional expression.
        Branches to true_label or false_label based on the condition.
        This is specifically used for boolean expressions with short-circuit evaluation.
        """
        # Create the blocks if they don't exist yet
        true_block = self.current_function.append_basic_block(true_label)
        false_block = self.current_function.append_basic_block(false_label)
        
        match exp:
            case BoolLiteral(value):
                # Simply branch to the appropriate block for boolean literals
                if value:
                    self.builder.branch(true_block)
                else:
                    self.builder.branch(false_block)
                    
            case BinaryOp(left, '&&', right):
                # For AND, create a mid block to evaluate the right operand only if left is true
                mid_label = self.fresh_label()
                mid_block = self.current_function.append_basic_block(mid_label)
                
                # Generate left operand, branch to mid_block if true, false_block if false
                self.condGen(ctx, left, mid_label, false_label)
                
                # Generate right operand in mid_block
                self.builder.position_at_end(mid_block)
                self.condGen(ctx, right, true_label, false_label)
            
            case BinaryOp(left, '||', right):
                # For OR, create a mid block to evaluate the right operand only if left is false
                mid_label = self.fresh_label()
                mid_block = self.current_function.append_basic_block(mid_label)
                
                # Generate left operand, branch to true_block if true, mid_block if false
                self.condGen(ctx, left, true_label, mid_label)
                
                # Generate right operand in mid_block
                self.builder.position_at_end(mid_block)
                self.condGen(ctx, right, true_label, false_label)
            
            case LogicalNegation(operand):
                # For NOT, simply swap the true and false branches
                self.condGen(ctx, operand, false_label, true_label)

            case BinaryOp(left, op, right) if op in ['==', '!=', '<', '<=', '>', '>=']:
                # For comparison operators, evaluate both sides and branch based on result
                val1 = self.expGen(ctx, left)
                val2 = self.expGen(ctx, right)                
                cond = self.builder.icmp_signed(op, val1, val2)
                self.builder.cbranch(cond, true_block, false_block)
            
            case _:
                # For other expressions, evaluate and branch based on result
                val = self.expGen(ctx, exp)
                self.builder.cbranch(val, true_block, false_block)

    def get_llvm_type(self, aguda_type: Type) -> ir.Type:
        """Convert AGUDA type to LLVM type."""
        match aguda_type:
            case BaseType('Int'):
                return ir.IntType(32)
            case BaseType("Bool"):
                return ir.IntType(1)
            case BaseType("Unit"):
                return ir.IntType(32)
            case FunctionType():
                param_types = [self.get_llvm_type(t) for t in aguda_type.param_types]
                return_type = self.get_llvm_type(aguda_type.return_type)
                return ir.FunctionType(return_type, param_types)
            case _:
                raise CodeGenerationError(f"Unsupported type: {aguda_type}", aguda_type.lineno, aguda_type.column)

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