from abc import ABC, abstractmethod

import re
import sympy

from cerebro.globals import VARIABLE_NAME_PATTERN, FUNCTION_PATTERN
from cerebro.enums import VariableScope, VariableContext


class Node(ABC):
    """
    Abstract class to define abstarct syntax tree(AST) nodes.
    """

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def extract(cls, sympy_object, symtables):
        """Extract type of AST node.

        :param cls: Defines the node class
        :param sympy_object: An object of Sympy
        :param symtables: Symbol tables containers
        
        :type cls: abc.ABCMeta
        :type sympy_object: sympy.core.assumptions.ManagedProperties
        :type symtables: dict

        :returns: Type of AST node

        :rtype: cls
        """
        if isinstance(sympy_object, sympy.Mul):
            return Mul.extract(sympy_object, symtables)

        if isinstance(sympy_object, sympy.Add):
            return Add.extract(sympy_object, symtables)

        if isinstance(sympy_object, sympy.Pow):
            return Pow.extract(sympy_object, symtables)

        if isinstance(sympy_object, (sympy.GreaterThan, sympy.StrictGreaterThan,
                                     sympy.LessThan, sympy.StrictLessThan,
                                     sympy.And, sympy.Or, sympy.Equality)):
            return BinaryOperator.extract(sympy_object, symtables)

        if isinstance(sympy_object, sympy.Number):
            return Numeral.extract(sympy_object, symtables)

        if Function.match(sympy_object):
            return Function.extract(sympy_object)

        if not sympy_object.is_symbol:
            raise Exception('Internal Error: Unknown node type')

        if Proprietorship.match(sympy_object):
            return Proprietorship.extract(sympy_object, symtables)

        if Derivative.match(sympy_object, symtables):
            return Derivative.extract(sympy_object, symtables)

        if Variable.match(sympy_object):
            return Variable.extract(sympy_object, symtables)

        raise Exception('Internal Error: Unknown node type')

    def traverse(self, func, parent=None, **func_kwargs):
        ret = [child.traverse(func, self, **func_kwargs) for child in self.children] if hasattr(self,
                                                                                                'children') else []
        return func(self, parent, ret, **func_kwargs)


class Operator(Node, ABC):
    """
    Class to take care of operator nodes in AST.
    """

    def __init__(self, children):
        """
        :param children: Child nodes of the Operator nodes, i.e. the operands

        :type children: list
        """
        super().__init__()
        self.children = children

    @classmethod
    def extract(cls, sympy_object, symtable):
        return cls([Node.extract(arg, symtable) for arg in sympy_object.args])


class BinaryOperator(Operator):
    _OP_MAP = {
        sympy.GreaterThan: '>=',
        sympy.StrictGreaterThan: '>',
        sympy.LessThan: '<=',
        sympy.StrictLessThan: '<',
        sympy.And: '&',
        sympy.Or: '|',
        sympy.Xor: '^',
        sympy.Equality: '==',
    }

    def __init__(self, children, op):
        """
        :param children: Child nodes of the BinaryOperator nodes, i.e. the operands
        :param op: The operator

        :type children: list
        :type op: str
        """
        super().__init__(children)
        self.op = op

    @classmethod
    def extract(cls, sympy_object, symtable):
        op = BinaryOperator._OP_MAP[type(sympy_object)]
        return cls([Node.extract(arg, symtable) for arg in sympy_object.args], op)

    def __repr__(self):
        return '({})'.format(self.op.join([repr(child) for child in self.children]))


class Mul(Operator):
    """
    Class to take care of multiplication operator nodes in AST.
    """

    def __init__(self, children):
        super().__init__(children)

    def __repr__(self):
        return "({})".format("*".join([str(child) for child in self.children]))


class Add(Operator):
    """
    Class to take care of addition operator nodes in AST.
    """

    def __init__(self, children):
        super().__init__(children)

    def __repr__(self):
        return "({})".format("+".join([str(child) for child in self.children]))


class Pow(Operator):
    """
    Class to take care of power operator nodes in AST.
    """

    def __init__(self, children):
        super().__init__(children)

    def __repr__(self):
        left_operand, right_operand = self.children
        return "({}^{})".format(repr(left_operand), repr(right_operand))


class Derivative(Operator):
    """
    Class to take care of derivative nodes in AST.
    """
    _PATTERN = re.compile('d(?P<NAME>{})'.format(VARIABLE_NAME_PATTERN))

    def __init__(self, children):
        super().__init__(children)

    @staticmethod
    def match(sympy_symbol, symtable):
        matched = Derivative._PATTERN.match(str(sympy_symbol))
        return matched if matched is not None \
                          and symtable['self'].get(matched.groupdict().get('NAME')) else None

    @classmethod
    def extract(cls, sympy_object, symtable):
        matched = Derivative.match(sympy_object, symtable)

        if matched is None:
            raise Exception('Internal Error: sympy_object is not a derivative of a variable')
        symbol = sympy.Symbol(matched.groupdict().get('NAME'))
        return Derivative([Variable.extract(symbol, symtable)])

    def __repr__(self):
        derived = self.children[0]
        return "d{}".format(repr(derived))


class Proprietorship(Operator):
    """
    Class to handle proprietorship of variables, e.g. in synapse equation(pre.r).
    """
    _PATTERN = re.compile(
        "^_(?P<OWNER>{name_pattern})_(?P<NAME>{name_pattern})$".format(name_pattern=VARIABLE_NAME_PATTERN))

    def __init__(self, owner, children):
        super().__init__(children)
        self.owner = owner
        self._display_name = None

    def generate_display_name(self, pre_display_name, post_display_name):
        self._display_name = '{0}.{1}'.format(
            pre_display_name if self.owner == 'pre' else post_display_name,
            repr(self.children[0])
        )

    @staticmethod
    def match(sympy_symbol):
        return Proprietorship._PATTERN.match(str(sympy_symbol))

    @classmethod
    def extract(cls, sympy_object, symtables):
        matched = Proprietorship.match(sympy_object)
        if matched is None:
            raise Exception('Internal Error: sympy_object is not a proprietorship')

        groups = matched.groupdict()
        owner = groups.get('OWNER')
        name = sympy.Symbol(groups.get('NAME'))
        spec = symtables[owner].get(str(name))
        return cls(owner, [Variable(name, spec)])

    def __repr__(self):
        return self._display_name


class Symbol(Node, ABC):
    """
    Class to take care of symbols.
    """
    def __init__(self, symbol):
        """
        :param symbol: The symbol

        :type symbol: sympy.core.symbol.Symbol or sympy.core.numbers.*
        """
        super().__init__()
        self.symbol = symbol

    @classmethod
    def extract(cls, sympy_object, symtable):
        return cls(sympy_object)

    def __repr__(self):
        return repr(self.symbol)


class Numeral(Symbol):
    """
    Class to handle numeral symbols
    """
    def __init__(self, symbol):
        super().__init__(symbol)


class Variable(Symbol):
    """
    Class to handle alphanumeric symbols, interpreted as variables.
    """
    _PATTERN = re.compile(VARIABLE_NAME_PATTERN)

    def __init__(self, symbol, spec):
        """
        :param symbol: The variable symbol
        :param spec: Variable's specifications

        :type symbol: sympy.core.symbol.Symbol
        :type spec: cerebro.compiler.compiler.Compiler.Variable
        """
        super().__init__(symbol)
        self.spec = spec

    @staticmethod
    def match(sympy_symbol):
        return Variable._PATTERN.match(str(sympy_symbol))

    @classmethod
    def extract(cls, sympy_object, symtable):
        return cls(sympy_object, symtable['self'].get(str(sympy_object)))

    def __repr__(self):
        super_repr = str(super().__repr__())
        if self.spec.scope == VariableScope.SHARED.value or \
                self.spec.context == VariableContext.NETWORK:
            return super_repr
        elif self.spec.context == VariableContext.NEURON:
            return super_repr + '[i]'
        else:
            return super_repr + '[i][j]'


class Function(Node):  # TODO generalize it for other mathematical functions
    """
    Class to handle functions used in equations.
    """
    _PATTERN = re.compile(FUNCTION_PATTERN)

    def __init__(self, function_name, **kwargs):
        """
        :param function_name: Name of the function
        :param \**kwargs: arguments of the function

        :type function_name: str
        """
        super().__init__()
        self.function_name = function_name
        self.param_1 = kwargs['param_1']
        self.param_2 = kwargs['param_2']

    @staticmethod
    def match(sympy_symbol):
        return Function._PATTERN.match(str(sympy_symbol))

    @staticmethod
    def extract(sympy_object):  # TODO to be considered
        matched = Function.match(sympy_object)
        if matched is None:
            raise BaseException()

        return Function(**matched.groupdict())

    def __repr__(self):
        return f"random_{self.function_name}({self.param_1}, {self.param_2})".lower()
