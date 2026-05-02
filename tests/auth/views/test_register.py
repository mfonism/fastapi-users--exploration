import uuid
from datetime import UTC, datetime

import pytest

from explore.app import app
from explore.auth.models import User
from tests.factories.user import build_signed_up_user


@pytest.mark.asyncio
async def test_register_creates_user(client, password_helper, session) -> None:
    terms_accepted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)

    response = await client.post(
        app.url_path_for("register:register"),
        json={
            "email": "alice@example.com",
            "full_name": "Alice Example",
            "password": "strongpass123",
            "terms_accepted_at": terms_accepted_at.isoformat(),
        },
    )

    assert response.status_code == 201

    payload = response.json()
    user_id = uuid.UUID(payload["id"])
    user = await session.get(User, user_id)

    assert user is not None
    assert user.email == "alice@example.com"
    assert user.full_name == "Alice Example"
    assert user.hashed_password != "strongpass123"
    assert user.terms_accepted_at == terms_accepted_at
    assert user.deactivated_at is None
    assert user.verified_at is None
    assert user.superuser_granted_at is None
    assert user.last_login_at is None

    password_verified, _ = password_helper.verify_and_update(
        "strongpass123", user.hashed_password
    )
    assert password_verified is True


@pytest.mark.asyncio
async def test_register_sends_verification_request(client, mocker) -> None:
    terms_accepted_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    verification_token = "random-verification-token"
    mocker.patch(
        "fastapi_users.manager.generate_jwt",
        return_value=verification_token,
    )
    mock_send_verification_request = mocker.patch(
        "explore.auth.models.send_verification_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("register:register"),
        json={
            "email": "alice@example.com",
            "full_name": "Alice Example",
            "password": "strongpass123",
            "terms_accepted_at": terms_accepted_at.isoformat(),
        },
    )

    assert response.status_code == 201
    mock_send_verification_request.assert_awaited_once_with(
        recipient_email="alice@example.com",
        recipient_name="Alice Example",
        token=verification_token,
    )


@pytest.mark.asyncio
async def test_register_rejects_duplicate_email(client, mocker, session) -> None:
    mock_send_verification_request = mocker.patch(
        "explore.auth.models.send_verification_request",
        autospec=True,
    )
    duplicate_email = "alice@example.com"
    session.add(build_signed_up_user(email=duplicate_email))
    await session.flush()

    response = await client.post(
        app.url_path_for("register:register"),
        json={
            "email": duplicate_email,
            "full_name": "Eve All",
            "password": "anotherstrongpass456",
            "terms_accepted_at": datetime(2000, 10, 10, 0, 5, tzinfo=UTC).isoformat(),
        },
    )

    assert response.status_code == 400
    mock_send_verification_request.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(
            {
                "email": "alice@example.com",
                "password": "strongpass123",
                "terms_accepted_at": datetime(
                    2000, 10, 10, 0, 0, tzinfo=UTC
                ).isoformat(),
            },
            id="missing_full_name",
        ),
        pytest.param(
            {
                "email": "alice@example.com",
                "full_name": "Alice Example",
                "password": "strongpass123",
            },
            id="missing_terms_accepted_at",
        ),
        pytest.param(
            {
                "email": "alice@example.com",
                "full_name": "Alice Example",
                "password": "strongpass123",
                "terms_accepted_at": "not-a-datetime",
            },
            id="invalid_terms_accepted_at",
        ),
    ],
)
async def test_register_validates_payload(client, mocker, payload) -> None:
    mock_send_verification_request = mocker.patch(
        "explore.auth.models.send_verification_request",
        autospec=True,
    )

    response = await client.post(app.url_path_for("register:register"), json=payload)

    assert response.status_code == 422
    mock_send_verification_request.assert_not_awaited()
