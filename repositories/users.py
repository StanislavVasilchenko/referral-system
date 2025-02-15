from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from settings import User
from src.models.referral_code import ReferralCode
from src.schemes.users import UserCreate


class UsersRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        self.model = User

    async def save(self, user: User):
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)

    async def create(self, user: UserCreate):
        user_in_db = self.model(
            email=user.email,
            password=user.password,
        )
        await self.save(user_in_db)
        return user

    async def get_user_by_email(self, email: str):
        query_in_db = select(self.model).where(self.model.email == email)
        result = await self._session.execute(query_in_db)
        return result.scalar()

    async def create_user_by_code(self, user: UserCreate):
        referral = await self.get_user_by_ref_code(user.code)
        user_in_db = self.model(
            email=user.email,
            password=user.password,
            referred_by=referral.id,
        )
        await self.save(user_in_db)
        return user

    async def get_user_by_ref_code(self, ref_code: str):
        query_in_db = (
            select(self.model)
            .join(ReferralCode)
            .where(
                ReferralCode.code == ref_code,
                ReferralCode.is_active == True,
            )
        )
        result = await self._session.execute(query_in_db)
        return result.scalar()

    async def get_referrals(self, user_id: int):
        query_in_db = select(self.model).where(self.model.referred_by == user_id)
        result = await self._session.execute(query_in_db)
        return result.scalars()
