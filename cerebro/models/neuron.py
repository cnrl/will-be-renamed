from cerebro.enums import EquationType
from cerebro.models.equations import NeuronEquations
from cerebro.models.variables import NeuronVariables


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
        self.variables = NeuronVariables(variables)

        self.equations = NeuronEquations(equations, EquationType.SIMPLE)
        self.spike = NeuronEquations(spike, EquationType.SPIKE) if spike is not None else None
        self.reset = NeuronEquations(reset, EquationType.RESET) if reset is not None else None

    def __repr__(self):
        return self.__class__.__name__ + """(
        Variables:
        """ + str(self.variables) + """
        Equations of the variables:
        """ + str(self.equations) + """
        Spiking condition:
        """ + str(self.spike) + """
        Reset after a spike:
        """ + str(self.reset) + ")"
