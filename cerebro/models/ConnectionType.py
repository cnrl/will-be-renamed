class ConnectionType:
    def __init__(self):
        pass

    def get_c_definition(self, connection):
        raise NotImplementedError("Cannot call get_name function of abstract class ConnectionType.")


class AllToAllConnection(ConnectionType):
    def __init__(self):
        super().__init__()

    def get_c_definition(self, connection):
        return f"connect_all_to_all(population{ connection.pre.id }.size, population{ connection.post.id }.size, 0.0)"


class ProbabilityConnection(ConnectionType):
    def __init__(self, probability):
        super().__init__()
        self.probability = probability

    def get_c_definition(self, connection):
        return f"connect_with_probability(" \
               f"population{ connection.pre.id }.size, population{ connection.post.id }.size, {self.probability})"


class GaussianConnection(ConnectionType):
    def __init__(self, sigma):
        super().__init__()
        self.sigma = sigma

    def get_c_definition(self, connection):
        return f""


class DoGConnection(ConnectionType):
    def __init__(self, sigma1, sigma2):
        super().__init__()
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    def get_c_definition(self):
        return f""


class FixedPreNumberConnection(ConnectionType):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def get_c_definition(self, connection):
        return f""


class FixedPostNumberConnection(ConnectionType):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def get_c_definition(self, connection):
        return f"population"
