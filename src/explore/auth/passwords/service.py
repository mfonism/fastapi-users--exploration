from fastapi import Request

from ...audit.models import AuditActorType
from ...audit.service import record_audit_log_entry
from ..users.manager import UserManager
from ..users.models import User
from .exceptions import ChangePasswordBadPassword


async def change_user_password(
    *,
    user: User,
    user_manager: UserManager,
    current_password: str,
    new_password: str,
    request: Request | None = None,
) -> None:
    password_verified, _ = user_manager.password_helper.verify_and_update(
        current_password,
        user.hashed_password,
    )
    if not password_verified:
        raise ChangePasswordBadPassword()

    await user_manager._update(user, {"password": new_password})
    await record_audit_log_entry(
        user_manager.user_db.session,
        actor_type=AuditActorType.USER,
        actor_user_id=user.id,
        action="user.password_changed",
        target_type="user",
        target_id=user.id,
        request=request,
    )
