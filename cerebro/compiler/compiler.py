"""This module contains a single class, responsible for compilation process.

*Classes*:

* **Compiler**:
    Base class to compile a network.

    - **Variable**:
        Base class for more low-level operations on variables.
    - **Equation**:
        Base class for more low-level operations on equations.
    - **Expression**:
        Base class for all right-hand-side expressions.
    - **NeuronExpression**:
        Base class for neuron expression.
    - **SynapseExpression**:
        Base class for synapse expression.
"""


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
    """
    Base class to compile a network.
    """
    def __init__(self, network):
        """
        :param network: The network object to be compiled

        :type network: cerebro.models.network.Network
        """
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
        """Analyses the network variables semantically and adds the them to the symbol table.

        :raises: ParseException: If network variable is defined to have `shared` scope.
        """
        network_variable_specs = [
            Compiler.Variable.from_parsed(variable, VariableContext.NETWORK) for variable in self.network.variables
        ]
        network_variable_specs.extend(Compiler.Variable.get_builtin_variables(VariableContext.NETWORK))

        self.symtable.enter_scope()
        for variable_spec in network_variable_specs:
            if variable_spec.scope == VariableScope.SHARED:
                raise ParseException('Network variables cannot have {} scope'.format(VariableScope.SHARED))

            self.symtable.define(variable_spec.name, variable_spec)
            if variable_spec.name != 't':
                self.network_variable_specs.append(variable_spec)

    def _population_semantic_analyzer(self, population):
        """Analyses a population variables and equations semantically and adds the variables to the symbol table.

        :param population: The population to be analysed.

        :type population: cerebro.models.population.Population

        :raises: ValueError: If the variables used in the equations are not defined.
        :raises: SemanticException: If not all compulsory variables are defined or `reset` expression contains an ODE.
        """
        population_variable_specs = [
            variable if isinstance(variable, Compiler.Variable) else
            Compiler.Variable.from_parsed(variable, VariableContext.NEURON) for variable in
            population.neuron.variables
        ]
        population_variable_specs.extend(Compiler.Variable.get_builtin_variables(VariableContext.NEURON))

        self.symtable.enter_scope()

        for variable_spec in population_variable_specs:
            self.symtable.define(variable_spec.name, variable_spec)
            existed = next((item for item in self.population_variable_specs[population] if item.name == variable_spec.name), None)
            if not existed:
                self.population_variable_specs[population].append(variable_spec)
            else:
                raise ValueError(f"Variable {variable_spec.name} redefined.")

        not_defined_adjectives = ADJECTIVE_VARIABLE_NAMES[VariableContext.NEURON] \
                                 - {variable_spec.name for variable_spec in population_variable_specs}
        if not_defined_adjectives:
            raise SemanticException(f"You should define all compulsory variables: {not_defined_adjectives}")

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
        """Analyses a connection variables and equations semantically and adds the variables to the symbol table.

        :param connection: The connection to be analysed.

        :type connection: cerebro.models.connection.Connection

        :raises: ValueError: If the variables used in the equations are not defined.
        :raises: SemanticException: If not all compulsory variables are defined.
        """
        connection_variable_specs = [
            variable if isinstance(variable, Compiler.Variable) else
            Compiler.Variable.from_parsed(variable, VariableContext.SYNAPSE) for variable in
            connection.synapse.variables
        ]
        connection_variable_specs.extend(Compiler.Variable.get_builtin_variables(VariableContext.SYNAPSE))

        self.symtable.enter_scope()

        for variable_spec in connection_variable_specs:
            self.symtable.define(variable_spec.name, variable_spec)
            existed = next((item for item in self.connection_variable_specs[connection] if item.name == variable_spec.name), None)
            if not existed:
                self.connection_variable_specs[connection].append(variable_spec)
            else:
                raise ValueError(f"Variable {variable_spec.name} redefined.")

        not_defined_adjectives = ADJECTIVE_VARIABLE_NAMES[VariableContext.SYNAPSE] \
                                 - {variable_spec.name for variable_spec in connection_variable_specs}

        if not_defined_adjectives:
            raise SemanticException(f"You should define all compulsory variables: {not_defined_adjectives}")

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
        """Analyse the whole network construction semantically."""
        self._network_variables_semantic_analyzer()

        for population in self.network.populations:
            self._population_semantic_analyzer(population)

        for connection in self.network.connections:
            self._connection_semantic_analyzer(connection)

    def code_gen(self):
        """Generates the wrapper class for the network.

        :returns: A wrapper module

        :rtype: module
        """
        return CodeGeneration(self.network, self.network.populations, self.network.connections,
                              self.network_variable_specs,
                              self.population_variable_specs, self.connection_variable_specs,
                              self.population_equations, self.population_reset_equations,
                              self.population_spike_condition, self.connection_equations,
                              self.connection_pre_spike, self.connection_post_spike).generate()

    def parse_expression(self, expression, context, symtables):
        """Parses the right-hand-side expression of an equation by traversing the parse tree.

        :param expression: The right-hand-side expression of an equation
        :param context: The context of the equation, i.e. Neuron or Synapse
        :param symtables: Symbol tables container for further parse tree traversal

        :type expression: str
        :type context: enum EquationContext
        :type symtables: dict

        :raises: SympifyError: If sympy fails to parse the given expression
        """
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
            """Checks the parse tree for semantic errors.

            :param node: the node to analyse
            :param parent: parent of the node to be analysed
            :param children: child nodes of the `node` object
            :param \**func_kwargs: See below
            :Keyword Arguments:
                * *symtable* (``dict``) --
                  Symbol Table object
                  
            :type node: cerebro.compiler.tree_converter.Node
            :type parent: cerebro.compiler.tree_converter.Node
            :type children: cerebro.compiler.tree_converter.Node

            :raises: SemanticException: If a constant variable is used as ODE variable.
            """
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
        """
        Base class for more low-level operations and detailed information on variables.
        """
        def __init__(self, name, init, c_type, variability, scope, context):
            """
            :param name: Name of the variable
            :param init: Initial value of the variable
            :param c_type: C type of the variable
            :param variability: Whether the parameter is constant or variable
            :param scope: Scope of the variable, i.e. shared or local
            :param context: Context of the variable, i.e. Neuron or Synapse

            :type name: str
            :type init: str
            :type c_type: str
            :type variability: str
            :type scope: str
            :type context: enum VariableContext
            """
            self.name = name
            self.init = init
            self.c_type = c_type
            self.variability = variability
            self.scope = scope
            self.context = context

        @staticmethod
        def _extract_constraints(constraints):
            """Extract the constraints defined for a variable.

            :param constraints: Constraints defined for a variable.

            :type constraints: str

            :returns: A dictionary of constraints

            :rtype: dict

            :raises: SemanticException: If there are invalid or confusing constraints.
            """
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
            """Generates a Variable object from the parsed variable.

            :param variable: The parsed variable object
            :param context: Context of the variable

            :type variable: cerebro.compiler.parser.VariableParser.ParsedVariable
            :type context: enum VariableContext

            :returns: The Variable object

            :rtype: cerebro.compiler.compiler.Compiler.Variable

            :raises: SemanticException: If the variable name is forbidden.
            """
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
            """Returns the builtin variables in the context.

            :param context: The context of the desired builtin variables

            :type context: enum VariableContext

            :returns: The builtin variables

            :rtype: list
            """
            return [Compiler.Variable(**variable_args) for variable_args in BUILTIN_VARIABLES if
                    variable_args['context'] == context]

    class Equation:
        """
        Base class for more low-level operations and detailed information on equations.
        """
        def __init__(self, variable, expression, equation_type, context, symtables):
            """
            :param variable: Variable that changes by the equation
            :param expression: right-hand-side expression of an equation
            :param equation_type: Type of the equation, i.e. simple or ODE
            :param context: Context in which the equation is defined
            :param symtables: Symbol tables container

            :type variable: str
            :type expression: str
            :type equation_type: str
            :type context: enum EquationContext
            :type symtables: dict
            """
            self.variable = variable
            expression_cls = Compiler.NeuronExpression \
                if context == EquationContext.NEURON else Compiler.SynapseExpression
            self.expression = expression_cls.from_parsed(expression, symtables)
            self.equation_type = equation_type

        def semantic_analyzer(self, symbol_table, context, **kwargs):
            """Semantic analysis of the equation.

            :param symbol_table: The symbol table object
            :param context: Context in which the equation is defined

            :type symbol_table: cerebro.compiler.symbol_table.SymbolTable
            :type context: enum EquationContext

            :raises: SemanticException: If variable is not defined in the scope or equation variable is constant.
            """
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
            """Generate an Equation object from parsed equation.

            :param parsed_equation: Parsed equation object
            :param context: Context of the equation
            :param symtables: Symbol tables container

            :type parsed_equation: cerebro.compiler.parser.EquationParser.ParsedEquation
            :type context: enum EquationContext
            :type symtables: dict

            :returns: The Equation object

            :rtype: cerebro.compiler.compiler.Compiler.Equation
            """
            return Compiler.Equation(
                parsed_equation.variable,
                parsed_equation.expression,
                parsed_equation.equation_type,
                context,
                symtables
            )

    class Expression:
        """Base class for right-hand-side expression parse tree."""
        def __init__(self, tree):
            """
            :param tree: The parse tree root

            :type tree: cerebro.compiler.tree_converter.Node
            """
            self.tree = tree

        @classmethod
        def from_parsed(cls, expression, symtables):
            return cls(Node.extract(sympy.sympify(expression), symtables))

        def __str__(self):
            return repr(self)

        def __repr__(self):
            return repr(self.tree)

    class NeuronExpression(Expression):
        """
        Base class for right-hand side expression of a neuron.
        """
        def semantic_analyzer(self, symbol_table):
            """Traverses the parse tree and analyzes nodes semantically.

            :param symbol_table: symbol table object

            :type symbol_table: cerebro.compiler.symbol_table.SymbolTable

            :raises: SemanticException: If variables in the equation are not defined in the scope.
            """
            def is_defined(node, parent, children, **kwargs):
                sym_table = kwargs.get('symbol_table')
                if isinstance(node, Variable) and sym_table.get(str(node.symbol)) is None and \
                        str(node.symbol) not in INTERNAL_VARIABLES:
                    raise SemanticException("Variable {} is not defined in this scope.".format(node.symbol))

            self.tree.traverse(is_defined, symbol_table=symbol_table)

    class SynapseExpression(Expression):
        """
        Base class for right-hand-side expression of a synapse.
        """
        def semantic_analyzer(self, symbol_table, **kwargs):
            """Traverses the parse tree and analyzes nodes semantically.

            :param symbol_table: Symbol table object
            :param \**kwargs: See below
            :Keyword Arguments:
                * *symbol_table* (``cerebro.compiler.symbol_table.SymbolTable``) -- Symbol table object of synapse
                * *connection* (``cerebro.models.connection.Connection``) -- Connection in which the synapse is used
                * *proprietor_symtables* (``cerebro.compiler.symbol_table.SymbolTable``) -- Symbol table object for pre and post neurons

            :type symbol_table: cerebro.compiler.symbol_table.SymbolTable

            :raises: SemanticException: If variable is not defined in the corresponding scope.
            """
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
