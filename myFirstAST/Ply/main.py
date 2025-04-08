"""
an Abstract syntax tree for the Simple programming language,
using Abstract Base Classes and dataclass

Usage:
  $ python3 main.py < ../example.simple


Author: Técnicas de Compilação
        Mestrado em Engenharia Informática
        Faculdade de Ciências
        Universidade de Lisboa
        2024/2025
        Alcides Fonseca
        Vasco T. Vasconcelos
"""

import syntax as s

store: dict[str, int] = {}

def eval(e: s.Exp) -> int:
    match e:
        case s.Var(v):
            return store[v]
        case s.Int(n):
            return n
        case s.Op(e1, op, e2):
            match op:
                case '+':
                    return eval(e1) + eval(e2)
                case '-':
                    return eval(e1) - eval(e2)
                case '/':
                    return eval(e1) // eval(e2)
                case '*':
                    return eval(e1) * eval(e2)
        case s.Let(var, e1, e2):
            store[var] = eval(e1)
            return eval(e2)

if __name__ == '__main__':
    import sys
    import parser as p
    ast = p.parser.parse(sys.stdin.read())
    print(ast)
    print(eval(ast))
