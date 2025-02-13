from fastapi import APIRouter, Depends
from src.schemes.users import UserOut, UserCreate
from src.services.users import UserService

service = UserService()
router = APIRouter(tags=["users"])


@router.post("/registration", response_model=UserOut)
async def create_user(user: UserCreate):
    return await service.create_user(user)
