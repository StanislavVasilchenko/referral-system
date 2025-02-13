import bcrypt
from repositories.users import UsersRepository
from settings.db_helper import db_helper
from src.schemes.users import UserCreate, UserOut


def hashed_password(
    password: str,
):
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode("utf-8")
    return password


def validate_password(
    password: str,
    hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )


class UserService:

    repository = UsersRepository(session=db_helper.scoped_session())

    async def create_user(self, user: UserCreate) -> UserOut:
        user.password = hashed_password(user.password)
        return await self.repository.create(user)
