from sympy.core.symbol import Symbol

from cnrl.exceptions import IllegalArgumentException
from cnrl.parser.Lexer import parameters_lexer, variable_lexer


class Parameters:
    def __init__(self, definitions, equations_list):
        self.definitions = definitions
        self.equations = equations_list
        self._check_args()

        variables = parameters_lexer(definitions) + variable_lexer(equations_list)
        var_set = set()
        for var in variables:
            if var['name'] not in var_set:
                var_set.add(var['name'])
            else:
                raise Exception("parameter {} is already defined in this scope".format(var['name']))
        self.vars = variables

    def _check_args(self):
        if not isinstance(self.definitions, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".definitions must be a string")

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tdefinitions:" + self.definitions + ")"

    def _replace_globals(self):
        for eq in self.equations:
            for sym in eq['rhs_parsed'].args:
                if type(sym) is Symbol:
                    pass # TODO n^3 !!!!


class NeuronParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_POP_VAR_NAMES

    def __init__(self, definitions, equations_list):
        super(NeuronParameters, self).__init__(definitions, equations_list)


class SynapseParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_PROJ_VAR_NAMES

    def __init__(self, definitions, equations_list):
        super(SynapseParameters, self).__init__(definitions, equations_list)

