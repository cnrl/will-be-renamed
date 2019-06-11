from abc import ABC, abstractmethod

from cerebro.exceptions import IllegalArgumentException
from cerebro.parser.parser import parse_variables
from cerebro.globals import SYNAPSE_INTERNAL_VARIABLES, NEURON_INTERNAL_VARIABLES
from cerebro.enums import VariableContext


class Variables(ABC):

    @abstractmethod
    def __init__(self, definitions):
        self.definitions = definitions

        self._check_args()

    def _check_args(self):
        if not isinstance(self.definitions, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".definitions must be a string")

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tdefinitions:" + self.definitions + ")"


class NeuronVariables(Variables):
    # TODO: check if all variables are not in globals.FORBIDDEN_POP_VAR_NAMES

    def __init__(self, definitions):
        super(NeuronVariables, self).__init__(definitions)

        self.vars = parse_variables(definitions, VariableContext.NEURON)
        self.vars.update(NEURON_INTERNAL_VARIABLES)


class SynapseVariables(Variables):
    # TODO: check if all variables are not in globals.FORBIDDEN_PROJ_VAR_NAMES

    def __init__(self, definitions):
        super(SynapseVariables, self).__init__(definitions)

        self.vars = parse_variables(definitions, VariableContext.SYNAPSE)
        self.vars.update(SYNAPSE_INTERNAL_VARIABLES)
