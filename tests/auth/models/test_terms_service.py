from datetime import UTC, datetime

import pytest
from starlette.requests import Request

from explore.auth.terms.exceptions import CurrentTermsDocumentNotConfigured
from explore.auth.terms.models import TermsDocument, TermsDocumentKind
from explore.auth.terms.service import (
    get_current_terms_document,
    record_terms_acceptance,
)
from tests.factories.user import build_signed_up_user


def build_request() -> Request:
    return Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/auth/register",
            "headers": [(b"user-agent", b"pytest")],
            "client": ("203.0.113.1", 12345),
        }
    )


@pytest.mark.asyncio
async def test_get_current_terms_document_returns_latest_published_document(
    session,
    mock_utcnow,
) -> None:
    now = datetime(2026, 7, 4, 12, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    old_terms = TermsDocument(
        kind=TermsDocumentKind.TERMS_OF_SERVICE,
        version="2026-01-01",
        published_at=datetime(2026, 1, 1, 0, 0, tzinfo=UTC),
    )
    current_terms = TermsDocument(
        kind=TermsDocumentKind.TERMS_OF_SERVICE,
        version="2026-07-04",
        published_at=datetime(2026, 7, 4, 0, 0, tzinfo=UTC),
    )
    future_terms = TermsDocument(
        kind=TermsDocumentKind.TERMS_OF_SERVICE,
        version="2026-12-01",
        published_at=datetime(2026, 12, 1, 0, 0, tzinfo=UTC),
    )
    retired_terms = TermsDocument(
        kind=TermsDocumentKind.TERMS_OF_SERVICE,
        version="2026-06-01",
        published_at=datetime(2026, 6, 1, 0, 0, tzinfo=UTC),
        retired_at=datetime(2026, 7, 1, 0, 0, tzinfo=UTC),
    )
    session.add_all([old_terms, current_terms, future_terms, retired_terms])
    await session.flush()

    terms_document = await get_current_terms_document(session)

    assert terms_document == current_terms


@pytest.mark.asyncio
async def test_get_current_terms_document_raises_if_not_configured(session) -> None:
    with pytest.raises(CurrentTermsDocumentNotConfigured):
        await get_current_terms_document(session)


@pytest.mark.asyncio
async def test_record_terms_acceptance_uses_current_terms_document(
    session,
    mock_utcnow,
) -> None:
    now = datetime(2026, 7, 4, 12, 0, tzinfo=UTC)
    mock_utcnow.return_value = now
    user = build_signed_up_user()
    terms_document = TermsDocument(
        kind=TermsDocumentKind.TERMS_OF_SERVICE,
        version="2026-07-04",
        published_at=datetime(2026, 7, 4, 0, 0, tzinfo=UTC),
    )
    session.add_all([user, terms_document])
    await session.flush()

    acceptance = await record_terms_acceptance(
        session,
        user=user,
        accepted_at=now,
        request=build_request(),
    )

    assert acceptance.user_id == user.id
    assert acceptance.terms_document_id == terms_document.id
    assert acceptance.accepted_at == now
    assert acceptance.ip_address == "203.0.113.1"
    assert acceptance.user_agent == "pytest"
