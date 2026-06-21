# Project Summary

## What The Project Does

Explore is a FastAPI authentication API built around `fastapi-users`. It
demonstrates a realistic account system with:

- user registration
- email verification
- Redis-backed bearer-token login and logout
- current-user profile reads and updates
- password reset and password change
- account deactivation and reactivation
- soft deletion
- email-change request and confirmation
- async PostgreSQL persistence
- Alembic database migrations
- pytest coverage for model behavior and API behavior

The project is not a frontend app. It is an API service meant to be exercised
through tests, OpenAPI docs, or curl/http clients.

## Main Technologies

| Technology | Role |
|---|---|
| Python 3.14 | Language runtime. |
| uv | Dependency management, virtual environment, and command runner. |
| FastAPI | Web framework and dependency injection. |
| fastapi-users | Authentication router generation, user manager hooks, password hashing, token helpers. |
| SQLAlchemy async ORM | Database models, async sessions, and persistence. |
| PostgreSQL | Application database. |
| Redis | Bearer token storage for login sessions. |
| Alembic | Database schema migrations. |
| Pydantic Settings | Environment-based configuration. |
| pytest / pytest-asyncio | Test runner for sync and async tests. |
| httpx ASGITransport | In-process API testing without running a server. |
| Ruff / pre-commit | Formatting and linting. |

## Major Concepts Students Learn

| Concept | Where It Appears |
|---|---|
| API design | `src/explore/app.py`, route modules under `src/explore/auth`. |
| Dependency injection | `get_async_session`, `get_user_manager`, current-user dependencies. |
| Environment config | `src/explore/env.py`, `src/explore/settings.py`, `.env.example`. |
| Async database access | `src/explore/db/config.py`, tests using async sessions. |
| ORM modeling | `User`, `UserEmailChange`, Alembic migrations. |
| Authentication lifecycle | registration, verification, login, logout, reset password. |
| Account lifecycle | active, verified, deleted, superuser, reactivated states. |
| Service-layer design | `passwords/service.py`, `reactivation/service.py`, `email_changes/service.py`. |
| Security basics | password hashing, token hashing, token expiry, non-enumeration responses. |
| API testing | `tests/auth/views/*`, fixtures in `tests/conftest.py`. |
| Clean commit history | one focused learning goal per commit. |

## Workshop Target

By the end, students should be able to explain:

1. How FastAPI receives a request and calls route dependencies.
2. How an async SQLAlchemy session reaches route and service code.
3. How `fastapi-users` is customized through schemas, manager hooks, and auth backends.
4. Why schema migrations are separate from ORM model definitions.
5. How tests can drive small API increments.
6. How authentication features can be decomposed into small, teachable tasks.

