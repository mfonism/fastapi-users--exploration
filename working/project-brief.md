# Project Brief

## Product Summary

Explore Auth API is a FastAPI backend service that demonstrates a realistic
authentication and account-management system using `fastapi-users`,
PostgreSQL, Redis, Alembic, and async SQLAlchemy.

The target implementation supports:

- registration
- email verification
- Redis-backed login and logout
- current-user profile read/update
- account deactivation
- soft deletion
- password reset
- password change
- account reactivation
- email-change request and confirmation
- local/test database bootstrap commands
- pytest coverage for API and model behavior

## Technical Context

| Area | Decision |
|---|---|
| Runtime | Python 3.14 |
| Package manager | uv |
| Web framework | FastAPI |
| Auth library | fastapi-users |
| Database | PostgreSQL |
| ORM | async SQLAlchemy |
| Migrations | Alembic |
| Token storage | Redis strategy through fastapi-users |
| Settings | pydantic-settings |
| Test runner | pytest and pytest-asyncio |
| HTTP test client | httpx ASGITransport |
| Formatting/linting | Ruff and pre-commit |

## Non-Goals

These are intentionally out of scope for this delivery plan:

- frontend application
- production email provider
- hosted deployment pipeline
- admin dashboard
- OAuth/social login
- multi-tenant authorization
- observability stack

## Delivery Assumptions

- PostgreSQL and Redis are available locally or through containers.
- The team is comfortable using uv.
- The roadmap is used as a classroom work simulation, so some tasks are ordered
  for learning rather than pure delivery speed.
- Senior-owned infrastructure tickets may be larger than student-owned feature
  tickets.
- The first implementation uses placeholder notification functions.
- Tests are required for model behavior and API endpoints.
- Migrations are reviewed as part of the PR process.
- Junior engineers may own tickets, so each task includes implementation notes.

## Teaching Sequence

The first domain concept is introduced before persistence:

1. Define a simple user shape with no database.
2. Set up async database infrastructure separately.
3. Convert the user shape into a SQLAlchemy model and migration.

This avoids asking students to learn FastAPI, Pydantic, async SQLAlchemy,
UUIDs, Alembic, and PostgreSQL all in the same step.

## Release Readiness Criteria

The project is releasable when:

- `uv run ruff check .` passes
- `uv run ruff format --check .` passes, or formatting has been applied
- `uv run pytest` passes against a bootstrapped test database
- `uv run alembic current` reports the expected head revision
- README setup instructions work from a clean checkout
- OpenAPI documents password fields as write-only
- empty command endpoints document 204 or 202, not 200 with content
