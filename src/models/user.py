from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.base import Base

if TYPE_CHECKING:
    from src.models.referral_code import ReferralCode


class User(Base):
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]
    referred_by: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True)

    referral_codes: Mapped[list["ReferralCode"]] = relationship(
        back_populates="user",
    )
    referrals: Mapped[list["User"]] = relationship(
        "User",
        back_populates="referrer",
    )
    referrer: Mapped["User"] = relationship(
        "User",
        remote_side="User.id",
        back_populates="referrals",
    )

    def __str__(self):
        return self.email
