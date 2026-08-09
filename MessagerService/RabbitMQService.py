from MessagerService.IMessageBrokerService import IMessageBrokerService
from pika import BasicProperties,BlockingConnection,ConnectionParameters

class RabbitMQService(IMessageBrokerService):

    ip_address = None

    def __init__(self, ip_address : str) -> None:
        self.ip_address = ip_address

    def establish_connection(self):
        """Creates a connection with the message broker"""

        connection = BlockingConnection(ConnectionParameters(host=self.ip_address))
        return connection