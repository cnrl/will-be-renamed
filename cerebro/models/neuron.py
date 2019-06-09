from cerebro.globals import FORBIDDEN_POPULATION_VAR_NAMES
from cerebro.models.variables import NeuronVariables
from cerebro.models.equations import NeuronEquations
from cerebro.parser.parser import check_variable_definition
from cerebro.enums import EquationType


class Neuron:
    """
        Class to define a neuron.
    """

    def __init__(self, variables='', equations='', spike=None, reset=None):
        """
            Parameters:

            > variables: Variables of the neuron and their initial values.
            > equations: Equations of the neuron, defining the temporal evolution of variables.
            > spike: Spike emission condition.
            > reset: Changes to the variables after a spike.
        """
        self.equations = NeuronEquations(equations, EquationType.SIMPLE)
        self.parameters = NeuronVariables(variables, self.equations.equations_list)
        self.spike = NeuronEquations(spike, EquationType.SPIKE) if spike is not None else None
        self.reset = NeuronEquations(reset, EquationType.RESET) if reset is not None else None

        check_variable_definition(self.equations, self.parameters.vars, FORBIDDEN_POPULATION_VAR_NAMES)

    def __repr__(self):
        return self.__class__.__name__ + """(
        Parameters:
        """ + str(self.parameters) + """
        Equations of the variables:
        """ + str(self.equations) + """
        Spiking condition:
        """ + str(self.spike) + """
        Reset after a spike:
        """ + str(self.reset) + ")"
