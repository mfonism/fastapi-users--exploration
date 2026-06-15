import hashlib
import secrets
import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ...db.base import Base
from ...utils import clock

EMAIL_CHANGE_TOKEN_BYTES = 32


def generate_email_change_token() -> str:
    return secrets.token_urlsafe(EMAIL_CHANGE_TOKEN_BYTES)


def hash_email_change_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


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
