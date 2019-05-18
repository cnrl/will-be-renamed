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
    def __init__(self, definitions):
        super(NeuronParameters, self).__init__(definitions)
        # TODO create something like this with parser as we talk
        self.vars = [
            {
                'name': 'x',
                'scope': 'local'
            },
            {
                'name': 'immrmissikslookatme',
                'scope': 'global'
            }
        ]
    # TODO: check if all parameters are not in globals.FORBIDDEN_POP_VAR_NAMES
    pass


class SynapseParameters(Parameters):
    def __init__(self, definitions):
        super(SynapseParameters, self).__init__(definitions)
        # TODO create something like this with parser as we talk
        self.vars = [
            {
                'name': 'x'
            }
        ]
    # TODO: check if all parameters are not in globals.FORBIDDEN_PROJ_VAR_NAMES
    pass
