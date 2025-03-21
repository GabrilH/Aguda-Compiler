__copyright__ = """
    Técnicas de Compilação
    Mestrado em Engenharia Informática
    Faculdade de Ciências
    Universidade de Lisboa
    2024/2025"""
__author__ = "Alcides Fonseca"

from abc import ABC # abstract base classes
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

def eval(store:dict[str, int], e:Expr) -> int:
    match e:
        case Variable(v):
            return store[v]
        case Literal(n):
            return v
        case Plus(e1, e2):
            return eval(store, e1) + eval(store, e2)

def interpret(stmts:list[Statement]):
    store:dict[str, int] = {}
    for stmt in stmts:
        match stmt:
            case Assignment(v, e):
                store[v] = eval(store, e)
            case Print(e):
                print(eval(store, e))

def validate_expr(defined_variables:set[str], e:Expr):
    match e:
        case Variable(v):
            if v not in defined_variables:
                raise Exception(f"Variable {v} not defined. Defined variables are {defined_variables}")
        case Literal(_): True
        case Plus(e1, e2):
            validate_expr(defined_variables, e1)
            validate_expr(defined_variables, e2)

def validate(stmts):
    defined_variables = set()
    for stmt in stmts:
        match stmt:
            case Assignment(v, e):
                validate_expr(defined_variables, e)
                defined_variables.add(v)
            case Print(e):
                validate_expr(defined_variables, e)

def wrapper(s:str) -> str:
    return f"""#include <stdio.h>\nint main() {{\n{s}\n  return 0;\n}}\n"""

def compile_expr(e:Expr) -> str:
    match e:
        case Variable(v):
            return v
        case Literal(n):
            return str(n)
        case Plus(Literal(n1), Literal(n2)):
            return f"  {n1 + n2}"
        case Plus(e1, e2):
            return f"  {compile_expr(e1)} + {compile_expr(e2)}"

def compile_stmt(stmt: Statement) -> str:
    match stmt:
        case Assignment(v, e):
            return f"  int {v} = {compile_expr(e)};"
        case Print(e):
            return f"""  printf("%d\\n", {compile_expr(e)});"""

def compile_stmts(stmts:list[Statement]) -> str:
    return "\n".join(compile_stmt(s) for s in stmts)

def compile(stmts:list[Statement]):
    compiled_stmts = compile_stmts(stmts)
    code = wrapper(compiled_stmts)
    with open("middle.c", "w") as f:
        f.write(code)
    os.system("gcc -o executable middle.c")

def main(fname:str):
    contents = open(fname).read()
    ast = parse(contents)
    validate(ast)
    # interpret(ast)
    compile(ast)

if __name__ == "__main__":
    filename = sys.argv[1]    
    main(filename)