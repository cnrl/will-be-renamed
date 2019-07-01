

class SymbolTable:
    def __init__(self):
        self.table = []
        self.contexts = []

    def enter_scope(self, context=None):
        self.table.append({})
        self.contexts.append(context)

    def add_variable(self, name, spec):
        self.table[-1][name] = spec

    def exit_scope(self):
        self.table.pop(-1)
        self.contexts.pop(-1)

    def is_defined(self, name):
        pass

    def get_spec(self):
        pass

    def get_scope(self):
        pass



