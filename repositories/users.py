from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from settings import User
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
        user_in_db = self.model(**user.model_dump())
        await self.save(user_in_db)
        return user

    async def get_user_by_email(self, email: str):
        query_in_db = select(self.model).where(self.model.email == email)
        result = await self._session.execute(query_in_db)
        return result.scalar()
