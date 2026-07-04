"""rename verified_at to email_verified_at

Revision ID: 94f3be8bd8e6
Revises: cdcbfcc50365
Create Date: 2026-07-04 17:48:41.401278+00:00
"""

from typing import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers (used by Alembic).
revision: str = "94f3be8bd8e6"
down_revision: str | Sequence[str] | None = "cdcbfcc50365"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def set_user_updated_at_function(verification_column: str) -> str:
    return f"""
        CREATE OR REPLACE FUNCTION set_user_updated_at() RETURNS trigger AS $$
        BEGIN
            IF ROW(
                NEW.email,
                NEW.full_name,
                NEW.hashed_password,
                NEW.{verification_column},
                NEW.deactivated_at,
                NEW.deleted_at,
                NEW.superuser_granted_at,
                NEW.terms_accepted_at
            ) IS DISTINCT FROM ROW(
                OLD.email,
                OLD.full_name,
                OLD.hashed_password,
                OLD.{verification_column},
                OLD.deactivated_at,
                OLD.deleted_at,
                OLD.superuser_granted_at,
                OLD.terms_accepted_at
            ) THEN
                NEW.updated_at = CURRENT_TIMESTAMP;
            END IF;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql
    """


def upgrade() -> None:
    op.alter_column(
        "user",
        "verified_at",
        new_column_name="email_verified_at",
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=True,
    )
    op.execute(set_user_updated_at_function("email_verified_at"))


def downgrade() -> None:
    op.alter_column(
        "user",
        "email_verified_at",
        new_column_name="verified_at",
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=True,
    )
    op.execute(set_user_updated_at_function("verified_at"))
