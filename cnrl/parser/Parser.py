from sympy import sympify, symbols, Eq

from cnrl.parser.Lexer import parameters_lexer, equations_lexer, variable_lexer


def parse_parameters(parameters):
    return symbols(" ".join([param["name"] for param in parameters_lexer(parameters)]))


def parse_equations(equations, parameters):
    equations = equations_lexer(equations)
    variables = variable_lexer(equations)
    parameters = parse_parameters(parameters)
    variables = symbols(" ".join([var["name"] for var in variables]))
    eqs = []
    for eq in equations:
        lhs = sympify(eq["lhs"], evaluate=False)
        rhs = sympify(eq["rhs"], evaluate=False)
        eqs.append(Eq(lhs, rhs))
    return eqs, parameters, variables
