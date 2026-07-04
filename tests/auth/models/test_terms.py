from datetime import UTC, datetime

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from explore.auth.terms.models import (
    TermsDocument,
    TermsDocumentKind,
    UserTermsAcceptance,
)
from tests.factories.user import build_signed_up_user


@pytest.mark.asyncio
async def test_user_terms_acceptance_records_policy_version(session) -> None:
    user = build_signed_up_user()
    terms_document = TermsDocument(
        kind=TermsDocumentKind.TERMS_OF_SERVICE,
        version="2026-07-04",
        published_at=datetime(2026, 7, 4, 0, 0, tzinfo=UTC),
    )
    session.add_all([user, terms_document])
    await session.flush()

    accepted_at = datetime(2026, 7, 4, 12, 0, tzinfo=UTC)
    acceptance = UserTermsAcceptance(
        user_id=user.id,
        terms_document_id=terms_document.id,
        accepted_at=accepted_at,
        ip_address="127.0.0.1",
        user_agent="pytest",
    )
    session.add(acceptance)
    await session.flush()

    saved_acceptance = await session.scalar(select(UserTermsAcceptance))

    assert saved_acceptance is not None
    assert saved_acceptance.user_id == user.id
    assert saved_acceptance.terms_document_id == terms_document.id
    assert saved_acceptance.accepted_at == accepted_at
    assert saved_acceptance.ip_address == "127.0.0.1"
    assert saved_acceptance.user_agent == "pytest"


@pytest.mark.asyncio
async def test_terms_document_version_is_unique_per_kind(session) -> None:
    session.add_all(
        [
            TermsDocument(
                kind=TermsDocumentKind.TERMS_OF_SERVICE,
                version="2026-07-04",
                published_at=datetime(2026, 7, 4, 0, 0, tzinfo=UTC),
            ),
            TermsDocument(
                kind=TermsDocumentKind.TERMS_OF_SERVICE,
                version="2026-07-04",
                published_at=datetime(2026, 7, 4, 0, 0, tzinfo=UTC),
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        await session.flush()
