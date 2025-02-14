import bcrypt
from fastapi import HTTPException, status
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from repositories.users import UsersRepository
from settings.db_helper import db_helper
from src.dependencies.auth_user import get_token_payload
from src.exceptions.user_exceptions import UserNotFoundException, InvalidEmailOrPassword
from src.schemes.users import UserCreate, UserOut, UserLogin, UserTokenInfo
from src.utils.auth import encode_jwt_token


def hashed_password(
    password: str,
):
    password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return password


def validate_password(
    password: str,
    hash_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hash_password,
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

    async def login_user(self, user: UserLogin) -> UserTokenInfo:
        user_db = await self.repository.get_user_by_email(user.email)
        if not user_db:
            raise UserNotFoundException
        if not validate_password(user.password, user_db.password):
            raise InvalidEmailOrPassword
        payload = {
            "sub": user.email.split("@")[0],
            "email": user.email,
        }

        token = encode_jwt_token(payload)
        return token

    # Testing
    async def get_current_user(self, payload: dict = Depends(get_token_payload)):
        email = payload.get("email")
        user_db = await self.repository.get_user_by_email(email)
        return user_db
