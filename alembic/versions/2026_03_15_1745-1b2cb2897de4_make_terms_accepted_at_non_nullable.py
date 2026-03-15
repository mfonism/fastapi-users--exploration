"""make terms_accepted_at non-nullable

Revision ID: 1b2cb2897de4
Revises: 9b4379a223f2
Create Date: 2026-03-15 17:45:46.454623+00:00
"""

from typing import Sequence

from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers (used by Alembic).
revision: str = "1b2cb2897de4"
down_revision: str | Sequence[str] | None = "9b4379a223f2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "user",
        "terms_accepted_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )


def downgrade() -> None:
    op.alter_column(
        "user",
        "terms_accepted_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )
