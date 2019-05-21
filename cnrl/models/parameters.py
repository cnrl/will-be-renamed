from cnrl.parser.Lexer import parameters_lexer, get_equation_variables
from cnrl.exceptions import IllegalArgumentException


class Parameters:
    def __init__(self, definitions, equations):
        self.definitions = definitions
        self.equations = equations
        self._check_args()

        variables = parameters_lexer(definitions) + get_equation_variables(equations)
        var_set = set()
        for var in variables :
            if var['name'] not in var_set:
                var_set.add(var['name'])
            else:
                raise Exception("parameter {} is already defined in this scope".format(var['name']) )
        self.vars = variables

    def _check_args(self):
        if not isinstance(self.definitions, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".definitions must be a string")
        if not isinstance(self.equations, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".equations must be a string")

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tdefinitions:" + self.definitions + ")"


class NeuronParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_POP_VAR_NAMES

    def __init__(self, definitions, equations):
        super(NeuronParameters, self).__init__(definitions, equations)


class SynapseParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_PROJ_VAR_NAMES

    def __init__(self, definitions, equations):
        super(SynapseParameters, self).__init__(definitions, equations)

