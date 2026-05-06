import pytest

from explore.app import app
from tests.factories.user import build_deleted_user, build_signed_up_user


@pytest.mark.asyncio
async def test_request_verify_token_sends_verification_request(
    client,
    mocker,
    session,
) -> None:
    verification_token = "random-verification-token"
    mocker.patch(
        "fastapi_users.manager.generate_jwt",
        return_value=verification_token,
    )
    mock_send_verification_request = mocker.patch(
        "explore.auth.models.send_verification_request",
        autospec=True,
    )

    signed_up_user = build_signed_up_user(email="alice@example.com")
    session.add(signed_up_user)
    await session.flush()

    response = await client.post(
        app.url_path_for("verify:request-token"),
        json={"email": "alice@example.com"},
    )

    assert response.status_code == 202

    mock_send_verification_request.assert_awaited_once_with(
        recipient_email="alice@example.com",
        recipient_name="Alice Example",
        token=verification_token,
    )


@pytest.mark.asyncio
async def test_request_verify_token_hides_deleted_user(
    client,
    mocker,
    session,
) -> None:
    mock_send_verification_request = mocker.patch(
        "explore.auth.models.send_verification_request",
        autospec=True,
    )

    deleted_user = build_deleted_user(email="alice@example.com")
    session.add(deleted_user)
    await session.flush()

    response = await client.post(
        app.url_path_for("verify:request-token"),
        json={"email": "alice@example.com"},
    )

    assert response.status_code == 202
    mock_send_verification_request.assert_not_awaited()
