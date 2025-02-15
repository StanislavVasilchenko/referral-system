from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.base import Base

if TYPE_CHECKING:
    from src.models.referral_code import ReferralCode


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

    referral_codes: Mapped[list["ReferralCode"]] = relationship(back_populates="user")

    def __str__(self):
        return self.email
