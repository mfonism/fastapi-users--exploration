"""add user email change table

Revision ID: cdcbfcc50365
Revises: fe2898271ec2
Create Date: 2026-05-26 22:12:12.274757+00:00
"""

from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers (used by Alembic).
revision: str = "cdcbfcc50365"
down_revision: str | Sequence[str] | None = "fe2898271ec2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "user_email_change",
        sa.Column("id", sa.Uuid(), server_default=sa.text("uuidv7()"), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("old_email", sa.String(length=320), nullable=False),
        sa.Column("new_email", sa.String(length=320), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("confirmed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("cancelled_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_email_change_token_hash"),
        "user_email_change",
        ["token_hash"],
        unique=True,
    )
    op.create_index(
        op.f("ix_user_email_change_user_id"),
        "user_email_change",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_user_email_change_user_id"), table_name="user_email_change")
    op.drop_index(
        op.f("ix_user_email_change_token_hash"), table_name="user_email_change"
    )
    op.drop_table("user_email_change")
