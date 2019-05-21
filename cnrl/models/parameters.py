from cnrl.parser.Lexer import parameters_lexer
from cnrl.exceptions import IllegalArgumentException


class Parameters:
    def __init__(self, definitions):
        self.definitions = definitions
        self._check_args()
        params = parameters_lexer(definitions)
        param_set = set()
        for param in params :
            if param['name'] not in param_set:
                param_set.add(param['name'])
            else:
                raise Exception("parameter {} is already defined in this scope".format(param['name']) )
        self.vars = params

    def _check_args(self):
        if not isinstance(self.definitions, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".definitions must be a string")

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tdefinitions:" + self.definitions + ")"


class NeuronParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_POP_VAR_NAMES

    def __init__(self, definitions):
        super(NeuronParameters, self).__init__(definitions)


class SynapseParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_PROJ_VAR_NAMES

    def __init__(self, definitions):
        super(SynapseParameters, self).__init__(definitions)

