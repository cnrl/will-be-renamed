from cnrl.globals import FORBIDDEN_CONNECTION_VAR_NAMES
from cnrl.models.parameters import SynapseParameters
from cnrl.models.equations import SynapseEquations
from cnrl.parser.parser import check_variable_definition

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
        self.equations = SynapseEquations(equations)
        self.parameters = SynapseParameters(parameters, self.equations.equations_list)
        check_variable_definition(self.equations, self.parameters.vars, FORBIDDEN_CONNECTION_VAR_NAMES)

    def __repr__(self):
        return self.__class__.__name__ + """(
            Parameters:
            """ + str(self.parameters) + """
            Equations of the variables:
            """ + str(self.equations) + ")"
