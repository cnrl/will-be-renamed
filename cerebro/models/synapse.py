"""Module containing a single to define a synapse.

Classes
-------
Synapse
    Base class to define a synapse.
"""

from cerebro.exceptions import IllegalArgumentException
from cerebro.models.parameter_guards import InstanceGuard
from cerebro.compiler.parser import VariableParser, EquationParser


class Synapse:
    """Base class to define a synapse.

    Attributes
    ----------
    variables : str
        A multi-line string, each line of which defines a variable.
    equations : str
        A multi-line string, each line of which defines an equation.
    """

    def __init__(self, variables='', equations='', pre_spike='', post_spike=''):
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
            A multi-line string, each line of which defines an equation.
            Each equation is either an ODE or a normal equation. In case of ODEs, the derivative should be placed
            on left hand side of the equation and everything else should be placed on the right hand side. In case
            of a normal equation, the variable value of which is meant to be changed should be placed on left hand
            side and the rest is placed on right hand side.

        Raises
        ------
        IllegalArgumentException : If arguments are not of appropriate type.
        """

        # parameter validation
        if not InstanceGuard(str).is_valid(variables):
            raise IllegalArgumentException(self.__class__.__name__ + ".variables must be an string")
        if not InstanceGuard(str).is_valid(equations):
            raise IllegalArgumentException(self.__class__.__name__ + ".equations must be an string")
        if not InstanceGuard(str).is_valid(pre_spike):
            raise IllegalArgumentException(self.__class__.__name__ + ".pre_spike must be an string")
        if not InstanceGuard(str).is_valid(post_spike):
            raise IllegalArgumentException(self.__class__.__name__ + ".post_spike must be an string")

        self.variables = VariableParser.from_lines(variables)
        self.equations = EquationParser.from_lines(equations)
        self.pre_spike = EquationParser.from_lines(pre_spike)
        self.post_spike = EquationParser.from_lines(post_spike)

    def __repr__(self):
        return self.__class__.__name__ + """(
            Variables:
            """ + str(self.variables) + """
            Equations of the variables:
            """ + str(self.equations) + """
            PreSpike equations:
            """ + str(self.pre_spike) + """
            PostSpike equations:
            """ + str(self.post_spike) + ")"
