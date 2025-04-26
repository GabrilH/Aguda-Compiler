from typing import Dict
from src.syntax import *

class SymbolTable:
    def __init__(self):
        self.table : Dict[str, Type] = {}
        self.parent : SymbolTable = None

    def insert(self, name: str, symbol_type: Type) -> None:
        self.table[name] = symbol_type

    def lookup(self, name: str) -> Type:
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

    def enter_scope(self) -> 'SymbolTable':
        child = SymbolTable()
        child.parent = self
        return child