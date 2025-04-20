from typing import Dict
from src.syntax import *

class SymbolTable:
    def __init__(self):
        self.table : Dict[str, Type] = {}
        self.parent : SymbolTable = None

    def insert(self, name: str, symbol_type: Type) -> None:
        # TODO Add this check to disallow shadowing
        # if name in self.table:
        #     raise NameError(f"Symbol '{name}' is already defined")
        self.table[name] = symbol_type

    def lookup(self, name: str) -> Type:
        if name in self.table:
            return self.table[name]
        if self.parent:
            return self.parent.lookup(name)
        return None

    def enter_scope(self) -> 'SymbolTable':
        child = SymbolTable()
        child.parent = self
        return child

    def exit_scope(self) -> 'SymbolTable':
        if self.parent is None:
            raise RuntimeError("Cannot exit global scope")
        return self.parent