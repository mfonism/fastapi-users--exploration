from collections.abc import AsyncGenerator
from functools import lru_cache
import re
from urllib.parse import quote_plus

from packaging.version import InvalidVersion, Version
import psycopg
from psycopg import sql
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..config import AppEnv
from ..settings import get_settings
from .base import Base

settings = get_settings()
REQUIRED_POSTGRES_VERSION = "18.3"
ADMIN_DATABASE_NAME = "postgres"


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


def is_local_or_test_env(app_env: AppEnv) -> bool:
    return app_env in {AppEnv.LOCAL, AppEnv.TEST}


def get_admin_db_url() -> str:
    user = quote_plus(settings.db_user)
    password = quote_plus(settings.db_password.get_secret_value())
    driver = settings.db_driver.replace("+asyncpg", "+psycopg")
    return (
        f"{driver}://{user}:{password}@"
        f"{settings.db_host}:{settings.db_port}/{ADMIN_DATABASE_NAME}"
    )


async def ensure_database() -> None:
    can_manage_roles_and_ownership = is_local_or_test_env(settings.app_env)

    async with await psycopg.AsyncConnection.connect(
        get_admin_db_url(), autocommit=True
    ) as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                "SELECT 1 FROM pg_roles WHERE rolname = %s",
                (settings.db_user,),
            )
            role_existence = await cursor.fetchone()

            if role_existence is None:
                if not can_manage_roles_and_ownership:
                    raise RuntimeError(
                        f"Role '{settings.db_user}' does not exist in {settings.app_env}."
                    )

                await cursor.execute(
                    sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD {}").format(
                        sql.Identifier(settings.db_user),
                        sql.Literal(settings.db_password.get_secret_value()),
                    )
                )

            await cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (settings.database_name,),
            )
            database_existence = await cursor.fetchone()

            if database_existence is None:
                if not can_manage_roles_and_ownership:
                    raise RuntimeError(
                        f"Database '{settings.database_name}' does not exist in {settings.app_env}."
                    )

                await cursor.execute(
                    sql.SQL("CREATE DATABASE {} OWNER {}").format(
                        sql.Identifier(settings.database_name),
                        sql.Identifier(settings.db_user),
                    )
                )
                return

            await cursor.execute(
                """
                SELECT pg_catalog.pg_get_userbyid(d.datdba)
                FROM pg_database d
                WHERE d.datname = %s
                """,
                (settings.database_name,),
            )
            owner_existence = await cursor.fetchone()
            owner = owner_existence[0] if owner_existence else None

            if owner != settings.db_user:
                if not can_manage_roles_and_ownership:
                    raise RuntimeError(
                        f"Database '{settings.database_name}' is owned by '{owner}', "
                        f"expected '{settings.db_user}' in {settings.app_env}."
                    )

                await cursor.execute(
                    sql.SQL("ALTER DATABASE {} OWNER TO {}").format(
                        sql.Identifier(settings.database_name),
                        sql.Identifier(settings.db_user),
                    )
                )


async def init_db():
    from . import registry  # noqa

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

        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_async_session_maker()() as session:
        yield session
