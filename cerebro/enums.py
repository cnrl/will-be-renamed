"""Widely used enumeration objects

Classes
----------
EquationType(Enum)
    All possible types for a context equation.
    Members:
        SIMPLE :
            Indicates the equation is defined for normal functionality of the context.
        RESET :
            Indicates the equation is defined for reset functionality of a neuron.
        SPIKE :
            Indicates the equation is spike condition of a neuron.

VariableContext(Enum)
    Possible contexts for a variable.
    Members:
        NEURON :
            Indicates the context of the variable is a neuron.
        SYNAPSE :
            Indicates the context of the variable is a synapse.
        NETWORK:
            Indicates the context of the variable is a network.

EquationContext(Enum)
    Possible contexts for a equation.
    Members:
        NEURON :
            Indicates the context of the equation is a neuron.
        SYNAPSE :
            Indicates the context of the equation is a synapse.

VariableType(Enum)
    Possible data types constraints for a context variable.
    Members:
        DOUBLE :
            Indicates double data type for a variable.
        INTEGER :
            Indicates int data type for a variable.
        FLOAT:
            Indicates float data type for a variable.

VariableVariability(Enum)
    Possible variability constraints for a context variable.
    Members:
        CONSTANT :
            Indicates constant constraint for a context variable.
        VARIABLE :
            Indicates no constraint on variability of a context variable.

VariableScope(Enum)
    Possible scope constraints for a context variable.
    Members:
        LOCAL :
            Indicates local constraint for a context variable.
        SHARED :
            Indicates that the context variable is shared in the parent context.
"""

from enum import Enum, unique


@unique
class EquationType(Enum):
    SIMPLE = "simple"
    RESET = "reset"
    SPIKE = "spike"


class VariableContext(Enum):
    NEURON = "neuron"
    SYNAPSE = "synapse"
    NETWORK = "network"


class EquationContext(Enum):
    NEURON = "neuron"
    SYNAPSE = "synapse"


class VariableType(Enum):
    DOUBLE = 'double'
    INTEGER = 'integer'
    FLOAT = 'float'


class VariableVariability(Enum):
    CONSTANT = 'constant'
    VARIABLE = 'variable'


class VariableScope(Enum):
    LOCAL = 'local'
    SHARED = 'shared'
