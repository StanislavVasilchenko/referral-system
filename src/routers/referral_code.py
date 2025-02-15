from fastapi import APIRouter, Depends, Query
from starlette import status

from src.schemes.referrals_code import (
    ReferralCodeCreate,
    ReferralCodeDelete,
    GetReferralCodeByEmail,
    ReferralCodeOut,
)
from src.schemes.users import UserSchema
from src.services.referral_code import ReferralCodeService

from src.services.users import UserService
from src.dependencies.auth_user import get_token_payload

user_services = UserService()
code_services = ReferralCodeService()
router = APIRouter(prefix="/api/referral_code", tags=["Referral Code"])


@router.post(
    "/create",
    response_model=ReferralCodeOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create Referral Code",
    description="Create Referral Code",
)
async def create_code(
    form_data: ReferralCodeCreate,
    user: UserSchema = Depends(user_services.get_current_user),
):
    return await code_services.created_referral_code(form_data, user.id)


@router.post(
    "/delete",
    dependencies=[Depends(get_token_payload)],
    status_code=status.HTTP_200_OK,
    summary="Delete Referral Code",
    description="Delete Referral Code",
)
async def delete_code(code: ReferralCodeDelete):
    ref_code = await code_services.delete_referral_code(code)
    return {
        "success": f"{ref_code.code} deleted successfully",
    }


@router.get(
    "/get_referral_code",
    response_model=ReferralCodeOut,
    dependencies=[
        Depends(get_token_payload),
    ],
    summary="Get Referral Code",
    description="Get Referral Code By User Email",
)
async def get_referral_code(
    form_data: GetReferralCodeByEmail = Query(),
):
    return await code_services.get_referral_code_by_email(form_data)
