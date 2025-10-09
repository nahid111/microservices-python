from app.config import settings
from app.subscriber import rabbitmq_subscriber

if __name__ == '__main__':
    print(f"Starting {settings.PROJECT_NAME}")
    rabbitmq_subscriber.start_consuming()
