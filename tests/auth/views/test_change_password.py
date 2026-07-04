from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from explore.app import app
from explore.audit.models import AuditActorType, AuditLogEntry
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_change_password_updates_user_password(
    client,
    authenticate_as,
    mock_utcnow,
    password_helper,
    session,
) -> None:
    old_password = "oldstrongpass123"
    new_password = "newstrongpass456"
    user = build_verified_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(old_password),
    )
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    old_hashed_password = user.hashed_password
    password_changed_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = password_changed_at

    response = await client.post(
        app.url_path_for("auth:change-password"),
        headers={
            "user-agent": "pytest",
            "x-request-id": "request-123",
        },
        json={
            "current_password": old_password,
            "new_password": new_password,
        },
    )

    assert response.status_code == 204
    await session.refresh(user)
    assert user.hashed_password != old_hashed_password

    new_password_verified, _ = password_helper.verify_and_update(
        new_password,
        user.hashed_password,
    )
    assert new_password_verified is True

    old_password_verified, _ = password_helper.verify_and_update(
        old_password,
        user.hashed_password,
    )
    assert old_password_verified is False

    audit_entry = await session.scalar(
        select(AuditLogEntry).where(AuditLogEntry.target_id == user.id)
    )
    assert audit_entry is not None
    assert audit_entry.actor_type == AuditActorType.USER
    assert audit_entry.actor_user_id == user.id
    assert audit_entry.action == "user.password_changed"
    assert audit_entry.target_type == "user"
    assert audit_entry.target_id == user.id
    assert audit_entry.occurred_at == password_changed_at
    assert audit_entry.ip_address == "127.0.0.1"
    assert audit_entry.user_agent == "pytest"
    assert audit_entry.request_id == "request-123"


@pytest.mark.asyncio
async def test_change_password_rejects_wrong_current_password(
    client,
    authenticate_as,
    password_helper,
    session,
) -> None:
    old_password = "oldstrongpass123"
    user = build_verified_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(old_password),
    )
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    old_hashed_password = user.hashed_password

    response = await client.post(
        app.url_path_for("auth:change-password"),
        json={
            "current_password": "wrongstrongpass123",
            "new_password": "newstrongpass456",
        },
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.hashed_password == old_hashed_password

    audit_entry = await session.scalar(
        select(AuditLogEntry).where(AuditLogEntry.target_id == user.id)
    )
    assert audit_entry is None
