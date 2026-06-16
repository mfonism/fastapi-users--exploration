from fastapi import APIRouter, Depends, Response, status

from ..dependencies import current_user
from ..users.manager import UserManager, get_user_manager
from ..users.models import User
from .exceptions import ChangePasswordBadPassword
from .schemas import PasswordChange

router = APIRouter()


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
        raise ChangePasswordBadPassword()

    await user_manager._update(user, {"password": password_change.new_password})
    return Response(status_code=status.HTTP_204_NO_CONTENT)
