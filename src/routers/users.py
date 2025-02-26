from fastapi import APIRouter, Query, Depends
from src.dependencies.auth_user import get_token_payload
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


@router.post(
    "/registration",
    response_model=UserOut,
    summary="Register a new user",
    description="Register a new user",
)
async def create_user(user: UserCreate):
    return await service.create_user(user)


@router.post(
    "/login",
    response_model=UserTokenInfo,
    summary="Login a user",
    description="Login a user and create JWT token",
)
async def auth_user(user: UserLogin):
    access_token, refresh_token = await service.login_user(user)
    return UserTokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.get(
    "/me_referrals",
    response_model=list[UserOut],
    summary="Get all referrals user",
    description="Get all referrals of an authorized user",
)
async def me_referrals(user: UserSchema = Depends(service.get_current_user)):
    return await service.get_referrals_auth_user(user)


@router.get(
    "/referrals",
    response_model=list[UserOut],
    dependencies=[Depends(get_token_payload)],
    summary="Get all referrals by user id",
    description="Get all referrals by user id",
)
async def get_referrals(referral_id: int = Query()):
    return await service.get_referrals(referral_id)
