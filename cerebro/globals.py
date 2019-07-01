from .enums import VariableContext

FORBIDDEN_VARIABLE_NAMES = {
    VariableContext.NEURON: {'t', 'dt', 'size', 'last_spike', 'spiked', 'r', 'g_exc'},
    VariableContext.SYNAPSE: {'t', 'dt', 'size', 'post_rank', 'pre_rank', 'w', 'inv_pre_rank', 'inv_post_rank'},
    VariableContext.NETWORK: set()
}

# TODO: complete list below
RESERVED_WORDS = {'population', 'connection', 'neuron', 'synapse', 'spike', 'reset', 'const', 'int', 'double', 'float'}


NEURON_INTERNAL_VARIABLES = {
    'r': {
        'scope': 'self',
        'init': 0,
        'ctype': 'double'
    },
    'g_exc': {
        'scope': 'self',
        'init': 0,
        'ctype': 'double'
    },
}

SYNAPSE_INTERNAL_VARIABLES = {
    'w': {
        'scope': 'self',
        'init': 1,
        'ctype': 'double'
    }
}

PACKAGE_NAME = 'Cerebro'

NAME_PATTERN = "[A-Za-z][A-Za-z0-9_]*"
NUMERAL_PATTERN = "[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?"
VARIABLE_CONSTRAINTS = ["population", "connection", "local", "const"]

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
