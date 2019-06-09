from sympy import sympify, Eq
from sympy.core.symbol import Symbol

from cerebro.parser.param_extractor import equations_lexer, variables_lexer
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

        try:
            rhs = sympify(rhs, evaluate=False)
        except Exception:
            raise ParseException("Invalid syntax for equation")

        eqs.append({"lhs_parsed": eq["lhs"], "rhs_parsed": rhs, "ode": eq["ode"]})

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
        if eq["is_ode"]:
            raise ParseException("Reset equation can not be an ODE")
    return eqs


def parse_conditions(conditions):
    """
        Parse the input string for spike argument in a neuron. It follows the pattern
        lhs op rhs
        where lhs is a variable, op is either >, <, >=, <=, !=, or ==, and rhs is a
        value. It returns a list of dictionaries with lhs, rhs, and op as the keys.
        :param conditions: str
        :return: list
        """
    return conditional_equations_lexer(conditions)


def parse_mathematical_expr(expr):
    return sympify(expr, evaluate=False)


def check_variable_definition(equations, variables, builtins):
    """
    Check if all symbols in an equation are defined. An exception is raised in case
    a variable or variable is not defined.
    :param equations: str
    :param variables: dict
    :param builtins: tuple
    :return: None
    """
    # TODO check pre.variable and post.variable differently and right
    builtins = {Symbol(builtin_symbol) for builtin_symbol in builtins}
    for eq in equations.equations_list:
        for sym in (eq["rhs_parsed"].atoms() or eq["lhs_parsed"].atoms()) - set(builtins):
            if isinstance(sym, Symbol) and str(sym) not in variables and not str(sym).startswith('_'):
                raise ParseException("{} is not defined in this scope.".format(sym))
