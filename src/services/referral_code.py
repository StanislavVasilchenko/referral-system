from asyncpg import DataError
from sqlalchemy.exc import IntegrityError
from repositories.referrals_code import ReferralCodeRepository
from settings.db_helper import db_helper
from src.exceptions.referral_code import (
    ReferralCodeException,
    ReferralCodeNotFound,
)
from src.schemes.referrals_code import (
    ReferralCodeCreate,
    ReferralCodeDelete,
    GetReferralCodeByEmail,
)


class ReferralCodeService:

    repository = ReferralCodeRepository(session=db_helper.scoped_session())

    async def created_referral_code(
        self, referral_code: ReferralCodeCreate, user_id: int
    ):
        user_code = await self.repository.get_active_code(user_id=user_id)
        if user_code:
            user_code.is_active = False
            await self.repository.save(user_code)
        try:
            code = await self.repository.create(referral_code, user_id)
        except IntegrityError:
            raise ReferralCodeException

        return code

    async def delete_referral_code(self, referral_code: ReferralCodeDelete):
        result = await self.repository.delete(referral_code)
        if not result:
            raise ReferralCodeNotFound
        return referral_code

    async def get_referral_code_by_email(self, query: GetReferralCodeByEmail):
        ref_code = await self.repository.get_referral_code_by_email(query)
        if not ref_code:
            raise ReferralCodeNotFound
        return ref_code
