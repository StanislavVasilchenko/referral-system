from fastapi import APIRouter, Query, Depends
from src.schemes.users import (
    UserOut,
    UserCreate,
    UserLogin,
    UserTokenInfo,
    UserSchema,
)
from src.services.users import UserService

service = UserService()
router = APIRouter(prefix="/api/user", tags=["Users"])


@router.post("/registration", response_model=UserOut)
async def create_user(user: UserCreate):
    return await service.create_user(user)


@router.post("/login", response_model=UserTokenInfo)
async def auth_user(user: UserLogin):
    token_jwt = await service.login_user(user)
    return UserTokenInfo(
        access_token=token_jwt,
        token_type="Bearer",
    )


@router.get("/me_referrals", response_model=list[UserOut])
async def me_referrals(user: UserSchema = Depends(service.get_current_user)):
    return await service.get_referrals_by_id(user)
