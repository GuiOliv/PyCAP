from abc import ABC, abstractmethod, abstractproperty

class IMessageBrokerService(ABC):
    """Interface for a message broker type e.g. RabbitMQ"""

    ip_address : str = abstractproperty()

    @abstractmethod
    def establish_connection(self):
        """Creates a connection with the message broker"""