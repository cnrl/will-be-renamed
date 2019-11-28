from cerebro.models import Neuron, Synapse, Network, Population, Connection, ConnectionType
import os

os.system("rm -rf build/")

neuron = Neuron(
    variables="""
        v = 0 : local
    """,
    equations="""
        v = v + 0.1
    """,
    spike="(v > 5)",
    reset="""
        v = 3
        v = Uniform(1.0, 7.0)
    """
)

synapse = Synapse(
    variables="""
        p = 0 : shared
        tau = 12 : constant     
        delay = 0
        x = 3
    """,
    equations="""
        x = p + tau - _pre_v + _post_v - n + Uniform(2, 3)
        dw/dt = w + 1
    """,
    pre_spike="""
    x = x + w
    """,
    post_spike="""
    x = x - w
    """
)

pop = Population(neuron=neuron, size=10)
pop2 = Population(neuron=neuron, size=10)

conn = Connection(pre=pop, post=pop2, synapse=synapse, connection_type=ConnectionType.AllToAllConnection())

net = Network(populations=[pop, pop2], connections=[conn], variables="n = 2")

net.compile()

net.simulate(8000, 1)
