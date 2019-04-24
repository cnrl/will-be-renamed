import inspect
from copy import deepcopy

class Connection:
    """
        TODO: Documentation
    """
    _instance_count = 0

    def __init__(self, pre, post, connection_type, synapse=None, name=None):
        self.pre = pre
        self.post = post
        self.connection_type = connection_type
        self.synapse = synapse() if inspect.isclass(synapse) else deepcopy(synapse)
        self.name = name or "Connection_{}".format(self._instance_count)

        self._instance_count += 1

    def __repr__(self):
        text = self.name + """

        Pre synaptic population:
        """ + str(self.pre) + """
        Post synaptic population:
        """ + str(self.post) + """
        Connection type:
        """ + str(self.type) + """
        Synapse:
        """ + str(self.synapse)

        return text
