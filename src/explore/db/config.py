import re
from collections.abc import AsyncGenerator
from functools import lru_cache

import psycopg
from packaging.version import InvalidVersion, Version
from psycopg import errors, sql
from sqlalchemy import text
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..config import AppEnv
from ..settings import get_settings

REQUIRED_POSTGRES_VERSION = "18.3"
ADMIN_DATABASE_NAME = "postgres"


@lru_cache
def get_engine():
    settings = get_settings()
    return create_async_engine(settings.core_db_url, echo=settings.debug)


@lru_cache
def get_async_session_maker():
    return async_sessionmaker(get_engine(), expire_on_commit=False)


def is_postgres_server_version_compatible(
    server_version: str, required_version: str
) -> bool:
    try:
        # server_version can include extra distro/build text.
        # Extract the first semantic-ish token
        # e.g. "18.3" from "PostgreSQL 18.3 (Debian 18.3-1.pgdg)".
        match = re.search(r"\d+\.\d+(?:\.\d+)?", server_version)
        if not match:
            return False

        actual = Version(match.group(0))
        required = Version(required_version.strip())
    except InvalidVersion:
        return False

    return actual.major == required.major


def is_local_or_test_env(app_env: AppEnv) -> bool:
    return app_env in {AppEnv.LOCAL, AppEnv.TEST}


def get_admin_db_url() -> URL:
    # This URL is passed to psycopg.AsyncConnection.connect(), not SQLAlchemy.
    # psycopg expects a plain PostgreSQL DSN ("postgresql://..."), while
    # SQLAlchemy-only driver suffixes (like "+asyncpg" / "+psycopg") are for
    # create_engine/create_async_engine URLs.
    settings = get_settings()

    return URL.create(
        drivername="postgresql",
        username=settings.db_user,
        password=settings.db_password.get_secret_value(),
        host=settings.db_host,
        port=settings.db_port,
        database=ADMIN_DATABASE_NAME,
    )


async def ensure_database() -> None:
    settings = get_settings()

    can_manage_roles_and_ownership = is_local_or_test_env(settings.app_env)

    admin_db_url = get_admin_db_url().render_as_string(hide_password=False)

    # Bootstrap db: async, to avoid blocking the event loop
    # (autocommit is required because CREATE DATABASE cannot run in a transaction)
    async with await psycopg.AsyncConnection.connect(
        admin_db_url, autocommit=True
    ) as conn:
        async with conn.cursor() as cursor:
            if can_manage_roles_and_ownership:
                # Create-first pattern is race-safe: duplicates mean another
                # process already created the same object
                try:
                    await cursor.execute(
                        sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD {}").format(
                            sql.Identifier(settings.db_user),
                            sql.Literal(settings.db_password.get_secret_value()),
                        )
                    )
                except errors.DuplicateObject:
                    pass

                try:
                    await cursor.execute(
                        sql.SQL("CREATE DATABASE {} OWNER {}").format(
                            sql.Identifier(settings.database_name),
                            sql.Identifier(settings.db_user),
                        )
                    )
                    # Newly created DB already has the expected owner

                except errors.DuplicateDatabase:
                    # Existing DB: continue to ownership verification
                    await _verify_and_fix_database_owner(
                        cursor, can_manage_roles_and_ownership
                    )

                return
            else:
                # In staging/production, validate only; do not mutate infra
                await cursor.execute(
                    "SELECT 1 FROM pg_roles WHERE rolname = %s",
                    (settings.db_user,),
                )
                if await cursor.fetchone() is None:
                    raise RuntimeError(
                        f"Role '{settings.db_user}' does not exist in "
                        f"{settings.app_env}."
                    )

                await cursor.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s",
                    (settings.database_name,),
                )
                if await cursor.fetchone() is None:
                    raise RuntimeError(
                        f"Database '{settings.database_name}' does not exist in "
                        f"{settings.app_env}."
                    )

            # Verify (and if allowed, fix) owner drift
            await _verify_and_fix_database_owner(cursor, can_manage_roles_and_ownership)


async def _verify_and_fix_database_owner(
    cursor, can_manage_roles_and_ownership: bool
) -> None:
    settings = get_settings()

    await cursor.execute(
        """
        SELECT pg_catalog.pg_get_userbyid(d.datdba)
        FROM pg_database d
        WHERE d.datname = %s
        """,
        (settings.database_name,),
    )

    owner_row = await cursor.fetchone()

    if owner_row is None:
        raise RuntimeError("Database owner should never be None!")

    owner = owner_row[0]

    if owner == settings.db_user:
        return

    if not can_manage_roles_and_ownership:
        raise RuntimeError(
            f"Database '{settings.database_name}' is owned by '{owner}'. "
            f"Expected '{settings.db_user}' as owner in {settings.app_env}."
        )

    await cursor.execute(
        sql.SQL("ALTER DATABASE {} OWNER TO {}").format(
            sql.Identifier(settings.database_name),
            sql.Identifier(settings.db_user),
        )
    )


async def init_db():
    settings = get_settings()

    if settings.app_env != AppEnv.TEST:
        await ensure_database()

    async with get_engine().begin() as conn:
        postgres_version = str(
            (await conn.execute(text("SHOW server_version"))).scalar_one()
        )

        if not is_postgres_server_version_compatible(
            postgres_version,
            REQUIRED_POSTGRES_VERSION,
        ):
            raise RuntimeError(
                "Unsupported PostgreSQL version. "
                f"Expected {REQUIRED_POSTGRES_VERSION}.x, "
                f"got server_version={postgres_version}."
            )


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = get_async_session_maker()

    async with async_session_maker() as session:
        yield session
