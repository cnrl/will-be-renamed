"""This module contains classes to define type of connection between populations.

Classes
-------
ConnectionType
    Abstract class for different connection types.
AllToAllConnection
    Base class to fully connect two populations of neurons.
ProbabilityConnection
    Base class to connect pre-synaptic neurons with a probability to post-synaptic neurons.
"""
from abc import ABC, abstractmethod


class ConnectionType(ABC):
    """Abstract class for different connection types.

    Methods
    -------
    get_c_definition(connection)
        Return the template code in C for render.
    """
    def __init__(self):
        pass

    @abstractmethod
    def get_c_definition(self, connection):
        """
        Parameters
        ----------
        connection : cerebro.models.Connection
            An object of the connection this type is applied to.

        Raises
        ------
        NotImplementedError : If the function of abstract class is called directly.
        """
        raise NotImplementedError("Cannot call get_name function of abstract class ConnectionType.")


class AllToAllConnection(ConnectionType):
    """Base class to fully connect two populations of neurons.

    Methods
    -------
    get_c_definition(connection)
        Return the template code in C for render.
    """
    def __init__(self):
        super().__init__()

    def get_c_definition(self, connection):
        """
        Parameters
        ----------
        connection : cerebro.models.Connection
            An object of the connection this type is applied to.

        Raises
        ------
        NotImplementedError : If the function of abstract class is called directly.
        """
        return f"connect_all_to_all(population{ connection.pre.id }.size, population{ connection.post.id }.size, 0.0)"


class ProbabilityConnection(ConnectionType):
    """Base class to connect pre-synaptic neurons with a probability to post-synaptic neurons.

        Methods
        -------
        get_c_definition(connection)
            Return the template code in C for render.
        """
    def __init__(self, probability):
        super().__init__()
        self.probability = probability

    def get_c_definition(self, connection):
        """
        Parameters
        ----------
        connection : cerebro.models.Connection
            An object of the connection this type is applied to.

        Raises
        ------
        NotImplementedError : If the function of abstract class is called directly.
        """
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
