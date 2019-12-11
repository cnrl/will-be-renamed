"""Module containing a single class to build a network.

*Classes*:

* **Network**:
    Base class to build a network.
"""

from cerebro.preprocessors import ImagePopulation
from cerebro.exceptions import IllegalArgumentException
from cerebro.models.population import Population
from cerebro.models.connection import Connection
from cerebro.compiler.compiler import Compiler
from cerebro.compiler.parser import VariableParser
from cerebro.parameter_guards import IterableGuard, InstanceGuard


class Network:
    """
    Base class to build a network.
    """
    _instance_count = 0

    def __init__(self, variables='', populations=None, connections=None):
        """
        :param variables: A multi-line string, each line of which defines a variable.
        :param populations: A list of populations in the network.
        :param connections: A list of connections in the network.

        :type variables: str
        :type populations: list of cerebro.models.population.Population
        :type connections: list of cerebro.models.connection.Connection

        :raises IllegalArgumentException: If arguments are not of appropriate type.
        """

        # parameter validation
        if not InstanceGuard(str).is_valid(variables):
            raise IllegalArgumentException(self.__class__.__name__ + ".variables must be a string")
        if (populations is not None) and not IterableGuard(Population).is_valid(populations):
            raise IllegalArgumentException(
                self.__class__.__name__ + ".populations must be an iterable of " + Population.__name__
            )
        if (connections is not None) and not IterableGuard(Connection).is_valid(connections):
            raise IllegalArgumentException(
                self.__class__.__name__ + ".connections must be an iterable of " + Connection.__name__
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
        """Compiles the code and generates the equivalent C++ code.

        c_module will be set after compilation and code generation process.
        """

        self.compiler = Compiler(network=self)
        self.compiler.semantic_analyzer()
        self.c_module = self.compiler.code_gen()
        self._bind_c_instances()
        for pop in self.populations:
            if isinstance(pop, ImagePopulation.ImagePopulation):
                pop.wrapper.set_tts(pop.intensity_to_latency())

    def simulate(self, duration, dt):
        """Simulates the network for `duration` time with `dt` step size."""
        self.c_module.initialize(dt)

        self.c_module.run_wrapper(duration / self.c_module.get_dt())

    def __hash__(self):
        return hash('network.{}'.format(self.id))
