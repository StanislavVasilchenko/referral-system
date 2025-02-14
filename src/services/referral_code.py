from asyncpg import DataError
from sqlalchemy.exc import IntegrityError
from repositories.referrals_code import ReferralCodeRepository
from settings.db_helper import db_helper
from src.exceptions.referral_code import ReferralCodeException
from src.schemes.referrals_code import ReferralCodeCreate


class ReferralCodeService:

    repository = ReferralCodeRepository(session=db_helper.scoped_session())

    async def created_referral_code(
        self, referral_code: ReferralCodeCreate, user_id: int
    ):
        try:
            code = await self.repository.create(referral_code, user_id)
        except IntegrityError:
            raise ReferralCodeException

        return code
