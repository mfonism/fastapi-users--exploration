from fastapi import APIRouter, Depends, HTTPException, Response, status

from .backends.redis import backend as redis_backend
from .dependencies import (
    current_user,
    fastapi_users,
)
from .email_changes.routes import router as email_changes_router
from .models import User, UserManager, get_user_manager
from .schemas import (
    PasswordChange,
    UserCreate,
)
from .users.routes import router as users_router
from .users.schemas import CurrentUserRead

router = APIRouter()

auth_router = fastapi_users.get_auth_router(
    redis_backend,
    requires_verification=True,
)

logout_route = next(
    (route for route in auth_router.routes if route.name == "auth:redis.logout"),
    None,
)

if logout_route:
    logout_route.status_code = status.HTTP_204_NO_CONTENT

router.include_router(
    auth_router,
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(CurrentUserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(CurrentUserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(email_changes_router)
router.include_router(users_router)


@router.post(
    "/auth/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    name="auth:change-password",
    tags=["auth"],
)
async def change_password(
    password_change: PasswordChange,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    password_verified, _ = user_manager.password_helper.verify_and_update(
        password_change.current_password,
        user.hashed_password,
    )
    if not password_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CHANGE_PASSWORD_BAD_PASSWORD",
        )

    await user_manager._update(user, {"password": password_change.new_password})
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/auth/deactivate",
    status_code=status.HTTP_204_NO_CONTENT,
    name="auth:deactivate",
    tags=["auth"],
)
async def deactivate(
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    await user_manager._update(user, {"is_active": False})
    return Response(status_code=status.HTTP_204_NO_CONTENT)
