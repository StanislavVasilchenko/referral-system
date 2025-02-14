from fastapi import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from jwt import InvalidTokenError

from src.exceptions.user_exceptions import InvalidToken
from src.utils.auth import decode_jwt_token

http_bearer = HTTPBearer(bearerFormat="Bearer")


def get_token_payload(
    cred: HTTPAuthorizationCredentials = Depends(http_bearer),
):
    token = cred.credentials
    try:
        payload = decode_jwt_token(token=token)
    except InvalidTokenError:
        raise InvalidToken
    return payload
