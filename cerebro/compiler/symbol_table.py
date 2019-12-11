"""Module for keeping variable specs.

*Classes*:

* **SymbolTable**:
    Class to keep variable specs in a symbol table.
"""


from cerebro.exceptions import InternalException


class SymbolTable:
    """
    Class to keep variable specs in a symbol table.
    """
    def __init__(self):
        self.scopes = []

    def enter_scope(self):
        """Create new scope."""
        self.scopes.append({})

    def define(self, name, spec):
        """Set variable's spec.

        :param name: Shows variable's name.
        :param spec: Indicates properties of a variable.

        :type name: str
        :type spec: cerebro.Compiler.Variable

        :raises InternalException: If the variable has not been defined in the scope.
        """
        try:
            self.scopes[-1][name] = spec
        except IndexError:
            raise InternalException("no scope to define the variable in")

    def exit_scope(self):
        """Exits a scope.

        :raises InternalException: If scope list is empty.
        """
        try:
            self.scopes.pop()
        except IndexError:
            raise InternalException("no scope to exit from")

    def get(self, name):
        """Returns a variable's spec and None if the variable does not exist.

        :param name: Shows a variable's name

        :type name: str

        :returns: variable's spec if variable exists

        :rtype: cerebro.compiler.compiler.Compiler.Variable or None
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]

        return None
