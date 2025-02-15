from typing import TYPE_CHECKING
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from settings.base import Base

if TYPE_CHECKING:
    from src.models.user import User


class ReferralCode(Base):
    code: Mapped[str] = mapped_column(unique=True)
    expiry_date: Mapped[datetime] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(default=True)

    user: Mapped["User"] = relationship(back_populates="referral_codes")
