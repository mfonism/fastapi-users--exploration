"""add terms acceptance tables

Revision ID: d87cad1ea74e
Revises: 94f3be8bd8e6
Create Date: 2026-07-04 17:52:57.136496+00:00
"""

from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers (used by Alembic).
revision: str = "d87cad1ea74e"
down_revision: str | Sequence[str] | None = "94f3be8bd8e6"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "terms_document",
        sa.Column("id", sa.Uuid(), server_default=sa.text("uuidv7()"), nullable=False),
        sa.Column("kind", sa.String(length=50), nullable=False),
        sa.Column("version", sa.String(length=64), nullable=False),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("retired_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("kind", "version", name="uq_terms_document_kind_version"),
    )
    op.create_table(
        "user_terms_acceptance",
        sa.Column("id", sa.Uuid(), server_default=sa.text("uuidv7()"), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("terms_document_id", sa.Uuid(), nullable=False),
        sa.Column("accepted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["terms_document_id"],
            ["terms_document.id"],
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id",
            "terms_document_id",
            name="uq_user_terms_acceptance_user_document",
        ),
    )
    op.create_index(
        op.f("ix_user_terms_acceptance_terms_document_id"),
        "user_terms_acceptance",
        ["terms_document_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_terms_acceptance_user_id"),
        "user_terms_acceptance",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_user_terms_acceptance_user_id"), table_name="user_terms_acceptance"
    )
    op.drop_index(
        op.f("ix_user_terms_acceptance_terms_document_id"),
        table_name="user_terms_acceptance",
    )
    op.drop_table("user_terms_acceptance")
    op.drop_table("terms_document")
