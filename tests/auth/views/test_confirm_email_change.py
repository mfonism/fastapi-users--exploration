from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import delete

from explore.app import app
from explore.auth.models import User, UserEmailChange, hash_email_change_token
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
async def test_confirm_email_change_logs_out_matching_current_session(
    client,
    authenticate_as,
    mock_utcnow,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

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

    # Confirming this user's identity change should log this session out.
    logout_response = await client.post(app.url_path_for("auth:redis.logout"))
    assert logout_response.status_code == 401


@pytest.mark.asyncio
async def test_confirm_email_change_keeps_unrelated_current_session(
    client,
    authenticate_as,
    mock_utcnow,
    session,
) -> None:
    current_user = build_verified_user(email="alice@example.com")
    email_change_user = build_verified_user(email="bob@example.com")
    session.add_all([current_user, email_change_user])
    await session.flush()
    await authenticate_as(client, current_user)

    confirmed_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = confirmed_at
    email_change = UserEmailChange(
        user_id=email_change_user.id,
        old_email="bob@example.com",
        new_email="bob.updated@example.com",
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

    # Confirming another user's identity change should not log this session out.
    logout_response = await client.post(app.url_path_for("auth:redis.logout"))
    assert logout_response.status_code == 204


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


@pytest.mark.asyncio
async def test_confirm_email_change_rejects_email_taken_during_update(
    client,
    mock_utcnow,
    mocker,
    session,
    session_factory,
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
        expires_at=now + timedelta(hours=1),
    )
    session.add(email_change)
    await session.flush()

    real_scalar = session.scalar
    competing_email_inserted = False

    async def scalar_with_competing_email_insert(*args, **kwargs):
        nonlocal competing_email_inserted

        result = await real_scalar(*args, **kwargs)

        # Trigger the competing write only after our manual duplicate-email
        # lookup has passed, so the final failure comes from the real DB index.
        statement = str(args[0]) if args else ""
        is_email_taken_lookup = (
            '"user".email' in statement and '"user".id !=' in statement
        )
        if result is None and is_email_taken_lookup and not competing_email_inserted:
            competing_email_inserted = True
            async with session_factory() as other_session:
                other_user = build_verified_user(email="alice.updated@example.com")
                other_session.add(other_user)
                await other_session.commit()

        return result

    mocker.patch.object(
        session,
        "scalar",
        side_effect=scalar_with_competing_email_insert,
    )

    try:
        response = await client.post(
            app.url_path_for("auth:confirm-email-change"),
            json={"token": "email-change-token"},
        )

        assert response.status_code == 400
        assert competing_email_inserted is True
    finally:
        # The competing write commits outside the test transaction, so the
        # normal fixture rollback cannot clean it up.
        async with session_factory() as cleanup_session:
            await cleanup_session.execute(
                delete(User).where(User.email == "alice.updated@example.com")
            )
            await cleanup_session.commit()
