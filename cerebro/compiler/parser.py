"""A module for parsing variables and equations, written in a neuron or synapse definition.

*Classes*:

* **VariableParser**:
    Base class to parse variables.

    - **ParsedVariable**:
        This class holds information of a parsed variable.

* **EquationParser**:
    Base class to parse equations.

    - **ParsedEquation**:
        This class holds information of a parsed equation.
"""


import re

from cerebro.globals import VARIABLE_NAME_PATTERN, NUMERAL_PATTERN, WORD_PATTERN
from cerebro.exceptions import ParseException


class VariableParser:
    """
    Base class to parse variables.
    """
    class ParsedVariable:
        """
        Holds name, initial value and constraints in a parsed variable.
        """
        def __init__(self, name, init, constraints):
            """
            :param name: Name of the variable
            :param init: Initial value of the variable
            :param constraints: Constraints defined for the variable

            :type name: str
            :type init: str
            :type constraints: str
            """
            self.name = name
            self.init = init
            self.constraints = constraints

    VARIABLE_DEFINITION_PATTERN = re.compile(
        "^\s*(?P<NAME>{})\s*=\s*(?P<INIT>{})\s*(:\s*(?P<CONSTRAINTS>({}\s*)*)\s*)?$".format(
            VARIABLE_NAME_PATTERN, NUMERAL_PATTERN, WORD_PATTERN
        )
    )

    @staticmethod
    def parse(definition):
        """This static method parses the definition of a variable.

        :param definition: Definition of a variable.

        :type definition: str

        :returns: Parsed variable, containing name, initial values and constraints of the defined variable.

        :rtype: cerebro.compiler.parser.VariableParser.ParsedVariable

        :raises: ParseException: If the definition is invalid.
        """
        matched = VariableParser.VARIABLE_DEFINITION_PATTERN.match(definition)

        if matched is None:
            raise ParseException("invalid variable definition: {}".format(definition))

        groups = matched.groupdict()
        constraints = (groups.get('CONSTRAINTS') or '').split()

        return VariableParser.ParsedVariable(
            name=groups["NAME"], init=groups["INIT"], constraints=constraints
        )

    @staticmethod
    def from_lines(definitions):
        """This static method splits variable definitions line by line and returns a list of parsed variables.

        :param definitions: Definition of some variables

        :type definitions: str

        :returns: List of parsed variables.

        :rtype: list
        """
        return [
            VariableParser.parse(definition) for definition in definitions.split('\n') if definition.strip()
        ]


class EquationParser:
    """
    Base class to parse variables.
    """
    class ParsedEquation:
        """
        Holds variable to change, expression by which it changes the variable and type of the equation(simple or ODE).
        """
        def __init__(self, variable, expression, equation_type):
            """
            :param variable: Variable to change
            :param expression: Expression by which the variable changes
            :param equation_type: Type of the equation(Simple or ODE)

            :type variable: str
            :type expression: str
            :type equation_type: str
            """
            self.variable = variable
            self.expression = expression
            self.equation_type = equation_type

    ODE_PATTERN = re.compile(
        "^\s*d(?P<NAME>{})\s*\/\s*dt\s*=\s*(?P<RHS>.+)\s*$".format(VARIABLE_NAME_PATTERN)
    )

    SIMPLE_PATTERN = re.compile(
        "^\s*(?P<NAME>{})\s*=\s*(?P<RHS>.+)\s*$".format(VARIABLE_NAME_PATTERN)
    )

    @staticmethod
    def parse(equation):
        """This static method parses the definition of an equation.

        :param equation: Definition of an equation.

        :type equation: str

        :returns: Parsed equation, containing equation's name, expression and type.

        :rtype: cerebro.compiler.parser.EquationParser.ParsedEquation

        :raises: ParseException: If the definition is invalid.
        """
        matched = EquationParser.ODE_PATTERN.match(equation)
        equation_type = 'ode' if matched is not None else 'simple'
        if matched is None:
            matched = EquationParser.SIMPLE_PATTERN.match(equation)

        if matched is None:
            raise ParseException('invalid equation')
        groups = matched.groupdict()

        return EquationParser.ParsedEquation(
            variable=groups['NAME'], expression=groups['RHS'], equation_type=equation_type
        )

    @staticmethod
    def from_lines(equations):
        """This static method splits equation definitions line by line and returns a list of parsed equations.

        :param equations: Definition of some variables

        :type equations: str

        :returns: List of parsed equations.

        :rtype: list
        """
        return [
            EquationParser.parse(equation) for equation in equations.split('\n') if equation.strip()
        ]
