from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings.config import settings


class DatabaseHelper:
    def __init__(self, url:str, echo:bool=False):
        self.enhine = create_async_engine(
            url = url,
            echo = echo,
        )
        self.session_factory = async_sessionmaker(
            bind = self.enhine,
            autocommit = False,
            autoflush = False,
            expire_on_commit = False,
        )

db_helper = DatabaseHelper(url=settings.db_url, echo=settings.db_echo)