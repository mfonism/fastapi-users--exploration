from fastapi import APIRouter, Depends, status

from ..backends.redis import backend as redis_backend
from ..dependencies import current_user, current_user_token
from ..models import User, UserManager, get_user_manager
from .schemas import CurrentUserRead, CurrentUserUpdate

router = APIRouter()


@router.get(
    "/users/me",
    response_model=CurrentUserRead,
    name="users:current_user",
    tags=["users"],
)
async def get_current_user(user: User = Depends(current_user)):
    return user


@router.patch(
    "/users/me",
    response_model=CurrentUserRead,
    name="users:patch_current_user",
    tags=["users"],
)
async def update_current_user(
    user_update: CurrentUserUpdate,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    return await user_manager._update(user, user_update.create_update_dict())


@router.delete(
    "/users/me",
    status_code=status.HTTP_204_NO_CONTENT,
    name="users:delete_current_user",
    tags=["users"],
)
async def delete_current_user(
    user_token: tuple[User, str] = Depends(current_user_token),
    user_manager: UserManager = Depends(get_user_manager),
    strategy=Depends(redis_backend.get_strategy),
):
    user, token = user_token
    await user_manager._update(user, {"is_deleted": True})
    return await redis_backend.logout(strategy, user, token)
