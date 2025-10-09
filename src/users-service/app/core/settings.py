import os

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """App settings."""

    PROJECT_NAME: str = 'Users-Service'
    DEBUG: bool = os.environ.get('DEBUG', 'true').lower() == 'true'

    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    SECRET_KEY_REFRESH: str = os.environ.get('SECRET_KEY_REFRESH')
    ACCESS_TOKEN_EXPIRES_IN: float = float(
        os.environ.get('ACCESS_TOKEN_EXPIRES_IN', '15')
    )
    REFRESH_TOKEN_EXPIRES_IN: float = float(
        os.environ.get('REFRESH_TOKEN_EXPIRES_IN', '60')
    )

    POSTGRES_USER: str = os.environ.get('POSTGRES_USER')
    POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
    POSTGRES_DB: str = os.environ.get('POSTGRES_DB')
    POSTGRES_HOST: str = os.environ.get('POSTGRES_HOST')
    POSTGRES_PORT: str = os.environ.get('POSTGRES_PORT')

    @property
    def DATABASE_URL(self) -> str:  # noqa: N802
        return f'postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


settings = Settings()
