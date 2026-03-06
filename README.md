# Explore

Exploration project for `fastapi-users` with FastAPI, PostgreSQL, Redis, Alembic, and `uv`.

## Prerequisites

- Python `3.14+`
- `uv`
- PostgreSQL running locally (default: `localhost:5432`)
- Redis running locally (default: `localhost:6379`) for auth token storage

Optional quick local containers:

```bash
docker run --rm --name explore-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:18.3
docker run --rm --name explore-redis -p 6379:6379 redis:7-alpine
```

## First-time local setup

<ToDO: are there any default env vars to set up? What about needing a postgres user with password postgres in postgres db>

Run these commands in order:

```bash
# 1) install dependencies
uv sync

# 2) ensure local DB exists (role/db/owner checks/bootstrap)
uv run db-bootstrap

# 3) apply schema migrations
uv run alembic upgrade head

# 4) optional: verify migration state
uv run alembic current

# 5) start API
uv run fastapi dev src/explore/app.py
```

Important:

- Do not start the API before running migrations.
- Startup checks DB connectivity/version, but does not create tables.

## Daily local workflow

```bash
uv run db-bootstrap
uv run alembic upgrade head
uv run pytest
uv run fastapi dev src/explore --app app
```

## Test workflow

Run tests with:

```bash
uv run pytest
```

Notes:

- Test fixtures set `APP_ENV=test`.
- Current pytest setup bootstraps and migrates the test DB in fixtures.
- You usually do not need to run manual test bootstrap/migration before `uv run pytest`.

## Configuration

Settings come from `pydantic-settings` in `src/explore/settings.py`.

Environment selection:

- `local` (default)
- `test`
- `staging`
- `production`

Supported aliases include `dev`, `testing`, `stage`, and `prod`.

Env file load order:

1. `.env`
2. `.env.<env>`

Environment variables override env file values.

## Database configuration defaults

Default DB-related values:

- `DB_DRIVER=postgresql+asyncpg`
- `DB_HOST=localhost`
- `DB_PORT=5432`
- `DB_USER=postgres`
- `DB_PASSWORD=postgres`
- `DB_BASE_NAME=explore`

Resolved DB names by environment:

- local: `explore`
- test: `explore_test`

PostgreSQL server version is checked in startup code (`src/explore/db/config.py`) against `REQUIRED_POSTGRES_VERSION`.

## Alembic commands

Create a migration from model changes:

```bash
uv run alembic revision --autogenerate -m "describe change"
```

Apply migrations:

```bash
uv run alembic upgrade head
```

Inspect state:

```bash
uv run alembic current
uv run alembic heads
uv run alembic history --verbose
```

## Convenience command

DB bootstrap command from `pyproject.toml`:

```bash
uv run db-bootstrap
```

This runs `explore.db.bootstrap:main`, which calls `ensure_database()`.

## API quick checks

Health:

```bash
curl http://127.0.0.1:8000/health
```

Register:

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"strongpass123"}'
```
