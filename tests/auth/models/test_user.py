from datetime import UTC, datetime

import pytest

from explore.auth.models import User, UserManager


def build_user(**overrides) -> User:
    data = {
        "email": "alice@yo.com",
        "full_name": "Alice Yo",
        "hashed_password": "hashed-password",
        "terms_accepted_at": datetime(2000, 1, 2, 0, 0, tzinfo=UTC),
    }
    data.update(overrides)
    return User(**data)


def test_is_active_false_sets_deactivated_at(mock_utcnow) -> None:
    timestamp = datetime(2010, 3, 4, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp
    user = build_user()

    user.is_active = False

    assert user.deactivated_at == timestamp
    mock_utcnow.assert_called_once_with()


def test_is_active_true_clears_deactivated_at(mock_utcnow) -> None:
    user = build_user(deactivated_at=datetime(2010, 3, 4, 0, 0, tzinfo=UTC))

    user.is_active = True

    assert user.deactivated_at is None
    mock_utcnow.assert_not_called()


def test_is_verified_true_sets_verified_at(mock_utcnow) -> None:
    timestamp = datetime(2010, 3, 4, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp
    user = build_user()

    user.is_verified = True

    assert user.verified_at == timestamp
    mock_utcnow.assert_called_once_with()


def test_is_verified_false_clears_verified_at(mock_utcnow) -> None:
    user = build_user(verified_at=datetime(2010, 3, 4, 0, 0, tzinfo=UTC))

    user.is_verified = False

    assert user.verified_at is None
    mock_utcnow.assert_not_called()


def test_is_superuser_true_sets_superuser_granted_at(mock_utcnow) -> None:
    timestamp = datetime(2010, 3, 4, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp
    user = build_user()

    user.is_superuser = True

    assert user.superuser_granted_at == timestamp
    mock_utcnow.assert_called_once_with()


def test_is_superuser_false_clears_superuser_granted_at(mock_utcnow) -> None:
    user = build_user(superuser_granted_at=datetime(2010, 3, 4, 0, 0, tzinfo=UTC))

    user.is_superuser = False

    assert user.superuser_granted_at is None
    mock_utcnow.assert_not_called()


@pytest.mark.asyncio
async def test_on_after_login_updates_last_login_at(mock_utcnow, mocker) -> None:
    timestamp = datetime(2010, 3, 4, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = timestamp
    user_db = mocker.Mock()
    user_db.update = mocker.AsyncMock()
    user = build_user()
    manager = UserManager(user_db)

    await manager.on_after_login(user)

    user_db.update.assert_awaited_once_with(user, {"last_login_at": timestamp})
    mock_utcnow.assert_called_once_with()
