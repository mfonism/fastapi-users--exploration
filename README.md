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

### 1) Create your `.env` file

Copy the example file:

```bash
cp .env.example .env
```

Then update values in `.env` for your local machine.

At minimum, confirm these DB settings are correct:

- `DB_HOST`: PostgreSQL host (usually `localhost`)
- `DB_PORT`: PostgreSQL port (usually `5432`)
- `DB_USER`: PostgreSQL login role to use
- `DB_PASSWORD`: password for that role
- `DB_BASE_NAME`: base app DB name (`explore` -> test DB becomes `explore_test`)

Defaults in `.env.example` are:

- `DB_HOST=localhost`
- `DB_PORT=5432`
- `DB_USER=postgres`
- `DB_PASSWORD=postgres`
- `DB_BASE_NAME=explore`

If your local Postgres uses different credentials, change them here before running setup.

### 2) Run setup commands

`db-bootstrap` connects to admin DB `postgres` using `DB_USER`/`DB_PASSWORD`,
then ensures the requested database(s) exist, have the expected owner, and are
migrated to the latest schema.

Run these commands in order:

```bash
# 1) install dependencies
uv sync

# 2) ensure local + test DBs exist and are migrated
uv run db-bootstrap

# 3) optional: verify migration state
uv run alembic current

# 4) start API
uv run fastapi dev src/explore/app.py
```

Important:

- `uv run db-bootstrap` bootstraps both `local` and `test` by default.
- Use `uv run db-bootstrap --app-env test` to prepare only the test DB.
- Use `uv run db-upgrade` when databases already exist and you only need to apply pending migrations.
- Startup checks DB connectivity/version, but does not create tables or run migrations.

## Daily local workflow

```bash
uv run db-bootstrap
uv run db-upgrade --app-env test
uv run pytest
uv run fastapi dev src/explore --app app
```

## Formatting and linting

Install hooks once:

```bash
uv run pre-commit install
```

Run formatting/linting checks:

```bash
uv run pre-commit run --all-files
```

Hooks configured:

- `ruff` (autofix + lint checks)

## Test workflow

Run tests with:

```bash
uv run pytest
```

Notes:

- Test fixtures set `APP_ENV=test`.
- Pytest assumes the test DB has already been bootstrapped and migrated.
- Before running tests for the first time, run `uv run db-bootstrap`.
- To prepare only the test DB from scratch, run `uv run db-bootstrap --app-env test`.
- To apply new schema changes to an existing test DB, run `uv run db-upgrade --app-env test`.
- SQLAlchemy query echo is off by default so failed tests stay readable.
  To debug database traffic for a test run, use:

```bash
DB_ECHO=true uv run pytest
```

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

When you add a new SQLAlchemy model, also import it in
`src/explore/db/registry.py`. Alembic loads that registry before reading
`Base.metadata`; without the import, autogenerate may miss the new table or
think an existing table disappeared.

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

By default this bootstraps and migrates both the `local` and `test` databases.

To bootstrap only one environment:

```bash
uv run db-bootstrap --app-env local
uv run db-bootstrap --app-env test
```

Migration-only command:

```bash
uv run db-upgrade
uv run db-upgrade --app-env test --revision head
uv run db-downgrade --app-env test --revision -1
```

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

## Future Plans

### Modular Model Capabilities

The `User` model currently owns several reusable account-state capabilities:

- soft deletion through `deleted_at` / `is_deleted`
- deactivation through `deactivated_at` / `is_active`
- verification through `verified_at` / `is_verified`
- timestamp tracking through `created_at` / `updated_at`

As more models are added, we may extract these repeated capabilities into
SQLAlchemy mixins. This would make the model layer more modular and create a
clear teaching example for inheritance and composition.

Possible mixins:

```python
class SoftDeletable:
    deleted_at = ...

    @property
    def is_deleted(self) -> bool: ...

    @classmethod
    def not_deleted(cls): ...

    @classmethod
    def deleted(cls): ...


class Deactivatable:
    deactivated_at = ...

    @property
    def is_active(self) -> bool: ...

    @classmethod
    def active(cls): ...

    @classmethod
    def deactivated(cls): ...


class Timestamped:
    created_at = ...
    updated_at = ...
```

Then a model could opt into only the capabilities it needs:

```python
class User(Base, SoftDeletable, Deactivatable, Timestamped):
    ...
```

The first safe refactor would be small:

1. Extract `SoftDeletable`.
2. Extract `Deactivatable`.
3. Add explicit query predicates such as `User.not_deleted()` and
   `User.active()`.
4. Keep `Verifiable` and superuser behavior on `User` until another model
   needs them.

The goal is not to hide filtering magically. Queries should still be explicit:

```python
select(User).where(User.not_deleted(), User.active())
```

These mixins should also expose reusable filtering predicates so query code does
not have to repeat column details everywhere:

```python
select(User).where(User.not_deleted())
select(User).where(User.deleted())
select(User).where(User.active())
select(User).where(User.deactivated())
```

Models can also define combined predicates for common domain concepts:

```python
class User(Base, SoftDeletable, Deactivatable, Timestamped):
    @classmethod
    def available(cls):
        return cls.not_deleted() & cls.active()
```

Then callers can use the domain-level predicate when that is what they mean:

```python
select(User).where(User.available())
```

This keeps soft-deleted and deactivated records visible when a feature
intentionally needs them, while reducing repeated query conditions in normal
application code.
