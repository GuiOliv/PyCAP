from dependency_injector import containers, providers
from src.PyCap_GuiOliv.MessagerService.RabbitMQService import RabbitMQService

class RabbitMQContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    MessageService = providers.Factory(
        RabbitMQService,
        ip_address=config.ip_address
    )
