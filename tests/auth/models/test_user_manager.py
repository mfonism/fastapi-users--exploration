from unittest.mock import AsyncMock

import pytest
from fastapi_users.db import SQLAlchemyUserDatabase

from explore.auth.users.manager import UserManager
from explore.auth.users.models import User
from tests.factories.user import build_verified_user


@pytest.mark.asyncio
async def test_update_keeps_changes_in_current_transaction(
    mocker,
    password_helper,
    session,
) -> None:
    user = build_verified_user()
    session.add(user)
    await session.flush()

    manager = UserManager(SQLAlchemyUserDatabase(session, User), password_helper)
    mock_commit = mocker.patch.object(session, "commit", new_callable=AsyncMock)
    mock_refresh = mocker.patch.object(session, "refresh", new_callable=AsyncMock)

    updated_user = await manager._update(user, {"full_name": "Alice Updated"})

    assert updated_user is user
    assert user.full_name == "Alice Updated"
    mock_commit.assert_not_awaited()
    mock_refresh.assert_not_awaited()
