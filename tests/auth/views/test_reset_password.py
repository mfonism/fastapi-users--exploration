import pytest
from fastapi_users.jwt import generate_jwt

from explore.app import app
from explore.auth.users.manager import UserManager
from tests.factories.user import build_deleted_user, build_signed_up_user


@pytest.mark.asyncio
async def test_reset_password_updates_user_password(
    client,
    password_helper,
    session,
) -> None:
    old_password = "oldstrongpass123"
    new_password = "newstrongpass456"
    user = build_signed_up_user(hashed_password=password_helper.hash(old_password))
    session.add(user)
    await session.flush()

    old_hashed_password = user.hashed_password
    reset_token = generate_jwt(
        {
            "sub": str(user.id),
            "password_fgpt": password_helper.hash(user.hashed_password),
            "aud": UserManager.reset_password_token_audience,
        },
        UserManager.reset_password_token_secret,
        UserManager.reset_password_token_lifetime_seconds,
    )

    response = await client.post(
        app.url_path_for("reset:reset_password"),
        json={"token": reset_token, "password": new_password},
    )

    assert response.status_code == 200
    await session.refresh(user)
    assert user.hashed_password != old_hashed_password

    new_password_verified, _ = password_helper.verify_and_update(
        new_password, user.hashed_password
    )
    assert new_password_verified is True

    old_password_verified, _ = password_helper.verify_and_update(
        old_password, user.hashed_password
    )
    assert old_password_verified is False


@pytest.mark.asyncio
async def test_reset_password_rejects_reused_token(
    client,
    password_helper,
    session,
) -> None:
    old_password = "oldstrongpass123"
    user = build_signed_up_user(hashed_password=password_helper.hash(old_password))
    session.add(user)
    await session.flush()

    reset_token = generate_jwt(
        {
            "sub": str(user.id),
            "password_fgpt": password_helper.hash(user.hashed_password),
            "aud": UserManager.reset_password_token_audience,
        },
        UserManager.reset_password_token_secret,
        UserManager.reset_password_token_lifetime_seconds,
    )

    first_response = await client.post(
        app.url_path_for("reset:reset_password"),
        json={"token": reset_token, "password": "newstrongpass456"},
    )

    assert first_response.status_code == 200

    await session.refresh(user)
    hashed_password_after_first_attempt = user.hashed_password

    second_response = await client.post(
        app.url_path_for("reset:reset_password"),
        json={"token": reset_token, "password": "anotherstrongpass789"},
    )

    assert second_response.status_code == 400

    await session.refresh(user)
    assert user.hashed_password == hashed_password_after_first_attempt


@pytest.mark.asyncio
async def test_reset_password_rejects_expired_token(
    client,
    password_helper,
    session,
) -> None:
    old_password = "oldstrongpass123"
    user = build_signed_up_user(hashed_password=password_helper.hash(old_password))
    session.add(user)
    await session.flush()

    old_hashed_password = user.hashed_password
    # generate a JWT with an `exp` claim in the past
    expired_reset_token = generate_jwt(
        {
            "sub": str(user.id),
            "password_fgpt": password_helper.hash(user.hashed_password),
            "aud": UserManager.reset_password_token_audience,
        },
        UserManager.reset_password_token_secret,
        lifetime_seconds=-1,
    )

    response = await client.post(
        app.url_path_for("reset:reset_password"),
        json={"token": expired_reset_token, "password": "newstrongpass456"},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.hashed_password == old_hashed_password


@pytest.mark.asyncio
async def test_reset_password_rejects_deleted_user(
    client,
    password_helper,
    session,
) -> None:
    old_password = "oldstrongpass123"
    new_password = "newstrongpass456"
    user = build_deleted_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(old_password),
    )
    session.add(user)
    await session.flush()

    old_hashed_password = user.hashed_password
    reset_token = generate_jwt(
        {
            "sub": str(user.id),
            "password_fgpt": password_helper.hash(user.hashed_password),
            "aud": UserManager.reset_password_token_audience,
        },
        UserManager.reset_password_token_secret,
        UserManager.reset_password_token_lifetime_seconds,
    )

    response = await client.post(
        app.url_path_for("reset:reset_password"),
        json={"token": reset_token, "password": new_password},
    )

    assert response.status_code == 400
    await session.refresh(user)
    assert user.hashed_password == old_hashed_password
