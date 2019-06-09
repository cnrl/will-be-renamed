from enum import Enum, unique


@unique
class EquationType(Enum):
    SIMPLE = "simple"
    RESET = "reset"
    SPIKE = "spike"


class VariableContext(Enum):
    NEURON = "neuron"
    SYNAPSE = "synapse"


class EquationContext(Enum):
    NEURON = "neuron"
    SYNAPSE = "synapse"
