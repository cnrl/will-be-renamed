"""Module containing a single class to build neuron instances.

Classes
-------
Neuron
    Base class to define a neuron.
"""

from cerebro.compiler.parser import VariableParser, EquationParser
from cerebro.models.parameter_guards import InstanceGuard
from cerebro.exceptions import IllegalArgumentException


class Neuron:
    """Base class to define a neuron.

    Attributes
    ----------
    variables : str
        A multi-line string, each line of which defines a variable.
    equations : str
        A multi-line string, each line of which defines an equation for normal functionality of the neuron.
    spike : str
        A string containing spike condition of the neuron.
    reset : str
        A string indicating equations by which variables should change after neuron resets.
    """

    def __init__(self, variables='', equations='', spike='', reset=''):
        """
        Parameters
        ----------
        variables : str
            A multi-line string, each line of which defines a variable.
            Template for each variable definition is as follows:
            name_of_variable = initial_value [: constraint_list]
            where "constraint_list" can have at most 3 elements separated with comma.
            Possible constraints are:
            1) data type constraints: Any of `int`, `double` or `float` can be defined as variable type constraint.
                Default type of variables is `float`.
            2) variability constraints: Any of words `constant` or `variable` can be used as variability constraint.
                All parameters are `variable` by default.
            3) scope constraints: Any of words `local` or `shared` can be used as scope constraint. Scope of all
                parameters is `local` by default.
        equations : str
            A multi-line string, each line of which defines an equation for normal functionality of the neuron.
            Each equation is either an ODE or a normal equation. In case of ODEs, the derivative should be placed
            on left hand side of the equation and everything else should be placed on the right hand side. In case
            of a normal equation, the variable value of which is meant to be changed should be placed on left hand
            side and the rest is placed on right hand side.
        spike : str
            A string containing spike condition of the neuron.
        reset : str
            A multi-line string indicating equations by which variables should change after neuron resets.

        Raises
        ------
        IllegalArgumentException : If arguments are not of appropriate type.
        """

        # parameter validation
        if not InstanceGuard(str).is_valid(variables):
            raise IllegalArgumentException(self.__class__.__name__ + ".variables must be an string")
        if not InstanceGuard(str).is_valid(equations):
            raise IllegalArgumentException(self.__class__.__name__ + ".equations must be an string")
        if not InstanceGuard(str).is_valid(spike):
            raise IllegalArgumentException(self.__class__.__name__ + ".spike must be an string")
        if not InstanceGuard(str).is_valid(reset):
            raise IllegalArgumentException(self.__class__.__name__ + ".reset must be an string")

        self.variables = VariableParser.from_lines(variables)
        self.equations = EquationParser.from_lines(equations)
        self.spike = spike
        self.reset = EquationParser.from_lines(reset)

    def __repr__(self):
        return self.__class__.__name__ + """(
        Variables:
        """ + str(self.variables) + """
        Equations of the variables:
        """ + str(self.equations) + """
        Spiking condition:
        """ + str(self.spike) + """
        Reset after a spike:
        """ + str(self.reset) + ")"
