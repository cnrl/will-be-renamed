from sympy import sympify, symbols, Eq

from cnrl.parser.Lexer import parameters_lexer, equations_lexer, variable_lexer, conditional_equations_lexer


def parse_parameters(parameters):
    return parameters_lexer(parameters)


def parse_equations(equations):
    equations = equations_lexer(equations)
    variables = variable_lexer(equations)
    eqs = []
    for eq in equations:
        lhs = sympify(eq["lhs"], evaluate=False)
        rhs = sympify(eq["rhs"], evaluate=False)
        eqs.append(Eq(lhs, rhs))
    return eqs, variables


def parse_conditions(conditions):
    return conditional_equations_lexer(conditions)


def parse_mathematical_expr(expr):
    return sympify(expr, evaluate=False)
