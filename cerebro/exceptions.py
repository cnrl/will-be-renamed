"""
Some more informative exceptions
"""


class IllegalArgumentException(Exception):
    """
    Inappropriate argument.
    """

    def __init__(self, message):
        self.message = message


class IllegalStateException(Exception):
    """
    Inappropriate code generation state.
    """

    def __init__(self, message):
        self.message = message


class ParseException(Exception):
    """
    Grammatically-ill string in context variables or equations.
    """

    def __init__(self, message):
        self.message = message


class SemanticException(Exception):
    """
    Semantically-ill string in context variables or equations.
    """

    def __init__(self, message):
        self.message = message


class InternalException(Exception):
    """
    Developmental issues in core code generation.
    """

    def __init__(self, message):
        self.message = message
