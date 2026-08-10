from src.PyCap_GuiOliv.MessagerService.IMessageBrokerService import IMessageBrokerService
from dependency_injector.wiring import Provide, inject
from src.PyCap_GuiOliv.Config.Container import RabbitMQContainer
from src.PyCap_GuiOliv.Config.Config import wireRabbitMQContainer
import sys, os
from src.PyCap_GuiOliv.MessagerService.Register import register

@inject
def main(rabbitMQ : IMessageBrokerService = Provide[RabbitMQContainer.MessageService]):
    @register(exchange_name="delayed-exchange", routing_key= "test")
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

if __name__ == "__main__":
    wireRabbitMQContainer([__name__])

    try:
        main()
    except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)