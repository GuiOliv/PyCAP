from MessagerService.IMessageBrokerService import IMessageBrokerService
from dependency_injector.wiring import Provide, inject
from Config.Container import RabbitMQContainer

@inject
def main(rabbitMQ : IMessageBrokerService = Provide[RabbitMQContainer.MessageService]):
    
    print(rabbitMQ.ip_address)

    connection = rabbitMQ.establish_connection()

    channel = connection.channel()

    print("channel")

if __name__ == "__main__":
    container = RabbitMQContainer()
    container.config.ip_address.from_env("RABBITMQ_IP", required=True)
    container.wire(modules=[__name__])

    main()