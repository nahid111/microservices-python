from dataclasses import dataclass

import environs


@dataclass
class Config:
    PROJECT_NAME: str
    RABBITMQ_HOST: str
    QUEUE_TO_SUBSCRIBE: str
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_DEFAULT_SENDER: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    @classmethod
    def load(cls):
        env = environs.Env()
        env.read_env()

        config = {
            "PROJECT_NAME": "Notification-Service",
            "RABBITMQ_HOST": env("RABBITMQ_HOST"),
            "QUEUE_TO_SUBSCRIBE": env("NOTIFICATION_QUEUE_TO_SUBSCRIBE"),
            "MAIL_SERVER": env.str("MAIL_SERVER", "smtp.mailtrap.io"),
            "MAIL_PORT": env.int("MAIL_PORT", 2525),
            "MAIL_DEFAULT_SENDER": "Notification-Service",
            "MAIL_USERNAME": env('MAIL_USERNAME'),
            "MAIL_PASSWORD": env('MAIL_PASSWORD')
        }
        return cls(**config)


settings = Config.load()
