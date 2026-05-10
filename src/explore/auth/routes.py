from fastapi import APIRouter, Depends, HTTPException, Response, status

from .backends.redis import backend as redis_backend
from .dependencies import current_user, fastapi_users
from .models import User, UserManager, get_user_manager
from .schemas import PasswordChange, UserCreate, UserRead, UserUpdate

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(redis_backend, requires_verification=True),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


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


router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


@router.get("/whoami", response_model=UserRead, tags=["users"])
async def whoami(user: User = Depends(current_user)):
    return user
