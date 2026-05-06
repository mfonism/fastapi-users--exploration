import uuid

from fastapi import Depends, HTTPException, status
from fastapi_users import FastAPIUsers

from .backends.redis import backend as redis_backend
from .models import User, get_user_manager

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [redis_backend])
current_active_verified_user = fastapi_users.current_user(
    active=True,
    verified=True,
)


async def current_user(
    user: User = Depends(current_active_verified_user),
) -> User:
    if user.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user
