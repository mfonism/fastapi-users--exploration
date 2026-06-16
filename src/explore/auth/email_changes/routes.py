from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from ...db.config import get_async_session
from ..backends.redis import backend as redis_backend
from ..dependencies import current_user, optional_current_user_token
from ..notifications import send_email_change_request
from ..users.models import User
from .schemas import EmailChangeConfirm, EmailChangeRequest
from .service import confirm_email_change, request_email_change

router = APIRouter()


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
    _, token = await request_email_change(
        session=session,
        user=user,
        new_email=email_change_request.new_email,
    )

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
    email_change = await confirm_email_change(
        session=session,
        token=email_change_confirm.token,
    )

    if user_token is not None:
        user, token = user_token
        if user.id == email_change.user_id:
            await redis_backend.logout(strategy, user, token)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
