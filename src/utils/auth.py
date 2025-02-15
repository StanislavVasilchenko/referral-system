from datetime import datetime, timezone, timedelta
from pathlib import Path

import jwt
from settings.config import settings


def encode_jwt_token(
    payload: dict,
    private_key: Path = settings.jwt_auth.private_key.read_text(),
    algorithm: str = settings.jwt_auth.algorithm,
    expires_minutes: int = settings.jwt_auth.access_token_expire,
    expires_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expires_timedelta:
        expire = now + expires_timedelta
    else:
        expire = now + timedelta(minutes=expires_minutes)
    to_encode.update(
        exp=expire,
    )

    encoded_jwt = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm,
    )
    return encoded_jwt


def decode_jwt_token(
    token: str | bytes,
    public_key: Path = settings.jwt_auth.public_key.read_text(),
    algorithm: str = settings.jwt_auth.algorithm,
):
    decoded_jwt = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded_jwt
