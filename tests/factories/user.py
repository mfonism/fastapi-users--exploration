from collections.abc import Mapping
from datetime import UTC, datetime

from explore.auth.users.models import User

__all__ = [
    "build_deleted_user",
    "build_plain_user",
    "build_signed_up_user",
    "build_superuser",
    "build_verified_user",
]

SIGNED_UP_AT = datetime(2000, 1, 2, 3, 0, tzinfo=UTC)
EMAIL_VERIFIED_AT = datetime(2000, 1, 2, 4, 0, tzinfo=UTC)
FIRST_LOGIN_AT = datetime(2000, 1, 2, 5, 0, tzinfo=UTC)
SUPERUSER_GRANTED_AT = datetime(2000, 1, 2, 6, 0, tzinfo=UTC)
DELETED_AT = datetime(2000, 1, 2, 7, 0, tzinfo=UTC)

_SIGNED_UP_STATE = {
    "email": "alice@example.com",
    "full_name": "Alice Example",
    "hashed_password": "hashed-password",
    "terms_accepted_at": SIGNED_UP_AT,
    "created_at": SIGNED_UP_AT,
    "updated_at": SIGNED_UP_AT,
}

_VERIFIED_STATE = {
    "email_verified_at": EMAIL_VERIFIED_AT,
}

_LOGGED_IN_STATE = _VERIFIED_STATE | {
    "last_login_at": FIRST_LOGIN_AT,
}

_SUPERUSER_STATE = _LOGGED_IN_STATE | {
    "superuser_granted_at": SUPERUSER_GRANTED_AT,
}

_DELETED_STATE = _LOGGED_IN_STATE | {
    "deleted_at": DELETED_AT,
}


def _build_user(
    extra_state: Mapping[str, object] | None = None,
    overrides: Mapping[str, object] | None = None,
) -> User:
    return User(**(_SIGNED_UP_STATE | dict(extra_state or {}) | dict(overrides or {})))


def build_signed_up_user(**overrides: object) -> User:
    return _build_user(overrides=overrides)


def build_verified_user(**overrides: object) -> User:
    return _build_user(_VERIFIED_STATE, overrides)


def build_plain_user(**overrides: object) -> User:
    return _build_user(_LOGGED_IN_STATE, overrides)


def build_superuser(**overrides: object) -> User:
    return _build_user(_SUPERUSER_STATE, overrides)


def build_deleted_user(**overrides: object) -> User:
    return _build_user(_DELETED_STATE, overrides)
