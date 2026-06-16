from fastapi_users import exceptions

from ..exceptions import AppAPIError


class AuthError(AppAPIError):
    pass


class UserDeleted(
    exceptions.UserInactive,
    exceptions.InvalidVerifyToken,
    exceptions.InvalidResetPasswordToken,
):
    pass
