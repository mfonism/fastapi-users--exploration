import os

import httpx
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession

# Set APP_ENV before importing project modules to ensure
# the `settings` object is initialized with the correct APP_ENV
from explore.env import AppEnv

os.environ.setdefault("APP_ENV", AppEnv.TEST.value)

from explore.app import app
from explore.db.config import (
    create_engine,
    get_async_session,
)


@pytest_asyncio.fixture
async def engine():
    engine = create_engine()
    try:
        yield engine
    finally:
        await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
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

        try:
            yield session
        finally:
            await session.close()
            await transaction.rollback()


@pytest_asyncio.fixture
async def client(session):
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
