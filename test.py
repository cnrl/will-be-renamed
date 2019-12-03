from cerebro.models import Neuron, Synapse, Network, Population, Connection, ConnectionType
from cerebro.preprocessors.ImagePopulation import ImagePopulation
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
        w = 1
        x = 3
    """,
    equations="""
        x = p + tau + _post_v - n + Uniform(2, 3)
        dw/dt = w + 1 + delay
    """,
    pre_spike="""
    x = x + w
    """,
    post_spike="""
    x = x - w
    """
)

image_pop = ImagePopulation(400, '/home/atenagm/cnrl/code/cerebro/akse.jpg', "DoG", size_of_gaussian_1=0.2, size_of_gaussian_2=0.1)
# image_pop.set_image('/home/atenagm/cnrl/code/cerebro/akse.jpg')

pop = Population(neuron=neuron, size=10)

conn = Connection(pre=image_pop, post=pop, synapse=synapse, connection_type=ConnectionType.AllToAllConnection())

net = Network(populations=[pop, image_pop], connections=[conn], variables="n = 2")

net.compile()

net.simulate(8000, 1)
