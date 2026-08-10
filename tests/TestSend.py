from PyCap.MessagerService.IMessageBrokerService import IMessageBrokerService
from dependency_injector.wiring import Provide, inject
from PyCap.Config.Container import RabbitMQContainer

@inject
def main(rabbitMQ : IMessageBrokerService = Provide[RabbitMQContainer.MessageService]):
    
    print(rabbitMQ.ip_address)

    rabbitMQ.establish_connection()

    rabbitMQ.publish_function("delayed-exchange", "test", body = "Hello World", delay = 5000)

    print("channel")

if __name__ == "__main__":
    container = RabbitMQContainer()
    container.config.ip_address.from_env("RABBITMQ_IP", required=True)
    container.wire(modules=[__name__])

    main()