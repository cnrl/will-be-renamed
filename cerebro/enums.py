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
