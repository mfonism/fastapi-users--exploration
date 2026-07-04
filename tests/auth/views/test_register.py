import uuid
from datetime import UTC, datetime

import pytest
from sqlalchemy import select

from explore.app import app
from explore.audit.models import AuditActorType, AuditLogEntry
from explore.auth.terms.models import (
    TermsDocument,
    TermsDocumentKind,
    UserTermsAcceptance,
)
from explore.auth.users.models import User
from tests.auth.views.assertions import assert_internal_user_fields_hidden
from tests.factories.user import build_signed_up_user


async def create_current_terms_document(session) -> TermsDocument:
    terms_document = TermsDocument(
        kind=TermsDocumentKind.TERMS_OF_SERVICE,
        version="2026-07-04",
        published_at=datetime(2000, 1, 1, 0, 0, tzinfo=UTC),
    )
    session.add(terms_document)
    await session.flush()
    return terms_document


@pytest.mark.asyncio
async def test_register_creates_user(
    client,
    password_helper,
    session,
    mock_utcnow,
) -> None:
    terms_accepted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    terms_document = await create_current_terms_document(session)
    mock_utcnow.return_value = terms_accepted_at

    response = await client.post(
        app.url_path_for("register:register"),
        headers={
            "user-agent": "pytest",
            "x-request-id": "request-123",
        },
        json={
            "email": "alice@example.com",
            "full_name": "Alice Example",
            "password": "strongpass123",
            "terms_accepted": True,
        },
    )

    assert response.status_code == 201

    payload = response.json()
    assert payload["email"] == "alice@example.com"
    assert payload["full_name"] == "Alice Example"
    assert_internal_user_fields_hidden(payload)

    user_id = uuid.UUID(payload["id"])
    user = await session.get(User, user_id)

    assert user is not None
    assert user.email == "alice@example.com"
    assert user.full_name == "Alice Example"
    assert user.hashed_password != "strongpass123"
    assert user.terms_accepted_at == terms_accepted_at
    assert user.deactivated_at is None
    assert user.email_verified_at is None
    assert user.superuser_granted_at is None
    assert user.last_login_at is None

    acceptance = await session.scalar(
        select(UserTermsAcceptance).where(UserTermsAcceptance.user_id == user.id)
    )
    assert acceptance is not None
    assert acceptance.terms_document_id == terms_document.id
    assert acceptance.accepted_at == terms_accepted_at

    audit_entries = (
        await session.scalars(
            select(AuditLogEntry)
            .where(AuditLogEntry.target_id == user.id)
            .order_by(AuditLogEntry.action)
        )
    ).all()
    assert [entry.action for entry in audit_entries] == [
        "user.registered",
        "user.terms_accepted",
    ]

    registered_entry = audit_entries[0]
    assert registered_entry.actor_type == AuditActorType.ANONYMOUS
    assert registered_entry.actor_user_id is None
    assert registered_entry.target_type == "user"
    assert registered_entry.target_id == user.id
    assert registered_entry.occurred_at == terms_accepted_at
    assert registered_entry.ip_address == "127.0.0.1"
    assert registered_entry.user_agent == "pytest"
    assert registered_entry.request_id == "request-123"

    terms_entry = audit_entries[1]
    assert terms_entry.actor_type == AuditActorType.USER
    assert terms_entry.actor_user_id == user.id
    assert terms_entry.target_type == "user"
    assert terms_entry.target_id == user.id
    assert terms_entry.subject_type == "terms_document"
    assert terms_entry.subject_id == terms_document.id
    assert terms_entry.occurred_at == terms_accepted_at

    password_verified, _ = password_helper.verify_and_update(
        "strongpass123", user.hashed_password
    )
    assert password_verified is True


@pytest.mark.asyncio
async def test_register_sends_verification_request(client, mocker, session) -> None:
    await create_current_terms_document(session)
    verification_token = "random-verification-token"
    mocker.patch(
        "fastapi_users.manager.generate_jwt",
        return_value=verification_token,
    )
    mock_send_verification_request = mocker.patch(
        "explore.auth.users.manager.send_verification_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("register:register"),
        json={
            "email": "alice@example.com",
            "full_name": "Alice Example",
            "password": "strongpass123",
            "terms_accepted": True,
        },
    )

    assert response.status_code == 201
    mock_send_verification_request.assert_awaited_once_with(
        recipient_email="alice@example.com",
        recipient_name="Alice Example",
        token=verification_token,
    )


@pytest.mark.asyncio
async def test_register_normalizes_email(client, mocker, session) -> None:
    await create_current_terms_document(session)
    mock_send_verification_request = mocker.patch(
        "explore.auth.users.manager.send_verification_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("register:register"),
        json={
            "email": "alice@ｅｘａｍｐｌｅ.com",
            "full_name": "Alice Example",
            "password": "strongpass123",
            "terms_accepted": True,
        },
    )

    assert response.status_code == 201

    payload = response.json()
    assert payload["email"] == "alice@example.com"

    user = await session.get(User, uuid.UUID(payload["id"]))
    assert user is not None
    assert user.email == "alice@example.com"
    mock_send_verification_request.assert_awaited_once_with(
        recipient_email="alice@example.com",
        recipient_name="Alice Example",
        token=mocker.ANY,
    )


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(client, mocker, session) -> None:
    mock_send_verification_request = mocker.patch(
        "explore.auth.users.manager.send_verification_request",
        autospec=True,
    )
    duplicate_email = "alice@example.com"
    session.add(build_signed_up_user(email=duplicate_email))
    await session.flush()

    response = await client.post(
        app.url_path_for("register:register"),
        json={
            "email": duplicate_email,
            "full_name": "Eve All",
            "password": "anotherstrongpass456",
            "terms_accepted": True,
        },
    )

    assert response.status_code == 400
    mock_send_verification_request.assert_not_awaited()


@pytest.mark.asyncio
async def test_register_rejects_duplicate_normalized_email(
    client,
    mocker,
    session,
) -> None:
    mock_send_verification_request = mocker.patch(
        "explore.auth.users.manager.send_verification_request",
        autospec=True,
    )
    session.add(build_signed_up_user(email="alice@example.com"))
    await session.flush()

    response = await client.post(
        app.url_path_for("register:register"),
        json={
            "email": "alice@ｅｘａｍｐｌｅ.com",
            "full_name": "Eve All",
            "password": "anotherstrongpass456",
            "terms_accepted": True,
        },
    )

    assert response.status_code == 400
    mock_send_verification_request.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {
                "email": "alice@example.com",
                "password": "strongpass123",
                "terms_accepted": True,
            },
            id="missing_full_name",
        ),
        pytest.param(
            {
                "email": "alice@example.com",
                "full_name": "Alice Example",
                "password": "strongpass123",
            },
            id="missing_terms_accepted",
        ),
        pytest.param(
            {
                "email": "alice@example.com",
                "full_name": "Alice Example",
                "password": "strongpass123",
                "terms_accepted": False,
            },
            id="terms_not_accepted",
        ),
        pytest.param(
            {
                "email": "not-an-email",
                "full_name": "Alice Example",
                "password": "strongpass123",
                "terms_accepted": True,
            },
            id="invalid_email",
        ),
    ],
)
async def test_register_validates_payload(client, mocker, payload) -> None:
    mock_send_verification_request = mocker.patch(
        "explore.auth.users.manager.send_verification_request",
        autospec=True,
    )

    response = await client.post(app.url_path_for("register:register"), json=payload)

    assert response.status_code == 422
    mock_send_verification_request.assert_not_awaited()
