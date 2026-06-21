from fastapi import APIRouter, Depends, Response, status
from fastapi_users import exceptions

from ..users.manager import UserManager, get_user_manager
from .schemas import ReactivationConfirm, ReactivationRequest
from .service import confirm_reactivation, request_reactivation

router = APIRouter()


@router.post(
    "/auth/request-reactivation",
    status_code=status.HTTP_202_ACCEPTED,
    response_class=Response,
    name="auth:request-reactivation",
    tags=["auth"],
)
async def request_user_reactivation(
    reactivation_request: ReactivationRequest,
    user_manager: UserManager = Depends(get_user_manager),
):
    try:
        await request_reactivation(
            user_manager=user_manager,
            email=reactivation_request.email,
        )
    except exceptions.UserNotExists:
        pass

    return Response(status_code=status.HTTP_202_ACCEPTED)


@router.post(
    "/auth/reactivate",
    status_code=status.HTTP_204_NO_CONTENT,
    name="auth:reactivate",
    tags=["auth"],
)
async def reactivate_user(
    reactivation_confirm: ReactivationConfirm,
    user_manager: UserManager = Depends(get_user_manager),
):
    await confirm_reactivation(
        user_manager=user_manager,
        token=reactivation_confirm.token,
    )

    return Response(status_code=status.HTTP_204_NO_CONTENT)
