import pytest
from email_validator import EmailNotValidError

from explore.utils.email import normalize_email


def test_normalize_email_canonicalizes_domain() -> None:
    assert normalize_email("alice@ｅｘａｍｐｌｅ.com") == "alice@example.com"


def test_normalize_email_strips_surrounding_whitespace() -> None:
    assert normalize_email("  alice@Example.COM  ") == "alice@example.com"


def test_normalize_email_rejects_invalid_email() -> None:
    with pytest.raises(EmailNotValidError):
        normalize_email("not-an-email")
