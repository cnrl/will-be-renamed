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
    pass


class SynapseEquations(Equations):
    pass
