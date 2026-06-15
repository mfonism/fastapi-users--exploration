from datetime import UTC, datetime, timedelta

from explore.auth.email_changes.models import (
    UserEmailChange,
    generate_email_change_token,
    hash_email_change_token,
)


def test_generate_email_change_token_returns_random_values() -> None:
    first_token = generate_email_change_token()
    second_token = generate_email_change_token()

    assert first_token
    assert second_token
    assert first_token != second_token


def test_hash_email_change_token_does_not_return_raw_token() -> None:
    token = "email-change-token"

    token_hash = hash_email_change_token(token)

    assert token_hash != token
    assert token_hash == hash_email_change_token(token)
    assert token_hash != hash_email_change_token("different-token")


def test_user_email_change_is_usable_before_expiry(mock_utcnow) -> None:
    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=now + timedelta(hours=1),
    )

    assert email_change.is_usable() is True


def test_user_email_change_is_not_usable_at_expiry(mock_utcnow) -> None:
    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=now,
    )

    assert email_change.is_usable() is False


def test_user_email_change_is_not_usable_after_confirmation(mock_utcnow) -> None:
    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=now + timedelta(hours=1),
        confirmed_at=now,
    )

    assert email_change.is_usable() is False


def test_user_email_change_is_not_usable_after_cancellation(mock_utcnow) -> None:
    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=now + timedelta(hours=1),
        cancelled_at=now,
    )

    assert email_change.is_usable() is False


def test_user_email_change_tracks_confirmation_time(mock_utcnow) -> None:
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=datetime(2000, 10, 10, 1, 0, tzinfo=UTC),
    )
    confirmed_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = confirmed_at

    confirmed = email_change.confirm()

    assert confirmed is True
    assert email_change.confirmed_at == confirmed_at


def test_user_email_change_confirm_is_noop_if_already_confirmed() -> None:
    confirmed_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=datetime(2000, 10, 10, 1, 0, tzinfo=UTC),
        confirmed_at=confirmed_at,
    )

    confirmed = email_change.confirm()

    assert confirmed is False
    assert email_change.confirmed_at == confirmed_at


def test_user_email_change_confirm_is_noop_if_cancelled() -> None:
    cancelled_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=datetime(2000, 10, 10, 1, 0, tzinfo=UTC),
        cancelled_at=cancelled_at,
    )

    confirmed = email_change.confirm()

    assert confirmed is False
    assert email_change.confirmed_at is None
    assert email_change.cancelled_at == cancelled_at


def test_user_email_change_confirm_is_noop_if_expired(mock_utcnow) -> None:
    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=now,
    )

    confirmed = email_change.confirm()

    assert confirmed is False
    assert email_change.confirmed_at is None


def test_user_email_change_tracks_cancellation_time(mock_utcnow) -> None:
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=datetime(2000, 10, 10, 1, 0, tzinfo=UTC),
    )
    cancelled_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = cancelled_at

    cancelled = email_change.cancel()

    assert cancelled is True
    assert email_change.cancelled_at == cancelled_at


def test_user_email_change_cancel_is_noop_if_already_cancelled() -> None:
    cancelled_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=datetime(2000, 10, 10, 1, 0, tzinfo=UTC),
        cancelled_at=cancelled_at,
    )

    cancelled = email_change.cancel()

    assert cancelled is False
    assert email_change.cancelled_at == cancelled_at


def test_user_email_change_cancel_is_noop_if_confirmed() -> None:
    confirmed_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    email_change = UserEmailChange(
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("token"),
        expires_at=datetime(2000, 10, 10, 1, 0, tzinfo=UTC),
        confirmed_at=confirmed_at,
    )

    cancelled = email_change.cancel()

    assert cancelled is False
    assert email_change.confirmed_at == confirmed_at
    assert email_change.cancelled_at is None
