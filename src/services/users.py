import bcrypt
from fastapi.params import Depends
from sqlalchemy.exc import IntegrityError
from repositories.users import UsersRepository
from settings.db_helper import db_helper
from src.dependencies.auth_user import (
    get_token_payload,
    create_access_token,
    create_refresh_token,
)
from src.exceptions.user_exceptions import (
    UserNotFoundException,
    InvalidEmailOrPassword,
    UserExistsException,
    UserWithCodeNotFound,
)
from src.schemes.users import (
    UserCreate,
    UserOut,
    UserLogin,
    UserSchema,
)


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
            if not user.code:
                return await self.repository.create(user)
            return await self.repository.create_user_by_code(user)
        except IntegrityError:
            raise UserExistsException
        except AttributeError:
            raise UserWithCodeNotFound

    async def login_user(self, user: UserLogin) -> tuple:
        user_db = await self.repository.get_user_by_email(user.email)
        if not user_db:
            raise UserNotFoundException
        if not validate_password(user.password, user_db.password):
            raise InvalidEmailOrPassword

        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        return access_token, refresh_token

    async def get_current_user(self, payload: dict = Depends(get_token_payload)):
        return await self.repository.get_user_by_email(payload.get("email"))

    async def get_referrals_auth_user(self, user: UserSchema):
        return await self.repository.get_referrals(user.id)

    async def get_referrals(self, referral_id: int):
        return await self.repository.get_referrals(referral_id)
