"""initial schema

Revision ID: 26756803edf8
Revises:
Create Date: 2026-03-05 09:03:58.085931+00:00

"""

from typing import Sequence, Union


# revision identifiers (used by Alembic).
revision: str = "26756803edf8"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
