from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Users-Service"

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_ROOT_PASSWORD: str

    SECRET_KEY: str
    SECRET_KEY_REFRESH: str
    ACCESS_TOKEN_EXPIRES_IN: int
    REFRESH_TOKEN_EXPIRES_IN: int

    class Config:
        extra = Extra.allow
        env_file = './.env'


settings = Settings()
