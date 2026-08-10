from PyCap_GuiOliv.MessagerService.RabbitMQService import RetryTypes, RabbitMQService
from dependency_injector.wiring import Provide, inject
from PyCap_GuiOliv.MessagerService.IMessageBrokerService import IMessageBrokerService
from PyCap_GuiOliv.Config.Container import RabbitMQContainer
import functools

@inject
def register(exchange_name : str, routing_key : str, exchange_type : str = "x-delayed-message", durable : bool = True, retryType : RetryTypes = RetryTypes.ALL, delayedRetryMin : int = 60000, rabbitMQ : RabbitMQService = Provide[RabbitMQContainer.MessageService]):
    def decorator_register(func):
        rabbitMQ.establish_connection()
        rabbitMQ.register_function(func=func, exchange_name=exchange_name, routing_key=routing_key, exchange_type=exchange_type, durable=durable, retryType=retryType, delayedRetryMin=delayedRetryMin)

    return decorator_register