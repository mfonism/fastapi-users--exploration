from email_validator import validate_email


def normalize_email(email: str) -> str:
    return validate_email(email.strip(), check_deliverability=False).normalized
