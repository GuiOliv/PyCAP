import pika, os, sys
from pika import BasicProperties

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters("172.17.0.2"))
    channel = connection.channel()

    args = {
        "x-delayed-type": "direct"
    }

    channel.exchange_declare("delayed-exchange", "x-delayed-message", durable=True,  arguments=args)

    header = {
        "x-delay": 5000
    }

    basicProperties = BasicProperties(headers=header, delivery_mode=1)

    channel.basic_publish(exchange='delayed-exchange',
                        routing_key='test',
                        body='Hello World!', properties=basicProperties)
    print(" [x] Sent 'Hello World!'")

    connection.close()

if __name__ == '__main__':
    try:
        while True:
            main()
            input()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)