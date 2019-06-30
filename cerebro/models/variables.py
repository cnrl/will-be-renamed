from cerebro.exceptions import IllegalArgumentException
from cerebro.parser.parser import variables_lexer
from cerebro.globals import SYNAPSE_INTERNAL_VARIABLES, NEURON_INTERNAL_VARIABLES
from cerebro.enums import VariableContext


class Variable:
    """
    This class is a class for variable definitions.
    """

    @staticmethod
    def from_raw(definitions):
        lexed = variables_lexer(definitions)
        return [Variable(name, spec['init'], spec['constraints']) for name, spec in lexed.items()]

    def __init__(self, name, init, constraints):
        """
        :param name: str
        :param init: str
        :param constraints: list[str]
        """
        self.name = name
        self.init = init
        self.constraints = constraints

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tname:" + self.name + ")"  # TODO improve repr
