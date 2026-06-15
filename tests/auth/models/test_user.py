from datetime import UTC, datetime

import pytest

from explore.auth.users.manager import UserManager
from tests.factories.user import (
    build_deleted_user,
    build_plain_user,
    build_signed_up_user,
    build_superuser,
    build_verified_user,
)


def test_repr_excludes_hashed_password() -> None:
    user = build_signed_up_user(hashed_password="super-secret-hash")

    representation = repr(user)

    assert "hashed_password" not in representation
    assert "super-secret-hash" not in representation


def test_is_verified_tracks_verified_at(mock_utcnow) -> None:
    user = build_signed_up_user()
    assert user.verified_at is None

    timestamp = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp

    user.is_verified = True

    assert user.verified_at == timestamp

    user.is_verified = False

    assert user.verified_at is None


def test_is_verified_true_is_noop_if_already_verified() -> None:
    verified_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_verified_user(verified_at=verified_at)

    user.is_verified = True

    assert user.verified_at == verified_at


def test_is_verified_false_is_noop_if_already_unverified() -> None:
    user = build_signed_up_user()

    user.is_verified = False

    assert user.verified_at is None


@pytest.mark.asyncio
async def test_on_after_login_updates_last_login_at(mock_utcnow, mocker) -> None:
    user = build_verified_user()
    user_db = mocker.Mock()
    user_db.update = mocker.AsyncMock()
    manager = UserManager(user_db)

    timestamp = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp

    await manager.on_after_login(user)

    user_db.update.assert_awaited_once_with(user, {"last_login_at": timestamp})


def test_is_active_tracks_deactivated_at(mock_utcnow) -> None:
    user = build_plain_user()
    assert user.deactivated_at is None

    timestamp = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp

    user.is_active = False

    assert user.deactivated_at == timestamp

    user.is_active = True

    assert user.deactivated_at is None


def test_is_active_false_is_noop_if_already_deactivated() -> None:
    deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_plain_user(deactivated_at=deactivated_at)

    user.is_active = False

    assert user.deactivated_at == deactivated_at


def test_is_active_true_is_noop_if_already_active() -> None:
    user = build_plain_user()

    user.is_active = True

    assert user.deactivated_at is None


def test_is_deleted_tracks_deleted_at(mock_utcnow) -> None:
    user = build_plain_user()
    assert user.deleted_at is None

    timestamp = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp

    user.is_deleted = True

    assert user.deleted_at == timestamp

    user.is_deleted = False

    assert user.deleted_at is None


def test_is_deleted_true_is_noop_if_already_deleted() -> None:
    deleted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_deleted_user(deleted_at=deleted_at)

    user.is_deleted = True

    assert user.deleted_at == deleted_at


def test_is_deleted_false_is_noop_if_not_deleted() -> None:
    user = build_plain_user()

    user.is_deleted = False

    assert user.deleted_at is None


def test_is_superuser_tracks_superuser_granted_at(mock_utcnow) -> None:
    user = build_plain_user()
    assert user.superuser_granted_at is None

    timestamp = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp

    user.is_superuser = True

    assert user.superuser_granted_at == timestamp

    user.is_superuser = False

    assert user.superuser_granted_at is None


def test_is_superuser_true_is_noop_if_already_superuser() -> None:
    superuser_granted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_superuser(superuser_granted_at=superuser_granted_at)

    user.is_superuser = True

    assert user.superuser_granted_at == superuser_granted_at


def test_is_superuser_false_is_noop_if_not_superuser() -> None:
    user = build_plain_user()

    user.is_superuser = False

    assert user.superuser_granted_at is None
