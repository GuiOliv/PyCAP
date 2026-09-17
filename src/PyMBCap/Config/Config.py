from PyMBCap.Config.Container import RabbitMQContainer

def wireRabbitMQContainer(modules : list[str]):
    container = RabbitMQContainer()
    container.config.ip_address.from_env("RABBITMQ_IP", required=True)
    container.config.port.from_env("RABBITMQ_PORT", required=True)
    container.wire(modules=modules)