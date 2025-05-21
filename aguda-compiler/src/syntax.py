from abc import ABC
from dataclasses import dataclass
from typing import List, Union

class ASTNode(ABC):
    lineno: int = None
    column: int = None

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
    type: Type

    def __str__(self):
        return f'{self.type}' + '[]'
    
    def __eq__(self, other):
        if isinstance(other, ArrayType):
            return self.type == other.type
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
class Sequence(Exp):
    first: Exp
    rest: Exp

    def __str__(self):
        #TODO indent no rest?
        return f'{self.first} ;\n{self.rest}'

@dataclass
class BinaryOp(Exp):
    left: Exp
    operator: str
    right: Exp

    def __str__(self):
        return f'{self.left} {self.operator} {self.right}'


@dataclass
class LogicalNegation(Exp):
    operand: Exp

    def __str__(self):
        return f'!{self.operand}'


@dataclass
class FunctionCall(Exp):
    id: Var
    arguments: List[Exp]

    def __str__(self):
        args = ', '.join(str(a) for a in self.arguments)
        return f'{self.id}({args})'


@dataclass
class ArrayAccess(Exp):
    array: Exp
    index: Exp

    def __str__(self):
        return f'{self.array}[{self.index}]'

@dataclass
class Group(Exp):
    exp: Exp

    def __str__(self):
        return f'(\n{indent(self.exp)}\n)'

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
        return f'while {self.condition} do {self.body}'


@dataclass
class ArrayCreation(Exp):
    type: Type
    size: Exp
    initial_value: Exp

    def __str__(self):
        return f'new {self.type} [{self.size} | {self.initial_value}]'

@dataclass
class TopLevelVariableDeclaration(Declaration):
    id: Var
    type: Type
    value: Exp

    def __str__(self):
        return f'let {self.id} : {self.type} =\n{indent(self.value)}'

@dataclass
class VariableDeclaration(Declaration):
    id: Var
    type: Type
    value: Exp

    def __str__(self):
        return f'let {self.id} : {self.type} = {self.value}'

@dataclass
class FunctionDeclaration(Declaration):
    id: Var
    parameters: List[Var]
    type: FunctionType
    body: Exp

    def __str__(self):
        params = ', '.join(str(p) for p in self.parameters)
        return (f'let {self.id}({params}) : {self.type} =\n'
                f'{indent(self.body)}')

@dataclass
class Program(ASTNode):
    declarations: List[Declaration]

    def __str__(self):
        return '\n'.join(str(decl) for decl in self.declarations)