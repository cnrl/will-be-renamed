from cnrl.generals import networks
from cnrl.models.Population import Population

class Network(object):
    """
        Class to build a network.

        Methods:
        > add(obj): Adds an object to the network
        > compile(): Every defined network needs to be compiled before simulation using the compile method.
    """
    _instance_count = 0

    def __init__(self, objects=None, name=None):
        """
            Parameters:

            > objects: A list of objects to be added to the network. Each object is either a population or a connections.
            > name: Name of the network.
        """
        self.populations = []
        self.connections = []
        if objects is not None:
            for obj in objects:
                self.add(obj)
        self.name = name or "Network_{}".format(self._instance_count)

        self._instance_count += 1
        networks.append(self)

    def add(self, obj):
        if issubclass(obj, Population):
            if obj not in self.populations:
                self.populations.append(obj)
        # TODO: add other classes (Connection, ...)

    def compile(self):
        pass
