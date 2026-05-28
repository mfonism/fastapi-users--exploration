from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..db.config import get_async_session
from .backends.redis import backend as redis_backend
from .dependencies import (
    current_user,
    current_user_token,
    fastapi_users,
    optional_current_user_token,
)
from .email_changes import (
    EmailChangeBadToken,
    EmailChangeEmailTaken,
    EmailChangeSameEmail,
    confirm_email_change,
    request_email_change,
)
from .models import User, UserManager, get_user_manager
from .notifications import send_email_change_request
from .schemas import (
    CurrentUserRead,
    CurrentUserUpdate,
    EmailChangeConfirm,
    EmailChangeRequest,
    PasswordChange,
    UserCreate,
)

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


@router.post(
    "/auth/request-email-change",
    status_code=status.HTTP_204_NO_CONTENT,
    name="auth:request-email-change",
    tags=["auth"],
)
async def request_current_user_email_change(
    email_change_request: EmailChangeRequest,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    try:
        _, token = await request_email_change(
            session=session,
            user=user,
            new_email=email_change_request.new_email,
        )
    except EmailChangeSameEmail:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="EMAIL_CHANGE_SAME_EMAIL",
        ) from None
    except EmailChangeEmailTaken:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="EMAIL_CHANGE_EMAIL_TAKEN",
        ) from None

    await send_email_change_request(
        recipient_email=str(email_change_request.new_email),
        recipient_name=user.full_name,
        token=token,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/auth/confirm-email-change",
    status_code=status.HTTP_204_NO_CONTENT,
    name="auth:confirm-email-change",
    tags=["auth"],
)
async def confirm_current_user_email_change(
    email_change_confirm: EmailChangeConfirm,
    user_token: tuple[User, str] | None = Depends(optional_current_user_token),
    session: AsyncSession = Depends(get_async_session),
    strategy=Depends(redis_backend.get_strategy),
):
    try:
        email_change = await confirm_email_change(
            session=session,
            token=email_change_confirm.token,
        )
    except EmailChangeBadToken:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="EMAIL_CHANGE_BAD_TOKEN",
        ) from None
    except EmailChangeEmailTaken:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="EMAIL_CHANGE_EMAIL_TAKEN",
        ) from None

    if user_token is not None:
        user, token = user_token
        if user.id == email_change.user_id:
            await redis_backend.logout(strategy, user, token)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


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
