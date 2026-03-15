from datetime import UTC, datetime

import pytest


@pytest.mark.asyncio
async def test_register_creates_user_and_returns_public_fields(client) -> None:
    email = "alice@example.com"

    response = await client.post(
        "/auth/register",
        json={"email": email, "password": "strongpass123"},
    )

    assert response.status_code == 201

    payload = response.json()
    assert payload["email"] == email
    assert payload["id"]
    assert payload["created_at"]
    assert payload["updated_at"]
    assert payload["last_login_at"] is None
    assert payload["superuser_granted_at"] is None
    assert payload["deactivated_at"] is None
    assert payload["deleted_at"] is None
    assert payload["verified_at"] is None
    assert payload["terms_accepted_at"] is None
    assert "password" not in payload
    assert "hashed_password" not in payload


@pytest.mark.asyncio
async def test_register_allows_same_email_in_a_new_test(client) -> None:
    email = "alice@example.com"

    response = await client.post(
        "/auth/register",
        json={"email": email, "password": "strongpass123"},
    )

    assert response.status_code == 201

    payload = response.json()
    assert payload["email"] == email
    assert payload["id"]
    assert payload["created_at"]
    assert payload["updated_at"]


@pytest.mark.asyncio
async def test_register_persists_terms_accepted_at(client) -> None:
    email = "terms@example.com"
    accepted_at = datetime(2026, 3, 15, 12, 0, tzinfo=UTC).isoformat()

    response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "strongpass123",
            "terms_accepted_at": accepted_at,
        },
    )

    assert response.status_code == 201

    payload = response.json()
    assert payload["email"] == email
    assert datetime.fromisoformat(
        payload["terms_accepted_at"].replace("Z", "+00:00")
    ) == datetime.fromisoformat(accepted_at)


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(client) -> None:
    email = "duplicate@example.com"
    payload = {"email": email, "password": "strongpass123"}

    first_response = await client.post("/auth/register", json=payload)
    second_response = await client.post("/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "REGISTER_USER_ALREADY_EXISTS"
