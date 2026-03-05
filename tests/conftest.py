import asyncio
import os
from pathlib import Path

import httpx
import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from sqlalchemy.ext.asyncio import AsyncSession


def _configure_test_env() -> None:
    os.environ["APP_ENV"] = "test"


@pytest_asyncio.fixture(scope="session")
async def initialize_test_environment():
    _configure_test_env()

    project_root = Path(__file__).resolve().parents[1]
    alembic_cfg = Config(str(project_root / "alembic.ini"))

    from explore.db.config import ensure_database, get_async_session_maker, get_engine
    from explore.settings import get_settings

    get_settings.cache_clear()

    # Bootstraps the test DB if missing (role/database ownership checks),
    # then applies schema through Alembic once per test session.
    await ensure_database()
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")

    yield

    await get_engine().dispose()
    get_engine.cache_clear()
    get_async_session_maker.cache_clear()
    get_settings.cache_clear()


@pytest_asyncio.fixture
async def client(initialize_test_environment: None):
    from explore.app import app
    from explore.db.config import get_async_session, get_engine

    engine = get_engine()
    async with engine.connect() as connection:
        transaction = await connection.begin()
        session = AsyncSession(bind=connection, expire_on_commit=False)

        async def override_get_async_session():
            yield session

        app.dependency_overrides[get_async_session] = override_get_async_session

        try:
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(
                transport=transport,
                base_url="http://testserver",
            ) as test_client:
                yield test_client
        finally:
            app.dependency_overrides.pop(get_async_session, None)
            await session.close()
            await transaction.rollback()
            await get_engine().dispose()
            get_engine.cache_clear()
