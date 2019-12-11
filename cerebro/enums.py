"""
Widely used enumeration objects
"""

from enum import Enum, unique


@unique
class EquationType(Enum):
    """
    All possible types for a context equation.
    """

    SIMPLE = "simple"
    RESET = "reset"
    SPIKE = "spike"


class VariableContext(Enum):
    """
    Possible contexts for a variable.
    """

    NEURON = "neuron"
    SYNAPSE = "synapse"
    NETWORK = "network"


class EquationContext(Enum):
    """
    Possible contexts for a equation.
    """

    NEURON = "neuron"
    SYNAPSE = "synapse"


class VariableType(Enum):
    """
    Possible data types constraints for a context variable.
    """

    DOUBLE = 'double'
    INTEGER = 'integer'
    FLOAT = 'float'


class VariableVariability(Enum):
    """
    Possible variability constraints for a context variable.
    """

    CONSTANT = 'constant'
    VARIABLE = 'variable'


class VariableScope(Enum):
    """
    Possible scope constraints for a context variable.
    """

    LOCAL = 'local'
    SHARED = 'shared'
