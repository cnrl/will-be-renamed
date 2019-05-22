from re import split, compile, findall

from cnrl.globals import named_constants, keywords


def is_name_valid(name):
    pattern = compile("^[a-zA-Z][a-zA-Z0-9_]*$")
    if not pattern.match(name) or name in named_constants or name in keywords:
        return False
    return True


def is_value_valid(value):
    numerical_pattern = compile("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
    if not numerical_pattern.match(value) and value not in named_constants:
        return False
    return True


def is_scope_valid(scope):
    if scope not in ["population", "connection", "self", "global"]:
        return False
    return True


def parameters_lexer(parameters):
    params = []
    if parameters != "":
        lines = split("[\n;]", parameters)
        lines = (lambda x: [i.strip() for i in x])(lines)
        # TODO Handle syntax error(apply a regular expression)
        for line in lines:
            if not line:
                continue
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

                if len(param_pieces) > 2:
                    scope = param_pieces[2].strip()
                    if not is_scope_valid(scope):
                        # TODO generate custom exception
                        raise Exception("Invalid flag for a parameter")
                else:
                    scope = "self"

            value = float(value)
            params.append({"name": name,
                           "init": value,
                           "scope": scope,
                           "ctype": "double"})

    return params


def ode_var_name(lhs):
    return findall("d([\w]+)/dt", lhs)


def equations_lexer(equations):
    eqs = []
    if equations != "":
        lines = split("[\n;]", equations)
        lines = (lambda x: [i.strip() for i in x])(lines)
        for line in lines:
            if not line:
                continue
            try:
                eq, flag = split("[:]", line, maxsplit=1)
            except ValueError:
                eq = line
                flag = ""

            try:
                lhs, rhs = (lambda x: [i.strip() for i in x])(split("[+\-/*%]?=", eq))
                if rhs is "":
                    # TODO generate custom exception
                    raise Exception("Invalid syntax for an equation")
                op = split("=", eq)[0][-1]
                if op in ["+", "-", "*", "/", "%"]:
                    rhs = lhs + op + "(" + rhs + ")"
            except ValueError:
                # TODO generate custom exception
                raise Exception("Invalid syntax for an equation")

            is_ode = len(ode_var_name(lhs)) == 1
            eqs.append({"lhs": lhs,
                        "rhs": rhs,
                        "constraint": flag,
                        "is_ode": is_ode})
    return eqs


def variable_lexer(equations):
    variables = []
    for eq in equations:
        lhs = str(eq["lhs_parsed"])
        print(lhs)
        if is_name_valid(lhs):
            name = lhs
        else:
            name = ode_var_name(lhs)
            if len(name) == 1:
                name = name[0].strip()
            else:
                # TODO generate custom exception
                raise Exception("Invalid syntax for an equation")
        constraint = eq["constraints"]
        if constraint is not "":
            flag = (lambda x: [i.strip() for i in x])(split("=", constraint, maxsplit=1))
            if flag[0] != "init":
                # TODO generate custom exception
                raise Exception("Invalid constraint for an equation")
            try:
                val = flag[1]
                if not is_value_valid(val):
                    # TODO generate custom exception
                    raise Exception("Invalid constraint for an equation")
            except IndexError:
                # TODO generate custom exception
                raise Exception("Invalid constraint for an equation")
        else:
            val = "0.0"

        rhs = eq["rhs_parsed"]
        val = float(val)
        variables.append({"name": name,
                          "init": val,
                          "scope": "self",
                          "ctype": "double",
                          "rhs": rhs})
    return variables


def conditional_equations_lexer(equations):
    # TODO extend this function more complex conditional equations
    eqs = []
    eq = equations
    if equations != "":
        try:
            lhs, rhs = (lambda x: [i.strip() for i in x])(split("[\>\<]=?", eq))
            if rhs is "":
                # TODO generate custom exception
                raise Exception("Invalid syntax for an equation")
            op = findall("[\>\<]=?", eq)
        except ValueError:
            try:
                lhs, rhs = (lambda x: [i.strip() for i in x])(split("[\!=]=", eq))
                if rhs is "":
                    # TODO generate custom exception
                    raise Exception("Invalid syntax for an equation")
                op = findall("[\!=]=?", eq)
            except ValueError:
                # TODO generate custom exception
                raise Exception("Invalid syntax for an equation")

        eqs.append({"lhs": lhs,
                    "rhs": rhs,
                    "op": op})
    return eqs
