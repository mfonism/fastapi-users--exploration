"""add user full_name

Revision ID: 9b4379a223f2
Revises: ae75ad39f758
Create Date: 2026-03-15 17:37:03.639302+00:00
"""

from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers (used by Alembic).
revision: str = "9b4379a223f2"
down_revision: str | Sequence[str] | None = "ae75ad39f758"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("user", sa.Column("full_name", sa.String(length=255), nullable=False))


def downgrade() -> None:
    op.drop_column("user", "full_name")
