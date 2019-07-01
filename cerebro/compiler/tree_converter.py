from abc import ABC, abstractmethod

import re
import sympy

from cerebro.globals import NAME_PATTERN


class Node(ABC):
    """
    Abstract class to define abstarct syntax tree(AST) nodes.
    """

    @abstractmethod
    def __init__(self):
        pass

    @classmethod
    def extract(cls, sympy_object, symtable):
        """
        Extract type of AST node.
        :param cls:
        :param sympy_object:
        :param symtable:
        :return:
        """

        if isinstance(sympy_object, sympy.Mul):
            return Mul.extract(sympy_object, symtable)

        if isinstance(sympy_object, sympy.Add):
            return Add.extract(sympy_object, symtable)

        if isinstance(sympy_object, sympy.Pow):
            return Pow.extract(sympy_object, symtable)

        if isinstance(sympy_object, sympy.Number):
            return Numeral.extract(sympy_object, symtable)

        if not sympy_object.is_symbol:
            print(sympy_object, type(sympy_object))
            raise Exception('Internal Error: Unknown node type')

        if Proprietorship.match(sympy_object):
            return Proprietorship.extract(sympy_object, symtable)

        if Derivative.match(sympy_object, symtable):
            return Derivative.extract(sympy_object, symtable)

        if Variable.match(sympy_object):
            return Variable.extract(sympy_object, symtable)

        raise Exception('Internal Error: Unknown node type')


    def traverse(self, func, **func_kwargs):
        ret = [child.traverse(func, func_kwargs) for child in self.children] if hasattr(self, 'children') else []
        return func(self, ret, func_kwargs)

class Operator(Node, ABC):
    """
    Class to take care of operator nodes in AST.
    """
    def __init__(self, children):
        super().__init__()
        self.children = children

    @classmethod
    def extract(cls, sympy_object, symtable):
        return cls([Node.extract(arg, symtable) for arg in sympy_object.args])


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
    PATTERN = re.compile('d(?P<NAME>{})'.format(NAME_PATTERN))

    def __init__(self, children):
        super().__init__(children)

    @staticmethod
    def match(sympy_symbol, symtable):
        matched = Derivative.PATTERN.match(str(sympy_symbol))
        return matched if matched is not None and symtable.is_defined(matched.groupdict().get('NAME')) else None

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
    PATTERN = re.compile("^_(?P<OWNER>{name_pattern})_(?P<NAME>{name_pattern})$".format(name_pattern=NAME_PATTERN))

    def __init__(self, children):
        super().__init__(children)

    @staticmethod
    def match(sympy_symbol):
        return Proprietorship.PATTERN.match(str(sympy_symbol))

    @classmethod
    def extract(cls, sympy_object, symtable):
        matched = Proprietorship.match(sympy_object)
        if matched is None:
            raise Exception('Internal Error: sympy_object is not a proprietorship')

        groups = matched.groupdict()
        owner = groups.get('OWNER')
        name = sympy.Symbol(groups.get('NAME'))
        return cls([owner, Variable(name)])

    def __repr__(self):
        owner, name = self.children
        return "{}.{}".format(owner, repr(name))


class Symbol(Node, ABC):
    def __init__(self, symbol):
        super().__init__()
        self.symbol = symbol

    @classmethod
    def extract(cls, sympy_object, symtable):
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
