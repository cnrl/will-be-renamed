from cnrl.code_generators.models import Population, ProjectionVar, Projection, PopulationVar
from cnrl.code_generators.api import generate

pop0 = Population(
    'pop0',
    [
        PopulationVar('tau', True),
        PopulationVar('Er', False),
        PopulationVar('Ee', False),
        PopulationVar('X', False)
    ]
)

pop1 = Population(
    'pop1',
    [
        PopulationVar('tau', False),
        PopulationVar('Er', False),
        PopulationVar('Ee', False),
        PopulationVar('X', False)
    ]
)

proj0 = Projection('proj1', [ProjectionVar('y')], pop0, pop1)

generate('net0', [pop0, pop1], [proj0])
