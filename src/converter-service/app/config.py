from dataclasses import dataclass

import environs


@dataclass
class Config:
    PROJECT_NAME: str
    MONGODB_URL: str
    RABBITMQ_HOST: str
    QUEUE_TO_PUBLISH: str
    QUEUE_TO_SUBSCRIBE: str

    @classmethod
    def load(cls):
        env = environs.Env()
        env.read_env()

        config = {
            "PROJECT_NAME": "Converter-Service",
            "MONGODB_URL": env("MONGODB_URL"),
            "RABBITMQ_HOST": env("RABBITMQ_HOST"),
            "QUEUE_TO_PUBLISH": env("CONVERTER_QUEUE_TO_PUBLISH"),
            "QUEUE_TO_SUBSCRIBE": env("CONVERTER_QUEUE_TO_SUBSCRIBE")
        }
        return cls(**config)


settings = Config.load()
