import pytest

from explore.app import app
from tests.factories.user import (
    build_deleted_user,
    build_signed_up_user,
    build_verified_user,
)


@pytest.mark.asyncio
async def test_login_allows_verified_user(client, password_helper, session) -> None:
    password = "strongpass123"
    user = build_verified_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(password),
    )
    session.add(user)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:redis.login"),
        data={
            "username": "alice@example.com",
            "password": password,
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_normalizes_email(client, password_helper, session) -> None:
    password = "strongpass123"
    user = build_verified_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(password),
    )
    session.add(user)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:redis.login"),
        data={
            "username": "alice@ｅｘａｍｐｌｅ.com",
            "password": password,
        },
    )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_rejects_invalid_email(client) -> None:
    response = await client.post(
        app.url_path_for("auth:redis.login"),
        data={
            "username": "not-an-email",
            "password": "strongpass123",
        },
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_rejects_unverified_user(client, password_helper, session) -> None:
    password = "strongpass123"
    user = build_signed_up_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(password),
    )
    session.add(user)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:redis.login"),
        data={
            "username": "alice@example.com",
            "password": password,
        },
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_rejects_deleted_user(client, password_helper, session) -> None:
    password = "strongpass123"
    user = build_deleted_user(
        email="alice@example.com",
        hashed_password=password_helper.hash(password),
    )
    session.add(user)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:redis.login"),
        data={
            "username": "alice@example.com",
            "password": password,
        },
    )

    assert response.status_code == 400
