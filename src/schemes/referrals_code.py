from datetime import datetime, timedelta
from pydantic import BaseModel, EmailStr


class ReferralCode(BaseModel):
    pass


class ReferralCodeCreate(ReferralCode):
    code: str = "Some Code"
    expiry_date: datetime = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")


class ReferralCodeOut(ReferralCode):
    code: str
    expiry_date: datetime


class ReferralCodeDelete(ReferralCode):
    code: str = "Your code"


class GetReferralCodeByEmail(ReferralCode):
    email: EmailStr
