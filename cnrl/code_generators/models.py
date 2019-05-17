from cnrl.exceptions import IllegalArgument
from cnrl.globals import forbidden_pop_var_names, forbidden_proj_var_names


class PopulationVar(object):
    def __init__(self, name, local):
        self.name = name
        self.local = local

        self._check_args()

    def _check_args(self):
        if type(self.name) != str:
            raise IllegalArgument("PopulationVar.name must be a string")
        if self.name.lower() in forbidden_pop_var_names:
            raise IllegalArgument("{} is not a valid name for PopulationVar.name".format(self.name))

        if type(self.local) != bool:
            raise IllegalArgument("PopulationVar.local must be a boolean")


class Population(object):
    def __init__(self, name, variables):
        self.name = name
        self.variables = variables

        self._check_args()

        self._class_name = self.name.title()

    def _check_args(self):
        if type(self.name) != str:
            raise IllegalArgument("Population.name must be a string")
        if not self.name.islower():
            raise IllegalArgument("Population.name must be lowercase")

        if type(self.variables) != list:
            raise IllegalArgument("Population.variables must be a list")
        for var in self.variables:
            if not isinstance(var, PopulationVar):
                raise IllegalArgument("Population.variables must be a list of PopulationVars")


class ProjectionVar(object):
    def __init__(self, name):
        self.name = name

        self._check_args()

    def _check_args(self):
        if type(self.name) != str:
            raise IllegalArgument("ProjectionVar.name must be a string")
        if self.name.lower() in forbidden_proj_var_names:
            raise IllegalArgument("{} is not a valid name for ProjectionVar.name".format(self.name))


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
            raise IllegalArgument("Projection.name must be a string")
        if not self.name.islower():
            raise IllegalArgument("Population.name must be lowercase")

        if type(self.variables) != list:
            raise IllegalArgument("Projection.variables must be a list")
        for var in self.variables:
            if not isinstance(var, ProjectionVar):
                raise IllegalArgument("Projection.variables must be a list of ProjectionVars")

        if not isinstance(self.source, Population):
            raise IllegalArgument("Projection.source must be a Population")

        if not isinstance(self.dest, Population):
            raise IllegalArgument("Projection.dest must be a Population")
