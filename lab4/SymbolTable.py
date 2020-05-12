from copy import deepcopy
from enum import Enum


class SCOPE(Enum):
    GLOBAL = 1
    LOCAL = 2
    LOOP = 3


class Symbol(object):
    def __init__(self, name, sym_type):
        self.name = name
        self.sym_type = sym_type


class VariableSymbol(Symbol):

    def __init__(self, name, sym_type):
        super().__init__(name, sym_type)


class SymbolTable(object):

    def __init__(self):
        self.current_scope_name = SCOPE.GLOBAL
        self.current_scope = {}
        self.scopes = [self.current_scope]

    def set_scope_name(self, scope: SCOPE):
        prev_scope = self.current_scope_name
        self.current_scope_name = scope
        return prev_scope

    def get_scope_name(self):
        return self.current_scope_name

    def put(self, name: str, symbol: Symbol):
        self.current_scope[name] = symbol

    def get(self, name: str):
        return self.current_scope[name]

    def get_scope(self):
        return self.current_scope

    def push_scope(self):
        self.current_scope = deepcopy(self.current_scope)
        self.scopes.append(self.current_scope)

    def pop_scope(self):
        return self.scopes.pop()
