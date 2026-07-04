"""add audit log table

Revision ID: f499d22cdeef
Revises: d87cad1ea74e
Create Date: 2026-07-04 18:07:01.666747+00:00
"""

from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers (used by Alembic).
revision: str = "f499d22cdeef"
down_revision: str | Sequence[str] | None = "d87cad1ea74e"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "audit_log_entry",
        sa.Column("id", sa.Uuid(), server_default=sa.text("uuidv7()"), nullable=False),
        sa.Column("actor_type", sa.String(length=50), nullable=False),
        sa.Column("actor_user_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("target_type", sa.String(length=100), nullable=False),
        sa.Column("target_id", sa.Uuid(), nullable=True),
        sa.Column("subject_type", sa.String(length=100), nullable=True),
        sa.Column("subject_id", sa.Uuid(), nullable=True),
        sa.Column("occurred_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("user_agent", sa.String(length=512), nullable=True),
        sa.Column("request_id", sa.String(length=128), nullable=True),
        sa.Column("reason", sa.String(length=512), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["actor_user_id"], ["user.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_audit_log_entry_action"), "audit_log_entry", ["action"], unique=False
    )
    op.create_index(
        op.f("ix_audit_log_entry_actor_user_id"),
        "audit_log_entry",
        ["actor_user_id"],
        unique=False,
    )
    op.create_index(
        "ix_audit_log_entry_subject",
        "audit_log_entry",
        ["subject_type", "subject_id"],
        unique=False,
    )
    op.create_index(
        "ix_audit_log_entry_target",
        "audit_log_entry",
        ["target_type", "target_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_audit_log_entry_target", table_name="audit_log_entry")
    op.drop_index("ix_audit_log_entry_subject", table_name="audit_log_entry")
    op.drop_index(
        op.f("ix_audit_log_entry_actor_user_id"), table_name="audit_log_entry"
    )
    op.drop_index(op.f("ix_audit_log_entry_action"), table_name="audit_log_entry")
    op.drop_table("audit_log_entry")
