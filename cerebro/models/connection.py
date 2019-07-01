from cerebro.models.population import Population
from cerebro.models.synapse import Synapse
from cerebro.exceptions import IllegalArgumentException
from cerebro.models.parameter_guards import InstanceGuard


class Connection:
    """
        Class to define a connection(gathering all synapses of the same type) between two populations.
    """
    _instance_count = 0

    def __init__(self, pre, post, synapse):
        """
            Parameters:

            > pre: Pre-synaptic population.
            > post: Post-synaptic population.
            > synapse: A synapse instance the connection is made of.
        """

        # parameter validation
        if not InstanceGuard(Population).is_valid(pre):
            raise IllegalArgumentException(self.__class__.__name__ + ".pre must be a " + Population.__class__.__name__)
        if not InstanceGuard(Population).is_valid(post):
            raise IllegalArgumentException(self.__class__.__name__ + ".post must be a " + Population.__class__.__name__)
        if not InstanceGuard(Synapse).is_valid(synapse):
            raise IllegalArgumentException(self.__class__.__name__ + ".synapse must be a " + Synapse.__class__.__name__)

        self.pre = pre
        self.post = post
        self.synapse = synapse

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
        if self.wrapper is None or \
                (not hasattr(self.wrapper, 'get_{}'.format(item)) and not hasattr(self.wrapper, item)):
            raise AttributeError('object {} has no attribute \'{}\''.format(self.__class__.__name__, item))
        if item.startswith('set'):
            return getattr(self.wrapper, item)
        return getattr(self.wrapper, 'get_{}'.format(item))()

    def __hash__(self):
        return self.id
