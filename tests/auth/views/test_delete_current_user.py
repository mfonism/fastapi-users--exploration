from datetime import UTC, datetime

import pytest

from explore.app import app
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_delete_current_user_soft_deletes_user(
    client,
    authenticate_as,
    mock_utcnow,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    await authenticate_as(client, user)

    deleted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = deleted_at

    response = await client.delete(app.url_path_for("users:delete_current_user"))

    assert response.status_code == 204
    await session.refresh(user)
    assert user.deleted_at == deleted_at


@pytest.mark.asyncio
async def test_delete_current_user_logs_out_current_session(
    client,
    authenticate_as,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    await authenticate_as(client, user)

    response = await client.delete(app.url_path_for("users:delete_current_user"))

    assert response.status_code == 204

    # FastAPI Users' logout flow does not know about our deleted state
    # If self-delete only marked the user deleted, this token could still log out,
    # so a 401 here shows self-delete already revoked the token. Otherwise, it
    # would be a 204.
    logout_response = await client.post(app.url_path_for("auth:redis.logout"))
    assert logout_response.status_code == 401
