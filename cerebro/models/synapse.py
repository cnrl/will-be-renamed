from cerebro.models.variables import Variable
from cerebro.models.equations import Equation


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
        self.variables = Variable.from_raw(variables)
        self.equations = Equation.from_raw(equations)

    def __repr__(self):
        return self.__class__.__name__ + """(
            Variables:
            """ + str(self.variables) + """
            Equations of the variables:
            """ + str(self.equations) + ")"
