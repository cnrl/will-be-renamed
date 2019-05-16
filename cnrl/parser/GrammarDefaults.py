import pyparsing as pp
from cnrl.api.models.General import named_constants, variables

# parameter grammar
_first = pp.Word(pp.alphas + "_", exact=1)
_rest = pp.Word(pp.alphanums + "_")
param_name = pp.Combine(_first + pp.Optional(_rest)).setResultsName("param name")

_int = pp.Word(pp.nums)
_sign = pp.Optional(pp.Or(pp.Literal("-") + pp.Literal("+")))
_signed_int = _sign + _int
_long_int = pp.Combine(_sign + pp.Word(pp.nums) + pp.Optional(pp.Literal("L")))
_double = pp.Or([pp.Combine(pp.Optional(_signed_int) + "." + _int),
                 pp.Combine(_signed_int + "." + pp.Optional(_int))])
param_value = pp.Or([_signed_int, _long_int, _double] +
                    (lambda x: [pp.Literal(i) for i in x])(named_constants)
                    ).setResultsName("param value")

_scope_literals = ["population", "connection", "self", "global"]
param_scope = pp.Or((lambda x: [pp.Literal(i) for i in x])(_scope_literals)).setResultsName("param scope")

param_syntax = param_name + "=" + param_value + pp.Optional(":" + param_scope)
parameters_syntax = pp.OneOrMore(param_syntax + ";")

# equation grammar
_mid_symbols = (lambda x: [pp.Literal(i) for i in x])(["=", "+=", "-=", "*=", "/=", "%="])
_operators = (lambda x: [pp.Literal(i) for i in x])(["-", "+", "/", "*", "**", "%"])
_d = pp.Literal("d")
_ode_left = pp.Combine(_d + pp.Or(variables) + pp.Literal("/") + _d + pp.Literal("t")).setResultsName("ode lhs")
_operand = pp.Or([param_name, param_value])
_rhs_single = pp.Combine(_operand + pp.Or(_operators) + _operand)
_rhs = pp.Combine(_rhs_single + pp.OneOrMore(pp.Optional(pp.Or(_operators) + _operand))).setResultsName("rhs")
_normal_eq_left = pp.Or(variables).setResultsName("normal lhs")
_ode = pp.Combine(_ode_left + pp.Or(_mid_symbols) + _rhs).setResultsName("ode")
_normal_eq = pp.Combine(_normal_eq_left + pp.Or(_mid_symbols) + _rhs).setResultsName("normal")
eq_syntax = pp.Or([_ode, _normal_eq])
equations_syntax = pp.OneOrMore(eq_syntax + ";")
