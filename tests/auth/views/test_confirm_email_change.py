from datetime import UTC, datetime, timedelta

import pytest

from explore.app import app
from explore.auth.models import UserEmailChange, hash_email_change_token
from tests.factories.user import (
    build_deleted_user,
    build_plain_user,
    build_verified_user,
)


@pytest.mark.asyncio
async def test_confirm_email_change_updates_user_email(
    client,
    mock_utcnow,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    confirmed_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = confirmed_at
    email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("email-change-token"),
        expires_at=confirmed_at + timedelta(hours=1),
    )
    session.add(email_change)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:confirm-email-change"),
        json={"token": "email-change-token"},
    )

    assert response.status_code == 204
    await session.refresh(user)
    await session.refresh(email_change)
    assert user.email == "alice.updated@example.com"
    assert user.verified_at == confirmed_at
    assert email_change.confirmed_at == confirmed_at


@pytest.mark.asyncio
async def test_confirm_email_change_rejects_unknown_token(client) -> None:
    response = await client.post(
        app.url_path_for("auth:confirm-email-change"),
        json={"token": "unknown-token"},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_confirm_email_change_rejects_expired_token(
    client,
    mock_utcnow,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("email-change-token"),
        expires_at=now,
    )
    session.add(email_change)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:confirm-email-change"),
        json={"token": "email-change-token"},
    )

    assert response.status_code == 400
    await session.refresh(user)
    await session.refresh(email_change)
    assert user.email == "alice@example.com"
    assert email_change.confirmed_at is None


@pytest.mark.asyncio
async def test_confirm_email_change_rejects_reused_token(
    client,
    session,
) -> None:
    confirmed_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_verified_user(email="alice.updated@example.com")
    session.add(user)
    await session.flush()
    email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("email-change-token"),
        expires_at=confirmed_at + timedelta(hours=1),
        confirmed_at=confirmed_at,
    )
    session.add(email_change)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:confirm-email-change"),
        json={"token": "email-change-token"},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_confirm_email_change_rejects_cancelled_token(
    client,
    session,
) -> None:
    cancelled_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()
    email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("email-change-token"),
        expires_at=cancelled_at + timedelta(hours=1),
        cancelled_at=cancelled_at,
    )
    session.add(email_change)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:confirm-email-change"),
        json={"token": "email-change-token"},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.email == "alice@example.com"


@pytest.mark.asyncio
async def test_confirm_email_change_rejects_deleted_user(
    client,
    mock_utcnow,
    session,
) -> None:
    user = build_deleted_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("email-change-token"),
        expires_at=now + timedelta(hours=1),
    )
    session.add(email_change)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:confirm-email-change"),
        json={"token": "email-change-token"},
    )

    assert response.status_code == 400
    await session.refresh(user)
    await session.refresh(email_change)
    assert user.email == "alice@example.com"
    assert email_change.confirmed_at is None


@pytest.mark.asyncio
async def test_confirm_email_change_rejects_deactivated_user(
    client,
    mock_utcnow,
    session,
) -> None:
    deactivated_at = datetime(2000, 10, 9, 0, 0, tzinfo=UTC)
    user = build_plain_user(
        email="alice@example.com",
        deactivated_at=deactivated_at,
    )
    session.add(user)
    await session.flush()

    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("email-change-token"),
        expires_at=now + timedelta(hours=1),
    )
    session.add(email_change)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:confirm-email-change"),
        json={"token": "email-change-token"},
    )

    assert response.status_code == 400
    await session.refresh(user)
    await session.refresh(email_change)
    assert user.email == "alice@example.com"
    assert user.deactivated_at == deactivated_at
    assert email_change.confirmed_at is None


@pytest.mark.asyncio
async def test_confirm_email_change_rejects_taken_email(
    client,
    mock_utcnow,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    other_user = build_verified_user(email="alice.updated@example.com")
    session.add_all([user, other_user])
    await session.flush()

    now = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="alice.updated@example.com",
        token_hash=hash_email_change_token("email-change-token"),
        expires_at=now + timedelta(hours=1),
    )
    session.add(email_change)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:confirm-email-change"),
        json={"token": "email-change-token"},
    )

    assert response.status_code == 400
    await session.refresh(user)
    await session.refresh(email_change)
    assert user.email == "alice@example.com"
    assert email_change.confirmed_at is None
