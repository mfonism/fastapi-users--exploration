from fastapi_users.jwt import generate_jwt
from pydantic import EmailStr

from ...settings import settings
from ...utils.email import normalize_email
from ..notifications import send_reactivation_request
from ..users.manager import UserManager

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
