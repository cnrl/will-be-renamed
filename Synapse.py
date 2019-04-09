from General import objects

class Synapse(object):

    """
        TODO: Documentation
    """

    def __init__(self, parameters='', equations='', functions=None, pre=None, post=None, psp=None, name=None):
        self.parameters = parameters
        self.equations = equations
        self.pre = pre
        self.post = post
        self.functions = functions
        self.psp = psp
        self.name = name or "My Synapse_{}".format(len(objects['synapses']))

        objects["synapses"].append(self)

    def __repr__(self):
        text = self.name + """

        Parameters:
        """ + str(self.parameters) + """
        Equations of the variables:
        """ + str(self.equations) + """
        Spiking condition:
        """ + str(self.pre) + """
        Reset after a spike:
        """ + str(self.post)

        return text
