class IllegalArgumentException(Exception):
    def __init__(self, message):
        self.message = message


class IllegalStateException(Exception):
    def __init__(self, message):
        self.message = message


class ParseException(Exception):
    def __init__(self, message):
        self.message = message


class SemanticException(Exception):
    def __init__(self, message):
        self.message = message


class InternalException(Exception):
    def __init__(self, message):
        self.message = message
