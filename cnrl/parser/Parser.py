from sympy import sympify, Eq

from cnrl.parser.Lexer import parameters_lexer, equations_lexer, variable_lexer, conditional_equations_lexer


def parse_parameters(parameters):
    return parameters_lexer(parameters)


def parse_equations(equations):
    equations = equations_lexer(equations)
    eqs = []
    for eq in equations:
        lhs = sympify(eq["lhs"], evaluate=False)
        rhs = sympify(eq["rhs"], evaluate=False)
        constraints = eq["constraint"]  # TODO check constraint validity(syntax)
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
            raise Exception("Reset equation can not be an ODE")
    return eqs, var


def parse_conditions(conditions):
    return conditional_equations_lexer(conditions)


def parse_mathematical_expr(expr):
    return sympify(expr, evaluate=False)
