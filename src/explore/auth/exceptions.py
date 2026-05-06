from fastapi_users import exceptions


class UserDeleted(
    exceptions.UserInactive,
    exceptions.InvalidVerifyToken,
    exceptions.InvalidResetPasswordToken,
):
    pass
