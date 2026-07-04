# Import every SQLAlchemy model here so Alembic sees all tables when it loads
# Base.metadata.
from ..audit.models import AuditLogEntry
from ..auth.email_changes.models import UserEmailChange
from ..auth.terms.models import TermsDocument, UserTermsAcceptance
from ..auth.users.models import User

ALL_MODELS = [
    User,
    UserEmailChange,
    TermsDocument,
    UserTermsAcceptance,
    AuditLogEntry,
]
