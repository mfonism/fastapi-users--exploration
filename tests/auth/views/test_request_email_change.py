from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select

from explore.app import app
from explore.auth.email_changes.service import EMAIL_CHANGE_TOKEN_LIFETIME_SECONDS
from explore.auth.models import UserEmailChange, hash_email_change_token
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_request_email_change_stores_request(
    client,
    authenticate_as,
    mock_utcnow,
    mocker,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com", full_name="Alice Example")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    requested_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = requested_at
    mocker.patch(
        "explore.auth.email_changes.service.generate_email_change_token",
        return_value="email-change-token",
    )
    mock_send_email_change_request = mocker.patch(
        "explore.auth.email_changes.routes.send_email_change_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("auth:request-email-change"),
        json={"new_email": "alice.updated@example.com"},
    )

    assert response.status_code == 204

    await session.refresh(user)
    assert user.email == "alice@example.com"

    email_change = await session.scalar(select(UserEmailChange))
    assert email_change is not None
    assert email_change.user_id == user.id
    assert email_change.old_email == "alice@example.com"
    assert email_change.new_email == "alice.updated@example.com"
    assert email_change.token_hash == hash_email_change_token("email-change-token")
    assert email_change.expires_at == requested_at + timedelta(
        seconds=EMAIL_CHANGE_TOKEN_LIFETIME_SECONDS
    )
    assert email_change.confirmed_at is None
    assert email_change.cancelled_at is None

    mock_send_email_change_request.assert_awaited_once_with(
        recipient_email="alice.updated@example.com",
        recipient_name="Alice Example",
        token="email-change-token",
    )


@pytest.mark.asyncio
async def test_request_email_change_normalizes_email(
    client,
    authenticate_as,
    mocker,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com", full_name="Alice Example")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)
    mocker.patch(
        "explore.auth.email_changes.service.generate_email_change_token",
        return_value="email-change-token",
    )
    mock_send_email_change_request = mocker.patch(
        "explore.auth.email_changes.routes.send_email_change_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("auth:request-email-change"),
        json={"new_email": "alice.updated@ｅｘａｍｐｌｅ.com"},
    )

    assert response.status_code == 204

    email_change = await session.scalar(select(UserEmailChange))
    assert email_change is not None
    assert email_change.new_email == "alice.updated@example.com"
    mock_send_email_change_request.assert_awaited_once_with(
        recipient_email="alice.updated@example.com",
        recipient_name="Alice Example",
        token="email-change-token",
    )


@pytest.mark.asyncio
async def test_request_email_change_rejects_current_email(
    client,
    authenticate_as,
    mocker,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)
    mock_send_email_change_request = mocker.patch(
        "explore.auth.email_changes.routes.send_email_change_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("auth:request-email-change"),
        json={"new_email": "alice@example.com"},
    )

    assert response.status_code == 400
    assert await session.scalar(select(UserEmailChange)) is None
    mock_send_email_change_request.assert_not_awaited()


@pytest.mark.asyncio
async def test_request_email_change_rejects_used_email(
    client,
    authenticate_as,
    mocker,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    other_user = build_verified_user(email="taken@example.com")
    session.add_all([user, other_user])
    await session.flush()
    await authenticate_as(client, user)
    mock_send_email_change_request = mocker.patch(
        "explore.auth.email_changes.routes.send_email_change_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("auth:request-email-change"),
        json={"new_email": "taken@example.com"},
    )

    assert response.status_code == 400
    assert await session.scalar(select(UserEmailChange)) is None
    mock_send_email_change_request.assert_not_awaited()


@pytest.mark.asyncio
async def test_request_email_change_cancels_unresolved_requests(
    client,
    authenticate_as,
    mock_utcnow,
    mocker,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    active_email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="first.updated@example.com",
        token_hash=hash_email_change_token("first-token"),
        expires_at=datetime(2000, 10, 10, 1, 0, tzinfo=UTC),
    )
    expired_email_change = UserEmailChange(
        user_id=user.id,
        old_email="alice@example.com",
        new_email="expired.updated@example.com",
        token_hash=hash_email_change_token("expired-token"),
        expires_at=datetime(2000, 10, 9, 0, 0, tzinfo=UTC),
    )
    session.add_all([active_email_change, expired_email_change])
    await session.flush()

    requested_at = datetime(2000, 10, 10, 0, 30, tzinfo=UTC)
    mock_utcnow.return_value = requested_at
    mocker.patch(
        "explore.auth.email_changes.service.generate_email_change_token",
        return_value="second-token",
    )
    mocker.patch(
        "explore.auth.email_changes.routes.send_email_change_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("auth:request-email-change"),
        json={"new_email": "second.updated@example.com"},
    )

    assert response.status_code == 204
    await session.refresh(active_email_change)
    await session.refresh(expired_email_change)
    assert active_email_change.cancelled_at == requested_at
    assert expired_email_change.cancelled_at == requested_at

    email_changes = (
        await session.scalars(
            select(UserEmailChange).order_by(UserEmailChange.new_email)
        )
    ).all()
    assert [email_change.new_email for email_change in email_changes] == [
        "expired.updated@example.com",
        "first.updated@example.com",
        "second.updated@example.com",
    ]
