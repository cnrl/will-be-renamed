import inspect
from copy import deepcopy


class Population(object):
    """
        Class to define a population of neurons.
    """
    _instance_count = 0

    def __init__(self, shape, neuron, name=None):
        """
            Parameters:

            > shape: The shape in which the neurons are placed as tuple. If an integer is given, it denotes the size of population.
            > neuron: A neuron instance the population is made of.
            > name: Name of the population.
        """
        self.shape = shape if isinstance(shape, tuple) else (shape, )
        self.dimension = len(shape)
        self.neuron = neuron() if inspect.isclass(neuron) else deepcopy(neuron)
        self.name = name or "population_{}".format(self._instance_count)

        self.size = 1
        for l in self.shape:
            self.size *= l

        self._instance_count += 1

    def __repr__(self):
        return self.name + """
        shape:
        """  + str(self.shape) + """
        neuron:
        """ + self.neuron.name


    def reset(self):
        pass

    def clear(self):
        pass

    def __len__(self):
        return self.size
