from src.PyCap_GuiOliv.Config.Container import RabbitMQContainer

def wireRabbitMQContainer(modules : list[str]):
    container = RabbitMQContainer()
    container.config.ip_address.from_env("RABBITMQ_IP", required=True)
    container.wire(modules=modules)