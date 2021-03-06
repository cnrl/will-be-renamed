"""Module containing a single class to define connection between two population of neurons.

*Classes*:

* **Connection**:
    Base class to define a connection between two population of neurons.
"""

from cerebro.models.population import Population
from cerebro.models.synapse import Synapse
from cerebro.exceptions import IllegalArgumentException
from cerebro.parameter_guards import InstanceGuard


class Connection:
    """
    Base class to define a connection between two population of neurons.
    """
    _instance_count = 0

    def __init__(self, pre, post, synapse, connection_type):
        """
        :param pre: Pre-synaptic population of neurons.
        :param post: Post-synaptic population of neurons.
        :param synapse: A synapse object that constructs the connection.
        :param connection_type: Represents type of connection. Use an object of a subclass of ConnectionType.

        :type pre: cerebro.models.population.Population
        :type post: cerebro.models.population.Population
        :type synapse: cerebro.models.synapse.Synapse
        :type connection_type: cerebro.models.connection_type.ConnectionType

        :raises IllegalArgumentException: If arguments are not of appropriate type.
        """

        # parameter validation
        if not InstanceGuard(Population).is_valid(pre):
            raise IllegalArgumentException(self.__class__.__name__ + ".pre must be a " + Population.__name__)
        if not InstanceGuard(Population).is_valid(post):
            raise IllegalArgumentException(self.__class__.__name__ + ".post must be a " + Population.__name__)
        if not InstanceGuard(Synapse).is_valid(synapse):
            raise IllegalArgumentException(self.__class__.__name__ + ".synapse must be a " + Synapse.__name__)

        self.pre = pre
        self.post = post
        self.synapse = synapse
        self.connection_type = connection_type

        self.wrapper = None

        self.id = Connection._instance_count
        Connection._instance_count += 1

    def __repr__(self):
        return self.__class__.__name__ + """(
        Pre synaptic population:
        """ + str(self.pre) + """
        Post synaptic population:
        """ + str(self.post) + """
        Synapse:
        """ + str(self.synapse) + ")"

    def __getattr__(self, item):
        """
            :raises AttributeError : If an attribute does not exist.
        """

        if self.wrapper is None or \
                (not hasattr(self.wrapper, 'get_{}'.format(item)) and not hasattr(self.wrapper, item)):
            raise AttributeError('object {} has no attribute \'{}\''.format(self.__class__.__name__, item))
        if item.startswith('set'):
            return getattr(self.wrapper, item)
        return getattr(self.wrapper, 'get_{}'.format(item))()

    def __hash__(self):
        return hash('connection.{}'.format(self.id))
