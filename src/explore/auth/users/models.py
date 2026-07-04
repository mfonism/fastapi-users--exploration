import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.schema import FetchedValue

from ...db.base import Base
from ...utils import clock


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
    email_verified_at: Mapped[datetime | None] = mapped_column(
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
        return self.email_verified_at is not None

    @is_verified.setter
    def is_verified(self, value: bool) -> None:
        if value == self.is_verified:
            return

        self.email_verified_at = clock.utcnow() if value else None

    @property
    def is_superuser(self) -> bool:
        return self.superuser_granted_at is not None

    @is_superuser.setter
    def is_superuser(self, value: bool) -> None:
        if value == self.is_superuser:
            return

        self.superuser_granted_at = clock.utcnow() if value else None
