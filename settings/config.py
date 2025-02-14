from os import getenv
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

BASE_DIR = Path(__file__).parent.parent


class DatabaseSettings(BaseSettings):
    db_url: str = (
        f"postgresql+asyncpg://"
        f"{getenv("DB_USER")}:"
        f"{getenv("DB_PASSWORD")}@"
        f"{getenv("DB_HOST")}:"
        f"{getenv("DB_PORT")}/"
        f"{getenv("DB_NAME")}"
    )
    db_echo: bool = False


class AuthSettings(BaseSettings):
    private_key: Path = BASE_DIR / "certs" / "private.pem"
    public_key: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire: int = 3


class Settings(BaseSettings):
    # database
    db: DatabaseSettings = DatabaseSettings()
    # jwt_auth
    jwt_auth: AuthSettings = AuthSettings()


settings = Settings()
