from cerebro.models.variable import Variable
from cerebro.models.equation import Equation
from cerebro.exceptions import IllegalArgumentException
from cerebro.models.parameter_guards import InstanceGuard


class Synapse:
    """
        Class to define a synapse
    """

    def __init__(self, variables='', equations=''):
        """
            Parameters:

            > variables: Variables of the synapse and their initial values.
            > equations: Equations of the synapse, defining the temporal evolution of variables.
        """

        # parameter validation
        if not InstanceGuard(str).is_valid(variables):
            raise IllegalArgumentException(self.__class__.__name__ + ".variables must be an string")
        if not InstanceGuard(str).is_valid(equations):
            raise IllegalArgumentException(self.__class__.__name__ + ".equations must be an string")

        self.variables = Variable.from_raw(variables)
        self.equations = Equation.from_raw(equations)

    def __repr__(self):
        return self.__class__.__name__ + """(
            Variables:
            """ + str(self.variables) + """
            Equations of the variables:
            """ + str(self.equations) + ")"
