from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base model for all users."""


class UserCreate(UserBase):
    email: EmailStr
    password: str


class UserOut(UserBase):
    email: EmailStr
