from sympy import sympify
from sympy.core.symbol import Symbol

from cerebro.compiler.param_extractor import equations_lexer, variables_lexer
from cerebro.exceptions import ParseException
from cerebro.globals import FORBIDDEN_CONNECTION_VAR_NAMES, FORBIDDEN_POPULATION_VAR_NAMES, RESERVED_WORDS
from cerebro.enums import VariableContext


def parse_variables(variables, context):
    """
    Parse variables argument in a neuron or synapse. It returns
    a dictionary with name of variable as the keys. The values are dictionaries with scope,
    init, and ctype as keys. If no scope and type is given as constraint to variable, self
    and double will be placed, respectively.
    Example:
    variables=\"\"\"
        x = 0.0 : population
                \"\"\"
    { 'x': {'scope': 'population', 'ctype': 'double', 'init': '0.0'}}
    :param variables: str
    :param context: VariableContext
    :return: dict
    """
    lexed = variables_lexer(variables, context)

    var_names = list(lexed.keys())
    for var_name in var_names:
        if context == VariableContext.NEURON and var_name in FORBIDDEN_POPULATION_VAR_NAMES:
            raise ParseException("{} is a reserved population variable name".format(var_name))
        if context == VariableContext.SYNAPSE and var_name in FORBIDDEN_CONNECTION_VAR_NAMES:
            raise ParseException("{} is a reserved connection variable name".format(var_name))
        if var_name in RESERVED_WORDS:
            raise ParseException("{} is a reserved core word".format(var_name))

    return lexed


def parse_equations(equations):
    """
    Parse equations argument in a neuron or synapse. It returns a list of dictionaries
    with keys lhs_parsed, rhs_parsed, is_ode, constraints, and equation_parsed.
    :param equations: str
    :return: list
    """
    equations = equations_lexer(equations)

    eqs = []

    for eq in equations:
        rhs = eq["rhs"].replace("pre.", "_pre_").replace("post.", "_post_")
        lhs = eq["lhs"]

        try:
            rhs = sympify(rhs, evaluate=False)
            lhs = Symbol(lhs)
        except Exception:
            raise ParseException("Invalid syntax for equation")

        eqs.append({"lhs_parsed": lhs, "rhs_parsed": rhs, "ode": eq["ode"]})

    return eqs


def parse_reset(equations):
    """
        Parse reset argument in a neuron. It returns a list of dictionaries with
        keys lhs_parsed, rhs_parsed, is_ode, constraints, and equation_parsed.
        It can not be and ODE!
        :param equations: str
        :return: list
        """
    eqs = parse_equations(equations)
    for eq in eqs:
        if eq["ode"]:
            raise ParseException("Reset equation can not be an ODE")

    return eqs


def parse_condition(conditions):
    """
        Parse the input string for spike argument in a neuron.
        :param conditions: str
        :return: list
        """
    try:
        return sympify(conditions, evaluate=False)
    except Exception:
        raise ParseException("Invalid syntax for spike conditions")
