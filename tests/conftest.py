import asyncio
import os

import httpx
import pytest_asyncio
from alembic.config import Config
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

from alembic import command


def _configure_test_env() -> None:
    os.environ["APP_ENV"] = "test"


@pytest_asyncio.fixture(scope="session")
async def initialize_test_environment():
    _configure_test_env()

    # Delay project imports until APP_ENV is set so cached settings/engine
    # are built for the test environment, not whichever env imported first.
    from explore.db.config import ensure_database, get_engine
    from explore.settings import BASE_DIR, get_settings

    alembic_cfg = Config(BASE_DIR / "alembic.ini")

    get_settings.cache_clear()

    await ensure_database()

    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")

    yield

    engine = get_engine()

    await engine.dispose()

    get_engine.cache_clear()
    get_settings.cache_clear()


@pytest_asyncio.fixture
async def client(initialize_test_environment: None):
    # Delay project imports until APP_ENV is set so cached settings/engine
    # are built for the test environment, not whichever env imported first.
    from explore.app import app
    from explore.db.config import get_async_session, get_engine

    engine = get_engine()

    async with engine.connect() as connection:
        transaction = await connection.begin()

        session = AsyncSession(bind=connection, expire_on_commit=False)

        await session.begin_nested()

        # Re-open a SAVEPOINT after each commit/rollback inside app code so the
        # outer transaction can still be rolled back at fixture teardown.
        @event.listens_for(session.sync_session, "after_transaction_end")
        def restart_savepoint(session_, transaction_):
            if transaction_.nested and not transaction_._parent.nested:
                session_.begin_nested()

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
            await engine.dispose()
            get_engine.cache_clear()
