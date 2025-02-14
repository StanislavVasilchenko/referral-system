from fastapi import HTTPException, status


class ReferralCodeException(HTTPException):
    def __init__(
        self,
        detail: str = "Referral Code Already Exists",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        self.detail = detail
        self.status_code = status_code


class ReferralCodeNotFound(HTTPException):
    def __init__(
        self,
        detail: str = "Referral Code Not Found",
        status_code: int = status.HTTP_404_NOT_FOUND,
    ):
        self.detail = detail
        self.status_code = status_code
