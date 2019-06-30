from cerebro.exceptions import IllegalArgumentException
from cerebro.models.population import Population
from cerebro.models.connection import Connection
from cerebro.code_generation.api import generate
from cerebro.models.variables import Variable


class Network:
    """
        Class to build a network.
    """
    _instance_count = 0

    def __init__(self, variables='', populations=None, connections=None):
        """
            Parameters:

            > populations: A list of population to be added to the network.
            > connections: A list of connections to be added to the network.
        """
        self.variables = Variable.from_raw(variables)
        self.populations = populations if populations is not None else []
        self.connections = connections if connections is not None else []

        self._check_args()

        self.c_module = None
        self.id = Network._instance_count
        Network._instance_count += 1

    def _bind_c_instances(self):
        for population in self.populations:
            population.wrapper = getattr(self.c_module, 'Population{}Wrapper'.format(population.id))(population.size)
        for connection in self.connections:
            connection.wrapper = getattr(self.c_module, 'Connection{}Wrapper'.format(connection.id))()

    def compile(self):
        self.c_module = generate(self.id, self.variables, self.populations, self.connections)
        self._bind_c_instances()

    def simulate(self, duration):
        self.c_module.initialize(0.001)
        self.c_module.run(duration / self.c_module.get_dt())

    def _check_args(self):
        if not isinstance(self.populations, (list, tuple)) or \
                not all([isinstance(pop, Population) for pop in self.populations]):
            raise IllegalArgumentException(
                self.__class__.__name__ + ".populations must be a list of " + Population.__class__.__name__
            )

        if not isinstance(self.connections, (list, tuple)) or \
                not all([isinstance(con, Connection) for con in self.connections]):
            raise IllegalArgumentException(
                self.__class__.__name__ + ".connection must be a list of " + Connection.__class__.__name__
            )
