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
        self.module.triple = "x86_64-unknown-linux-gnu"
        self.builder : Optional[ir.IRBuilder] = None
        self.current_function : Optional[ir.Function] = None
        self.label_counter = 0

    def generate(self, program: Program) -> str:
        """Generate LLVM IR code from the AST."""
        ctx = SymbolTable[Tuple[ir.Value, Type]]() # SymbolTable with a tuple of LLVM Value and AGUDA Type
        self.add_builtins(ctx)	
        self.first_pass(ctx, program)
        self.second_pass(ctx, program)
        return str(self.module)
    
    def add_builtins(self, ctx: SymbolTable[Tuple[ir.Value, Type]]):
        """
        Adds built-in functions to the module with their implementations.
        """
        printf_type = ir.FunctionType(ir.IntType(32), [ir.IntType(8).as_pointer()], var_arg=True)
        printf_func = ir.Function(self.module, printf_type, "printf")
        printf_func.linkage = "external"

        self._create_power_function()

    def first_pass(self, ctx: SymbolTable[Tuple[ir.Value, Type]], program: Program):
        """
        First pass over the AST to collect function types and global variables.
        """
        for decl in program.declarations:
            match decl:
                case FunctionDeclaration(id, _, type, _):
                    param_types = [self.get_llvm_type(t) for t in type.param_types]
                    return_type = self.get_llvm_type(type.return_type)
                    func_type = ir.FunctionType(return_type, param_types)
                    func = ir.Function(self.module, func_type, id.name)
                    ctx.insert(id.name, (func, type))
                case TopLevelVariableDeclaration(id, type, value):
                    if isinstance(value, (IntLiteral, BoolLiteral, UnitLiteral)):
                        var_type = self.get_llvm_type(type)
                        var = ir.GlobalVariable(self.module, var_type, id.name)
                        var.initializer, _ = self.expGen(ctx.enter_scope(), value)
                        ctx.insert(id.name, (var, type))
                    else:
                        raise CodeGenerationError(f"Top-level variable declarations must be initialized with literals ({decl.lineno}, {decl.column})")

    def second_pass(self, ctx: SymbolTable[Tuple[ir.Value, Type]], program: Program):
        """
        Second pass over the AST to generate LLVM code.
        """
        for decl in program.declarations:
            if isinstance(decl, FunctionDeclaration):
                self.generate_function(ctx, decl)

    def generate_function(self, ctx: SymbolTable[Tuple[ir.Value, Type]], func_decl: FunctionDeclaration):
        """Generate LLVM code for a function declaration."""
        func, _ = ctx.lookup(func_decl.id.name)
        
        entry_block = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(entry_block)
        self.current_function = func
        
        local_ctx = ctx.enter_scope()
        self._setup_function_parameters(local_ctx, func_decl, func)
        value, _ = self.expGen(local_ctx, func_decl.body)
        
        self.builder.ret(value)

    def expGen(self, ctx: SymbolTable[Tuple[ir.Value, Type]], exp: Exp) -> Tuple[ir.Value, Type]:
        """
        Generate LLVM code for an expression.
        Returns the LLVM value containing the result and the AGUDA type of the expression.
        """
        match exp:
            case IntLiteral(value):
                return ir.Constant(ir.IntType(32), value), BaseType("Int")
            case BoolLiteral(value):
                return ir.Constant(ir.IntType(1), 1 if value else 0), BaseType("Bool")
            case UnitLiteral():
                return ir.Constant(ir.IntType(1), 0), BaseType("Unit")
            case Var(name):
                var_value, var_aguda_type = ctx.lookup(name)
                return self.builder.load(var_value), var_aguda_type
            case VariableDeclaration(id, type, value):
                # Allocate space for the variable
                var_llvm_type = self.get_llvm_type(type)
                var_ptr = self.builder.alloca(var_llvm_type)
                
                # Store the value
                val, var_aguda_type = self.expGen(ctx.enter_scope(),value)
                self.builder.store(val, var_ptr)
                ctx.insert(id.name, (var_ptr, var_aguda_type))

                return self.expGen(ctx, UnitLiteral())
            
            case BinaryOp(left, op, right):
                # Handle short-circuit boolean operations
                if op in ['&&', '||']:
                    return self.boolGen(ctx, exp)
                
                # For other binary operators, evaluate both sides
                val1, _ = self.expGen(ctx, left)
                val2, _ = self.expGen(ctx, right)

                match op:
                    case '+':
                        return self.builder.add(val1, val2), BaseType("Int")
                    case '-':
                        return self.builder.sub(val1, val2), BaseType("Int")
                    case '*':
                        return self.builder.mul(val1, val2), BaseType("Int")
                    case '/':
                        return self.builder.sdiv(val1, val2), BaseType("Int")
                    case '%':
                        return self.builder.srem(val1, val2), BaseType("Int")
                    case '^':
                        power_func = self.module.get_global('_power')
                        return self.builder.call(power_func, [val1, val2]), BaseType("Int")
                    case '==' | '!=' | '<' | '<=' | '>' | '>=':
                        return self.builder.icmp_signed(op, val1, val2), BaseType("Bool")
                    case _:
                        raise CodeGenerationError(f"Unsupported binary operator: {op} ({exp.lineno}, {exp.column})")

            case LogicalNegation(operand):
                operand_val, _ = self.expGen(ctx, operand)
                return self.builder.not_(operand_val), BaseType("Bool")

            case FunctionCall(id, arguments):
                # Special handling for print function
                if id.name == "print":
                    return self.callPrint(ctx, arguments[0])
                
                # Regular function calls
                arg_values = [val for val, _ in [self.expGen(ctx, arg) for arg in arguments]]
                func, func_aguda_type = ctx.lookup(id.name)
                return self.builder.call(func, arg_values), func_aguda_type.return_type
            
            case Conditional(condition, then_branch, else_branch):
                then_label, else_label, end_label = self.fresh_cond_labels()
                then_block = self.current_function.append_basic_block(then_label)
                else_block = self.current_function.append_basic_block(else_label)
                end_block = self.current_function.append_basic_block(end_label)
                
                # Generate condition and branch
                cond_val, _ = self.expGen(ctx, condition)
                self.builder.cbranch(cond_val, then_block, else_block)
                
                # Generate then branch
                self.builder.position_at_end(then_block)
                then_val, then_aguda_type = self.expGen(ctx.enter_scope(), then_branch)
                then_block_end = self.builder.block
                self.builder.branch(end_block)
                
                # Generate else branch
                self.builder.position_at_end(else_block)
                else_val, _ = self.expGen(ctx.enter_scope(), else_branch)
                else_block_end = self.builder.block
                self.builder.branch(end_block)

                # Create phi node for result
                self.builder.position_at_end(end_block)
                phi = self.builder.phi(then_val.type)
                phi.add_incoming(then_val, then_block_end)
                phi.add_incoming(else_val, else_block_end)
                
                return phi, then_aguda_type
            
            case WhileLoop(condition, body):
                cond_label, body_label, end_label = self.fresh_while_labels()
                cond_block = self.current_function.append_basic_block(cond_label)
                body_block = self.current_function.append_basic_block(body_label)
                end_block = self.current_function.append_basic_block(end_label)
                
                # Branch to condition block
                self.builder.branch(cond_block)
                
                # Generate condition
                self.builder.position_at_end(cond_block)
                cond_val, _ = self.expGen(ctx, condition)
                self.builder.cbranch(cond_val, body_block, end_block)
                
                # Generate body
                self.builder.position_at_end(body_block)
                self.expGen(ctx.enter_scope(), body)
                self.builder.branch(cond_block)
                
                self.builder.position_at_end(end_block)
                return self.expGen(ctx, UnitLiteral())
            
            case Sequence(first, rest):
                self.expGen(ctx, first)
                return self.expGen(ctx, rest)
            
            case Assignment(lhs, exp):
                val, _ = self.expGen(ctx, exp)
                if isinstance(lhs, Var):
                    var_ptr, _ = ctx.lookup(lhs.name)
                    self.builder.store(val, var_ptr)
                else:
                    raise CodeGenerationError(f"Array assignments not supported ({lhs.lineno}, {lhs.column})")
                return self.expGen(ctx, UnitLiteral())
            
            case Group(exp):
                return self.expGen(ctx.enter_scope(), exp)
            
            case _:
                raise CodeGenerationError(f"Not implemented: Generating code for ({exp.lineno}, {exp.column}) expression '{exp}'")
        
    def boolGen(self, ctx: SymbolTable[Tuple[ir.Value, Type]], exp: Exp) -> Tuple[ir.Value, Type]:
        """
        Generate LLVM code for a boolean expression.
        Returns the LLVM value containing the result and the AGUDA type of the expression.
        """
        result_ptr = self.builder.alloca(ir.IntType(1))
        
        fresh_num = self.fresh()
        end_block = self.current_function.append_basic_block(f"bool_{fresh_num}_end")
        
        match exp:
            case BinaryOp(left, '&&', right):
                eval_right_block = self.current_function.append_basic_block(f"bool_{fresh_num}_right")

                # Store false result for the case when left is false
                self.builder.store(ir.Constant(ir.IntType(1), 0), result_ptr)
                
                # Evaluate left operand
                left_val, _ = self.expGen(ctx, left)
                self.builder.cbranch(left_val, eval_right_block, end_block)
                
                # Evaluate right operand only if left was true
                self.builder.position_at_end(eval_right_block)
                right_val, _ = self.expGen(ctx, right)
                self.builder.store(right_val, result_ptr)
                self.builder.branch(end_block)
                
            case BinaryOp(left, '||', right):
                eval_right_block = self.current_function.append_basic_block(f"bool_{fresh_num}_right")

                # Store true result for the case when left is true
                self.builder.store(ir.Constant(ir.IntType(1), 1), result_ptr)
                
                # Evaluate left operand
                left_val, _ = self.expGen(ctx, left)
                self.builder.cbranch(left_val, end_block, eval_right_block)
                
                # Evaluate right operand only if left was false
                self.builder.position_at_end(eval_right_block)
                right_val, _ = self.expGen(ctx, right)
                self.builder.store(right_val, result_ptr)
                self.builder.branch(end_block)
                
            case _:
                raise CodeGenerationError(f"Unexpected expression in boolGen: {exp}")
        
        self.builder.position_at_end(end_block)
        return self.builder.load(result_ptr), BaseType("Bool")
    
    def callPrint(self, ctx: SymbolTable[Tuple[ir.Value, Type]], exp: Exp) -> Tuple[ir.Value, Type]:
        """
        Generate LLVM code for a print function call.
        Returns the LLVM value containing the result and the AGUDA type of the expression.
        """
        printf_func = self.module.get_global('printf')
        arg_val, arg_type = self.expGen(ctx, exp)
        match arg_type:
            case BaseType("Int"):
                str_ptr = self._create_global_string("%d\0")
                self.builder.call(printf_func, [str_ptr, arg_val])
                
            case BaseType("Bool"):
                true_ptr = self._create_global_string("true\0")
                false_ptr = self._create_global_string("false\0")
                selected_ptr = self.builder.select(arg_val, true_ptr, false_ptr)
                self.builder.call(printf_func, [selected_ptr])
                
            case BaseType("Unit"):
                str_ptr = self._create_global_string("unit\0")
                self.builder.call(printf_func, [str_ptr])
                
            case _:
                raise CodeGenerationError(f"Unsupported type for print: {arg_type}")
        
        # Bypass printf return type
        return self.expGen(ctx, UnitLiteral())

    def get_llvm_type(self, aguda_type: Type) -> ir.Type:
        """Convert AGUDA type to LLVM type."""
        match aguda_type:
            case BaseType('Int'):
                return ir.IntType(32)
            case BaseType("Bool"):
                return ir.IntType(1)
            case BaseType("Unit"):
                return ir.IntType(1)
            case _:
                raise CodeGenerationError(f"Not implemented: Generating code for ({aguda_type.lineno}, {aguda_type.column}) type '{aguda_type}'")

    def fresh(self) -> int:
        """Generate a fresh number."""
        num = self.label_counter
        self.label_counter += 1
        return num

    def fresh_cond_labels(self) -> Tuple[str, str, str]:
        """Generate a set of related labels for a conditional expression."""
        cond_num = self.fresh()
        then_label = f"cond_{cond_num}_then"
        else_label = f"cond_{cond_num}_else"
        end_label = f"cond_{cond_num}_end"
        return then_label, else_label, end_label

    def fresh_while_labels(self) -> Tuple[str, str, str]:
        """Generate a set of related labels for a while loop."""
        loop_num = self.fresh()
        cond_label = f"while_{loop_num}_cond"
        body_label = f"while_{loop_num}_body"
        end_label = f"while_{loop_num}_end"
        return cond_label, body_label, end_label
    
    def _setup_function_parameters(self, ctx: SymbolTable[Tuple[ir.Value, Type]], func_decl: FunctionDeclaration, func: ir.Function):
        """
        Setup function parameters. Raises an error if a parameter is a function type.
        """
        for param_var, param_type, arg in zip(func_decl.parameters, func_decl.type.param_types, func.args):          
            param_ptr = self.builder.alloca(self.get_llvm_type(param_type))
            self.builder.store(arg, param_ptr)
            ctx.insert(param_var.name, (param_ptr, param_type))
    
    def _create_global_string(self, string: str) -> ir.Value:
        """
        Create a global variable for a string literal.
        Returns the pointer to the string.
        """
        string_const = ir.Constant(ir.ArrayType(ir.IntType(8), len(string)), bytearray(string.encode("utf8")))
        global_var = ir.GlobalVariable(self.module, string_const.type, f"str_{self.fresh()}")
        global_var.linkage = 'internal'
        global_var.global_constant = True
        global_var.initializer = string_const
        prt = self.builder.gep(global_var, [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), 0)])
        return prt
        
    def _create_power_function(self):
        """
        Power function implementation based on the LLVM IR code
        generated by the compiler from tcomp000_power-iterative\power-iterative.agu
        """
        power_type = ir.FunctionType(ir.IntType(32), [ir.IntType(32), ir.IntType(32)])
        power_func = ir.Function(self.module, power_type, "_power")
        
        entry_block = power_func.append_basic_block('entry')
        while_cond_block = power_func.append_basic_block('while_0_cond')
        while_body_block = power_func.append_basic_block('while_0_body')
        while_end_block = power_func.append_basic_block('while_0_end')
        
        builder = ir.IRBuilder(entry_block)
        
        # Get function arguments
        base_arg = power_func.args[0]
        exp_arg = power_func.args[1]
        
        # Allocate and store parameters
        base_ptr = builder.alloca(ir.IntType(32))
        builder.store(base_arg, base_ptr)
        
        exp_ptr = builder.alloca(ir.IntType(32))
        builder.store(exp_arg, exp_ptr)
        
        # Allocate and initialize result to 1
        result_ptr = builder.alloca(ir.IntType(32))
        builder.store(ir.Constant(ir.IntType(32), 1), result_ptr)
        
        # Branch to while condition
        builder.branch(while_cond_block)
        
        # While condition block
        builder.position_at_end(while_cond_block)
        exp_val = builder.load(exp_ptr)
        cond = builder.icmp_signed('>', exp_val, ir.Constant(ir.IntType(32), 0))
        builder.cbranch(cond, while_body_block, while_end_block)
        
        # While body block
        builder.position_at_end(while_body_block)
        result_val = builder.load(result_ptr)
        base_val = builder.load(base_ptr)
        new_result = builder.mul(result_val, base_val)
        builder.store(new_result, result_ptr)
        
        exp_val = builder.load(exp_ptr)
        new_exp = builder.sub(exp_val, ir.Constant(ir.IntType(32), 1))
        builder.store(new_exp, exp_ptr)
        builder.branch(while_cond_block)
        
        # While end block
        builder.position_at_end(while_end_block)
        final_result = builder.load(result_ptr)
        builder.ret(final_result)
        
        return power_func