from cnrl.models.parameters import NeuronParameters
from cnrl.models.equations import NeuronEquations


class Neuron:
    """
        Class to define a neuron.
    """

    def __init__(self, parameters='', equations='', spike=None, reset=None):
        """
            Parameters:

            > parameters: Parameters of the neuron and their initial values.
            > equations: Equations of the neuron, defining the temporal evolution of variables.
            > spike: Spike emission condition.
            > reset: Changes to the variables after a spike.
        """
        self.equations = NeuronEquations(equations, 'simple')
        self.parameters = NeuronParameters(parameters, self.equations.equations_list)
        self.spike = NeuronEquations(spike, 'spike', self.parameters) if spike is not None else None
        self.reset = NeuronEquations(reset, 'reset', self.parameters) if reset is not None else None

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
