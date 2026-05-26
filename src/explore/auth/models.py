import hashlib
import secrets
import uuid
from datetime import datetime
from typing import Any

import jwt
from fastapi import Depends, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, UUIDIDMixin, exceptions
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users.jwt import decode_jwt
from sqlalchemy import DateTime, ForeignKey, String, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import FetchedValue

from ..db.base import Base
from ..db.config import get_async_session
from ..settings import settings
from ..utils import clock
from .exceptions import UserDeleted
from .notifications import send_password_reset_request, send_verification_request

EMAIL_CHANGE_TOKEN_BYTES = 32


def generate_email_change_token() -> str:
    return secrets.token_urlsafe(EMAIL_CHANGE_TOKEN_BYTES)


def hash_email_change_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


class User(Base):
    __tablename__ = "user"

    # Identity
    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        server_default=text("uuidv7()"),
    )
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    full_name: Mapped[str] = mapped_column(String(length=255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)

    # Account status
    verified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deactivated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Authorization
    superuser_granted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Compliance
    terms_accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Activity
    last_login_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Audit timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        server_onupdate=FetchedValue(),
    )

    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, email={self.email!r}, full_name={self.full_name!r})"
        )

    @property
    def is_active(self) -> bool:
        return self.deactivated_at is None

    @is_active.setter
    def is_active(self, value: bool) -> None:
        if value == self.is_active:
            return

        self.deactivated_at = None if value else clock.utcnow()

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None

    @is_deleted.setter
    def is_deleted(self, value: bool) -> None:
        if value == self.is_deleted:
            return

        self.deleted_at = clock.utcnow() if value else None

    @property
    def is_verified(self) -> bool:
        return self.verified_at is not None

    @is_verified.setter
    def is_verified(self, value: bool) -> None:
        if value == self.is_verified:
            return

        self.verified_at = clock.utcnow() if value else None

    @property
    def is_superuser(self) -> bool:
        return self.superuser_granted_at is not None

    @is_superuser.setter
    def is_superuser(self, value: bool) -> None:
        if value == self.is_superuser:
            return

        self.superuser_granted_at = clock.utcnow() if value else None


class UserEmailChange(Base):
    __tablename__ = "user_email_change"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        server_default=text("uuidv7()"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    old_email: Mapped[str] = mapped_column(String(length=320), nullable=False)
    new_email: Mapped[str] = mapped_column(String(length=320), nullable=False)
    token_hash: Mapped[str] = mapped_column(
        String(length=64),
        unique=True,
        index=True,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    confirmed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    cancelled_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    def is_usable(self) -> bool:
        return (
            self.confirmed_at is None
            and self.cancelled_at is None
            and self.expires_at > clock.utcnow()
        )

    def confirm(self) -> bool:
        confirmed_at = clock.utcnow()
        if (
            self.confirmed_at is not None
            or self.cancelled_at is not None
            or self.expires_at <= confirmed_at
        ):
            return False

        self.confirmed_at = confirmed_at
        return True

    def cancel(self) -> bool:
        if self.cancelled_at is not None or self.confirmed_at is not None:
            return False

        self.cancelled_at = clock.utcnow()
        return True


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.reset_password_token_secret
    verification_token_secret = settings.verification_token_secret

    def _raise_if_deleted(self, user: User) -> None:
        if user.is_deleted:
            raise UserDeleted()

    async def authenticate(self, credentials: OAuth2PasswordRequestForm):
        user = await super().authenticate(credentials)

        if user is not None:
            self._raise_if_deleted(user)

        return user

    async def request_verify(self, user: User, request: Request | None = None) -> None:
        self._raise_if_deleted(user)
        await super().request_verify(user, request)

    async def forgot_password(self, user: User, request: Request | None = None) -> None:
        self._raise_if_deleted(user)
        await super().forgot_password(user, request)

    async def verify(self, token: str, request: Request | None = None) -> User:
        try:
            return await super().verify(token, request)
        except exceptions.UserAlreadyVerified:
            return await self._get_already_verified_user(token)

    async def _get_already_verified_user(self, token: str) -> User:
        try:
            data = decode_jwt(
                token,
                self.verification_token_secret,
                [self.verification_token_audience],
            )
        except jwt.PyJWTError:
            raise exceptions.InvalidVerifyToken() from None

        try:
            email = data["email"]
        except KeyError:
            raise exceptions.InvalidVerifyToken() from None

        try:
            user = await self.get_by_email(email)
        except exceptions.UserNotExists:
            raise exceptions.InvalidVerifyToken() from None

        self._raise_if_deleted(user)
        return user

    async def _update(self, user: User, update_dict: dict[str, Any]) -> User:
        self._raise_if_deleted(user)
        return await super()._update(user, update_dict)

    async def on_after_register(self, user: User, request: Request | None = None):
        await self.request_verify(user, request)

    async def on_after_request_verify(
        self, user: User, token: str, request: Request | None = None
    ):
        await send_verification_request(
            recipient_email=user.email,
            recipient_name=user.full_name,
            token=token,
        )

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ):
        await send_password_reset_request(
            recipient_email=user.email,
            recipient_name=user.full_name,
            token=token,
        )

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        await self.user_db.update(user, {"last_login_at": clock.utcnow()})


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
