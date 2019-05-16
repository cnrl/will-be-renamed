from cnrl.parser.GrammarDefaults import parameters_syntax, equations_syntax


def parse_parameters(parameters):
    return parameters_syntax.parseString(parameters)


def parse_equations(equations):
    return equations_syntax.parseString(equations)


# string = """salam = 5:self; khubi=6:self;
#             hashem=0;"""
# print(parse_parameters(string))
