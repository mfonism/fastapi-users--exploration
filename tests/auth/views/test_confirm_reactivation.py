from datetime import UTC, datetime

import pytest
from fastapi_users.jwt import generate_jwt

from explore.app import app
from explore.auth.reactivation.service import (
    REACTIVATION_TOKEN_AUDIENCE,
    REACTIVATION_TOKEN_LIFETIME_SECONDS,
)
from explore.settings import settings
from tests.factories.user import (
    build_deleted_user,
    build_plain_user,
    build_verified_user,
)


def generate_reactivation_token(
    *,
    user_id: object,
    deactivated_at: datetime | str,
    lifetime_seconds: int = REACTIVATION_TOKEN_LIFETIME_SECONDS,
) -> str:
    if isinstance(deactivated_at, datetime):
        deactivated_at = deactivated_at.isoformat()

    return generate_jwt(
        {
            "sub": str(user_id),
            "deactivated_at": deactivated_at,
            "aud": REACTIVATION_TOKEN_AUDIENCE,
        },
        settings.reactivation_token_secret,
        lifetime_seconds,
    )


@pytest.mark.asyncio
async def test_reactivate_clears_deactivated_at(
    client,
    session,
) -> None:
    deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_plain_user(
        email="alice@example.com",
        deactivated_at=deactivated_at,
    )
    session.add(user)
    await session.flush()
    reactivation_token = generate_reactivation_token(
        user_id=user.id,
        deactivated_at=deactivated_at,
    )

    response = await client.post(
        app.url_path_for("auth:reactivate"),
        json={"token": reactivation_token},
    )

    assert response.status_code == 204
    await session.refresh(user)
    assert user.deactivated_at is None


@pytest.mark.asyncio
async def test_reactivate_rejects_reused_token(
    client,
    session,
) -> None:
    deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_plain_user(
        email="alice@example.com",
        deactivated_at=deactivated_at,
    )
    session.add(user)
    await session.flush()
    reactivation_token = generate_reactivation_token(
        user_id=user.id,
        deactivated_at=deactivated_at,
    )

    first_response = await client.post(
        app.url_path_for("auth:reactivate"),
        json={"token": reactivation_token},
    )
    second_response = await client.post(
        app.url_path_for("auth:reactivate"),
        json={"token": reactivation_token},
    )

    assert first_response.status_code == 204
    assert second_response.status_code == 400


@pytest.mark.asyncio
async def test_reactivate_rejects_expired_token(
    client,
    session,
) -> None:
    deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_plain_user(
        email="alice@example.com",
        deactivated_at=deactivated_at,
    )
    session.add(user)
    await session.flush()
    expired_reactivation_token = generate_reactivation_token(
        user_id=user.id,
        deactivated_at=deactivated_at,
        lifetime_seconds=-1,
    )

    response = await client.post(
        app.url_path_for("auth:reactivate"),
        json={"token": expired_reactivation_token},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.deactivated_at == deactivated_at


@pytest.mark.asyncio
async def test_reactivate_rejects_deleted_user(
    client,
    session,
) -> None:
    deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_deleted_user(
        email="alice@example.com",
        deactivated_at=deactivated_at,
    )
    session.add(user)
    await session.flush()
    reactivation_token = generate_reactivation_token(
        user_id=user.id,
        deactivated_at=deactivated_at,
    )

    response = await client.post(
        app.url_path_for("auth:reactivate"),
        json={"token": reactivation_token},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.deactivated_at == deactivated_at


@pytest.mark.asyncio
async def test_reactivate_rejects_active_user(
    client,
    session,
) -> None:
    token_deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()
    reactivation_token = generate_reactivation_token(
        user_id=user.id,
        deactivated_at=token_deactivated_at,
    )

    response = await client.post(
        app.url_path_for("auth:reactivate"),
        json={"token": reactivation_token},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.deactivated_at is None


@pytest.mark.asyncio
async def test_reactivate_rejects_stale_token(
    client,
    session,
) -> None:
    old_deactivated_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    current_deactivated_at = datetime(2000, 10, 11, 0, 0, tzinfo=UTC)
    user = build_plain_user(
        email="alice@example.com",
        deactivated_at=current_deactivated_at,
    )
    session.add(user)
    await session.flush()
    reactivation_token = generate_reactivation_token(
        user_id=user.id,
        deactivated_at=old_deactivated_at,
    )

    response = await client.post(
        app.url_path_for("auth:reactivate"),
        json={"token": reactivation_token},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.deactivated_at == current_deactivated_at
