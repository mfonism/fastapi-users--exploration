import pytest

from explore.app import app
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_logout_revokes_access_token(client, authenticate_as, session) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    await authenticate_as(client, user)

    protected_endpoint = app.url_path_for("whoami")

    # assert that authenticated user can access protected endpoint
    authenticated_response = await client.get(protected_endpoint)
    assert authenticated_response.status_code == 200

    # log the user out
    logout_response = await client.post(app.url_path_for("auth:redis.logout"))
    assert logout_response.status_code == 204

    # assert that logged out user cannot access protected endpoint
    logged_out_response = await client.get(protected_endpoint)
    assert logged_out_response.status_code == 401
