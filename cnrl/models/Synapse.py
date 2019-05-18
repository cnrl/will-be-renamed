
class Synapse(object):

    """
        Class to define a synapse
    """
    _instance_count = 0

    def __init__(self, parameters='', equations='', functions=None, pre=None, post=None, psp=None, name=None):
        """
            Parameters:

            > parameters: Parameters of the synapse and their initial values.
            > equations: Equations of the synapse, defining the temporal evolution of variables.
            > functions: Definition of additional functions used in `equations`.
            > pre: Variable updates when a pre-synaptic spike is received.
            > post: Variable updates when a post-synaptic spike is emitted.
            > psp: Influence of a synapse on post-synaptic neuron.
            > name: Name of the syanpse.
        """
        self.parameters = parameters
        self.equations = equations
        self.pre = pre
        self.post = post
        self.functions = functions
        self.psp = psp
        self.name = name or "My Synapse_{}".format(self._instance_count)

        self._instance_count += 1

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
