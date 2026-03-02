from collections.abc import AsyncGenerator
from functools import lru_cache

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..settings import get_settings
from .base import Base

settings = get_settings()


@lru_cache
def get_engine():
    return create_async_engine(settings.core_db_url, echo=settings.debug)


@lru_cache
def get_async_session_maker():
    return async_sessionmaker(get_engine(), expire_on_commit=False)


async def init_db():
    from . import registry  # noqa

    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session_maker()() as session:
        yield session
