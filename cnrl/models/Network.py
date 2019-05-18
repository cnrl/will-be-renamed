from cnrl.generals import networks
from cnrl.models.Population import Population
from cnrl.parser.Parser import parse_conditions, parse_mathematical_expr, parse_equations, parse_parameters, parse_reset


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
        network_objects = {"population": {"equations": [], "param_var": [], "reset": [], "spike": []},
                           "connection": {"equations": [], "param_var": [], "psp": [], "pre": [], "post": []}}
        for pop in self.populations:
            network_objects["population"]["param_var"].append(parse_parameters(pop.neuron.parameters))
            network_objects["population"]["equations"].append(parse_equations(pop.neuron.equations))
            network_objects["population"]["reset"].append(parse_reset(pop.neuron.reset))
            network_objects["population"]["spike"].append(parse_conditions(pop.neuron.spike))
        for con in self.connections:
            network_objects["connection"]["param_var"].append(parse_parameters(con.synapse.parameters))
            network_objects["connection"]["equations"].append(parse_equations(con.synapse.equations))
            network_objects["connection"]["psp"].append(parse_mathematical_expr(con.synapse.psp))
            network_objects["connection"]["pre"].append(parse_equations(con.synapse.pre))
            network_objects["connection"]["post"].append(parse_equations(con.synapse.post))
        for obj in network_objects["population"]:
            if len(set(obj["param_var"])) != len(obj["param_var"]):
                raise Exception("Same name for multiple variables")
        for obj in network_objects["connection"]:
            if len(set(obj["param_var"])) != len(obj["param_var"]):
                raise Exception("Same name for multiple variables")
        pass
