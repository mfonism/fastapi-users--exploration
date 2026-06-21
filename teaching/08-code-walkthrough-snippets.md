# Code Walkthrough Snippets

These snippets are not a replacement for the task files. They are short
teaching anchors for live coding.

## Minimal FastAPI App

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

Teaching point: start with a route that has no database, no auth, and no
external services.

## Environment Enum

```python
from enum import StrEnum


class AppEnv(StrEnum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"
```

Teaching point: use explicit names for deployment modes instead of scattering
string literals through the app.

## Settings Shape

```python
from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: AppEnv = AppEnv.LOCAL
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: SecretStr = SecretStr("postgres")
    db_base_name: str = "explore"

    @property
    def database_name(self) -> str:
        if self.app_env == AppEnv.TEST:
            return f"{self.db_base_name}_test"
        return self.db_base_name
```

Teaching point: keep config loading separate from feature logic.

## Async Session Dependency

```python
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async_session_maker = get_async_session_maker()

    async with async_session_maker() as session:
        yield session
```

Teaching point: route code should ask FastAPI for a session instead of creating
one manually.

## Timestamp-Backed Account State

```python
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column

from ...utils import clock


class User(Base):
    deactivated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    @property
    def is_active(self) -> bool:
        return self.deactivated_at is None

    @is_active.setter
    def is_active(self, value: bool) -> None:
        if value == self.is_active:
            return

        self.deactivated_at = None if value else clock.utcnow()
```

Teaching point: the API can expose a simple boolean while the database keeps
the audit timestamp.

## Route And Service Split

```python
@router.post("/auth/change-password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    password_change: PasswordChange,
    user: User = Depends(current_user),
    user_manager: UserManager = Depends(get_user_manager),
):
    await change_user_password(
        user=user,
        user_manager=user_manager,
        current_password=password_change.current_password,
        new_password=password_change.new_password,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

```python
async def change_user_password(
    *,
    user: User,
    user_manager: UserManager,
    current_password: str,
    new_password: str,
) -> None:
    password_verified, _ = user_manager.password_helper.verify_and_update(
        current_password,
        user.hashed_password,
    )
    if not password_verified:
        raise ChangePasswordBadPassword()

    await user_manager._update(user, {"password": new_password})
```

Teaching point: route functions handle HTTP and dependencies; service functions
hold business rules.

## Token Hashing For Email Changes

```python
import hashlib
import secrets

EMAIL_CHANGE_TOKEN_BYTES = 32


def generate_email_change_token() -> str:
    return secrets.token_urlsafe(EMAIL_CHANGE_TOKEN_BYTES)


def hash_email_change_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()
```

Teaching point: store enough information to verify a token, but do not store
the raw token.

## Endpoint Test Pattern

```python
@pytest.mark.asyncio
async def test_get_current_user_returns_authenticated_user(
    client,
    authenticate_as,
    session,
) -> None:
    user = build_verified_user(email="alice@example.com")
    session.add(user)
    await session.flush()

    await authenticate_as(client, user)
    response = await client.get(app.url_path_for("users:current_user"))

    assert response.status_code == 200
    assert response.json()["email"] == "alice@example.com"
```

Teaching point: tests should set up one clear state, perform one request, and
assert the behavior that matters.

