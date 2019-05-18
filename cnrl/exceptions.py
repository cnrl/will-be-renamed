class IllegalArgumentException(Exception):
    def __init__(self, message):
        self.message = message


class IllegalArgument(Exception):
    def __init__(self, message):
        self.message = message


class IllegalState(Exception):
    def __init__(self, message):
        self.message = message
