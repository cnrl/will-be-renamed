from re import split


def parameters_string_manipulation(parameters):
    lines = split("[\n;]", parameters)
    lines = (lambda x: [i.strip() for i in x])(lines)
    # TODO Handle syntax error(apply a regular expression)
    params = (lambda x: [tuple(split("[=:]", i)) for i in x])(lines)
    return params

string = """salam=5; khubi?=tof:baqal
            hashem=0"""
parameters_string_manipulation(string)
