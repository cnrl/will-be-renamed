from cerebro.models.equation import Equation
from cerebro.models.variable import Variable
from cerebro.compiler.parser import parse_condition
from cerebro.models.parameter_guards import InstanceGuard
from cerebro.exceptions import IllegalArgumentException


class Neuron:
    """
        Class to define a neuron.
    """

    def __init__(self, variables='', equations='', spike='', reset=''):
        """
            Parameters:

            > variables: Variables of the neuron and their initial values.
            > equations: Equations of the neuron, defining the temporal evolution of variables.
            > spike: Spike emission condition.
            > reset: Changes to the variables after a spike.
        """

        # parameter validation
        if not InstanceGuard(str).is_valid(variables):
            raise IllegalArgumentException(self.__class__.__name__ + ".variables must be an string")
        if not InstanceGuard(str).is_valid(equations):
            raise IllegalArgumentException(self.__class__.__name__ + ".equations must be an string")
        if not InstanceGuard(str).is_valid(spike):
            raise IllegalArgumentException(self.__class__.__name__ + ".spike must be an string")
        if not InstanceGuard(str).is_valid(reset):
            raise IllegalArgumentException(self.__class__.__name__ + ".reset must be an string")

        self.variables = Variable.from_raw(variables)
        self.equations = Equation.from_raw(equations)
        self.spike = parse_condition(spike)
        self.reset = Equation.from_raw(reset)

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
