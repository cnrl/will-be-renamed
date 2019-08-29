from cerebro.models import Neuron, Synapse, Network, Population, Connection
import os
os.system("rm -rf build/")

neuron = Neuron(
    variables="""
        v = 0 : local
    """,
    equations="""
        v = 5
    """,
    spike="(v > 5)",
    reset="""
        v = 3
        v = 10
    """
)

synapse = Synapse(
    variables="""
        p = 0 : shared
        tau = 12 : constant
        x = 3
    """,
    equations="""
        x = p + tau - _pre_v + _post_v - n
    """
)

pop = Population(neuron=neuron, size=10)
pop2 = Population(neuron=neuron, size=10)

conn = Connection(pre=pop, post=pop2, synapse=synapse)

net = Network(populations=[pop, pop2], connections=[conn], variables="n = 2")

net.compile()

