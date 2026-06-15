# Import every SQLAlchemy model here so Alembic sees all tables when it loads
# Base.metadata.
from ..auth.email_changes.models import UserEmailChange
from ..auth.users.models import User

ALL_MODELS = [User, UserEmailChange]
