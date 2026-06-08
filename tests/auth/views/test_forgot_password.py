import pytest

from explore.app import app
from tests.factories.user import build_deleted_user, build_signed_up_user


@pytest.mark.asyncio
async def test_forgot_password_sends_password_reset_request(
    client,
    mocker,
    session,
) -> None:
    reset_token = "random-reset-token"
    mocker.patch(
        "fastapi_users.manager.generate_jwt",
        return_value=reset_token,
    )
    mock_send_password_reset_request = mocker.patch(
        "explore.auth.models.send_password_reset_request",
        autospec=True,
    )

    user = build_signed_up_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    response = await client.post(
        app.url_path_for("reset:forgot_password"),
        json={"email": "alice@ｅｘａｍｐｌｅ.com"},
    )

    assert response.status_code == 202
    mock_send_password_reset_request.assert_awaited_once_with(
        recipient_email="alice@example.com",
        recipient_name="Alice Example",
        token=reset_token,
    )


@pytest.mark.asyncio
async def test_forgot_password_hides_deleted_user(
    client,
    mocker,
    session,
) -> None:
    mock_send_password_reset_request = mocker.patch(
        "explore.auth.models.send_password_reset_request",
        autospec=True,
    )

    deleted_user = build_deleted_user(email="alice@example.com")
    session.add(deleted_user)
    await session.flush()

    response = await client.post(
        app.url_path_for("reset:forgot_password"),
        json={"email": "alice@example.com"},
    )

    assert response.status_code == 202
    mock_send_password_reset_request.assert_not_awaited()
