import jwt
from fastapi_users import exceptions
from fastapi_users.jwt import decode_jwt, generate_jwt
from pydantic import EmailStr

from ...settings import settings
from ...utils.email import normalize_email
from ..notifications import send_reactivation_request
from ..users.manager import UserManager
from ..users.models import User
from .exceptions import ReactivationBadToken

REACTIVATION_TOKEN_AUDIENCE = "explore:auth:reactivate"
REACTIVATION_TOKEN_LIFETIME_SECONDS = 3600


async def request_reactivation(
    *,
    user_manager: UserManager,
    email: EmailStr,
) -> None:
    user = await user_manager.get_by_email(normalize_email(str(email)))
    if user.is_deleted or user.is_active:
        return

    token = generate_jwt(
        {
            "sub": str(user.id),
            "deactivated_at": user.deactivated_at.isoformat(),
            "aud": REACTIVATION_TOKEN_AUDIENCE,
        },
        settings.reactivation_token_secret,
        REACTIVATION_TOKEN_LIFETIME_SECONDS,
    )

    await send_reactivation_request(
        recipient_email=user.email,
        recipient_name=user.full_name,
        token=token,
    )


async def confirm_reactivation(
    *,
    user_manager: UserManager,
    token: str,
) -> User:
    try:
        data = decode_jwt(
            token,
            settings.reactivation_token_secret,
            [REACTIVATION_TOKEN_AUDIENCE],
        )
    except jwt.PyJWTError:
        raise ReactivationBadToken() from None

    try:
        user_id = data["sub"]
        deactivated_at = data["deactivated_at"]
    except KeyError:
        raise ReactivationBadToken() from None

    try:
        parsed_id = user_manager.parse_id(user_id)
    except exceptions.InvalidID:
        raise ReactivationBadToken() from None

    try:
        user = await user_manager.get(parsed_id)
    except exceptions.UserNotExists:
        raise ReactivationBadToken() from None

    if user.is_deleted or user.is_active:
        raise ReactivationBadToken()

    if user.deactivated_at is None or user.deactivated_at.isoformat() != deactivated_at:
        raise ReactivationBadToken()

    return await user_manager._update(user, {"is_active": True})
