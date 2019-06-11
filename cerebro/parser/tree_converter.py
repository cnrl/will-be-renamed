from abc import ABC, abstractmethod

import re
import sympy

from cerebro.globals import NAME_PATTERN


class Node(ABC):

    @abstractmethod
    def __init__(self):
        pass

    @staticmethod
    def extract(sympy_object, **kwargs):
        is_variable = kwargs.get('is_variable')
        if is_variable is None:
            raise Exception('Internal Error: Node.extract should have is_variable method in kwargs')

        if isinstance(sympy_object, sympy.Mul):
            return Mul.extract(sympy_object, **kwargs)

        if isinstance(sympy_object, sympy.Add):
            return Add.extract(sympy_object, **kwargs)

        if isinstance(sympy_object, sympy.Pow):
            return Pow.extract(sympy_object, **kwargs)

        if isinstance(sympy_object, sympy.Number):
            return Numeral.extract(sympy_object, **kwargs)

        if not sympy_object.is_symbol:
            print(sympy_object, type(sympy_object))
            raise Exception('Internal Error: Unknown node type')

        if Proprietorship.match(sympy_object):
            return Proprietorship.extract(sympy_object)

        if Derivative.match(sympy_object, is_variable):
            return Derivative.extract(sympy_object, **kwargs)

        if Variable.match(sympy_object):
            return Variable.extract(sympy_object)

        raise Exception('Internal Error: Unknown node type')


class Operator(Node, ABC):
    def __init__(self, children):
        super().__init__()
        self.children = children

    @classmethod
    def extract(cls, sympy_object, **kwargs):
        return cls([Node.extract(arg, **kwargs) for arg in sympy_object.args])


class Mul(Operator):
    def __init__(self, children):
        super().__init__(children)

    def __repr__(self):
        return "({})".format("*".join([str(child) for child in self.children]))


class Add(Operator):
    def __init__(self, children):
        super().__init__(children)

    def __repr__(self):
        return "({})".format("+".join([str(child) for child in self.children]))


class Pow(Operator):
    def __init__(self, children):
        super().__init__(children)

    def __repr__(self):
        left_operand, right_operand = self.children
        return "({}^{})".format(repr(left_operand), repr(right_operand))


class Derivative(Operator):
    PATTERN = re.compile('d(?P<NAME>{})'.format(NAME_PATTERN))

    def __init__(self, children):
        super().__init__(children)

    @staticmethod
    def match(sympy_symbol, is_variable):
        matched = Derivative.PATTERN.match(str(sympy_symbol))
        return matched if matched is not None and is_variable(matched.groupdict().get('NAME')) else None

    @staticmethod
    def extract(sympy_object, **kwargs):
        is_variable = kwargs.get('is_variable')
        if is_variable is None:
            raise Exception('Internal Error: Node.extract should have is_variable method in kwargs')
        matched = Derivative.match(sympy_object, is_variable)

        if matched is None:
            raise Exception('Internal Error: sympy_object is not a derivative of a variable')
        symbol = sympy.Symbol(matched.groupdict().get('NAME'))
        return Derivative([Variable.extract(symbol, **kwargs)])

    def __repr__(self):
        derived = self.children[0]
        return "d{}".format(repr(derived))


class Proprietorship(Operator):
    PATTERN = re.compile("^_(?P<OWNER>{name_pattern})_(?P<NAME>{name_pattern})$".format(name_pattern=NAME_PATTERN))

    def __init__(self, children):
        super().__init__(children)

    @staticmethod
    def match(sympy_symbol):
        return Proprietorship.PATTERN.match(str(sympy_symbol))

    @staticmethod
    def extract(sympy_object, **kwargs):
        matched = Proprietorship.match(sympy_object)
        if matched is None:
            raise Exception('Internal Error: sympy_object is not a proprietorship')

        groups = matched.groupdict()
        owner = groups.get('OWNER')
        name = sympy.Symbol(groups.get('NAME'))
        return Proprietorship([owner, Variable(name)])

    def __repr__(self):
        owner, name = self.children
        return "{}.{}".format(owner, repr(name))


class Symbol(Node, ABC):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

    @classmethod
    def extract(cls, sympy_object, **kwargs):
        return cls(sympy_object)

    def __repr__(self):
        return repr(self.symbol)


class Numeral(Symbol):
    def __init__(self, symbol):
        super().__init__(symbol)


class Variable(Symbol):
    PATTERN = re.compile(NAME_PATTERN)

    def __init__(self, symbol):
        super().__init__(symbol)

    @staticmethod
    def match(sympy_symbol):
        return Variable.PATTERN.match(str(sympy_symbol))
