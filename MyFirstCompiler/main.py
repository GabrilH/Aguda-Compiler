from abc import ABC
from dataclasses import dataclass
import os
import sys
from typing import Any



class Expr(ABC):
    pass

@dataclass
class Literal(Expr):
    value:int

@dataclass
class Variable(Expr):
    name:str

@dataclass
class Plus(Expr):
    left:Expr
    right:Expr

class Statement(ABC):
    pass

@dataclass
class Assignment(Statement):
    lhs:str
    rhs:Expr

@dataclass
class Print(Statement):
    value:Expr



def parse_expr(s:str) -> Expr:
    if "+" in s:
        p1, p2 = s.split("+")
        left = parse_expr(p1.strip())
        right = parse_expr(p2.strip())
        return Plus(left, right)
    elif s[0].isdigit():
        try:
            v = int(s)
            return Literal(v)
        except:
            raise Exception(f"Could not parse expression {s}")
    else:
        return Variable(s.strip())

def parse(contents:str) -> list[Statement]:
    program:list[Statement] = []
    for line in contents.split("\n"):
        if not line or line[0] == "#":
            continue
        elif line.startswith("print"):
            expr:Expr = parse_expr(line[5:].strip())
            p = Print(expr)
            program.append(p)
        elif "=" in line:
            p1, p2 = line.split("=")

            assign = Assignment(p1.strip(), parse_expr(p2.strip()))
            program.append(assign)
        else:
            raise Exception(f"Line {line} not correct!")
    return program

def eval(execution_frame:dict[str, int], e:Expr) -> int:
    if isinstance(e, Literal):
        return e.value
    elif isinstance(e, Variable):
        return execution_frame[e.name]
    elif isinstance(e, Plus):
        a = eval(execution_frame, e.left)
        b = eval(execution_frame, e.right)
        return a + b
    else:
        raise Exception("Not implemented")

def interpreter(stmts:list[Statement]):
    execution_frame:dict[str, int] = {}
    for stmt in stmts:
        if isinstance(stmt, Assignment):
            v = eval(execution_frame, stmt.rhs)
            execution_frame[stmt.lhs] = v
        elif isinstance(stmt, Print):
            v = eval(execution_frame, stmt.value)
            print(v)
        else:
            pass
    #print("Debug", execution_frame)

def validate_expr(defined_variables:list[str], e:Expr):
    if isinstance(e, Variable):
        if e.name not in defined_variables:
            raise Exception(f"Variable {e.name} not defined. Defined variables are {defined_variables}")
    elif isinstance(e, Plus):
        validate_expr(defined_variables, e.left)
        validate_expr(defined_variables, e.right)

def validate(stmts):
    defined_variables = []
    for stmt in stmts:
        if isinstance(stmt, Assignment):
            validate_expr(defined_variables, stmt.rhs)
            defined_variables.append(stmt.lhs)
        elif isinstance(stmt, Print):
            validate_expr(defined_variables, stmt.value)
        else:
            pass


def wrapper(s:str) -> str:
    return f"""#include <stdio.h>\nint main() {{\n{s}\nreturn 0;}}"""

def compile_expr(e:Expr) -> str:
    if isinstance(e, Literal):
        return str(e.value)
    elif isinstance(e, Variable):
        return e.name
    elif isinstance(e, Plus):
        if isinstance(e.left, Literal) and isinstance(e.right, Literal):
            v = e.left.value + e.right.value
            return f"{v}"

        a = compile_expr(e.left)
        b = compile_expr(e.right)
        return f"{a} + {b}"
    else:
        raise Exception("Not implemented")

def compile_stmt(stmt: Statement) -> str:
    if isinstance(stmt, Assignment):
        v = compile_expr(stmt.rhs)
        return f"int {stmt.lhs} = {v};"
    elif isinstance(stmt, Print):
        v = compile_expr(stmt.value)
        return f"""printf("%d\\n", {v});"""
    else:
        return ""

def compile_stmts(stmts:list[Statement]) -> str:
    return "\n".join(compile_stmt(s) for s in stmts)

def compiler(stmts:list[Statement]):
    compiled_stmts = compile_stmts(stmts)
    codigo = wrapper(compiled_stmts)
    with open("middle.c", "w") as f:
        f.write(codigo)
    os.system("gcc -o executable middle.c")

def main(fname:str):
    contents = open(fname).read()
    ast = parse(contents)
    validate(ast)
    #interpreter(ast)
    compiler(ast)

if __name__ == "__main__":
    filename = sys.argv[1]    
    main(filename)