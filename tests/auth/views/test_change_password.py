import pytest

from explore.app import app
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_change_password_updates_user_password(
    client,
    authenticate_as,
    password_helper,
    session,
) -> None:
    old_password = "oldstrongpass123"
    new_password = "newstrongpass456"
    user = build_verified_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(old_password),
    )
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    old_hashed_password = user.hashed_password

    response = await client.post(
        app.url_path_for("auth:change-password"),
        json={
            "current_password": old_password,
            "new_password": new_password,
        },
    )

    assert response.status_code == 204
    await session.refresh(user)
    assert user.hashed_password != old_hashed_password

    new_password_verified, _ = password_helper.verify_and_update(
        new_password,
        user.hashed_password,
    )
    assert new_password_verified is True

    old_password_verified, _ = password_helper.verify_and_update(
        old_password,
        user.hashed_password,
    )
    assert old_password_verified is False


@pytest.mark.asyncio
async def test_change_password_rejects_wrong_current_password(
    client,
    authenticate_as,
    password_helper,
    session,
) -> None:
    old_password = "oldstrongpass123"
    user = build_verified_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(old_password),
    )
    session.add(user)
    await session.flush()
    await authenticate_as(client, user)

    old_hashed_password = user.hashed_password

    response = await client.post(
        app.url_path_for("auth:change-password"),
        json={
            "current_password": "wrongstrongpass123",
            "new_password": "newstrongpass456",
        },
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.hashed_password == old_hashed_password
