from cnrl.exceptions import IllegalArgumentException
from cnrl.parser.Lexer import parameters_lexer, variable_lexer
from cnrl.globals import SYNAPSE_INTERNAL_VARIABLES, NEURON_INTERNAL_VARIABLES

class Parameters:
    # TODO define all variables in parameters, there shan't be variable definition in equations
    def __init__(self, definitions, equations_list):
        self.definitions = definitions
        self.equations = equations_list
        self._check_args()

        self.vars = parameters_lexer(definitions)
        self.vars.update(variable_lexer(equations_list))

    def _check_args(self):
        if not isinstance(self.definitions, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".definitions must be a string")

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tdefinitions:" + self.definitions + ")"



class NeuronParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_POP_VAR_NAMES

    def __init__(self, definitions, equations_list):
        super(NeuronParameters, self).__init__(definitions, equations_list)
        self.vars.update(NEURON_INTERNAL_VARIABLES)


class SynapseParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_PROJ_VAR_NAMES

    def __init__(self, definitions, equations_list):
        super(SynapseParameters, self).__init__(definitions, equations_list)
        self.vars.update(SYNAPSE_INTERNAL_VARIABLES)

