import uuid
from datetime import datetime

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from ..utils import clock
from .models import AuditActorType, AuditLogEntry


async def record_audit_log_entry(
    session: AsyncSession,
    *,
    action: str,
    target_type: str,
    target_id: uuid.UUID | None = None,
    actor_type: AuditActorType = AuditActorType.SYSTEM,
    actor_user_id: uuid.UUID | None = None,
    subject_type: str | None = None,
    subject_id: uuid.UUID | None = None,
    occurred_at: datetime | None = None,
    request: Request | None = None,
    reason: str | None = None,
) -> AuditLogEntry:
    entry = AuditLogEntry(
        actor_type=actor_type,
        actor_user_id=actor_user_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        subject_type=subject_type,
        subject_id=subject_id,
        occurred_at=occurred_at or clock.utcnow(),
        ip_address=request.client.host if request and request.client else None,
        user_agent=request.headers.get("user-agent") if request else None,
        request_id=request.headers.get("x-request-id") if request else None,
        reason=reason,
    )
    session.add(entry)
    await session.flush()
    return entry
