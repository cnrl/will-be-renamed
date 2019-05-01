from re import split
from CustomExceptions import Parameter_name_Exception


def parameters_string_manipulation(parameters):
    lines = split("[\n;]", parameters)
    lines = (lambda x: [i.strip() for i in x])(lines)
    # TODO Handle syntax error(apply a regular expression)
    params = (lambda x: [tuple(split("[=:]", i)) for i in x])(lines)
    return params


def parse_parameters(parameters):
    for param in parameters:
        pattern = re.compile("[a-zA-Z_]+")
        if not pattern.match(param[0]):
            raise(Parameter_name_Exception("Invalid syntax for name of a parameter"))

string = """salam=5; khubi?=tof:baqal
            hashem=0"""
parameters_string_manipulation(string)
