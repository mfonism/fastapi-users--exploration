import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
    UniqueConstraint,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from ...db.base import Base


class TermsDocument(Base):
    __tablename__ = "terms_document"
    __table_args__ = (
        UniqueConstraint("kind", "version", name="uq_terms_document_kind_version"),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        server_default=text("uuidv7()"),
    )
    kind: Mapped[str] = mapped_column(String(length=50), nullable=False)
    version: Mapped[str] = mapped_column(String(length=64), nullable=False)
    published_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    retired_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )


class UserTermsAcceptance(Base):
    __tablename__ = "user_terms_acceptance"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "terms_document_id",
            name="uq_user_terms_acceptance_user_document",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        server_default=text("uuidv7()"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )
    terms_document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("terms_document.id"),
        index=True,
        nullable=False,
    )
    accepted_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    ip_address: Mapped[str | None] = mapped_column(String(length=45), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(length=512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
