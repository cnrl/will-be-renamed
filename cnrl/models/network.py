from cnrl.exceptions import IllegalArgumentException
from cnrl.models.population import Population
from cnrl.models.connection import Connection
from cnrl.code_generation.api import generate

class Network:
    """
        Class to build a network.
    """
    _instance_count = 0

    def __init__(self, populations=None, connections=None):
        """
            Parameters:

            > populations: A list of population to be added to the network.
            > connections: A list of connections to be added to the network.
        """
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
        self.c_module = generate(self.id, self.populations, self.connections)
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
