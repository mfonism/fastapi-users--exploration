from datetime import UTC, datetime

import pytest

from explore.auth.models import UserManager
from tests.factories.user import (
    build_plain_user,
    build_signed_up_user,
    build_verified_user,
)


def test_is_verified_tracks_verified_at(mock_utcnow) -> None:
    user = build_signed_up_user()
    assert user.verified_at is None

    timestamp = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp

    user.is_verified = True

    assert user.verified_at == timestamp

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


def test_is_superuser_tracks_superuser_granted_at(mock_utcnow) -> None:
    user = build_plain_user()
    assert user.superuser_granted_at is None

    timestamp = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp

    user.is_superuser = True

    assert user.superuser_granted_at == timestamp

    user.is_superuser = False

    assert user.superuser_granted_at is None
