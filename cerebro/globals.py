"""Objects with a wide range of use in the package

Objects
-------
FORBIDDEN_VARIABLE_NAMES : dict of .enums.VariableContext: set of str
    Set of meaningful variables in each context. These variables can not be redefined as variables in a context.
INTERNAL_VARIABLES : set of str
    Set of variables that can be explicitly used in an equation in a context.
RESERVED_WORDS : set of str
    Set of words that are reserved in the project and cannot be used as name of variables in a context.
PACKAGE_NAME : str
    Name of the package.
VARIABLE_NAME_PATTERN : str
    Regex template for context variable matches.
NUMERAL_PATTERN : str
    Regex template for numerals used in a context equation or variable.
WORD_PATTERN : str
    Regex template for words(i.e. non-numerals).
ACCEPTABLE_CONSTRAINTS : dict of str: dict of str: str/set of str
    Defines valid values for constraints used in context equations.
ACCEPTABLE_PROPRIETOR : set of str
    Defines valid proprietor words in context equations.
"""

from .enums import VariableContext

FORBIDDEN_VARIABLE_NAMES = {
    VariableContext.NEURON: {'t', 'dt', 'size', 'last_spike', 'spiked', 'r', 'g_exc'},
    VariableContext.SYNAPSE: {'t', 'dt', 'size', 'post_rank', 'pre_rank', 'inv_pre_rank', 'inv_post_rank'},
    VariableContext.NETWORK: set()
}

ADJECTIVE_VARIABLE_NAMES = {
    VariableContext.NEURON: set(),
    VariableContext.SYNAPSE: {'w', },
    VariableContext.NETWORK: set()
}

ACCEPTABLE_FUNCTION_NAMES = {'Normal', 'Uniform'}

INTERNAL_VARIABLES = {'t', 'g_exc'}

# TODO: complete list below
RESERVED_WORDS = {'population', 'connection', 'neuron', 'synapse', 'spike', 'reset', 'const', 'int', 'double', 'float'}

PACKAGE_NAME = 'Cerebro'

VARIABLE_NAME_PATTERN = "[A-Za-z][A-Za-z0-9_]*"
NUMERAL_PATTERN = "[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
WORD_PATTERN = "\w+"

FUNCTION_PATTERN = \
    "^(?P<function_name>{valid_functions})\((?P<param_1>{numeral_pattern}),\s* (?P<param_2>{numeral_pattern})\)$".format(
        valid_functions='|'.join(ACCEPTABLE_FUNCTION_NAMES),
        numeral_pattern=NUMERAL_PATTERN
    )

ACCEPTABLE_CONSTRAINTS = {
    'type': {
        'default': 'float',
        'values': {'double', 'integer', 'float'}
    },
    'variability': {
        'default': 'variable',
        'values': {'constant', 'variable'},
    },
    'scope': {
        'default': 'local',
        'values': {'local', 'shared'}
    }
}

ACCEPTABLE_PROPRIETOR = {'pre', 'post'}

BUILTIN_VARIABLES = [
    {
        'name': 'g_exc',
        'init': '0',
        'c_type': 'float',
        'variability': 'variable',
        'scope': 'local',
        'context': VariableContext.NEURON
    },
    # {
    #     'name': 't',
    #     'init': '0',
    #     'c_type': 'int',
    #     'variability': 'variable',
    #     'scope': 'local',
    #     'context': VariableContext.NETWORK
    # }
]
