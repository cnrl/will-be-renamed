from cerebro.models.variables import SynapseVariables
from cerebro.models.equations import SynapseEquations


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
        self.variables = SynapseVariables(variables)

        self.equations = SynapseEquations(equations)

    def __repr__(self):
        return self.__class__.__name__ + """(
            Variables:
            """ + str(self.variables) + """
            Equations of the variables:
            """ + str(self.equations) + ")"
