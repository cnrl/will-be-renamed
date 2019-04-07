from General import objects

class Synapse(object):
    '''
        TO-BE-WRITTEN DOCUMENT :))))
    '''
    def __init__(self, parameters="", equations="", functions=None, pre=None, post=None, psp=None, name=None):
        self.parameters = parameters
        self.equations = equations
        self.pre = pre
        self.post = post
        self.functions = functions
        self.psp = psp
        if not name:
            self.name = "My Spiking Neural Network"
        else:
            self.name = name

        objects["synapses"].append(self)
