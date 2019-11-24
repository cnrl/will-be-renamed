"""A module for parsing variables and equations, written in a neuron or synapse definition.
TODO complete doc and check doc syntax when online

Classes
-------
VariableParser
    Base class to parse variables.
EquationParser
    Base class to parse equations.
"""


import re

from cerebro.globals import VARIABLE_NAME_PATTERN, NUMERAL_PATTERN, WORD_PATTERN
from cerebro.exceptions import ParseException


class VariableParser:
    """Base class to parse variables.

    Attributes
    ----------
    VARIABLE_DEFINITION_PATTERN : (static)
        Holds pattern object for compiled regular expression pattern of variable definition.

    Static Methods
    --------------
    parse(definition)
        Returns the parsed variable after matching definition with VARIABLE_DEFINITION_PATTERN.
    from_lines(definitions)
        Returns the list of line-by-line-parsed variables.
    """
    class ParsedVariable:
        def __init__(self, name, init, constraints):
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
        return [
            VariableParser.parse(definition) for definition in definitions.split('\n') if definition.strip()
        ]


class EquationParser:
    """Base class to parse variables.

    Attributes
    ----------
    ODE_PATTERN : (static)
        Holds pattern object for compiled regular expression pattern of an ODE definition.
    SIMPLE_PATTERN : (static)
        Holds pattern object for compiled regular expression pattern of a simple equation definition.

    Static Methods
    --------------
    parse(definition)
        Returns the parsed equation after matching definition with ODE_PATTERN and SIMPLE_PATTERN.
    from_lines(definitions)
        Returns the list of line-by-line-parsed equations.
    """
    class ParsedEquation:
        def __init__(self, variable, expression, equation_type):
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
        return [
            EquationParser.parse(equation) for equation in equations.split('\n') if equation.strip()
        ]
