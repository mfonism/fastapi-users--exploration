from datetime import UTC, datetime

import pytest

from explore.app import app
from tests.auth.views.assertions import assert_internal_user_fields_hidden
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_patch_current_user_updates_full_name(
    client,
    authenticate_as,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com", full_name="Alice Example")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    response = await client.patch(
        app.url_path_for("users:patch_current_user"),
        json={
            "full_name": "Alice Updated",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["email"] == "alice@example.com"
    assert payload["full_name"] == "Alice Updated"
    assert_internal_user_fields_hidden(payload)

    await session.refresh(user)
    assert user.email == "alice@example.com"
    assert user.full_name == "Alice Updated"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        pytest.param({"email": "alice.updated@example.com"}, id="email"),
        pytest.param({"password": "newstrongpass123"}, id="password"),
        pytest.param(
            {"email_verified_at": datetime(2000, 10, 10, 0, 0, tzinfo=UTC).isoformat()},
            id="email_verified_at",
        ),
        pytest.param(
            {"deleted_at": datetime(2000, 10, 10, 0, 0, tzinfo=UTC).isoformat()},
            id="deleted_at",
        ),
        pytest.param(
            {"deactivated_at": datetime(2000, 10, 10, 0, 0, tzinfo=UTC).isoformat()},
            id="deactivated_at",
        ),
        pytest.param(
            {
                "superuser_granted_at": datetime(
                    2000,
                    10,
                    10,
                    0,
                    0,
                    tzinfo=UTC,
                ).isoformat()
            },
            id="superuser_granted_at",
        ),
    ],
)
async def test_patch_current_user_rejects_account_state_fields(
    client,
    authenticate_as,
    payload,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    response = await client.patch(
        app.url_path_for("users:patch_current_user"),
        json=payload,
    )

    assert response.status_code == 422
