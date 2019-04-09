from General import objects

class Population(object):
    """
        TODO: Documentation
    """

    def __init__(self, shape, neuron, name=None):
        self.shape = shape if isinstance(shape, tuple) else (shape, )
        self.dimension = len(shape)
        self.neuron = neuron
        self.name = name or "population_{}".format(len(objects['populations']))

        self.size = 1
        for l in self.shape:
            self.size *= l

    def __repr__(self):
        return self.name + """
        shape:
        """  + self.shape + """
        neuron:
        """ + self.neuron.name


    def reset(self):
        pass

    def clear(self):
        pass

    def __len__(self):
        return self.size
