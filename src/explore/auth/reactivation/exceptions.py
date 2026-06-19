from ..exceptions import AuthError


class ReactivationError(AuthError):
    pass


class ReactivationBadToken(ReactivationError):
    detail = "REACTIVATION_BAD_TOKEN"
