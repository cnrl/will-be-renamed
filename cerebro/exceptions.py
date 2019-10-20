"""Some more informative exceptions

Classes
-------
IllegalArgumentException(Exception)
    Inappropriate argument.
    Methods defined here:
        __init__(self, message)
            initializes self.message with the given message string.

IllegalStateException(Exception)
    Inappropriate code generation state.
    Methods defined here:
        __init__(self, message)
            initializes self.message with the given message string.

ParseException(Exception)
    Grammatically-ill string in context variables or equations.
    Methods defined here:
        __init__(self, message)
            initializes self.message with the given message string.

SemanticException(Exception)
    Semantically-ill string in context variables or equations.
    Methods defined here:
        __init__(self, message)
            initializes self.message with the given message string.

InternalException(Exception)
    Developmental issues in core code generation.
    Methods defined here:
        __init__(self, message)
            initializes self.message with the given message string.
"""


class IllegalArgumentException(Exception):
    """Inappropriate argument."""

    def __init__(self, message):
        self.message = message


class IllegalStateException(Exception):
    """Inappropriate code generation state."""

    def __init__(self, message):
        self.message = message


class ParseException(Exception):
    """Grammatically-ill string in context variables or equations."""

    def __init__(self, message):
        self.message = message


class SemanticException(Exception):
    """Semantically-ill string in context variables or equations."""

    def __init__(self, message):
        self.message = message


class InternalException(Exception):
    """Developmental issues in core code generation."""

    def __init__(self, message):
        self.message = message
