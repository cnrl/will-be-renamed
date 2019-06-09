from sympy import sympify, Eq
from sympy.core.symbol import Symbol

from cerebro.parser.lexer import parameters_lexer, equations_lexer, conditional_equations_lexer, ode_var_name
from cerebro.exceptions import ParserException


def parse_parameters(parameters):
    """
    Parse parameters argument in a neuron or synapse. It returns
    a dictionary with name of parameter as the keys. The values are dictionaries with scope,
    init, and ctype as keys. If no scope and type is given as constraint to parameter, self
    and double will be placed, respectively.
    Example:
    parameters=\"\"\"
        x = 0.0 : population
                \"\"\"
    { 'x': {'scope': 'population', 'ctype': 'double', 'init': '0.0'}}
    :param parameters: str
    :return: dict
    """
    return parameters_lexer(parameters)


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
        rhs = eq["rhs"].replace("pre.", "_pre_")
        rhs = rhs.replace("post.", "_post_")
        lhs = eq["lhs"].replace("pre.", "_pre_")
        lhs = lhs.replace("post.", "_post_")

        if eq['is_ode']:
            lhs = Symbol(ode_var_name(lhs)[0])
        try:
            if not eq['is_ode']:
                lhs = sympify(lhs, evaluate=False)
            rhs = sympify(rhs, evaluate=False)
        except Exception:
            raise ParserException("Invalid syntax for equation")
        constraints = eq["constraint"]
        eqs.append({"lhs_parsed": lhs,
                    "rhs_parsed": rhs,
                    "is_ode": eq["is_ode"],
                    "constraints": constraints,
                    "equation_parsed": Eq(lhs, rhs)})
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
            raise ParserException("Reset equation can not be an ODE")
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


def check_variable_definition(equations, parameters, builtins):
    """
    Check if all symbols in an equation are defined. An exception is raised in case
    a variable or parameter is not defined.
    :param equations: str
    :param parameters: dict
    :param builtins: tuple
    :return: None
    """
    # TODO check pre.variable and post.variable differently and right
    builtins = {Symbol(builtin_symbol) for builtin_symbol in builtins}
    for eq in equations.equations_list:
        for sym in (eq["rhs_parsed"].atoms() or eq["lhs_parsed"].atoms()) - set(builtins):
            if isinstance(sym, Symbol) and str(sym) not in parameters and not str(sym).startswith('_'):
                raise ParserException("{} is not defined in this scope.".format(sym))