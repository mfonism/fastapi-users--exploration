from datetime import UTC, datetime

import pytest

from explore.app import app
from tests.factories.user import (
    build_deleted_user,
    build_plain_user,
    build_verified_user,
)


@pytest.mark.asyncio
async def test_request_reactivation_sends_reactivation_request(
    client,
    mocker,
    session,
) -> None:
    reactivation_token = "random-reactivation-token"
    mocker.patch(
        "explore.auth.reactivation.service.generate_jwt",
        return_value=reactivation_token,
    )
    mock_send_reactivation_request = mocker.patch(
        "explore.auth.reactivation.service.send_reactivation_request",
        autospec=True,
    )

    deactivated_user = build_plain_user(
        email="alice@example.com",
        full_name="Alice Example",
        deactivated_at=datetime(2000, 10, 10, 0, 0, tzinfo=UTC),
    )
    session.add(deactivated_user)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:request-reactivation"),
        json={"email": "alice@ｅｘａｍｐｌｅ.com"},
    )

    assert response.status_code == 202
    mock_send_reactivation_request.assert_awaited_once_with(
        recipient_email="alice@example.com",
        recipient_name="Alice Example",
        token=reactivation_token,
    )


@pytest.mark.asyncio
async def test_request_reactivation_hides_active_user(
    client,
    mocker,
    session,
) -> None:
    mock_send_reactivation_request = mocker.patch(
        "explore.auth.reactivation.service.send_reactivation_request",
        autospec=True,
    )

    active_user = build_verified_user(email="alice@example.com")
    session.add(active_user)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:request-reactivation"),
        json={"email": "alice@example.com"},
    )

    assert response.status_code == 202
    mock_send_reactivation_request.assert_not_awaited()


@pytest.mark.asyncio
async def test_request_reactivation_hides_deleted_user(
    client,
    mocker,
    session,
) -> None:
    mock_send_reactivation_request = mocker.patch(
        "explore.auth.reactivation.service.send_reactivation_request",
        autospec=True,
    )

    deleted_user = build_deleted_user(email="alice@example.com")
    session.add(deleted_user)
    await session.flush()

    response = await client.post(
        app.url_path_for("auth:request-reactivation"),
        json={"email": "alice@example.com"},
    )

    assert response.status_code == 202
    mock_send_reactivation_request.assert_not_awaited()


@pytest.mark.asyncio
async def test_request_reactivation_hides_unknown_user(
    client,
    mocker,
) -> None:
    mock_send_reactivation_request = mocker.patch(
        "explore.auth.reactivation.service.send_reactivation_request",
        autospec=True,
    )

    response = await client.post(
        app.url_path_for("auth:request-reactivation"),
        json={"email": "alice@example.com"},
    )

    assert response.status_code == 202
    mock_send_reactivation_request.assert_not_awaited()
