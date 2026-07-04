from datetime import UTC, datetime

import pytest
from fastapi_users.jwt import generate_jwt
from sqlalchemy import select

from explore.app import app
from explore.audit.models import AuditActorType, AuditLogEntry
from explore.auth.users.manager import UserManager
from tests.auth.views.assertions import assert_internal_user_fields_hidden
from tests.factories.user import build_signed_up_user


@pytest.mark.asyncio
async def test_verify_marks_user_verified(client, mock_utcnow, session) -> None:
    user = build_signed_up_user()
    session.add(user)
    await session.flush()

    verification_token = generate_jwt(
        {
            "sub": str(user.id),
            "email": user.email,
            "aud": UserManager.verification_token_audience,
        },
        UserManager.verification_token_secret,
        UserManager.verification_token_lifetime_seconds,
    )
    email_verified_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = email_verified_at

    response = await client.post(
        app.url_path_for("verify:verify"),
        headers={
            "user-agent": "pytest",
            "x-request-id": "request-123",
        },
        json={"token": verification_token},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == user.email
    assert_internal_user_fields_hidden(payload)

    await session.refresh(user)
    assert user.email_verified_at == email_verified_at

    audit_entry = await session.scalar(select(AuditLogEntry))
    assert audit_entry is not None
    assert audit_entry.actor_type == AuditActorType.USER
    assert audit_entry.actor_user_id == user.id
    assert audit_entry.action == "user.email_verified"
    assert audit_entry.target_type == "user"
    assert audit_entry.target_id == user.id
    assert audit_entry.occurred_at == email_verified_at
    assert audit_entry.ip_address == "127.0.0.1"
    assert audit_entry.user_agent == "pytest"
    assert audit_entry.request_id == "request-123"


@pytest.mark.asyncio
async def test_verify_is_idempotent(client, mock_utcnow, session) -> None:
    user = build_signed_up_user()
    session.add(user)
    await session.flush()

    verification_token = generate_jwt(
        {
            "sub": str(user.id),
            "email": user.email,
            "aud": UserManager.verification_token_audience,
        },
        UserManager.verification_token_secret,
        UserManager.verification_token_lifetime_seconds,
    )
    email_verified_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = email_verified_at

    first_response = await client.post(
        app.url_path_for("verify:verify"),
        json={"token": verification_token},
    )
    assert first_response.status_code == 200

    second_response = await client.post(
        app.url_path_for("verify:verify"),
        json={"token": verification_token},
    )
    assert second_response.status_code == 200

    await session.refresh(user)
    assert user.email_verified_at == email_verified_at

    audit_entries = (await session.scalars(select(AuditLogEntry))).all()
    assert [entry.action for entry in audit_entries] == ["user.email_verified"]


@pytest.mark.asyncio
async def test_verify_rejects_expired_token(client, session) -> None:
    user = build_signed_up_user()
    session.add(user)
    await session.flush()

    # Generate JWT with an `exp` claim in the past
    expired_verification_token = generate_jwt(
        {
            "sub": str(user.id),
            "email": user.email,
            "aud": UserManager.verification_token_audience,
        },
        UserManager.verification_token_secret,
        lifetime_seconds=-1,
    )

    response = await client.post(
        app.url_path_for("verify:verify"),
        json={"token": expired_verification_token},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.email_verified_at is None


@pytest.mark.asyncio
async def test_verify_rejects_deleted_user(client, session) -> None:
    deleted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_signed_up_user(deleted_at=deleted_at)
    session.add(user)
    await session.flush()

    verification_token = generate_jwt(
        {
            "sub": str(user.id),
            "email": user.email,
            "aud": UserManager.verification_token_audience,
        },
        UserManager.verification_token_secret,
        UserManager.verification_token_lifetime_seconds,
    )

    response = await client.post(
        app.url_path_for("verify:verify"),
        json={"token": verification_token},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.email_verified_at is None
    assert user.deleted_at == deleted_at
