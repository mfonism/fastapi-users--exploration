from unittest.mock import AsyncMock

import pytest

from explore.db.config import get_async_session


class SessionContext:
    def __init__(self, session) -> None:
        self.session = session

    async def __aenter__(self):
        return self.session

    async def __aexit__(self, *_exc_info) -> None:
        return None


@pytest.mark.asyncio
async def test_get_async_session_commits_successful_request(mocker) -> None:
    session = mocker.Mock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()

    mocker.patch(
        "explore.db.config.get_async_session_maker",
        return_value=lambda: SessionContext(session),
    )

    session_generator = get_async_session()

    assert await anext(session_generator) is session

    with pytest.raises(StopAsyncIteration):
        await anext(session_generator)

    session.commit.assert_awaited_once()
    session.rollback.assert_not_awaited()


@pytest.mark.asyncio
async def test_get_async_session_rolls_back_failed_request(mocker) -> None:
    session = mocker.Mock()
    session.commit = AsyncMock()
    session.rollback = AsyncMock()

    mocker.patch(
        "explore.db.config.get_async_session_maker",
        return_value=lambda: SessionContext(session),
    )

    session_generator = get_async_session()

    assert await anext(session_generator) is session

    with pytest.raises(RuntimeError, match="boom"):
        await session_generator.athrow(RuntimeError("boom"))

    session.commit.assert_not_awaited()
    session.rollback.assert_awaited_once()
