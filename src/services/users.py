from repositories.users import UsersRepository
from settings.db_helper import db_helper
from src.schemes.users import UserCreate, UserOut


class UserService:

    repository = UsersRepository(session=db_helper.scoped_session())

    async def create_user(self, user: UserCreate) -> UserOut:
        return await self.repository.create(user)
