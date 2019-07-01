from .symbol_table import SymbolTable
from cerebro.globals import ACCEPTABLE_CONSTRAINTS
from cerebro.exceptions import ParseException, SemanticException
from cerebro.enums import VariableScope, VariableContext, EquationContext, VariableVariability
from cerebro.globals import FORBIDDEN_VARIABLE_NAMES, RESERVED_WORDS, ACCEPTABLE_PROPRIETOR
from .tree_converter import Node, Variable, Derivative, Proprietorship
from copy import deepcopy


import sympy


class VariableSpec:
    def __init__(self, name, init, type, variability, scope):
        self.name = name
        self.init = init
        self.type = type
        self.const = variability
        self.scope = scope


class Compiler:
    def __init__(self, network):
        self.network = network
        self.symtable = SymbolTable()
        self.population_symbol_tables = {}

    def semantic_analyzer(self):
        network_variable_specs = [self.parse_variable(variable, VariableContext.NETWORK)
                                  for variable in self.network.variables]

        self.symtable.enter_scope()
        for variable_spec in network_variable_specs:
            if variable_spec.scope != VariableScope.LOCAL:
                raise ParseException('Network variables cannot have {} scope'.format(VariableScope.SHARED))
            self.symtable.add_variable(variable_spec.name, variable_spec)

        for population in self.network.populations:
            population_variable_specs = [self.parse_variable(variable, VariableContext.NEURON)
                                         for variable in population.neuron.variables]

            self.symtable.enter_scope()

            for variable_spec in population_variable_specs:
                self.symtable.add_variable(variable_spec.name, variable_spec)


            # parse equations
            self.population_symbol_tables[population] = deepcopy(self.symtable)
            self.symtable.exit_scope()

        for connection in self.network.connections:
            connection_variable_specs = [self.parse_variable(variable, VariableContext.SYNAPSE)
                                         for variable in connection.synapse.variables]

            self.symtable.enter_scope()

            for variable_spec in connection_variable_specs:
                self.symtable.add_variable(variable_spec.name, variable_spec)

            # parse connection equations

            self.symtable.exit_scope()


    def parse_constraints(self, constraints):
        spec = {}
        for constraint_type in ACCEPTABLE_CONSTRAINTS:
            constraint = ACCEPTABLE_CONSTRAINTS[constraint_type]['values'] & set(constraints)
            if len(constraint) > 1:
                raise ParseException('There should be one {} constraint per variable'.format(constraint_type))
            elif len(constraint) == 0: # TODO check : there may be charandiat in constraints and ignore case
                spec[constraint_type] = ACCEPTABLE_CONSTRAINTS[constraint_type]['default']
            else:
                spec[constraint_type] = constraint.pop()
        return spec

    def parse_variable(self, variable, context):
        if variable.name in (FORBIDDEN_VARIABLE_NAMES[context] | RESERVED_WORDS):
            raise ParseException('Forbidden name for variable: {}'.format(variable.name))
        spec = self.parse_constraints(variable.constraints)
        return VariableSpec(variable.name, variable.init, **spec)


    def parse_equation(self, equation, context):
        pass

    def parse_expression(self, expression, context, symtable):
        if context == EquationContext.SYNAPSE:
            for proprietor in ACCEPTABLE_PROPRIETOR:
                expression = expression.repalce('{}.'.format(proprietor), '_{}_'.format(proprietor))
        expression = sympy.sympify(expression, evaluate=False)
        tree = Node.extract(expression, symtable)

        def semantic_tree(node, children, **func_kwargs):
            symtable = func_kwargs.get('symtable')
            if isinstance(node, Variable):
                if not symtable.is_defined(node.symbol):
                    raise SemanticException('Variable {} is not defined in this scope.'.format(node.symbol))

            if isinstance(node, Derivative):
                variable, = node.children
                if symtable.get_spec(variable.symbol).variability == VariableVariability.CONSTANT:
                    raise SemanticException('Cannot derive constant variable: {}'.format(variable.symbol))


        tree.traverse(semantic_tree)