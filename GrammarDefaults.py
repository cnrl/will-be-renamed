import pyparsing as pp
from General import named_constants

_first = pp.Word(pp.alphas + "_", exact=1)
_rest = pp.Word(pp.alphanums + "_")
param_name = pp.Combine(_first + pp.Optional(_rest)).setResultsName("param name")
_int = pp.Word(pp.nums)
_long_int = pp.Combine(pp.Word(pp.nums) + pp.Optional(pp.Literal("L")))
_double = pp.Or([pp.Combine(pp.Optional(_int) + "." + _int), \
                    pp.Combine(_int + "." + pp.Optional(_int))])
param_value = pp.Or([_int, _long_int, _double] + named_constants).setResultsName("param value")
