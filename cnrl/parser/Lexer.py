from re import split, compile, findall

from cnrl.globals import named_constants, keywords
from cnrl.exceptions import ParserException


def is_name_valid(name):
    """
    Check if a user-defined name is valid. name can start with a letter and can only contain
    alphnumerals and _.
    :param name: str
    :return: bool
    """
    pattern = compile("^[a-zA-Z][a-zA-Z0-9_]*$")
    if not pattern.match(name) or name in named_constants or name in keywords:
        return False
    return True


def is_value_valid(value):
    """
    Check if the syntax given for the value of a parameter or variable is correct.
    :param value: str
    :return: bool
    """
    numerical_pattern = compile("[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?")
    if not numerical_pattern.match(value) and value not in named_constants:
        return False
    return True


def is_scope_valid(scope):
    """
    Check if the syntax for scope/constraint of a parameter is valid or not.
    :param scope: str
    :return: bool
    """
    if scope not in ["population", "connection", "self", "global"]:
        return False
    return True


def parameters_lexer(parameters):
    """
    Lex the input string for parameters argument in a neuron or synapse. It returns
    a dictionary with name of parameter as the keys. The values are dictionaries with scope,
    init, and ctype as keys. If no scope and type is given as constraint to parameter, self
    and double will be placed, respectively.
    Example:
    parameters=\"\"\"
        x = 0.0 : population
                \"\"\"
    { 'x': {'scope': 'population', 'ctype': 'double', 'init': '0.0'}}
    :param parameters: str
    :return: dict
    """
    params = {}
    if parameters != "":
        lines = split("[\n;]", parameters)
        lines = (lambda x: [i.strip() for i in x])(lines)
        for line in lines:
            if not line:
                continue
            param_pieces = split("[=:]", line)
            if len(param_pieces) < 2 or len(param_pieces) > 3:
                raise ParserException("Invalid syntax for parameters argument")
            else:
                name = param_pieces[0].strip()
                if not is_name_valid:
                    raise ParserException("Invalid name for a parameter")
                value = param_pieces[1].strip()
                if not is_value_valid(value):
                    raise ParserException("Invalid value for a parameter")

                if len(param_pieces) > 2:
                    scope = param_pieces[2].strip()
                    if not is_scope_valid(scope):
                        raise ParserException("Invalid flag for a parameter")
                else:
                    scope = "self"

            value = float(value)
            if name in params:
                raise Exception("{} is already defined".format(name))
            params[name] = {
                "init": value,
                "scope": scope,
                "ctype": "double"
            }

    return params


def ode_var_name(lhs):
    """
    Extracts gradient variable in an ODE.
    :param lhs: str
    :return: list
    """
    return findall("d([\w]+)/dt", lhs)


def equations_lexer(equations):
    """
    Lex the input string for equations argument in a neuron or synapse. The equation is
    either a normal equation or an ODE. For a normal equation, the left hand side should
    only contain the variable whose values will change. For an ODE, the left hand side
    should be the derivative expression d[var]/dt where [var] is the variable whose values
    will change. This function will return a list of dictionaries. Each dictionary contains
    lhs, rhs, constraint, and is_ode as its keys.
    Example:
    equations=\"\"\"
        g_exc += x + 3
        dv/dt = 5*x + 4 : init = 0.1
            \"\"\"
    [{"lhs": "g_exc", "rhs": "g_exc + (x + 3)", "constraint": "", "is_ode": False},
     {"lhs": "dv/dt", "rhs": "5*x + 4", "constraint": "init = 0.1", "is_ode": True}]
    :param equations: str
    :return: list
    """
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
                    raise ParserException("Invalid syntax for an equation")
                op = split("=", eq)[0][-1]
                if op in ["+", "-", "*", "/", "%"]:
                    rhs = lhs + op + "(" + rhs + ")"
            except ValueError:
                raise ParserException("Invalid syntax for an equation")

            is_ode = len(ode_var_name(lhs)) == 1
            eqs.append({"lhs": lhs,
                        "rhs": rhs,
                        "constraint": flag,
                        "is_ode": is_ode})
    return eqs


def variable_lexer(equations):
    """
    Extract variable name from an equation. It returns a dictionary similar to
    what did the parameter_lexer. It has one more key in each value of the dict
    which is rhs of the equation in which the variable is defined.
    :param equations: str
    :return: dict
    """
    variables = {}
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
                raise ParserException("Invalid syntax for an equation")
        constraint = eq["constraints"]
        if constraint is not "":
            flag = (lambda x: [i.strip() for i in x])(split("=", constraint, maxsplit=1))
            if flag[0] != "init":
                raise ParserException("Invalid constraint for an equation")
            try:
                val = flag[1]
                if not is_value_valid(val):
                    raise ParserException("Invalid constraint for an equation")
            except IndexError:
                raise ParserException("Invalid constraint for an equation")
        else:
            val = "0.0"

        rhs = eq["rhs_parsed"]
        val = float(val)
        variables[name] = {
              "init": val,
              "scope": "self",
              "ctype": "double",
              "rhs": rhs
        }
    return variables


def conditional_equations_lexer(equations):
    """
    Lex the input string for spike argument in a neuron. It follows the pattern
    lhs op rhs
    where lhs is a variable, op is either >, <, >=, <=, !=, or ==, and rhs is a
    value. It returns a list of dictionaries with lhs, rhs, and op as the keys.
    :param equations: str
    :return: list
    """
    eqs = []
    eq = equations
    if equations != "":
        try:
            lhs, rhs = (lambda x: [i.strip() for i in x])(split("[\>\<]=?", eq))
            if rhs is "":
                raise ParserException("Invalid syntax for an equation")
            op = findall("[\>\<]=?", eq)
        except ValueError:
            try:
                lhs, rhs = (lambda x: [i.strip() for i in x])(split("[\!=]=", eq))
                if rhs is "":
                    raise ParserException("Invalid syntax for an equation")
                op = findall("[\!=]=?", eq)
            except ValueError:
                raise ParserException("Invalid syntax for an equation")

        eqs.append({"lhs": lhs,
                    "rhs": rhs,
                    "op": op})
    return eqs
