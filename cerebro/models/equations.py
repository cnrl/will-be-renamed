from cerebro.compiler.parser import equations_lexer


class Equation:
    """
    This class is an abstract class for equation definitions.
    """
    @staticmethod
    def from_raw(equations):
        lexed = equations_lexer(equations)
        return [Equation(**equation_spec) for equation_spec in lexed]

    def __init__(self, lhs, rhs, equation_type):
        self.lhs, self.rhs = lhs, rhs
        self.type = equation_type

    def __repr__(self):
        return self.__class__.__name__ + "(\n\tequations:" + self.lhs + " = " + self.rhs + ")"
