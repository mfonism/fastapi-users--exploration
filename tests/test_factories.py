from .factories import (
    build_plain_user,
    build_signed_up_user,
    build_superuser,
    build_verified_user,
)


def test_build_signed_up_user() -> None:
    user = build_signed_up_user()

    assert user.is_active
    assert not user.is_verified
    assert not user.is_superuser


def test_build_verified_user_creates_signed_up_user_with_verification() -> None:
    user = build_verified_user()

    assert user.is_active
    assert user.is_verified
    assert not user.is_superuser


def test_build_plain_user_creates_verified_user_with_initial_login() -> None:
    user = build_plain_user()

    assert user.is_active
    assert user.is_verified
    assert not user.is_superuser
    assert user.last_login_at is not None


def test_build_superuser_creates_superuser_with_initial_login() -> None:
    user = build_superuser()

    assert user.is_active
    assert user.is_verified
    assert user.is_superuser
    assert user.last_login_at is not None
