from PyMBCap.MessagerService.IMessageBrokerService import IMessageBrokerService
from pika import BasicProperties,BlockingConnection,ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel
from enum import Enum
import aio_pika
import asyncio

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
    port = None
    host = None
    user = None
    password = None
    connection = None

    args = {
        "x-delayed-type": "direct"
    }

    def __header__(self, delay : int) -> dict:
        return {
            "x-delay": delay
        }

    def __init__(self, ip_address : str, port : int, host : str, user : str, password : str) -> None:
        self.ip_address = ip_address
        self.port = int(port)
        self.host = host
        self.user = user
        self.password = password

    async def establish_connection(self):
        """Creates a connection with the message broker"""

        self.connection = await aio_pika.connect_robust(host=self.ip_address, port=self.port, login=self.user, password=self.password)
        return self.connection

    async def publish_function(self, exchange_name : str, routing_key : str, exchange_type : str = "x-delayed-message", delay : int = 0, durable : bool = True, body : str = ""):
        channel = await self.connection.channel()

        exc = await channel.declare_exchange(name=exchange_name, type=exchange_type, durable=durable, arguments=self.args)

        basic_properties = BasicProperties(headers=self.__header__(delay=delay), delivery_mode=1)

        message = aio_pika.Message(
            body=bytes(body, encoding="utf8"),
            delivery_mode=1,
            headers=self.__header__(delay=delay)
        )

        await exc.publish(message=message, routing_key=routing_key)

        print("Message Sent")

    async def register_function(self, func, exchange_name : str, routing_key : str, exchange_type : str = "x-delayed-message", durable : bool = True, retryType : RetryTypes = RetryTypes.ALL, delayedRetryMin : int = 60000):
        channel = await self.connection.channel()

        exc = await channel.declare_exchange(name=exchange_name, type=exchange_type, durable=durable, arguments=self.args)

        queue = await channel.declare_queue(name=routing_key, durable=durable, arguments={"x-queue-type": "quorum", "x-delayed-retry-type": retryType.value, "x-delayed-retry-min": delayedRetryMin})

        await queue.bind(exc)
        await queue.consume(func)

        print("Listening")
        await asyncio.Future()
