import uuid
from datetime import datetime
from enum import StrEnum

from sqlalchemy import DateTime, ForeignKey, Index, String, func, text
from sqlalchemy.orm import Mapped, mapped_column

from ..db.base import Base


class AuditActorType(StrEnum):
    ANONYMOUS = "anonymous"
    SYSTEM = "system"
    USER = "user"


class AuditLogEntry(Base):
    __tablename__ = "audit_log_entry"
    __table_args__ = (
        Index("ix_audit_log_entry_target", "target_type", "target_id"),
        Index("ix_audit_log_entry_subject", "subject_type", "subject_id"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        server_default=text("uuidv7()"),
    )
    actor_type: Mapped[str] = mapped_column(String(length=50), nullable=False)
    actor_user_id: Mapped[uuid.UUID | None] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL"),
        index=True,
        nullable=True,
    )
    action: Mapped[str] = mapped_column(String(length=120), index=True, nullable=False)
    target_type: Mapped[str] = mapped_column(String(length=100), nullable=False)
    target_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    subject_type: Mapped[str | None] = mapped_column(String(length=100), nullable=True)
    subject_id: Mapped[uuid.UUID | None] = mapped_column(nullable=True)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    ip_address: Mapped[str | None] = mapped_column(String(length=45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(length=512), nullable=True)
    request_id: Mapped[str | None] = mapped_column(String(length=128), nullable=True)
    reason: Mapped[str | None] = mapped_column(String(length=512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
