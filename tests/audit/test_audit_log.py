from datetime import UTC, datetime

import pytest
from starlette.requests import Request

from explore.audit.models import AuditActorType, AuditLogEntry
from explore.audit.service import record_audit_log_entry
from tests.factories.user import build_verified_user


def build_request() -> Request:
    return Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/auth/change-password",
            "headers": [
                (b"user-agent", b"pytest"),
                (b"x-request-id", b"request-123"),
            ],
            "client": ("203.0.113.1", 12345),
        }
    )


@pytest.mark.asyncio
async def test_record_audit_log_entry(session) -> None:
    user = build_verified_user()
    session.add(user)
    await session.flush()

    occurred_at = datetime(2026, 7, 4, 12, 0, tzinfo=UTC)
    entry = await record_audit_log_entry(
        session,
        actor_type=AuditActorType.USER,
        actor_user_id=user.id,
        action="user.password_changed",
        target_type="user",
        target_id=user.id,
        subject_type="password",
        occurred_at=occurred_at,
        request=build_request(),
        reason="user-requested",
    )

    saved_entry = await session.get(AuditLogEntry, entry.id)

    assert saved_entry is not None
    assert saved_entry.actor_type == AuditActorType.USER
    assert saved_entry.actor_user_id == user.id
    assert saved_entry.action == "user.password_changed"
    assert saved_entry.target_type == "user"
    assert saved_entry.target_id == user.id
    assert saved_entry.subject_type == "password"
    assert saved_entry.subject_id is None
    assert saved_entry.occurred_at == occurred_at
    assert saved_entry.ip_address == "203.0.113.1"
    assert saved_entry.user_agent == "pytest"
    assert saved_entry.request_id == "request-123"
    assert saved_entry.reason == "user-requested"


@pytest.mark.asyncio
async def test_record_audit_log_entry_defaults_to_system_actor(
    session,
    mock_utcnow,
) -> None:
    occurred_at = datetime(2026, 7, 4, 12, 0, tzinfo=UTC)
    mock_utcnow.return_value = occurred_at

    entry = await record_audit_log_entry(
        session,
        action="system.maintenance.started",
        target_type="system",
    )

    assert entry.actor_type == AuditActorType.SYSTEM
    assert entry.actor_user_id is None
    assert entry.occurred_at == occurred_at
