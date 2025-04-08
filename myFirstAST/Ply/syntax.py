"""
an Abstract syntax tree for the Simple programming language,
using Abstract Base Classes and dataclass

Usage:
  $ pip3 install ply
  $ python3 main.py < ../example.simple


Author: Técnicas de Compilação
        Mestrado em Engenharia Informática
        Faculdade de Ciências
        Universidade de Lisboa
        2024/2025
        Alcides Fonseca
        Vasco T. Vasconcelos
"""

from abc import ABC # abstract base classes
from dataclasses import dataclass

class Exp(ABC):
    pass

@dataclass
class Var(Exp):
    name: str
    
@dataclass
class Int(Exp):
    value: int

@dataclass
class Let(Exp):
    variable: str
    header: Exp
    body: Exp

@dataclass
class Op(Exp):
    left: Exp
    op: str
    right: Exp
