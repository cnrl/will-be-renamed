from cerebro.parser.param_extractor import variables_lexer, equations_lexer
from cerebro.enums import VariableContext

a= variables_lexer("""
            tau =   10.0  :          population const
    
        
        Er = -60.0
        Ee = 0.0    : population
        T = -45.0   : population
    """, VariableContext.NEURON)

b = equations_lexer("""
        dv/dt = ((Er - v) + g_exc *(Ee- v)) / tau + 1000
        x = 4 + asghar
    """)

print(b)
