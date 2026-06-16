from ..exceptions import AuthError


class EmailChangeError(AuthError):
    pass


class EmailChangeEmailTaken(EmailChangeError):
    detail = "EMAIL_CHANGE_EMAIL_TAKEN"


class EmailChangeBadToken(EmailChangeError):
    detail = "EMAIL_CHANGE_BAD_TOKEN"


class EmailChangeSameEmail(EmailChangeError):
    detail = "EMAIL_CHANGE_SAME_EMAIL"
