from cerebro.exceptions import IllegalArgumentException
from cerebro.models.population import Population
from cerebro.models.connection import Connection
from cerebro.compiler.compiler import Compiler
from cerebro.code_generation.api import generate
from cerebro.compiler.parser import VariableParser
from cerebro.models.parameter_guards import IterableGuard, InstanceGuard


class Network:
    """
        Class to build a network.
    """
    _instance_count = 0

    def __init__(self, variables='', populations=None, connections=None):
        """
            Parameters:

            > variables: An string of variable definitions
            > populations: A list of population to be added to the network.
            > connections: A list of connections to be added to the network.
        """

        # parameter validation
        if not InstanceGuard(str).is_valid(variables):
            raise IllegalArgumentException(self.__class__.__name__ + ".variables must be an string")
        if (populations is not None) and not IterableGuard(Population).is_valid(populations):
            raise IllegalArgumentException(
                self.__class__.__name__ + ".populations must be an iterable of " + Population.__class__.__name__
            )
        if (connections is not None) and not IterableGuard(Connection).is_valid(connections):
            raise IllegalArgumentException(
                self.__class__.__name__ + ".connections must be an iterable of " + Connection.__class__.__name__
            )

        self.variables = VariableParser.from_lines(variables)
        self.populations = populations if populations is not None else []
        self.connections = connections if connections is not None else []

        self.c_module = None
        self.compiler = None
        self.id = Network._instance_count
        Network._instance_count += 1

    def _bind_c_instances(self):
        for population in self.populations:
            population.wrapper = getattr(self.c_module, 'Population{}Wrapper'.format(population.id))(population.size)
        for connection in self.connections:
            connection.wrapper = getattr(self.c_module, 'Connection{}Wrapper'.format(connection.id))()

    def compile(self):
        self.compiler = Compiler(network=self)
        self.compiler.semantic_analyzer()
        #self.c_module = generate(self.id, self.variables, self.populations, self.connections)
        #self._bind_c_instances()

    def simulate(self, duration, dt):
        self.c_module.initialize(dt)
        self.c_module.run(duration / self.c_module.get_dt())

    def __hash__(self):
        return self.id
