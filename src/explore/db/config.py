from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from .. import settings
from .base import Base

engine = create_async_engine(settings.CORE_DB_URL, echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
    from . import registry  # noqa

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # Keep local SQLite dev DB compatible when evolving the user schema.
        result = await conn.execute(text("PRAGMA table_info('user')"))
        existing_columns = {row[1] for row in result}
        if "deactivated_at" not in existing_columns:
            await conn.execute(text("ALTER TABLE user ADD COLUMN deactivated_at DATETIME"))
        if "verified_at" not in existing_columns:
            await conn.execute(text("ALTER TABLE user ADD COLUMN verified_at DATETIME"))


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
