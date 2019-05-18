class IllegalArgumentException(Exception):
    def __init__(self, message):
        self.message = message


class IllegalStateException(Exception):
    def __init__(self, message):
        self.message = message
