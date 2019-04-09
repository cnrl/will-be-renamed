from General import objects


class Neuron(object):
    """
        TO-BE-WRITTEN DOCUMENT :))))
    """

    def __init__(self, parameters='', equations='', functions=None, spike=None, refractory=None, reset=None, name=None):
        self.parameters = parameters
        self.equations = equations
        self.functions = functions
        self.spike = spike
        self.reset = reset
        self.refractory = refractory
        self.name = name or "My Neuron_{}".format(len(objects['neurons']))

        objects["neurons"].append(self)


    def __repr__(self):
        text = self.name + """

        Parameters:
        """ + str(self.parameters) + """
        Equations of the variables:
        """ + str(self.equations) + """
        Spiking condition:
        """ + str(self.spike) + """
        Reset after a spike:
        """ + str(self.reset)

        return text
