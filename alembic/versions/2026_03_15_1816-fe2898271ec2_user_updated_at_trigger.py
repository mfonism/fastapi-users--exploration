"""user updated_at trigger

Revision ID: fe2898271ec2
Revises: 7ca027594778
Create Date: 2026-03-15 18:16:11.260764+00:00
"""

from typing import Sequence

from alembic import op

# revision identifiers (used by Alembic).
revision: str = "fe2898271ec2"
down_revision: str | Sequence[str] | None = "7ca027594778"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE FUNCTION set_user_updated_at() RETURNS trigger AS $$
        BEGIN
            IF ROW(
                NEW.email,
                NEW.full_name,
                NEW.hashed_password,
                NEW.verified_at,
                NEW.deactivated_at,
                NEW.deleted_at,
                NEW.superuser_granted_at,
                NEW.terms_accepted_at
            ) IS DISTINCT FROM ROW(
                OLD.email,
                OLD.full_name,
                OLD.hashed_password,
                OLD.verified_at,
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
    )
    op.execute(
        """
        CREATE TRIGGER user_set_updated_at_trigger
        BEFORE UPDATE ON "user"
        FOR EACH ROW
        EXECUTE FUNCTION set_user_updated_at()
        """
    )


def downgrade() -> None:
    op.execute('DROP TRIGGER user_set_updated_at_trigger ON "user"')
    op.execute("DROP FUNCTION set_user_updated_at()")
