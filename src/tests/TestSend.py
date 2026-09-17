from PyMBCap.MessagerService.IMessageBrokerService import IMessageBrokerService
from dependency_injector.wiring import Provide, inject
from PyMBCap.Config.Container import RabbitMQContainer
from PyMBCap.Config.Config import wireRabbitMQContainer
import asyncio

@inject
async def main(rabbitMQ : IMessageBrokerService = Provide[RabbitMQContainer.MessageService]):
    await rabbitMQ.establish_connection()

    await rabbitMQ.publish_function("delayed-exchange", "test", body = "Hello World", delay = 5000)

    print("channel")

if __name__ == "__main__":
    wireRabbitMQContainer([__name__])

    asyncio.run(main())