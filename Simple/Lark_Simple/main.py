"""
A parser for the Simple programming language

Note: The grammar for the simple language must be refactored to remove ambiguity

Usage:
  $ pip3 install lark-parser
  $ python3 main.py < example.simple


Author: Técnicas de Compilação
        Mestrado em Engenharia Informática
        Faculdade de Ciências
        Universidade de Lisboa
        2024/2025
        Alcides Fonseca
        Vasco T. Vasconcelos
"""

from lark import Lark

simple_grammar = r"""
    ?start : exp

    ?exp: term
        | "let" NAME "=" exp "in" exp
        | array_access "=" exp

    ?term: factor
        | term "+" factor
        | term "-" factor

    ?factor: primary
        | factor "*" primary
        | factor "/" primary

    ?primary: NUMBER
        | "-" primary
        | NAME
        | "(" exp ")"
        | array_access

    ?array_access: "vals" "[" NUMBER "]"

    %import common.CNAME -> NAME
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

parser = Lark(simple_grammar, parser='lalr')

if __name__ == '__main__':
    import sys
    print(parser.parse(sys.stdin.read()))
