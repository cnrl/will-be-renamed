from functools import reduce

from cnrl.exceptions import IllegalArgumentException
from cnrl.models.Neuron import Neuron


class Population:
    """
        Class to define a population of neurons.
    """
    _instance_count = 0

    def __init__(self, shape, neuron):
        """
            Parameters:

            > shape: The shape in which the neurons are placed as tuple.
              If an integer is given, it denotes the size of population.
            > neuron: A neuron instance the population is made of.
        """
        self.shape = shape if isinstance(shape, tuple) else (shape,)
        self.neuron = neuron

        self._check_args()

        self.dimension = len(shape)
        self.size = reduce(lambda x, y: x * y, self.shape)

        self._id = Population._instance_count
        self._instance_count += 1

    def _check_args(self):
        if not isinstance(self.shape, tuple) or \
                not all([isinstance(element, int) for element in self.shape]):
            raise IllegalArgumentException(
                self.__class__.__name__ + ".shape must be an integer or a tuple of integers"
            )

        if not isinstance(self.neuron, Neuron):
            raise IllegalArgumentException(
                self.__class__.__name__ + ".neuron must be a " + Neuron.__class__.__name__
            )

    def __repr__(self):
        return self.__class__.__name__ + """(
                Shape:
                """ + str(self.shape) + """
                Neuron:
                """ + str(self.neuron) + ")"

    def __len__(self):
        return self.size
