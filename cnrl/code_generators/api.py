from cnrl.code_generators.models import Population, Projection
from cnrl.exceptions import IllegalArgument


def generate(pops, projs):
    _check_args(pops, projs)


def _check_args(pops, projs):
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
