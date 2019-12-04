import matplotlib.pyplot as plt
import numpy as np

state = {}
is_plot = 1
variable = 'v'
context = 'Population1'


def get_state_callback(state):
    global is_plot
    global context
    global variable
    print(is_plot)
    if is_plot == 1:
        plt.ion()
        plt.clf()
        y = state[context][variable]
        plt.plot(y)
        plt.draw()
        plt.pause(0.001)


def plot(cntx, vrl):
    global is_plot
    global context
    global variable
    is_plot = 1
    variable = vrl
    context = cntx