from sympy.parsing.sympy_parser import parse_expr
from sympy.abc import x
from sympy import *


class DecisionMaker:

    """
    This class provides arbitrary decision maker
    x is spike number of neuron in last interval size of spike history
    policy is a function describing the possibility of winning based on x (not from 100, just comparative)

    Defining policy using different neuron-related functions rather than spike number
    & Defining policy for population including multiple neurons will implement later

    """

    history = []
    _instance_count = 0
    _interval = 5

    def __init__(self, policy='', name=None, population_attribute=None, neuron_attribute= None):
        self.policy = policy
        self.population_attribute = population_attribute or "mn_spikes"
        self.neuron_attribute= neuron_attribute or "n_spikes"
        self.name = name or "Decision Maker".format(self._instance_count)
        self._instance_count += 1

    def update_history(self, history):
        self.history = history

    def choose(self, population=None, new_history=None, new_interval=None):

        if new_history:
            self.update_history(new_history)
        if new_interval:
            self._interval = new_interval
        p_func = parse_expr(self.policy)
        possibilities = [p_func.evalf(subs={x: self.history[i].count(1)}) for i in range(len(self.history))]
        s = sum(possibilities)
        possibilities = [e/s for e in possibilities]
        print("Winner is population", possibilities.index(max(possibilities))+1)
        return possibilities


# mv_module = DecisionMaker('x', "Majority_voting")
# h = [
#     [1, 0, 0, 1, 0],
#     [0, 1, 0, 1, 1],
#     [0, 1, 1, 1, 0],
#     [1, 0, 1, 1, 1]
# ]
# print(mv_module.choose(new_history=h))
