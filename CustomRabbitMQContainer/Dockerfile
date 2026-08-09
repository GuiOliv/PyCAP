FROM rabbitmq:4.3.4-management
COPY ./rabbitmq_delayed_message_exchange-v4.3.3.ez /opt/rabbitmq/plugins/
COPY ./leveled-1.1.0-35-g6dd1a91.ez /opt/rabbitmq/plugins/
RUN rabbitmq-plugins enable rabbitmq_delayed_message_exchange