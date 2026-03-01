import uuid
from datetime import datetime, timezone

from fastapi import Depends
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from .. import settings
from ..db.base import Base
from ..db.config import get_async_session


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    superuser_granted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deactivated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    terms_accepted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    @property
    def is_active(self) -> bool:
        return self.deactivated_at is None

    @is_active.setter
    def is_active(self, value: bool) -> None:
        self.deactivated_at = None if value else datetime.now(timezone.utc)

    @property
    def is_verified(self) -> bool:
        return self.verified_at is not None

    @is_verified.setter
    def is_verified(self, value: bool) -> None:
        self.verified_at = datetime.now(timezone.utc) if value else None

    @property
    def is_superuser(self) -> bool:
        return self.superuser_granted_at is not None

    @is_superuser.setter
    def is_superuser(self, value: bool) -> None:
        self.superuser_granted_at = datetime.now(timezone.utc) if value else None


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.RESET_PASSWORD_TOKEN_SECRET
    verification_token_secret = settings.VERIFICATION_TOKEN_SECRET


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
