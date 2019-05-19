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
    # TODO: check if all parameters are not in globals.FORBIDDEN_POP_VAR_NAMES

    def __init__(self, definitions):
        super(NeuronParameters, self).__init__(definitions)

        # TODO: fill this like:
        # self.vars = [
        #     {
        #         'name': 'x',
        #         'scope': 'local'
        #     },
        #     {
        #         'name': 'y',
        #         'scope': 'global'
        #     }
        # ]
        self.vars = []


class SynapseParameters(Parameters):
    # TODO: check if all parameters are not in globals.FORBIDDEN_PROJ_VAR_NAMES

    def __init__(self, definitions):
        super(SynapseParameters, self).__init__(definitions)

        # TODO: fill this like:
        # self.vars = [
        #     {
        #         'name': 'x'
        #     }
        # ]
        self.vars = []
