import pytest


@pytest.mark.asyncio
async def test_register_returns_201_with_user_payload(client) -> None:
    email = "alice@example.com"
    response = await client.post(
        "/auth/register",
        json={"email": email, "password": "strongpass123"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["email"] == email
    assert "id" in payload
    assert "created_at" in payload
    assert "updated_at" in payload


@pytest.mark.asyncio
async def test_register_returns_201_with_user_payload_again(client) -> None:
    email = "alice@example.com"
    response = await client.post(
        "/auth/register",
        json={"email": email, "password": "strongpass123"},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["email"] == email
    assert "id" in payload
    assert "created_at" in payload
    assert "updated_at" in payload
