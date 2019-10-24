"""Module for keeping variable specs.

Classes
-------
SymbolTable
    Class to keep variable specs in a symbol table.
"""


from cerebro.exceptions import InternalException


class SymbolTable:
    """Class to keep variable specs in a symbol table.

    Attributes
    ----------
    scopes : list of dict of str: cerebro.Compiler.Variable
        Stores variables' specs

    Methods
    -------
    enter_scope()
        Create new scope.
    define(name, spec)
        Set variable's spec.
    exit_scope()
        Exits a scope.
    get(name)
        Returns a variable's spec.
    """
    def __init__(self):
        self.scopes = []

    def enter_scope(self):
        """Create new scope."""
        self.scopes.append({})

    def define(self, name, spec):
        """Set variable's spec.

        Parameters
        ----------
        name : str
            Shows variable's name.
        spec : cerebro.Compiler.Variable
            Indicates properties of a variable.

        Raises
        ------
        InternalException : If the variable has not been defined in the scope.
        """
        try:
            self.scopes[-1][name] = spec
        except IndexError:
            raise InternalException("no scope to define the variable in")

    def exit_scope(self):
        """Exits a scope.

        Raises
        ------
        InternalException : If scope list is empty.
        """
        try:
            self.scopes.pop()
        except IndexError:
            raise InternalException("no scope to exit from")

    def get(self, name):
        """Returns a variable's spec and None if the variable does not exist.

        Parameters
        ----------
        name : str
            Shows a variable's name
        """
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]

        return None
