from fastapi import Request

from ...audit.models import AuditActorType
from ...audit.service import record_audit_log_entry
from .manager import UserManager
from .models import User


async def deactivate_user(
    *,
    user: User,
    user_manager: UserManager,
    request: Request | None = None,
) -> None:
    await user_manager._update(user, {"is_active": False})
    await record_audit_log_entry(
        user_manager.user_db.session,
        actor_type=AuditActorType.USER,
        actor_user_id=user.id,
        action="user.deactivated",
        target_type="user",
        target_id=user.id,
        occurred_at=user.deactivated_at,
        request=request,
    )
