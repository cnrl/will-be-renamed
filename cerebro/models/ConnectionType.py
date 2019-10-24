class ConnectionType:
    def __init__(self):
        pass

    def get_c_definition(self):
        raise NotImplementedError("Cannot call get_name function of abstract class ConnectionType.")


class AllToAllConnection(ConnectionType):
    def __init__(self):
        super().__init__()

    def get_c_definition(self):
        return "connect_all_to_all({{ connection.pre.id }}.size, {{ connection.post.id }}.size)"


class ProbabilityConnection(ConnectionType):
    def __init__(self, probability):
        super().__init__()
        self.probability = probability

    def get_c_definition(self):
        return "connect_with_probability({{ connection.pre.id }}.size, {{ connection.post.id }}.size, {}".format(
                                                                                                    self.probability)


class GaussianConnection(ConnectionType):
    def __init__(self, sigma):
        super().__init__()
        self.sigma = sigma

    def get_c_definition(self):
        return ""


class DoGConnection(ConnectionType):
    def __init__(self, sigma1, sigma2):
        super().__init__()
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    def get_c_definition(self):
        return ""


class FixedPreNumberConnection(ConnectionType):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def get_c_definition(self):
        return ""


class FixedPostNumberConnection(ConnectionType):
    def __init__(self, number):
        super().__init__()
        self.number = number

    def get_c_definition(self):
        return ""
