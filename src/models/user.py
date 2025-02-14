from sqlalchemy.orm import Mapped, mapped_column
from settings.base import Base


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

    def __str__(self):
        return self.email
