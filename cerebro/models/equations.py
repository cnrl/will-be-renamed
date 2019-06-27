from abc import ABC, abstractmethod

from cerebro.parser.parser import parse_equations, parse_conditions, parse_reset
from cerebro.exceptions import IllegalArgumentException
from cerebro.enums import EquationType


class Equations(ABC):
    """
    This class is an abstract class for equation definitions.
    """

    @abstractmethod
    def __init__(self, equations):
        self.equations = equations
        self._check_args()

    def _check_args(self):
        if not isinstance(self.equations, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".equations must be a string")

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tequations:" + self.equations + ")"


class NeuronEquations(Equations):
    """
    This class takes care of neuron equations.
    """
    def __init__(self, equations, equation_type):
        super().__init__(equations)

        if equation_type == EquationType.SIMPLE:
            self.equations_list = parse_equations(equations)
        elif equation_type == EquationType.SPIKE:
            self.equations_list = parse_conditions(equations)
        elif equation_type == EquationType.RESET:
            self.equations_list = parse_reset(equations)


class SynapseEquations(Equations):
    """
    This class takes care of synapse equations.
    """
    def __init__(self, equations):
        super().__init__(equations)
        self.equations_list = parse_equations(equations)
