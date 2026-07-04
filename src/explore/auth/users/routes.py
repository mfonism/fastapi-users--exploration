from fastapi import APIRouter, Depends, Request, Response, status

from ..backends.redis import backend as redis_backend
from ..dependencies import current_user, current_user_token
from .manager import UserManager, get_user_manager
from .models import User
from .schemas import CurrentUserRead, CurrentUserUpdate
from .service import deactivate_user, soft_delete_user

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
    request: Request,
    user_token: tuple[User, str] = Depends(current_user_token),
    user_manager: UserManager = Depends(get_user_manager),
    strategy=Depends(redis_backend.get_strategy),
):
    user, token = user_token
    await soft_delete_user(user=user, user_manager=user_manager, request=request)
    return await redis_backend.logout(strategy, user, token)


@router.post(
    "/auth/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
    name="auth:deactivate",
    tags=["auth"],
)
async def deactivate(
    request: Request,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    await deactivate_user(user=user, user_manager=user_manager, request=request)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
