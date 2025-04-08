from abc import ABC
from dataclasses import dataclass
from typing import List, Optional, Union

# Base class for all AST nodes
class ASTNode(ABC):
    pass

# Base class for all expressions
class Expression(ASTNode):
    pass

# Variable node
@dataclass
class Variable(Expression):
    name: str

# Literal nodes
@dataclass
class IntLiteral(Expression):
    value: int

@dataclass
class BoolLiteral(Expression):
    value: bool

@dataclass
class NullLiteral(Expression):
    pass

@dataclass
class StringLiteral(Expression):
    value: str

# Binary operator node
@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression

# Unary operator node
@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression

# Function call node
@dataclass
class FunctionCall(Expression):
    name: str
    arguments: List[Expression]

# Array access node
@dataclass
class ArrayAccess(Expression):
    array: Expression
    index: Expression

# Assignment node
@dataclass
class Assignment(ASTNode):
    lhs: Union[Variable, ArrayAccess]
    rhs: Expression

# Variable declaration node
@dataclass
class VariableDeclaration(ASTNode):
    name: str
    type: str
    value: Expression

# Function declaration node
@dataclass
class FunctionDeclaration(ASTNode):
    name: str
    parameters: List[str]
    return_type: str
    body: Expression

# Conditional node
@dataclass
class Conditional(Expression):
    condition: Expression
    then_branch: Expression
    else_branch: Expression

# While loop node
@dataclass
class WhileLoop(Expression):
    condition: Expression
    body: Expression

# Array creation node
@dataclass
class ArrayCreation(Expression):
    type: str
    size: Expression
    initial_value: Expression

# Sequence of expressions node
@dataclass
class Sequence(Expression):
    expressions: List[Expression]

# Program node
@dataclass
class Program(ASTNode):
    declarations: List[ASTNode]

#TODO Cenas talvez a mais
@dataclass
class FunctionType(ASTNode):
    parameter_types: List[str]
    return_type: str
