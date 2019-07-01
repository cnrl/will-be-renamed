import re

from cerebro.globals import NAME_PATTERN, NUMERAL_PATTERN, VARIABLE_CONSTRAINTS
from cerebro.exceptions import ParseException
from cerebro.enums import VariableContext


def variables_lexer(variables):
    """
    Lex the input string for variables argument in a neuron or synapse. It returns
    a dictionary with name of variable as the keys. The values are dictionaries with scope,
    init, and ctype as keys. If no scope and type is given as constraint to variable, self
    and double will be placed, respectively.
    Example:
    variables=\"\"\"
        x = 0.0 : population
                \"\"\"
    { 'x': {'scope': 'population', 'ctype': 'double', 'init': '0.0', 'const': True}}
    :param variables: str
    :return: dict
    """

    keywords_pattern = "(" + '|'.join(map(lambda x: '{}\s*'.format(x), VARIABLE_CONSTRAINTS)) + ")+"
    scoped_pattern = "^\s*(?P<NAME>{})\s*=\s*(?P<VALUE>{})\s*:\s*(?P<CONSTRAINTS>{})\s*$".format(
        NAME_PATTERN, NUMERAL_PATTERN, keywords_pattern
    )
    not_scoped_pattern = "^\s*(?P<NAME>{})\s*=\s*(?P<VALUE>{})\s*$".format(NAME_PATTERN, NUMERAL_PATTERN)

    params = {}

    for line in [part for part in variables.split('\n') if part.strip()]:
        matched = re.compile(scoped_pattern).search(line)

        if matched is None:
            matched = re.compile(not_scoped_pattern).search(line)

        if matched is None:
            raise ParseException("invalid variable definition: {}".format(line))

        groups = matched.groupdict()

        var_name = groups.get("NAME")
        var_value = groups.get("VALUE")
        var_constraints = groups.get("CONSTRAINTS")

        # var_specs = {'ctype': "double", 'init': var_value, 'const': False, 'scope': 'local'}
        var_specs = {'init': var_value, 'constraints': var_constraints}
        # if var_constraints is not None:
        #     split_constraints = var_constraints.split()
        #     check_variable_constraints(split_constraints, context)
        #     apply_variable_constraints(var_specs, split_constraints)

        params[var_name] = var_specs

    return params


def check_variable_constraints(constraints, context):
    """
    Checks constraints, defined in front of each variable.
    :param constraints: str
    :param context: str
    :return: None
    """
    scopes = ['population', 'connection', 'local']
    scopes_appearance = map(lambda x: x in constraints, scopes)
    if sum(scopes_appearance) > 1:
        raise ParseException("too many scope constraints")

    if context == VariableContext.NEURON:
        if 'connection' in constraints:
            raise ParseException("bad scope constraint")
    else:
        if 'population' in constraints:
            raise ParseException("bad scope constraint")


def apply_variable_constraints(var_specs, constraints):
    """
    Set variable constraint elements in variables' dictionary.
    :param var_specs: dict
    :param constraints: list of str
    :return: None
    """
    for constraint in constraints:
        if constraint == 'const':
            var_specs.update({'const': True})

        if constraint == 'population':
            var_specs.update({'scope': 'population'})

        if constraint == 'connection':
            var_specs.update({'scope': 'connection'})

        if constraint == 'local':
            var_specs.update({'scope': 'local'})


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
        dv/dt = 5*x + 4
            \"\"\"
    [{"lhs": "g_exc", "rhs": "g_exc + (x + 3)", "ode": False},
     {"lhs": "dv/dt", "rhs": "5*x + 4", "ode": True}]
    :param equations: str
    :return: list
    """

    ode_pattern = "^\s*d(?P<NAME>{})\s*\/\s*dt\s*=\s*(?P<RHS>.+)\s*$".format(NAME_PATTERN)
    simple_pattern = "^\s*(?P<NAME>{})\s*=\s*(?P<RHS>.+)\s*$".format(NAME_PATTERN)

    eqs = []

    for line in [part for part in equations.split('\n') if part.strip()]:
        eq_specs = {'lhs': None, 'rhs': None, 'equation_type': 'simple'}

        ode_matched = re.compile(ode_pattern).search(line)
        simple_matched = re.compile(simple_pattern).search(line)
        matched = None

        if ode_matched is not None:
            eq_specs.update({'equation_type': 'ode'})
            matched = ode_matched

        if simple_matched is not None:
            eq_specs.update({'equation_type': 'simple'})
            matched = simple_matched

        if matched is None:
            raise ParseException("invalid equation: {}".format(line))

        lhs = matched.groupdict().get("NAME")
        rhs = matched.groupdict().get("RHS")
        eq_specs.update({'lhs': lhs, 'rhs': rhs})

        eqs.append(eq_specs)

    return eqs
