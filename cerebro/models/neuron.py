from cerebro.models.equations import Equation
from cerebro.models.variables import Variable
from cerebro.compiler.parser import parse_condition


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
        self.variables = Variable.from_raw(variables)

        self.equations = Equation.from_raw(equations)
        self.spike = parse_condition(spike) if spike is not None else None
        self.reset = Equation.from_raw(reset) if reset is not None else None

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
