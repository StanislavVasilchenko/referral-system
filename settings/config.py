from os import getenv
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    db_url: str = (f"postgresql+asyncpg://"
                   f"{getenv("DB_USER")}:"
                   f"{getenv("DB_PASSWORD")}@"
                   f"{getenv("DB_HOST")}:"
                   f"{getenv("DB_PORT")}/"
                   f"{getenv("DB_NAME")}")
    db_echo: bool = False


settings = Settings()
