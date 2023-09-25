import json
import pika

from app import logger
from app.config import settings


class RabbitMQPublisher:
    def __init__(self, queue_name=None):
        self.queue_name = queue_name if queue_name else settings.QUEUE_TO_PUBLISH
        self._conn = None
        self._channel = None

    def connect(self):
        if not self._conn or self._conn.is_closed:
            self._conn = pika.BlockingConnection(
                pika.ConnectionParameters(host=settings.RABBITMQ_HOST)
            )
            self._channel = self._conn.channel()
            self._channel.queue_declare(queue=self.queue_name)

    def close(self):
        if self._conn and self._conn.is_open:
            logger.info('closing queue connection\n')
            self._conn.close()

    def publish(self, message):
        self.connect()
        try:
            self._channel.basic_publish(
                exchange='',  # using default exchange
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE)
            )
            logger.info(f"\nMessage sent to {self.queue_name}: {message}")
        except Exception as e:
            logger.error(f"Error publishing message: {str(e)}")
            raise e
        finally:
            self.close()


rabbitmq_publisher = RabbitMQPublisher()
