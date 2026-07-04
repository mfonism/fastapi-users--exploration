from fastapi import APIRouter, Depends, Request, Response, status

from ..dependencies import current_user
from ..users.manager import UserManager, get_user_manager
from ..users.models import User
from .schemas import PasswordChange
from .service import change_user_password

router = APIRouter()


@router.post(
    "/auth/change-password",
    status_code=status.HTTP_204_NO_CONTENT,
    name="auth:change-password",
    tags=["auth"],
)
async def change_password(
    request: Request,
    password_change: PasswordChange,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    await change_user_password(
        user=user,
        user_manager=user_manager,
        current_password=password_change.current_password,
        new_password=password_change.new_password,
        request=request,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
