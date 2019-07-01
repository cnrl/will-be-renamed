from cerebro.exceptions import InternalException


class SymbolTable:
    def __init__(self):
        self.scopes = []

    def enter_scope(self):
        self.scopes.append({})

    def define(self, name, spec):
        try:
            self.scopes[-1][name] = spec
        except IndexError:
            raise InternalException("no scope to define the variable in")

    def exit_scope(self):
        try:
            self.scopes.pop()
        except IndexError:
            raise InternalException("no scope to exit from")

    def get(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]

        return None
