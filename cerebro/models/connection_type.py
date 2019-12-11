"""This module contains classes to define type of connection between populations.

*Classes*:

* **ConnectionType**:
    Abstract class for different connection types.
* **AllToAllConnection**:
    Base class to fully connect two populations of neurons.
* **ProbabilityConnection**:
    Base class to connect pre-synaptic neurons with a probability to post-synaptic neurons.
* **GaussianConnection**:
    Base class to connect pre-synaptic neurons to post-synaptic neurons based on Gaussian density.
* **DoGConnection**:
    Base class to connect pre-synaptic neurons to post-synaptic neurons based on Difference of Gaussian density.
"""
from abc import ABC, abstractmethod


class ConnectionType(ABC):
    """
    Abstract class for different connection types.
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_c_definition(self, connection):
        """
        :param connection: An object of the connection this type is applied to.

        :type connection: cerebro.models.Connection

        :raises NotImplementedError: If the function of abstract class is called directly.
        """
        raise NotImplementedError("Cannot call get_name function of abstract class ConnectionType.")


class AllToAllConnection(ConnectionType):
    """
    Base class to fully connect two populations of neurons.
    """
    def __init__(self):
        super().__init__()

    def get_c_definition(self, connection):
        """
        :param connection: An object of the connection this type is applied to.

        :type connection: cerebro.models.Connection

        :raises NotImplementedError: If the function of abstract class is called directly.
        """
        return f"connect_all_to_all(population{ connection.pre.id }.size, population{ connection.post.id }.size)"


class ProbabilityConnection(ConnectionType):
    """
    Base class to connect pre-synaptic neurons with a probability to post-synaptic neurons.
    """
    def __init__(self, probability):
        """
        :param probability: Probability value of neurons to be connected.

        :type probability: float
        """
        super().__init__()
        self.probability = probability

    def get_c_definition(self, connection):
        """
        :param connection: An object of the connection this type is applied to.

        :type connection: cerebro.models.Connection

        :raises NotImplementedError: If the function of abstract class is called directly.
        """
        return f"connect_with_probability(" \
               f"population{ connection.pre.id }.size, population{ connection.post.id }.size, {self.probability})"


class GaussianConnection(ConnectionType):
    """
    Base class to connect pre-synaptic neurons to post-synaptic neurons based on Gaussian density.
    """
    def __init__(self, sigma):
        """
        :param sigma: Standard deviation for the Gaussian density.

        :type sigma: float
        """
        super().__init__()
        self.sigma = sigma

    def get_c_definition(self, connection):
        """
        :param connection: An object of the connection this type is applied to.

        :type connection: cerebro.models.Connection

        :raises NotImplementedError: If the function of abstract class is called directly.
        """
        return f"connect_gaussian(" \
               f"population{ connection.pre.id }.size, population{ connection.post.id }.size, { self.sigma })"


class DoGConnection(ConnectionType):
    """
    Base class to connect pre-synaptic neurons to post-synaptic neurons based on Difference of Gaussian density.
    """
    def __init__(self, sigma1, sigma2):
        """
        :param sigma1: Standard deviation of the first Gaussian density.
        :param sigma2: Standard deviation of the second Gaussian density.

        :type sigma1: float
        :type sigma2: float
        """
        super().__init__()
        self.sigma1 = sigma1
        self.sigma2 = sigma2

    def get_c_definition(self, connection):
        """
        :param connection: An object of the connection this type is applied to.

        :type connection: cerebro.models.Connection

        :raises NotImplementedError: If the function of abstract class is called directly.
        """
        return f"connect_dog(" \
               f"population{ connection.pre.id }.size, population{ connection.post.id }.size, { self.sigma1 }, { self.sigma2 })"


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
