from PyCap.MessagerService.IMessageBrokerService import IMessageBrokerService
from pika import BasicProperties,BlockingConnection,ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from enum import Enum

class RetryTypes(Enum):
    """These are the possible types of delayed retry types which are native to RabbitMQ.
        The options are ALL, RETURNED or FAILED.
        This feature is only possible when using the Quorum queue type.
        For more information, please refer to the documentation in https://www.rabbitmq.com/blog/2026/04/23/rabbitmq-4.3-release.
    """
    ALL = "all"
    RETURNED = "returned"
    FAILED = "failed"

class RabbitMQService(IMessageBrokerService):

    ip_address = None
    connection = None

    args = {
        "x-delayed-type": "direct"
    }

    def __header__(self, delay : int) -> dict:
        return {
            "x-delay": delay
        }

    def __init__(self, ip_address : str) -> None:
        self.ip_address = ip_address

    def establish_connection(self):
        """Creates a connection with the message broker"""

        self.connection = BlockingConnection(ConnectionParameters(host=self.ip_address))
        return self.connection

    def publish_function(self, exchange_name : str, routing_key : str, exchange_type : str = "x-delayed-message", delay : int = 0, durable : bool = True, body : str = ""):
        channel = self.connection.channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable, arguments=self.args)

        basic_properties = BasicProperties(headers=self.__header__(delay=delay), delivery_mode=1)

        channel.basic_publish(exchange=exchange_name,
                               routing_key=routing_key,
                               body=body, properties=basic_properties)

        self.connection.close()

    def register_function(self, func, exchange_name : str, routing_key : str, exchange_type : str = "x-delayed-message", durable : bool = True, retryType : RetryTypes = RetryTypes.ALL, delayedRetryMin : int = 60000):
        channel : BlockingChannel = self.connection.channel()

        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=durable, arguments=self.args)

        channel.queue_declare(queue=routing_key, durable=durable, arguments={"x-queue-type": "quorum", "x-delayed-retry-type": retryType.value, "x-delayed-retry-min": delayedRetryMin})

        channel.queue_bind(exchange=exchange_name, queue=routing_key)

        channel.basic_consume(queue=routing_key, on_message_callback=func, auto_ack=True)

        print("Listening")
        channel.start_consuming()
