import os
from cnrl.code_generators.models import Population, Projection
from cnrl.exceptions import IllegalArgument, IllegalState


# generates cpp code, compiles it and returns dynamically loaded module
def generate(name, pops, projs):
    _check_args(pops, projs)

    base_path = _create_dirs(name)


def _check_args(name, pops, projs):
    if type(name) != str:
        raise IllegalArgument("name must be a string")

    if type(pops) != list:
        raise IllegalArgument("pops must be a list")
    for pop in pops:
        if not isinstance(pop, Population):
            raise IllegalArgument("pops must be a list of Populations")

    if type(projs) != list:
        raise IllegalArgument("projs must be a list")
    for proj in projs:
        if not isinstance(proj, Projection):
            raise IllegalArgument("projs must be a list of Projections")


def _create_dirs(name):
    cwd = os.getcwd()

    dir_path = os.path.join(cwd, 'build')

    if os.path.exists(dir_path):
        raise IllegalState('cannot create build folder, a file or directory with this name exists')

    os.mkdir(dir_path)

    base_path = os.path.join(dir_path, name)
    os.mkdir(base_path)

    return base_path
