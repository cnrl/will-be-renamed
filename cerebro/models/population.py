"""Module containing a single class to build a population of neurons.

Classes
-------
Population
    Base class to define a population of neurons.
"""

from cerebro.exceptions import IllegalArgumentException
from cerebro.models.neuron import Neuron
from cerebro.models.parameter_guards import InstanceGuard


class Population:
    """Base class to define a population of neurons.

    Attributes
    ----------
    size : int
        An integer denoting size of the population, i.e. number of neurons in the population.
    neuron : cerebro.model.neuron.Neuron
        A Neuron object which constructs the population.
    wrapper :
        # TODO
    id : int
        Identifier number of each population.
    """
    _instance_count = 0

    def __init__(self, size, neuron):
        """
        Parameters
        ----------
        size : int
            An integer denoting size of the population, i.e. number of neurons in the population.
        neuron : cerebro.models.neuron.Neuron
            A Neuron object which constructs the population.

        Raises
        ------
        IllegalArgumentException : If arguments are not of appropriate type.
        """

        # parameter validation
        if not InstanceGuard(int).is_valid(size):
            raise IllegalArgumentException(self.__class__.__name__ + ".size must be an integer")
        if not InstanceGuard(Neuron).is_valid(neuron):
            raise IllegalArgumentException(self.__class__.__name__ + ".neuron must be a " + Neuron.__name__)

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
        """
        Raises
        ------
        AttributeError : If an attribute does not exist.
        """

        if self.wrapper is None or not hasattr(self.wrapper, 'get_{}'.format(item)):
            raise AttributeError('object {} has no attribute \'{}\''.format(self.__class__.__name__, item))

        return getattr(self.wrapper, 'get_{}'.format(item))()

    def __hash__(self):
        return hash('population.{}'.format(self.id))
