from collections import defaultdict
from copy import deepcopy
import sympy

from .symbol_table import SymbolTable
from cerebro.globals import ACCEPTABLE_CONSTRAINTS, BUILTIN_VARIABLES, ADJECTIVE_VARIABLE_NAMES
from cerebro.exceptions import ParseException, SemanticException
from cerebro.enums import VariableScope, VariableContext, EquationContext, VariableVariability
from cerebro.globals import FORBIDDEN_VARIABLE_NAMES, RESERVED_WORDS, ACCEPTABLE_PROPRIETOR, INTERNAL_VARIABLES
from cerebro.code_generation.api import CodeGeneration
from .tree_converter import Node, Variable, Derivative, Proprietorship


class Compiler:
    def __init__(self, network):
        self.network = network
        self.symtable = SymbolTable()
        self.network_variable_specs = []
        self.population_variable_specs = defaultdict(list)
        self.connection_variable_specs = defaultdict(list)
        self.population_equations = defaultdict(list)
        self.population_reset_equations = defaultdict(list)
        self.population_spike_condition = {}

        self.connection_equations = defaultdict(list)
        self.connection_pre_spike = defaultdict(list)
        self.connection_post_spike = defaultdict(list)

        self.population_symbol_tables = {}

    def _network_variables_semantic_analyzer(self):
        network_variable_specs = [
            Compiler.Variable.from_parsed(variable, VariableContext.NETWORK) for variable in self.network.variables
        ]

        self.symtable.enter_scope()
        for variable_spec in network_variable_specs:
            if variable_spec.scope == VariableScope.SHARED:
                raise ParseException('Network variables cannot have {} scope'.format(VariableScope.SHARED))

            self.symtable.define(variable_spec.name, variable_spec)
            self.network_variable_specs.append(variable_spec)

    def _population_semantic_analyzer(self, population):
        population_variable_specs = [
            Compiler.Variable.from_parsed(variable, VariableContext.NEURON) for variable in population.neuron.variables
        ]
        population_variable_specs.extend(Compiler.Variable.get_builtin_variables(VariableContext.NEURON))

        self.symtable.enter_scope()

        for variable_spec in population_variable_specs:
            self.symtable.define(variable_spec.name, variable_spec)
            self.population_variable_specs[population].append(variable_spec)

        not_defined_adjectives = ADJECTIVE_VARIABLE_NAMES[VariableContext.NEURON] \
                                 - {variable_spec.name for variable_spec in population_variable_specs}
        if not_defined_adjectives:
            raise SemanticException(f"You should define all adjective variables: !!!!!{not_defined_adjectives}")

        for parsed_equation in population.neuron.equations:
            self.parse_expression(
                parsed_equation.expression,
                EquationContext.NEURON,
                {
                    'self': self.symtable
                }
            )
            equation = Compiler.Equation.from_parsed(
                parsed_equation,
                EquationContext.NEURON,
                {
                    'self': self.symtable
                }
            )
            equation.semantic_analyzer(self.symtable, EquationContext.NEURON)
            self.population_equations[population].append(equation)

        spike_expression = Compiler.NeuronExpression.from_parsed(
            population.neuron.spike,
            {
                'self': self.symtable
            }
        )
        spike_expression.semantic_analyzer(self.symtable)
        self.population_spike_condition[population] = spike_expression

        for parsed_equation in population.neuron.reset:
            equation = Compiler.Equation.from_parsed(
                parsed_equation,
                EquationContext.NEURON,
                {
                    'self': self.symtable
                }
            )
            if equation.equation_type == 'ode':
                raise SemanticException("Reset expression cannot be an ODE: pop{}".format(population.id))
            equation.semantic_analyzer(self.symtable, EquationContext.NEURON)
            self.population_reset_equations[population].append(equation)

        self.population_symbol_tables[population] = deepcopy(self.symtable)

        self.symtable.exit_scope()

    def _connection_semantic_analyzer(self, connection):
        connection_variable_specs = [
            Compiler.Variable.from_parsed(variable, VariableContext.SYNAPSE) for variable in
            connection.synapse.variables
        ]
        connection_variable_specs.extend(Compiler.Variable.get_builtin_variables(VariableContext.SYNAPSE))

        self.symtable.enter_scope()

        for variable_spec in connection_variable_specs:
            self.symtable.define(variable_spec.name, variable_spec)
            self.connection_variable_specs[connection].append(variable_spec)

        not_defined_adjectives = ADJECTIVE_VARIABLE_NAMES[VariableContext.SYNAPSE] \
                                 - {variable_spec.name for variable_spec in connection_variable_specs}

        if not_defined_adjectives:
            raise SemanticException(f"You should define all adjective variables: !!!!!{not_defined_adjectives}")

        for parsed_equation in connection.synapse.equations:
            self.parse_expression(
                parsed_equation.expression,
                EquationContext.SYNAPSE,
                {
                    'self': self.symtable,
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                }
            )
            equation = Compiler.Equation.from_parsed(
                parsed_equation,
                EquationContext.SYNAPSE,
                {
                    'self': self.symtable,
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                }
            )
            equation.semantic_analyzer(
                self.symtable,
                EquationContext.SYNAPSE,
                proprietor_symtables={
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                },
                connection=connection
            )
            self.connection_equations[connection].append(equation)

        for parsed_equation in connection.synapse.pre_spike:
            self.parse_expression(
                parsed_equation.expression,
                EquationContext.SYNAPSE,
                {
                    'self': self.symtable,
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                }
            )
            # FIXME: check if only related variables are affected
            equation = Compiler.Equation.from_parsed(
                parsed_equation,
                EquationContext.SYNAPSE,
                {
                    'self': self.symtable,
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                }
            )
            equation.semantic_analyzer(
                self.symtable,
                EquationContext.SYNAPSE,
                proprietor_symtables={
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                },
                connection=connection
            )
            self.connection_pre_spike[connection].append(equation)

        for parsed_equation in connection.synapse.post_spike:
            self.parse_expression(
                parsed_equation.expression,
                EquationContext.SYNAPSE,
                {
                    'self': self.symtable,
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                }
            )
            # FIXME: check if only related variables are affected
            equation = Compiler.Equation.from_parsed(
                parsed_equation,
                EquationContext.SYNAPSE,
                {
                    'self': self.symtable,
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                }
            )
            equation.semantic_analyzer(
                self.symtable,
                EquationContext.SYNAPSE,
                proprietor_symtables={
                    'pre': self.population_symbol_tables[connection.pre],
                    'post': self.population_symbol_tables[connection.post]
                },
                connection=connection
            )
            self.connection_post_spike[connection].append(equation)
        self.symtable.exit_scope()

    def semantic_analyzer(self):
        self._network_variables_semantic_analyzer()

        for population in self.network.populations:
            self._population_semantic_analyzer(population)

        for connection in self.network.connections:
            self._connection_semantic_analyzer(connection)

    def code_gen(self):
        return CodeGeneration(self.network, self.network.populations, self.network.connections,
                              self.network_variable_specs,
                              self.population_variable_specs, self.connection_variable_specs,
                              self.population_equations, self.population_reset_equations,
                              self.population_spike_condition, self.connection_equations).generate()

    def parse_expression(self, expression, context, symtables):
        if context == EquationContext.SYNAPSE:
            for proprietor in ACCEPTABLE_PROPRIETOR:
                expression = expression.replace('{}.'.format(proprietor), '_{}_'.format(proprietor))
        try:
            expression = sympy.sympify(expression, evaluate=True)
        except:
            print(expression)
            raise
        tree = Node.extract(
            expression,
            symtables
        )

        def semantic_tree(node, parent, children, **func_kwargs):
            sym_table = func_kwargs.get('symtable')
            # if isinstance(node, Variable):
            #     if not sym_table.is_defined(node.symbol):
            #         raise SemanticException('Variable {} is not defined in this scope.'.format(node.symbol))

            if isinstance(node, Derivative):
                variable, = node.children
                if sym_table.get_spec(variable.symbol).variability == VariableVariability.CONSTANT:
                    raise SemanticException('Cannot derive constant variable: {}'.format(variable.symbol))

        tree.traverse(semantic_tree)

    class Variable:
        def __init__(self, name, init, c_type, variability, scope, context):
            self.name = name
            self.init = init
            self.c_type = c_type
            self.variability = variability
            self.scope = scope
            self.context = context

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
                scope=spec['scope'],
                context=context
            )

        @staticmethod
        def get_builtin_variables(context):
            return [Compiler.Variable(**variable_args) for variable_args in BUILTIN_VARIABLES if
                    variable_args['context'] == context]

    class Equation:
        def __init__(self, variable, expression, equation_type, context, symtables):
            self.variable = variable
            expression_cls = Compiler.NeuronExpression \
                if context == EquationContext.NEURON else Compiler.SynapseExpression
            self.expression = expression_cls.from_parsed(expression, symtables)
            self.equation_type = equation_type

        def semantic_analyzer(self, symbol_table, context, **kwargs):
            var_spec = symbol_table.get(self.variable)
            if var_spec is None:
                raise SemanticException('Variable {} is not defined in this scope.'.format(self.variable))
            elif var_spec.variability == VariableVariability.CONSTANT:
                raise SemanticException('Variable {} is defined as constant.'.format(self.variable))
            if context == EquationContext.NEURON:
                self.expression.semantic_analyzer(symbol_table)
            else:
                self.expression.semantic_analyzer(symbol_table, **kwargs)
            self.variable = var_spec

        @staticmethod
        def from_parsed(parsed_equation, context, symtables):
            return Compiler.Equation(
                parsed_equation.variable,
                parsed_equation.expression,
                parsed_equation.equation_type,
                context,
                symtables
            )

    class Expression:
        def __init__(self, tree):
            self.tree = tree

        @classmethod
        def from_parsed(cls, expression, symtables):
            return cls(Node.extract(sympy.sympify(expression), symtables))

        def __str__(self):
            return repr(self)

        def __repr__(self):
            return repr(self.tree)

    class NeuronExpression(Expression):
        def semantic_analyzer(self, symbol_table):
            def is_defined(node, parent, children, **kwargs):
                sym_table = kwargs.get('symbol_table')
                if isinstance(node, Variable) and sym_table.get(str(node.symbol)) is None and \
                        str(node.symbol) not in INTERNAL_VARIABLES:
                    raise SemanticException("Variable {} is not defined in this scope.".format(node.symbol))

            self.tree.traverse(is_defined, symbol_table=symbol_table)

    class SynapseExpression(Expression):
        def semantic_analyzer(self, symbol_table, **kwargs):
            proprietor_symtables = kwargs.get('proprietor_symtables')
            connection = kwargs.get('connection')

            def is_defined(node, parent, children, **kwargs):
                sym_table = kwargs.get('symbol_table')
                connection = kwargs.get('connection')
                proprietor_symbol_tables = kwargs.get('proprietor_symtables')
                if isinstance(node, Variable):
                    if not isinstance(parent, Proprietorship):
                        if sym_table.get(str(node.symbol)) is None and str(node.symbol) not in INTERNAL_VARIABLES:
                            raise SemanticException("Variable {} is not defined in this scope.".format(node.symbol))
                    else:
                        parent.generate_display_name(
                            'population{}'.format(connection.pre.id),
                            'population{}'.format(connection.post.id)
                        )
                        if proprietor_symbol_tables[parent.owner].get(str(node.symbol)) is None and \
                                str(node.symbol) not in INTERNAL_VARIABLES:
                            raise SemanticException("Variable {} is not defined in {} population scope.".format(
                                node.symbol, parent.owner
                            ))

            self.tree.traverse(
                is_defined,

                symbol_table=symbol_table,
                proprietor_symtables=proprietor_symtables,
                connection=connection
            )
