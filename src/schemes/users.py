from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base model for all users."""


class UserCreate(UserBase):
    email: EmailStr
    password: str = "123qwerty"


class UserOut(UserBase):
    email: EmailStr


class UserLogin(UserBase):
    email: EmailStr
    password: str = "123qwerty"


class UserTokenInfo(UserBase):
    access_token: str
    token_type: str
