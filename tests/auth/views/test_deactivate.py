from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from explore.app import app
from explore.audit.models import AuditActorType, AuditLogEntry
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_deactivate_marks_current_user_inactive(
    client,
    authenticate_as,
    mock_utcnow,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = deactivated_at

    response = await client.post(
        app.url_path_for("auth:deactivate"),
        headers={
            "user-agent": "pytest",
            "x-request-id": "request-123",
        },
    )

    assert response.status_code == 204
    await session.refresh(user)
    assert user.deactivated_at == deactivated_at

    audit_entry = await session.scalar(
        select(AuditLogEntry).where(AuditLogEntry.target_id == user.id)
    )
    assert audit_entry is not None
    assert audit_entry.actor_type == AuditActorType.USER
    assert audit_entry.actor_user_id == user.id
    assert audit_entry.action == "user.deactivated"
    assert audit_entry.target_type == "user"
    assert audit_entry.target_id == user.id
    assert audit_entry.occurred_at == deactivated_at
    assert audit_entry.ip_address == "127.0.0.1"
    assert audit_entry.user_agent == "pytest"
    assert audit_entry.request_id == "request-123"

    protected_response = await client.get(app.url_path_for("users:current_user"))
    assert protected_response.status_code == 401
