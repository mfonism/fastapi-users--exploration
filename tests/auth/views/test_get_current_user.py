import pytest

from explore.app import app
from tests.auth.views.assertions import assert_internal_user_fields_hidden
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_get_current_user_requires_authentication(client) -> None:
    response = await client.get(app.url_path_for("users:current_user"))

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_current_user_returns_authenticated_user(
    client,
    authenticate_as,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    await authenticate_as(client, user)
    response = await client.get(app.url_path_for("users:current_user"))

    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == "alice@example.com"
    assert_internal_user_fields_hidden(payload)
