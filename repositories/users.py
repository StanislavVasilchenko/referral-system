from sqlalchemy.ext.asyncio import AsyncSession
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
