from abc import ABC
from dataclasses import dataclass
from typing import List, Union

class ASTNode(ABC):
    pass

class Declaration(ASTNode):
    pass

class Exp(ASTNode):
    pass

class Type(ASTNode):
    pass

def indent(s, level=2):
    return '\n'.join(' ' * level + line for line in str(s).splitlines())

@dataclass
class BaseType(Type):
    name: str

    def __str__(self):
        return self.name
    
    def __eq__(self, other):
        if isinstance(other, BaseType):
            return self.name == other.name
        return False

@dataclass
class ArrayType(Type):
    base_type: Type
    dimensions: int

    def __str__(self):
        return f'{self.base_type}' + '[]' * self.dimensions
    
    def __eq__(self, other):
        if isinstance(other, ArrayType):
            return (self.base_type == other.base_type and
                    self.dimensions == other.dimensions)
        return False


@dataclass
class FunctionType(Type):
    param_types: List[Type]
    return_type: Type

    def __str__(self):
        # TODO talvez não meter () quando apenas um parametro
        params = ', '.join(str(t) for t in self.param_types)
        return f'({params}) -> {self.return_type}'
    
    def __eq__(self, other):
        if isinstance(other, FunctionType):
            return (self.param_types == other.param_types and
                    self.return_type == other.return_type)
        return False

@dataclass
class Var(Exp):
    name: str

    def __str__(self):
        return self.name


@dataclass
class IntLiteral(Exp):
    value: int

    def __str__(self):
        return str(self.value)


@dataclass
class BoolLiteral(Exp):
    value: bool

    def __str__(self):
        return 'true' if self.value else 'false'


@dataclass
class UnitLiteral(Exp):
    def __str__(self):
        return 'unit'

@dataclass
class StringLiteral(Exp):
    value: str

    def __str__(self):
        return f'"{self.value}"'

@dataclass
class BinaryOp(Exp):
    left: Exp
    operator: str
    right: Exp

    def __str__(self):
        if self.operator == ';':
            return f'{self.left} ;\n{self.right}'
        return f'{self.left} {self.operator} {self.right}'


@dataclass
class LogicalNegation(Exp):
    operand: Exp

    def __str__(self):
        return f'!{self.operand}'


@dataclass
class FunctionCall(Exp):
    name: Var
    arguments: List[Exp]

    def __str__(self):
        args = ', '.join(str(a) for a in self.arguments)
        return f'{self.name}({args})'


@dataclass
class ArrayAccess(Exp):
    array: Exp
    index: Exp

    def __str__(self):
        return f'{self.array}[{self.index}]'


@dataclass
class Assignment(ASTNode):
    lhs: Union[Var, ArrayAccess]
    exp: Exp

    def __str__(self):
        return f'set {self.lhs} = {self.exp}'


@dataclass
class Conditional(Exp):
    condition: Exp
    then_branch: Exp
    else_branch: Exp

    def __str__(self):
        return (f'if {self.condition} then\n'
                f'{indent(self.then_branch)}\n'
                f'else\n'
                f'{indent(self.else_branch)}')


@dataclass
class WhileLoop(Exp):
    condition: Exp
    body: Exp

    def __str__(self):
        return f'while {self.condition} do\n{indent(self.body)}'


@dataclass
class ArrayCreation(Exp):
    type: Type
    size: Exp
    initial_value: Exp

    def __str__(self):
        return f'new {self.type} [{self.size} | {self.initial_value}]'


@dataclass
class VariableDeclaration(Declaration):
    name: Var
    type: Type
    value: Exp

    def __str__(self):
        return f'let {self.name} : {self.type} =\n{indent(self.value)}'

@dataclass
class FunctionDeclaration(Declaration):
    name: Var
    parameters: List[Var]
    type: FunctionType
    body: Exp

    def __str__(self):
        params = ', '.join(str(p) for p in self.parameters)
        return (f'let {self.name}({params}) : {self.type} =\n'
                f'{indent(self.body)}')

@dataclass
class Program(ASTNode):
    declarations: List[Declaration]

    def __str__(self):
        return '\n'.join(str(decl) for decl in self.declarations)