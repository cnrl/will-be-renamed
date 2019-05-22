from sympy import sympify, Eq

from cnrl.parser.Lexer import parameters_lexer, equations_lexer, conditional_equations_lexer
from cnrl.exceptions import ParserException


def parse_parameters(parameters):
    return parameters_lexer(parameters)


def parse_equations(equations):
    equations = equations_lexer(equations)
    eqs = []
    for eq in equations:
        rhs = eq["rhs"].replace("pre.", "_pre_")
        rhs = rhs.replace("post.", "_post_")
        lhs = eq["lhs"].replace("pre.", "_pre_")
        lhs = lhs.replace("post.", "_post_")
        try:
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
    eqs, var = parse_equations(equations)
    for eq in eqs:
        if eq["is_ode"]:
            raise ParserException("Reset equation can not be an ODE")
    return eqs, var


def parse_conditions(conditions):
    return conditional_equations_lexer(conditions)


def parse_mathematical_expr(expr):
    return sympify(expr, evaluate=False)
