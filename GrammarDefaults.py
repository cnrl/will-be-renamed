import pyparsing as pp
from General import named_constants


_first = pp.Word(pp.alphas + "_", exact=1)
_rest = pp.Word(pp.alphanums + "_")
param_name = pp.Combine(_first + pp.Optional(_rest)).setResultsName("param name")

_int = pp.Word(pp.nums)
_long_int = pp.Combine(pp.Word(pp.nums) + pp.Optional(pp.Literal("L")))
_double = pp.Or([pp.Combine(pp.Optional(_int) + "." + _int), \
                    pp.Combine(_int + "." + pp.Optional(_int))])
param_value = pp.Or([_int, _long_int, _double] + \
                (lambda x: [pp.Literal(i) for i in x])(named_constants) \
                ).setResultsName("param value")

_scope_literals = ["population", "connection", "self", "global"]
param_scope = pp.Or((lambda x: [pp.Literal(i) for i in x])(_scope_literals)).setResultsName("param scope")

param_syntax = param_name + "=" + param_value + pp.Optional(":" + param_scope)
parameters_syntax = pp.OneOrMore(param_syntax + ";")
