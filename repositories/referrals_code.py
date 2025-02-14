from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from settings import ReferralCode
from src.schemes.referrals_code import ReferralCodeCreate, ReferralCodeDelete


class ReferralCodeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.model = ReferralCode

    async def save(self, code: ReferralCode) -> None:
        self.session.add(code)
        await self.session.commit()
        await self.session.refresh(code)

    async def create(self, ref_code: ReferralCodeCreate, user_id: int):
        code_in_db = self.model(**ref_code.model_dump(), user_id=user_id)
        await self.save(code_in_db)
        return ref_code

    async def get_active_code(self, user_id: int):
        db_query = select(ReferralCode).where(
            ReferralCode.user_id == user_id,
            ReferralCode.is_active == True,
        )
        codes = await self.session.execute(db_query)
        return codes.scalar_one_or_none()

    async def delete(self, ref_code: ReferralCodeDelete):
        db_query = select(self.model).where(self.model.code == ref_code.code)
        ref_code_db = await self.session.execute(db_query)
        instance = ref_code_db.scalar_one_or_none()
        if instance:
            await self.session.delete(instance)
            await self.session.commit()
        return instance
