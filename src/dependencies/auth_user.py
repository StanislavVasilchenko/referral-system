from datetime import timedelta
from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from jwt import InvalidTokenError

from settings.config import settings
from src.exceptions.user_exceptions import InvalidToken
from src.schemes.users import UserLogin
from src.utils.auth import decode_jwt_token, encode_jwt_token

http_bearer = HTTPBearer(bearerFormat="Bearer")


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.jwt_auth.access_token_expire,
    expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {
        "type": token_type,
    }
    jwt_payload.update(token_data)
    return encode_jwt_token(
        payload=jwt_payload,
        expires_minutes=expire_minutes,
        expires_timedelta=expire_timedelta,
    )


def create_access_token(user: UserLogin) -> str:
    payload = {
        "sub": user.email.split("@")[0],
        "email": user.email,
    }
    return create_jwt(
        token_type="access",
        token_data=payload,
    )


def create_refresh_token(user: UserLogin) -> str:
    payload = {
        "email": user.email,
    }
    return create_jwt(
        token_type="refresh",
        token_data=payload,
        expire_timedelta=timedelta(days=settings.jwt_auth.refresh_token_expire_days),
    )


def get_token_payload(
    cred: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = cred.credentials
    try:
        payload = decode_jwt_token(token=token)
    except InvalidTokenError:
        raise InvalidToken
    return payload
