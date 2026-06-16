from ..exceptions import AuthError


class PasswordError(AuthError):
    pass


class ChangePasswordBadPassword(PasswordError):
    detail = "CHANGE_PASSWORD_BAD_PASSWORD"
