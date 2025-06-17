import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    PROJECT_NAME: str = "Users-Service"
    DEBUG: bool = os.environ["DEBUG"]

    SECRET_KEY: str = os.environ["SECRET_KEY"]
    SECRET_KEY_REFRESH: str = os.environ["SECRET_KEY_REFRESH"]
    ACCESS_TOKEN_EXPIRES_IN: int = os.environ["ACCESS_TOKEN_EXPIRES_IN"]
    REFRESH_TOKEN_EXPIRES_IN: int = os.environ["REFRESH_TOKEN_EXPIRES_IN"]

    POSTGRES_USER: str = os.environ["POSTGRES_USER"]
    POSTGRES_PASSWORD: str = os.environ["POSTGRES_PASSWORD"]
    POSTGRES_DB: str = os.environ["POSTGRES_DB"]
    POSTGRES_HOST: str = os.environ["POSTGRES_HOST"]
    POSTGRES_PORT: str = os.environ["POSTGRES_PORT"]

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
