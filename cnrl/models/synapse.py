from cnrl.models.parameters import SynapseParameters
from cnrl.models.equations import SynapseEquations


class Synapse:
    """
        Class to define a synapse
    """

    def __init__(self, parameters='', equations=''):
        """
            Parameters:

            > parameters: Parameters of the synapse and their initial values.
            > equations: Equations of the synapse, defining the temporal evolution of variables.
        """
        self.parameters = SynapseParameters(parameters, equations)
        self.equations = SynapseEquations(equations)

    def __repr__(self):
        return self.__class__.__name__ + """(
            Parameters:
            """ + str(self.parameters) + """
            Equations of the variables:
            """ + str(self.equations) + ")"
