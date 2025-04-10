from abc import ABC
from dataclasses import dataclass
from typing import List, Optional, Union

class ASTNode(ABC):
    pass

class Declaration(ASTNode):
    pass

class Exp(ASTNode):
    pass

class Type(ASTNode):
    pass

@dataclass
class BaseType(Type):
    name: str

@dataclass
class ArrayType(Type):
    base_type: Type
    dimensions: int

@dataclass
class FunctionType(Type):
    param_types: List[Type]
    return_type: Type

@dataclass
class FunctionType(ASTNode):
    param_types: List[Type]
    return_type: Type

@dataclass
class Var(Exp):
    name: str

@dataclass
class IntLiteral(Exp):
    value: int

@dataclass
class BoolLiteral(Exp):
    value: bool

@dataclass
class UnitLiteral(Exp):
    pass
# TODO Serão a mesma coisa?
@dataclass
class NullLiteral(Exp):
    pass

@dataclass
class StringLiteral(Exp):
    value: str

@dataclass
class BinaryOp(Exp):
    left: Exp
    operator: str
    right: Exp

@dataclass
class LogicalNegation(Exp):
    operand: Exp

@dataclass
class FunctionCall(Exp):
    name: str
    arguments: List[Exp]

@dataclass
class ArrayAccess(Exp):
    array: Exp
    index: Exp

@dataclass
class Assignment(ASTNode):
    lhs: Union[Var, ArrayAccess]
    exp: Exp

@dataclass
class Conditional(Exp):
    condition: Exp
    then_branch: Exp
    else_branch: Exp

@dataclass
class WhileLoop(Exp):
    condition: Exp
    body: Exp

@dataclass
class ArrayCreation(Exp):
    type: Type
    size: Exp
    initial_value: Exp

@dataclass
class VariableDeclaration(Declaration):
    name: str
    type: Type
    value: Exp

@dataclass
class FunctionDeclaration(Declaration):
    name: str
    parameters: List[str]
    return_type: FunctionType
    body: Exp

@dataclass
class Program(ASTNode):
    declarations: List[Declaration]