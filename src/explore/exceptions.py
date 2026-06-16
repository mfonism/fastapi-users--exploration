class AppError(Exception):
    pass


class AppAPIError(AppError):
    status_code = 400
    detail: str
