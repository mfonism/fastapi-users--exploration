import pytest

from explore.app import app
from tests.factories.user import build_deleted_user, build_verified_user


@pytest.mark.asyncio
async def test_whoami_requires_authentication(client) -> None:
    response = await client.get(app.url_path_for("whoami"))

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_whoami_returns_current_user(client, authenticate_as, session) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    await authenticate_as(client, user)
    response = await client.get(app.url_path_for("whoami"))

    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"


@pytest.mark.asyncio
async def test_whoami_rejects_deleted_user(client, authenticate_as, session) -> None:
    user = build_deleted_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    await authenticate_as(client, user)
    response = await client.get(app.url_path_for("whoami"))

    assert response.status_code == 401
