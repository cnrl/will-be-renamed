from cnrl.models.Population import Population
from cnrl.models.Synapse import Synapse
from cnrl.exceptions import IllegalArgumentException


class Connection:
    """
        Class to define a connection(gathering all synapses of the same type) between two populations.
    """
    _instance_count = 0

    def __init__(self, pre, post, synapse=None):
        """
            Parameters:

            > pre: Pre-synaptic population.
            > post: Post-synaptic population.
            > synapse: A synapse instance the connection is made of.
        """
        self.pre = pre
        self.post = post
        self.synapse = synapse

        self._check_args()

        self._id = Connection._instance_count
        self._instance_count += 1

    def _check_args(self):
        if not isinstance(self.pre, Population):
            raise IllegalArgumentException(self.__class__.__name__ + ".pre must be a " + Population.__class__.__name__)

        if not isinstance(self.post, Population):
            raise IllegalArgumentException(self.__class__.__name__ + ".post must be a " + Population.__class__.__name__)

        if self.synapse is not None and not isinstance(self.synapse, Synapse):
            raise IllegalArgumentException(self.__class__.__name__ + ".synapse must be a " + Synapse.__class__.__name__)

    def __repr__(self):
        return self.__class__.__name__ + """(
        Pre synaptic population:
        """ + str(self.pre) + """
        Post synaptic population:
        """ + str(self.post) + """
        Synapse:
        """ + str(self.synapse) + ")"
