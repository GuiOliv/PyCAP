# PyCAP

PyCAP is a simple package inspired by [dotnetcore.CAP](https://cap.dotnetcore.xyz/). Its purpose is to make implementing and working with a message broker e.g. RabbitMQ in Python, with a delay.

**Right now, only RabbitMQ is implemented. Feel free to issue a pull request with another implementation. If you plan on doing so, please send me an email.**

## HOW TO SETUP

## Setup Custom Container
This package requires a plugin for RabbitMQ if you want to use it with a delay. To set it up, this repository contains a folder named CustomRabbitMQContainer, that includes a Dockerfile, a docker-compose.yml, and 2 plugins.
The container must be running for the package to work.

### Wire the RabbitMQ Container for Dependency Injection

This package relies on dependency injection.
This means that, for it to be injected, it must be first "added as a service". You can do so by following the example bellow:

```python
from PyCap.Config.Config import wireRabbitMQContainer

if __name__ == "__main__":
    wireRabbitMQContainer([__name__])

    main()
```

*** You must also add the `RABBITMQ_IP` in your .env or environment, with the IP to the container. You can find this out by doing ```docker inspect [id of the container]```. ***

## Publish

To publish a message, simply establish a connection and fill in the required arguments, just like:
```python
from PyCap.MessagerService.IMessageBrokerService import IMessageBrokerService
from dependency_injector.wiring import Provide, inject
from PyCap.Config.Container import RabbitMQContainer

@inject
def main(rabbitMQ : IMessageBrokerService = Provide[RabbitMQContainer.MessageService]):
    rabbitMQ.establish_connection()

    rabbitMQ.publish_function([exchange name], [routing_key], body = "Hello World", delay = 5000)

    print("Sent!")
```

In the example above, after filling in exchange name and queue name, there are also other optional arguments.

```python
    def publish_function(self, exchange_name : str, routing_key : str, exchange_type : str = "x-delayed-message", delay : int = 0, durable : bool = True, body : str = ""):
```
Delay is in milliseconds. 

## Receive / Listen

To mark the function that is supposed to be triggered by the published message, use the decorator above the function with the same exchange_name and routing_key as you used to publish.

```python
from PyCap.MessagerService.IMessageBrokerService import IMessageBrokerService
from dependency_injector.wiring import Provide, inject
from PyCap.Config.Container import RabbitMQContainer
from PyCap.MessagerService.Register import register

@inject
def main(rabbitMQ : IMessageBrokerService = Provide[RabbitMQContainer.MessageService]):
    @register(exchange_name=[exchange name], routing_key=[routing_key])
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")
```

In the example above, after filling in exchange name and queue name, there are also other optional arguments.

```python
    def register_function(self, func, exchange_name : str, routing_key : str, exchange_type : str = "x-delayed-message", durable : bool = True, retryType : RetryTypes = RetryTypes.ALL, delayedRetryMin : int = 60000):
```

delayedRetryMin is in milliseconds.

## Final words

If you need extra clarification, or want to implement a feature or expansion, don't hesitate to email me at gui.p.oliv@proton.me.
You are also free to open an issue!

