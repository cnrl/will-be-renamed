General Structure
=================

Fundamentals
------------

In Cerebro, a neural network comprises a number of neuronal populations, connected with connection objects. Each
connection object has a connectivity pattern, through which synapses are generated between neurons.

Each Neuron is defined by some variables and different equations, i.e. equations by which the variables are modified
through the simulation process, equations defining variables after spike reset, and logical expressions defining the
spike condition. Each synapse is also defined by some variables and numerous equations, some of which are applied only
if pre/post-synaptic neuron fires.

Variables can be either local to each neuron(or synapse), shared through the whole population(or connection), or defined
globally in the network. They can also be defined as constants so that they would never change in a simulation.

After defining a network and its elements, the network should be compiled. In compilation process, the variables and
equations are inserted in the code and an equivalent C++ code will be generated for further simulations. This transition
from python to C++ enables the network to run faster. In simulation, the network runs for a specific duration and each
part can be monitored for capturing the network state and performance.

Code Structure
--------------

The first step to write a script is to import the package:

.. code-block:: python

    from cerebro.models import *


As described previously, the network is built in a bottom-up manner. So the next step would be to define the neurons
and synapses. Let's define a neuron with following properties:

.. code-block:: python

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


And consider a synapse to be defined as below:

.. code-block:: python

    synapse = Synapse(
        variables="""
            p = 0 : shared
            tau = 12 : constant
            w = 1
            x = 3
        """,
        equations="""
            x = p + tau + _post_v - n + Uniform(0, 1)
            dw/dt = w - 0.1
        """,
        pre_spike="""
        x = x + w
        """,
        post_spike="""
        x = x - w
        """
    )


Where ``n`` will be defined as a global variable in the network and ``_post_v`` refers to variable ``v`` of the
post-synaptic neuron(In design procedure, we know which neurons are going to be connected through this synapse).

After defining our neuron(s) and synapse(s), the more high-level blocks can be made:

.. code-block:: python

    pop0 = Population(neuron=neuron, size=10)
    pop1 = Population(neuron=neuron, size=10)

    connection = Connection(pre=pop0, post=pop1, synapse=synapse, connection_type=connection_type.AllToAllConnection())

    network = Network(populations=[pop0, pop1], connections=[connection], variables="n = 2")


Now that the whole network is defined, we can compile it and simulate the network for some duration according to some
step size dt:

.. code-block:: python

    network.compile()
    network.simulate(duration=10, dt=0.1)

So this is the basic network definition. There are ways to monitor variables while simulating. This functionality,
together with more detailed descriptions of above blocks and other properties will be explained in the tutorial.