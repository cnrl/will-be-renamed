from cnrl.GrammarDefaults import parameters_syntax


def parse_parameters(parameters):
    return parameters_syntax.parseString(parameters)


# string = """salam = 5:self; khubi=6:self;
#             hashem=0;"""
# print(parse_parameters(string))
