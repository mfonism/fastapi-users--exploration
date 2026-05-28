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
current_active_verified_user_token = fastapi_users.authenticator.current_user_token(
    active=True,
    verified=True,
)
optional_current_active_verified_user_token = (
    fastapi_users.authenticator.current_user_token(
        optional=True,
        active=True,
        verified=True,
    )
)


async def current_user(
    user: User = Depends(current_active_verified_user),
) -> User:
    if user.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user


async def current_user_token(
    user_token: tuple[User, str] = Depends(current_active_verified_user_token),
) -> tuple[User, str]:
    user, _ = user_token
    if user.is_deleted:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user_token


async def optional_current_user_token(
    user_token: tuple[User | None, str | None] = Depends(
        optional_current_active_verified_user_token
    ),
) -> tuple[User, str] | None:
    user, token = user_token
    if user is None or token is None or user.is_deleted:
        return None

    return user_token
