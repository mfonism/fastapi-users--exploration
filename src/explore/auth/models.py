import uuid
from datetime import datetime

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import DateTime, String, func, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import FetchedValue

from ..db.base import Base
from ..db.config import get_async_session
from ..settings import settings
from ..utils import clock
from .notifications import send_verification_request


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


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.reset_password_token_secret
    verification_token_secret = settings.verification_token_secret

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

    async def on_after_login(
        self,
        user: User,
        request: Request | None = None,
        response: Response | None = None,
    ) -> None:
        await self.user_db.update(user, {"last_login_at": clock.utcnow()})


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
