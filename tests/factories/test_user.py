from tests.factories.user import (
    DELETED_AT,
    FIRST_LOGIN_AT,
    SIGNED_UP_AT,
    SUPERUSER_GRANTED_AT,
    VERIFIED_AT,
    build_deleted_user,
    build_plain_user,
    build_signed_up_user,
    build_superuser,
    build_verified_user,
)


def test_build_signed_up_user() -> None:
    user = build_signed_up_user()

    assert user.email == "alice@example.com"
    assert user.full_name == "Alice Example"
    assert user.terms_accepted_at == SIGNED_UP_AT
    assert user.created_at == SIGNED_UP_AT
    assert user.updated_at == SIGNED_UP_AT
    assert user.verified_at is None
    assert user.last_login_at is None
    assert user.superuser_granted_at is None


def test_build_verified_user() -> None:
    user = build_verified_user()

    assert user.terms_accepted_at == SIGNED_UP_AT
    assert user.verified_at == VERIFIED_AT
    assert user.last_login_at is None
    assert user.superuser_granted_at is None


def test_build_plain_user() -> None:
    user = build_plain_user()

    assert user.terms_accepted_at == SIGNED_UP_AT
    assert user.verified_at == VERIFIED_AT
    assert user.last_login_at == FIRST_LOGIN_AT
    assert user.superuser_granted_at is None


def test_build_superuser() -> None:
    user = build_superuser()

    assert user.terms_accepted_at == SIGNED_UP_AT
    assert user.verified_at == VERIFIED_AT
    assert user.last_login_at == FIRST_LOGIN_AT
    assert user.superuser_granted_at == SUPERUSER_GRANTED_AT


def test_build_deleted_user() -> None:
    user = build_deleted_user()

    assert user.terms_accepted_at == SIGNED_UP_AT
    assert user.verified_at == VERIFIED_AT
    assert user.last_login_at == FIRST_LOGIN_AT
    assert user.deleted_at == DELETED_AT
