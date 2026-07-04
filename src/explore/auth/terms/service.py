from datetime import datetime

from fastapi import Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...utils import clock
from ..users.models import User
from .exceptions import CurrentTermsDocumentNotConfigured
from .models import TermsDocument, UserTermsAcceptance

TERMS_OF_SERVICE = "terms_of_service"


async def get_current_terms_document(
    session: AsyncSession,
    *,
    kind: str = TERMS_OF_SERVICE,
) -> TermsDocument:
    terms_document = await session.scalar(
        select(TermsDocument)
        .where(
            TermsDocument.kind == kind,
            TermsDocument.retired_at.is_(None),
            TermsDocument.published_at <= clock.utcnow(),
        )
        .order_by(TermsDocument.published_at.desc())
        .limit(1)
    )

    if terms_document is None:
        raise CurrentTermsDocumentNotConfigured()

    return terms_document


async def record_terms_acceptance(
    session: AsyncSession,
    *,
    user: User,
    accepted_at: datetime,
    request: Request | None = None,
) -> UserTermsAcceptance:
    terms_document = await get_current_terms_document(session)
    acceptance = UserTermsAcceptance(
        user_id=user.id,
        terms_document_id=terms_document.id,
        accepted_at=accepted_at,
        ip_address=request.client.host if request and request.client else None,
        user_agent=request.headers.get("user-agent") if request else None,
    )

    session.add(acceptance)
    await session.flush()
    return acceptance
