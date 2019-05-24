from cnrl.parser.Parser import parse_equations, parse_conditions, parse_reset
from cnrl.exceptions import IllegalArgumentException


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
    def __init__(self, equations, equation_type):
        super().__init__(equations)

        if equation_type == 'simple':
            self.equations_list = parse_equations(equations)
        elif equation_type == 'spike':
            self.equations_list = parse_conditions(equations)
        elif equation_type == 'reset':
            self.equations_list = parse_reset(equations)


class SynapseEquations(Equations):
    def __init__(self, equations):
        super().__init__(equations)
        self.equations_list = parse_equations(equations)
