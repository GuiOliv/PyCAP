#!/usr/bin/env python
import pika, sys, os

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()

    args = {
    "x-delayed-type": "direct"
    }

    channel.exchange_declare("delayed-exchange", "x-delayed-message", durable=True, arguments=args)

    result = channel.queue_declare(queue='test', durable=True, arguments={"x-queue-type": "quorum", "x-delayed-retry-type": "all", "x-delayed-retry-min": 60000})
    queue_name = result.method.queue


    channel.queue_bind(exchange='delayed-exchange', queue=queue_name)
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)