from copy import deepcopy
from enum import Enum


class SCOPE(Enum):  # for now we care only if we are inside LOOP or not there
    GLOBAL = 1
    LOCAL = 2
    LOOP = 3


class SymbolTable(object):

    def __init__(self):
        self.current_scope_name = SCOPE.GLOBAL
        self.current_scope = {}  # ID:str -> Variable mapping with scope distinction
        self.scopes = []

    def set_scope_name(self, scope: SCOPE):
        prev_scope = self.current_scope_name
        self.current_scope_name = scope
        return prev_scope

    def get_scope_name(self):
        return self.current_scope_name

    def put(self, name: str, symbol: any):
        self.current_scope[name] = symbol

    def get(self, name: str):
        return self.current_scope[name]

    def get_scope(self):
        return self.current_scope

    def push_scope(self):
        self.scopes.append(self.current_scope)
        self.current_scope = deepcopy(self.current_scope)

    def pop_scope(self):
        self.current_scope = self.scopes.pop()
        return self.current_scope
