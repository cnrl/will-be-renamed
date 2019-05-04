from re import split, compile
from CustomExceptions import Parameter_name_Exception


def parameters_string_manipulation(parameters):
    lines = split("[\n;]", parameters)
    lines = (lambda x: [i.strip() for i in x])(lines)
    # TODO Handle syntax error(apply a regular expression)
    params = (lambda x: [tuple((lambda y: [j.strip() for j in y])(split("[=:]", i))) for i in x])(lines)
    return params


def parse_parameters(parameters):
    for param in parameters:
        print(param)
        pattern = compile("[a-zA-Z_]+")
        if not pattern.match(param[0]):
            raise(Parameter_name_Exception("Invalid syntax for name of a parameter: " + param[0]))
        # TODO: add rest of paarameter parsing and resolve bug for name(khubi? is a valid name :/)

string = """salam = 5 ; khubi?=tof:baqal
            hashem=0"""
p = parameters_string_manipulation(string)
parse_parameters(p)
