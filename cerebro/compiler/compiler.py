from copy import deepcopy
import sympy

from .symbol_table import SymbolTable
from cerebro.globals import ACCEPTABLE_CONSTRAINTS
from cerebro.exceptions import ParseException, SemanticException
from cerebro.enums import VariableScope, VariableContext, EquationContext, VariableVariability
from cerebro.globals import FORBIDDEN_VARIABLE_NAMES, RESERVED_WORDS, ACCEPTABLE_PROPRIETOR
from .tree_converter import Node, Variable, Derivative


class Compiler:
    def __init__(self, network):
        self.network = network
        self.symtable = SymbolTable()
        self.population_symbol_tables = {}
        self.population_equations = {}
        self.connection_equations = {}

    def _network_variables_semantic_analyzer(self):
        network_variable_specs = [
            Compiler.Variable.from_parsed(variable, VariableContext.NETWORK) for variable in self.network.variables
        ]

        self.symtable.enter_scope()
        for variable_spec in network_variable_specs:
            if variable_spec.scope == VariableScope.SHARED:
                raise ParseException('Network variables cannot have {} scope'.format(VariableScope.SHARED))

            self.symtable.define(variable_spec.name, variable_spec)

    def _population_semantic_analyzer(self, population):
        population_variable_specs = [
            Compiler.Variable.from_parsed(variable, VariableContext.NEURON) for variable in population.neuron.variables
        ]

        self.symtable.enter_scope()

        for variable_spec in population_variable_specs:
            self.symtable.define(variable_spec.name, variable_spec)

        # parse equations
        for equation in population.equations:
            pass

        self.population_symbol_tables[population] = deepcopy(self.symtable)

        self.symtable.exit_scope()

    def _connection_semantic_analyzer(self, connection):
        connection_variable_specs = [
            Compiler.Variable.from_parsed(variable, VariableContext.SYNAPSE) for variable in
            connection.synapse.variables
        ]

        self.symtable.enter_scope()

        for variable_spec in connection_variable_specs:
            self.symtable.define(variable_spec.name, variable_spec)

        # parse connection equations

        self.symtable.exit_scope()

    def semantic_analyzer(self):
        self._network_variables_semantic_analyzer()

        for population in self.network.populations:
            self._population_semantic_analyzer(population)

        for connection in self.network.connections:
            self._connection_semantic_analyzer(connection)

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

    class Variable:
        def __init__(self, name, init, c_type, variability, scope):
            self.name = name
            self.init = init
            self.c_type = c_type
            self.variability = variability
            self.scope = scope

        @staticmethod
        def _extract_constraints(constraints):
            spec = {}
            constraints_set = set(constraints)

            for constraint_type in ACCEPTABLE_CONSTRAINTS:
                acceptable_constraints = ACCEPTABLE_CONSTRAINTS[constraint_type]['values']
                constraint = acceptable_constraints.intersection(constraints_set)

                if len(constraint) > 1:
                    raise SemanticException('There should be one {} constraint per variable'.format(constraint_type))
                elif len(constraint) == 0:  # TODO ignore case
                    spec[constraint_type] = ACCEPTABLE_CONSTRAINTS[constraint_type]['default']
                else:
                    spec[constraint_type] = constraint.pop()

                constraints_set -= acceptable_constraints
            if len(constraints_set) > 0:
                raise SemanticException('Unknown constraint(s) for variable: {}'.format(constraints_set))

            return spec

        @staticmethod
        def from_parsed(variable, context):
            if variable.name in FORBIDDEN_VARIABLE_NAMES[context].union(RESERVED_WORDS):
                raise SemanticException('Forbidden name for variable: {}'.format(variable.name))

            spec = Compiler.Variable._extract_constraints(variable.constraints)

            return Compiler.Variable(
                name=variable.name,
                init=variable.init,
                c_type=spec['type'],
                variability=spec['variability'],
                scope=spec['scope']
            )

    class Equation:
        def __init__(self, variable, expression, equation_type):
            self.variable = variable
            self.expression = expression
            self.equation_type = equation_type

    class Expression:
        def __init__(self, tree):
            self.tree = tree

        @staticmethod
        def from_parsed(expression, symbol_table):
            return Compiler.Expression(Node.extract(sympy.sympify(expression), symbol_table))
