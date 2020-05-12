class Symbol(object):
    def __init__(self, name, sym_type):
        self.name = name
        self.sym_type = sym_type


class VariableSymbol(Symbol):

    def __init__(self, name, sym_type):
        super().__init__(name, sym_type)


class SymbolTable(object):

    def __init__(self, parent: str, name: str):
        self.scopes = []
        self.symbols = {}
        self.parent = parent
        self.name = name

    def put(self, name: str, symbol: Symbol):
        self.symbols[name] = symbol

    def get(self, name: str):
        return self.symbols[name]

    def getParentScope(self):
        return self.parent

    def pushScope(self, name: str):
        return self.scopes.append(name)

    def popScope(self):
        return self.scopes.pop()
