from cnrl.exceptions import IllegalArgumentException
from cnrl.globals import FORBIDDEN_POP_VAR_NAMES, FORBIDDEN_PROJ_VAR_NAMES


class PopulationVar(object):
    def __init__(self, name, local):
        self.name = name
        self.local = local

        self._check_args()

    def _check_args(self):
        if type(self.name) != str:
            raise IllegalArgumentException("PopulationVar.name must be a string")
        if self.name.lower() in FORBIDDEN_POP_VAR_NAMES:
            raise IllegalArgumentException("{} is not a valid name for PopulationVar.name".format(self.name))

        if type(self.local) != bool:
            raise IllegalArgumentException("PopulationVar.local must be a boolean")


class Population(object):
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

        self._check_args()

        self._class_name = self.name.title()

    def _check_args(self):
        if type(self.name) != str:
            raise IllegalArgumentException("Population.name must be a string")
        if not self.name.islower():
            raise IllegalArgumentException("Population.name must be lowercase")

        if type(self.variables) != list:
            raise IllegalArgumentException("Population.variables must be a list")
        for var in self.variables:
            if not isinstance(var, PopulationVar):
                raise IllegalArgumentException("Population.variables must be a list of PopulationVars")


class ProjectionVar(object):
    def __init__(self, name):
        self.name = name

        self._check_args()

    def _check_args(self):
        if type(self.name) != str:
            raise IllegalArgumentException("ProjectionVar.name must be a string")
        if self.name.lower() in FORBIDDEN_PROJ_VAR_NAMES:
            raise IllegalArgumentException("{} is not a valid name for ProjectionVar.name".format(self.name))


class Projection(object):
    def __init__(self, name, variables, source, dest):
        self.name = name
        self.variables = variables
        self.source = source
        self.dest = dest

        self._check_args()

        self._class_name = self.name.title()

    def _check_args(self):
        if type(self.name) != str:
            raise IllegalArgumentException("Projection.name must be a string")
        if not self.name.islower():
            raise IllegalArgumentException("Population.name must be lowercase")

        if type(self.variables) != list:
            raise IllegalArgumentException("Projection.variables must be a list")
        for var in self.variables:
            if not isinstance(var, ProjectionVar):
                raise IllegalArgumentException("Projection.variables must be a list of ProjectionVars")

        if not isinstance(self.source, Population):
            raise IllegalArgumentException("Projection.source must be a Population")

        if not isinstance(self.dest, Population):
            raise IllegalArgumentException("Projection.dest must be a Population")
