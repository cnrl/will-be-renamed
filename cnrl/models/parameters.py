from cnrl.exceptions import IllegalArgumentException


class Parameters:
    def __init__(self, definitions):
        self.definitions = definitions

        self._check_args()

    def _check_args(self):
        if not isinstance(self.definitions, str):
            raise IllegalArgumentException(self.__class__.__name__ + ".definitions must be a string")

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tdefinitions:" + self.definitions + ")"


class NeuronParameters(Parameters):
    pass


class SynapseParameters(Parameters):
    pass
