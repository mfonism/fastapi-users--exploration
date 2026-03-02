from collections.abc import AsyncGenerator
from functools import lru_cache
import re

from packaging.version import InvalidVersion, Version
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..settings import get_settings
from .base import Base

settings = get_settings()
REQUIRED_POSTGRES_VERSION = "18.3"


@lru_cache
def get_engine():
    return create_async_engine(settings.core_db_url, echo=settings.debug)


@lru_cache
def get_async_session_maker():
    return async_sessionmaker(get_engine(), expire_on_commit=False)


def is_postgres_server_version_compatible(
    server_version: str,
    required_version: str,
) -> bool:
    try:
        # server_version can include extra distro/build text.
        # Extract the first semantic-ish token, e.g. "18.3" from
        # "PostgreSQL 18.3 (Debian 18.3-1.pgdg)".
        match = re.search(r"\d+\.\d+(?:\.\d+)?", server_version)
        if not match:
            return False

        actual = Version(match.group(0))
        required = Version(required_version.strip())
    except InvalidVersion:
        return False

    if len(required.release) < 2:
        return False

    return actual.release[:2] == required.release[:2]


async def init_db():
    from . import registry  # noqa

    async with get_engine().begin() as conn:
        postgres_version = str((await conn.execute(text("SHOW server_version"))).scalar_one())
        if not is_postgres_server_version_compatible(
            postgres_version,
            REQUIRED_POSTGRES_VERSION,
        ):
            raise RuntimeError(
                "Unsupported PostgreSQL version. "
                f"Expected {REQUIRED_POSTGRES_VERSION}.x, "
                f"got server_version={postgres_version}."
            )

        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session_maker()() as session:
        yield session
