from datetime import datetime, timedelta

from pydantic import BaseModel


class ReferralCode(BaseModel):
    pass


class ReferralCodeCreate(ReferralCode):
    code: str = "Some Code"
    expiry_date: datetime = datetime.now() + timedelta(days=1)
    # user_id: int | None = None


class ReferralCodeOut(ReferralCode):
    code: str
    expiry_date: datetime
    user_id: int | None
