from PyMBCap.MessagerService.RabbitMQService import RetryTypes, RabbitMQService
from dependency_injector.wiring import Provide, inject
from PyMBCap.MessagerService.IMessageBrokerService import IMessageBrokerService
from PyMBCap.Config.Container import RabbitMQContainer
import functools

@inject
async def register(func, exchange_name : str, routing_key : str, exchange_type : str = "x-delayed-message", durable : bool = True, retryType : RetryTypes = RetryTypes.ALL, delayedRetryMin : int = 60000, rabbitMQ : RabbitMQService = Provide[RabbitMQContainer.MessageService]):
    await rabbitMQ.establish_connection()
    await rabbitMQ.register_function(func=func, exchange_name=exchange_name, routing_key=routing_key, exchange_type=exchange_type, durable=durable, retryType=retryType, delayedRetryMin=delayedRetryMin)
