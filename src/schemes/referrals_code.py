from datetime import datetime, timedelta

from pydantic import BaseModel


class ReferralCode(BaseModel):
    pass


class ReferralCodeCreate(ReferralCode):
    code: str = "Some Code"
    expiry_date: datetime = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


class ReferralCodeOut(ReferralCode):
    code: str
    expiry_date: datetime
    user_id: int | None


class ReferralCodeDelete(ReferralCode):
    code: str = "Your code"
