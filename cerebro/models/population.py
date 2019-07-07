from cerebro.exceptions import IllegalArgumentException
from cerebro.models.neuron import Neuron
from cerebro.models.parameter_guards import InstanceGuard


class Population:
    """
        Class to define a population of neurons.
    """
    _instance_count = 0

    def __init__(self, size, neuron):
        """
            Parameters:

            > size: The size denoting the size of population.
            > neuron: A neuron instance the population is made of.
        """

        # parameter validation
        if not InstanceGuard(int).is_valid(size):
            raise IllegalArgumentException(self.__class__.__name__ + ".size must be an integer")
        if not InstanceGuard(Neuron).is_valid(neuron):
            raise IllegalArgumentException(self.__class__.__name__ + ".neuron must be a " + Neuron.__class__.__name__)

        self.size = size
        self.neuron = neuron
        self.wrapper = None
        self.id = Population._instance_count
        Population._instance_count += 1

    def __repr__(self):
        return self.__class__.__name__ + """(
                Size:
                """ + str(self.size) + """
                Neuron:
                """ + str(self.neuron) + ")"

    def __len__(self):
        return self.size

    def __getattr__(self, item):
        if self.wrapper is None or not hasattr(self.wrapper, 'get_{}'.format(item)):
            raise AttributeError('object {} has no attribute \'{}\''.format(self.__class__.__name, item))

        return getattr(self.wrapper, 'get_{}'.format(item))()

    def __hash__(self):
        return 'population.{}'.format(self.id)
