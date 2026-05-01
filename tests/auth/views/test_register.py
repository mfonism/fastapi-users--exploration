import uuid
from datetime import UTC, datetime

import pytest

from explore.auth.models import User


@pytest.mark.asyncio
async def test_register_creates_user(client, password_helper, session) -> None:
    terms_accepted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)

    response = await client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "full_name": "Alice Example",
            "password": "strongpass123",
            "terms_accepted_at": terms_accepted_at.isoformat(),
        },
    )

    assert response.status_code == 201

    payload = response.json()
    user_id = uuid.UUID(payload["id"])
    user = await session.get(User, user_id)

    assert user is not None
    assert user.email == "alice@example.com"
    assert user.full_name == "Alice Example"
    assert user.hashed_password != "strongpass123"
    assert user.terms_accepted_at == terms_accepted_at
    assert user.is_active is True
    assert user.is_verified is False
    assert user.is_superuser is False
    assert user.last_login_at is None

    password_verified, _ = password_helper.verify_and_update(
        "strongpass123", user.hashed_password
    )
    assert password_verified is True


@pytest.mark.asyncio
async def test_register_returns_created_user_data(client) -> None:
    terms_accepted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)

    response = await client.post(
        "/auth/register",
        json={
            "email": "alice@example.com",
            "full_name": "Alice Example",
            "password": "strongpass123",
            "terms_accepted_at": terms_accepted_at.isoformat(),
        },
    )

    assert response.status_code == 201

    payload = response.json()
    assert set(payload) == {
        "created_at",
        "deactivated_at",
        "deleted_at",
        "email",
        "full_name",
        "id",
        "last_login_at",
        "superuser_granted_at",
        "terms_accepted_at",
        "updated_at",
        "verified_at",
    }
    assert payload["email"] == "alice@example.com"
    assert payload["full_name"] == "Alice Example"
    assert uuid.UUID(payload["id"]) is not None
    assert datetime.fromisoformat(payload["created_at"]) is not None
    assert datetime.fromisoformat(payload["updated_at"]) is not None
    assert payload["last_login_at"] is None
    assert payload["superuser_granted_at"] is None
    assert payload["deactivated_at"] is None
    assert payload["deleted_at"] is None
    assert payload["verified_at"] is None
    assert datetime.fromisoformat(payload["terms_accepted_at"]) == terms_accepted_at
    assert "password" not in payload
    assert "hashed_password" not in payload


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(client, mock_utcnow) -> None:
    DUPLICATE_EMAIL = "alice@example.com"

    alice_accepted_terms_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    alice_registered_at = datetime(2000, 10, 10, 0, 1, tzinfo=UTC)
    eve_accepted_terms_at = datetime(2000, 10, 10, 0, 5, tzinfo=UTC)
    eve_registered_at = datetime(2000, 10, 10, 0, 10, tzinfo=UTC)

    mock_utcnow.return_value = alice_registered_at
    await client.post(
        "/auth/register",
        json={
            "email": DUPLICATE_EMAIL,
            "full_name": "Alice Example",
            "password": "strongpass123",
            "terms_accepted_at": alice_accepted_terms_at.isoformat(),
        },
    )

    mock_utcnow.return_value = eve_registered_at
    response = await client.post(
        "/auth/register",
        json={
            "email": DUPLICATE_EMAIL,
            "full_name": "Eve All",
            "password": "anotherstrongpass456",
            "terms_accepted_at": eve_accepted_terms_at.isoformat(),
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {
                "full_name": "Alice Example",
                "password": "strongpass123",
                "terms_accepted_at": datetime(
                    2000, 10, 10, 0, 0, tzinfo=UTC
                ).isoformat(),
            },
            id="missing_email",
        ),
        pytest.param(
            {
                "email": "alice@example.com",
                "password": "strongpass123",
                "terms_accepted_at": datetime(
                    2000, 10, 10, 0, 0, tzinfo=UTC
                ).isoformat(),
            },
            id="missing_full_name",
        ),
        pytest.param(
            {
                "email": "alice@example.com",
                "full_name": "Alice Example",
                "password": "strongpass123",
            },
            id="missing_terms_accepted_at",
        ),
        pytest.param(
            {
                "email": "alice@example.com",
                "full_name": "Alice Example",
                "password": "strongpass123",
                "terms_accepted_at": "not-a-datetime",
            },
            id="invalid_terms_accepted_at",
        ),
    ],
)
async def test_register_validates_payload(client, payload) -> None:
    response = await client.post("/auth/register", json=payload)

    assert response.status_code == 422
