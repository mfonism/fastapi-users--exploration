from datetime import UTC, datetime

import pytest

from explore.app import app
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_deactivate_marks_current_user_inactive(
    client,
    authenticate_as,
    mock_utcnow,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = deactivated_at

    response = await client.post(app.url_path_for("auth:deactivate"))

    assert response.status_code == 204
    await session.refresh(user)
    assert user.deactivated_at == deactivated_at

    protected_response = await client.get(app.url_path_for("whoami"))
    assert protected_response.status_code == 401
