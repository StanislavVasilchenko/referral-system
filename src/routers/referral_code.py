from fastapi import APIRouter, Depends, Query
from src.schemes.referrals_code import (
    ReferralCodeCreate,
    ReferralCodeDelete,
    GetReferralCodeByEmail,
    ReferralCodeOut,
)
from src.schemes.users import UserSchema
from src.services.referral_code import ReferralCodeService
from src.services.users import UserService

user_services = UserService()
code_services = ReferralCodeService()
router = APIRouter(prefix="/api/referral_code", tags=["Referral Code"])


@router.post("/create")
async def create_code(
    form_data: ReferralCodeCreate,
    user: UserSchema = Depends(user_services.get_current_user),
):
    return await code_services.created_referral_code(form_data, user.id)


@router.post("/delete", dependencies=[Depends(user_services.get_current_user)])
async def delete_code(code: ReferralCodeDelete):
    ref_code = await code_services.delete_referral_code(code)
    return {
        "success": f"{ref_code} deleted successfully",
    }


@router.get(
    "/get_referral_code",
    response_model=ReferralCodeOut,
    dependencies=[
        Depends(user_services.get_current_user),
    ],
)
async def get_referral_code(
    form_data: GetReferralCodeByEmail = Query(),
):
    return await code_services.get_referral_code_by_email(form_data)
