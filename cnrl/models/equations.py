from cnrl.parser.Parser import parse_equations, parse_conditions, parse_reset
from cnrl.exceptions import IllegalArgumentException, ParserException
from sympy.core.symbol import Symbol


class Equations:
    def __init__(self, equations):
        self.equations = equations
        self._check_args()

    def _check_args(self):
        if not isinstance(self.equations, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".equations must be a string")

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tequations:" + self.equations + ")"


class NeuronEquations(Equations):
    def __init__(self, equations, equation_type, parameters_list):
        super().__init__(equations)

        if equation_type == 'simple':
            self.equations_list = parse_equations(equations)
        elif equation_type == 'spike':
            self.equations_list = parse_conditions(equations)
        elif equation_type == 'reset':
            self.equations_list = parse_reset(equations)

        for eq in self.equations_list:
            for sym in eq["rhs_parsed"].args:
                if type(sym) is Symbol and str(sym) not in parameters_list.var_set:
                    raise ParserException("{} is not defined in this scope.".format(sym))
            if equation_type != 'simple':
                for sym in eq["lhs_parsed"].args:
                    if type(sym) is Symbol and str(sym) not in parameters_list.var_set:
                        raise ParserException("{} is not defined in this scope.".format(sym))


class SynapseEquations(Equations):
    pass
