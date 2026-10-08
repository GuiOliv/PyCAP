from PyMBCap.Config.Container import RabbitMQContainer

def wireRabbitMQContainer(modules : list[str]):
    container = RabbitMQContainer()
    container.config.ip_address.from_env("RABBITMQ_IP", required=False)
    container.config.port.from_env("RABBITMQ_PORT", required=False)
    container.config.host.from_env("RABBITMQ_HOST", required=False)
    container.config.user.from_env("RABBITMQ_USER", required=False)
    container.config.password.from_env("RABBITMQ_PASS", required=False)

    if container.config.ip_config is None and container.config.host is None:
        raise Exception("You either need an IP address, or a host URL")

    container.wire(modules=modules)