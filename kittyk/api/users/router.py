from fastapi import APIRouter

from kittyk.api.dependencies import UserAuth
from kittyk.api.users.schemas import UserSchema


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_current_user(auth: UserAuth) -> UserSchema:
    return UserSchema.from_orm(auth.user)
