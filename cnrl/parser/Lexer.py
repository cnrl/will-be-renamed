from re import split, compile
from cnrl.api.models.General import named_constants, keywords


def is_name_valid(name):
    pattern = compile("[a-zA-Z_][a-zA-Z0-9_]*")
    if not pattern.match(name) or name in named_constants or name in keywords:
        return False
    return True


def is_value_valid(value):
    numerical_pattern = compile("[-+]?[0-9]+[.][0-9]*")
    if not numerical_pattern.match(value) and value not in named_constants:
        return False
    return True


def is_scope_valid(scope):
    if scope not in ["population", "connection", "self", "global"]:
        return False
    return True


def parameters_lexer(parameters):
    params = []
    lines = split("[\n;]", parameters)
    lines = (lambda x: [i.strip() for i in x])(lines)
    # TODO Handle syntax error(apply a regular expression)
    for line in lines:
        param_pieces = split("[=:]", line)
        if len(param_pieces) < 2 or len(param_pieces) > 3:
            # TODO generate custom exception
            raise Exception("Invalid syntax for parameters argument")
        else:
            name = param_pieces[0].strip()
            if not is_name_valid:
                # TODO generate custom exception
                raise Exception("Invalid name for a parameter")
            value = param_pieces[1].strip()
            if not is_value_valid(value):
                # TODO generate custom exception
                raise Exception("Invalid value for a parameter")
            eq = name + "=" + value
            if len(param_pieces) > 2:
                scope = param_pieces[2].strip()
                if not is_scope_valid(scope):
                    # TODO generate custom exception
                    raise Exception("Invalid flag for a parameter")
            else:
                scope = "self"

        params.append({"name": name,
                       "init": value,
                       "scope": scope,
                       "eq": eq})

    return params


def equations_lexer(equations):
    eqs = []
    lines = split("[\n;]", equations)
    lines = (lambda x: [i.strip() for i in x])(lines)
    for line in lines:
        try:
            eq, flag = split("[:]", line, maxsplit=1)
        except ValueError:
            eq = line
            flag = ""

        try:
            lhs, rhs = (lambda x: [i.strip() for i in x])(split("[+-/*%]?=", eq))
            if rhs is "":
                # TODO generate custom exception
                raise Exception("Invalid syntax for an equation")
            op = split("=", eq)[0][-1]
            if op in ["+", "-", "*", "/", "%"]:
                rhs = lhs + op + rhs
        except ValueError:
            # TODO generate custom exception
            raise Exception("Invalid syntax for an equation")

        # TODO check flag validity
        eqs.append({"lhs": lhs,
                    "rhs": rhs,
                    "constraint": flag})
    return eqs
