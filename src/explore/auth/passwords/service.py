from ..users.manager import UserManager
from ..users.models import User
from .exceptions import ChangePasswordBadPassword


async def change_user_password(
    *,
    user: User,
    user_manager: UserManager,
    current_password: str,
    new_password: str,
) -> None:
    password_verified, _ = user_manager.password_helper.verify_and_update(
        current_password,
        user.hashed_password,
    )
    if not password_verified:
        raise ChangePasswordBadPassword()

    await user_manager._update(user, {"password": new_password})
