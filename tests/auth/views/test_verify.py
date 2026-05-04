from datetime import UTC, datetime

import pytest
from fastapi_users.jwt import generate_jwt

from explore.app import app
from explore.auth.models import UserManager
from tests.factories.user import build_signed_up_user


@pytest.mark.asyncio
async def test_verify_marks_user_verified(client, mock_utcnow, session) -> None:
    user = build_signed_up_user()
    session.add(user)
    await session.flush()

    verification_token = generate_jwt(
        {
            "sub": str(user.id),
            "email": user.email,
            "aud": UserManager.verification_token_audience,
        },
        UserManager.verification_token_secret,
        UserManager.verification_token_lifetime_seconds,
    )
    verified_at = datetime(2000, 10, 10, 0, 0, tzinfo=UTC)
    mock_utcnow.return_value = verified_at

    response = await client.post(
        app.url_path_for("verify:verify"),
        json={"token": verification_token},
    )

    assert response.status_code == 200
    await session.refresh(user)
    assert user.verified_at == verified_at
