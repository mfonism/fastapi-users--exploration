from datetime import timedelta

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils import clock
from .email_identity import normalize_email
from .models import (
    User,
    UserEmailChange,
    generate_email_change_token,
    hash_email_change_token,
)

EMAIL_CHANGE_TOKEN_LIFETIME_SECONDS = 3600
USER_EMAIL_UNIQUE_INDEX = "ix_user_email"


class EmailChangeEmailTaken(Exception):
    pass


class EmailChangeBadToken(Exception):
    pass


class EmailChangeSameEmail(Exception):
    pass


async def request_email_change(
    *,
    session: AsyncSession,
    user: User,
    new_email: EmailStr,
) -> tuple[UserEmailChange, str]:
    new_email = normalize_email(str(new_email))
    if new_email == user.email:
        raise EmailChangeSameEmail()

    existing_user = await session.scalar(select(User).where(User.email == new_email))
    if existing_user is not None:
        raise EmailChangeEmailTaken()

    await cancel_unresolved_email_changes(session=session, user=user)

    token = generate_email_change_token()
    now = clock.utcnow()
    email_change = UserEmailChange(
        user_id=user.id,
        old_email=user.email,
        new_email=new_email,
        token_hash=hash_email_change_token(token),
        expires_at=now + timedelta(seconds=EMAIL_CHANGE_TOKEN_LIFETIME_SECONDS),
    )
    session.add(email_change)
    await session.flush()

    return email_change, token


async def cancel_unresolved_email_changes(
    *,
    session: AsyncSession,
    user: User,
) -> None:
    unresolved_email_changes = await session.scalars(
        select(UserEmailChange).where(
            UserEmailChange.user_id == user.id,
            UserEmailChange.confirmed_at.is_(None),
            UserEmailChange.cancelled_at.is_(None),
        )
    )

    for email_change in unresolved_email_changes:
        email_change.cancel()


async def confirm_email_change(
    *,
    session: AsyncSession,
    token: str,
) -> UserEmailChange:
    email_change = await session.scalar(
        select(UserEmailChange).where(
            UserEmailChange.token_hash == hash_email_change_token(token)
        )
    )
    if email_change is None:
        raise EmailChangeBadToken()

    if not email_change.is_usable():
        raise EmailChangeBadToken()

    user = await session.get(User, email_change.user_id)
    if user is None:
        raise EmailChangeBadToken()

    if user.is_deleted or not user.is_active:
        raise EmailChangeBadToken()

    existing_user = await session.scalar(
        select(User).where(
            User.email == email_change.new_email,
            User.id != user.id,
        )
    )
    if existing_user is not None:
        raise EmailChangeEmailTaken()

    if not email_change.confirm():
        raise EmailChangeBadToken()

    user.email = email_change.new_email
    user.verified_at = email_change.confirmed_at
    try:
        await session.flush()
    except IntegrityError as error:
        if _is_user_email_unique_violation(error):
            raise EmailChangeEmailTaken() from None

        raise

    return email_change


def _is_user_email_unique_violation(error: IntegrityError) -> bool:
    constraint_names = (
        getattr(error.orig, "constraint_name", None),
        getattr(error.orig.__cause__, "constraint_name", None),
    )
    return USER_EMAIL_UNIQUE_INDEX in constraint_names
