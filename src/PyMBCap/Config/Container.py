from dependency_injector import containers, providers
from PyMBCap.MessagerService.RabbitMQService import RabbitMQService

class RabbitMQContainer(containers.DeclarativeContainer):

    config = providers.Configuration()

    MessageService = providers.Factory(
        RabbitMQService,
        ip_address=config.ip_address,
        port = config.port
    )
