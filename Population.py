import inspect
from copy import deepcopy


class Population(object):
    """
        TODO: Documentation
    """
    _instance_count = 0
    def __init__(self, shape, neuron, name=None):
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
