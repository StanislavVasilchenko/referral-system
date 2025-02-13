import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
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

    async def create_user(self, user: UserCreate) -> UserOut | dict[str:str]:
        user.password = hashed_password(user.password)
        try:
            return await self.repository.create(user)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User already exists",
            )
