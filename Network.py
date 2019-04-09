from General import networks
from Population import Population

class Network(object):
    _instance_count = 0
    def __init__(self, objects=None, name=None):
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
