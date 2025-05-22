from typing import Dict, TypeVar, Generic
from src.syntax import *

T = TypeVar('T')

class SymbolTable(Generic[T]):
    def __init__(self):
        self.table : Dict[str, T] = {}
        self.parent : 'SymbolTable[T]' = None

    def insert(self, name: str, value: T) -> None:
        self.table[name] = value

    def lookup(self, name: str) -> T:
        if name in self.table:
            return self.table[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def contains(self, name: str) -> bool:
        if name in self.table:
            return True
        if self.parent:
            return self.parent.contains(name)
        return False

    def enter_scope(self) -> 'SymbolTable[T]':
        child = SymbolTable()
        child.parent = self
        return child
