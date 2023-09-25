import pika
from app import logger
from app.config import settings
from app.converter import convert


class RabbitMQSubscriber:
    def __init__(self, queue_name=None):
        self.queue_name = queue_name if queue_name else settings.QUEUE_TO_SUBSCRIBE
        self.connection = None
        self.channel = None

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)

    def close(self):
        if self.connection and self.connection.is_open:
            logger.info('closing queue connection\n')
            self.connection.close()

    def callback(self, ch, method, properties, body):
        err = convert(body)
        if err:
            ch.basic_nack(delivery_tag=method.delivery_tag)
        else:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"\nMessage processed from {self.queue_name}: {body}.")

    def start_consuming(self):
        self.connect()
        print(f"Started consuming from {self.queue_name}")
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
        self.close()


rabbitmq_subscriber = RabbitMQSubscriber()
