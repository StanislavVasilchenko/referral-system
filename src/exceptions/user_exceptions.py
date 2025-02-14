from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    def __init__(
        self,
        detail: str = "User not found",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        self.detail = detail
        self.status_code = status_code


class InvalidEmailOrPassword(HTTPException):
    def __init__(
        self,
        detail: str = "Invalid email or password",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        self.detail = detail
        self.status_code = status_code


class InvalidToken(HTTPException):
    def __init__(
        self,
        detail: str = "Not authenticated",
        status_code: int = status.HTTP_401_UNAUTHORIZED,
    ):
        self.detail = detail
        self.status_code = status_code
