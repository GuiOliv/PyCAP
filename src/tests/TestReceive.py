from PyMBCap.MessagerService.IMessageBrokerService import IMessageBrokerService
from dependency_injector.wiring import Provide, inject
from PyMBCap.Config.Container import RabbitMQContainer
from PyMBCap.Config.Config import wireRabbitMQContainer
import sys, os
from PyMBCap.MessagerService.Register import register
import asyncio

@inject
async def main(rabbitMQ : IMessageBrokerService = Provide[RabbitMQContainer.MessageService]):
    async def callback(message):
        async with message.process():
            print(f" [x] Received {message.body}")

    await register(func=callback,exchange_name="delayed-exchange", routing_key= "test")

if __name__ == "__main__":
    wireRabbitMQContainer([__name__])

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)