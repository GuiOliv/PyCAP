from abc import ABC, abstractmethod, abstractproperty

class IMessageBrokerService(ABC):
    """Interface for a message broker type e.g. RabbitMQ"""

    ip_address : str = abstractproperty()

    @abstractmethod
    async def establish_connection(self):
        """Creates a connection with the message broker"""

    @abstractmethod
    async def publish_function(self, *args):
        """Publishes a message to the message broker"""

    @abstractmethod
    async def register_function(self, *args):
        """Registers a function that consumes the message"""
