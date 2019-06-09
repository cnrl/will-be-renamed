FORBIDDEN_POPULATION_VAR_NAMES = ('t', 'dt', 'size', 'last_spike', 'spiked', 'r', 'g_exc')
FORBIDDEN_CONNECTION_VAR_NAMES = ('t', 'dt', 'size', 'post_rank', 'pre_rank', 'w', 'inv_pre_rank', 'inv_post_rank')

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

PACKAGE_NAME = 'cerebro'

keywords = []
named_constants = []
