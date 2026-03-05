# Explore

In which I explore `fastapi-users`

## Start server

`uv run fastapi dev src/explore/app.py`

Requires Python `3.14+`.

On startup, the app bootstraps PostgreSQL:
- Connects to the admin database `postgres`
- Ensures the app role exists (local/test only)
- Ensures the app database exists and is owned by that role
- Creates app tables

## Testing

Run all tests:

`APP_ENV=test python -m unittest discover -s tests -p 'test_*.py' -q`

Run one test file:

`APP_ENV=test python -m unittest -q tests/test_settings.py`

## Configuration

Settings are loaded with `pydantic-settings` via `get_settings()` in [`src/explore/settings.py`](src/explore/settings.py).

### Environment selection

Use `APP_ENV` to choose the active environment:

- `local`
- `test`
- `staging`
- `production`

Supported aliases include `dev`, `testing`, `stage`, and `prod`.

### Env file loading

The app loads, in order:

1. `.env` (shared defaults)
2. `.env.<env>` (environment-specific override)

Examples:

- `.env.local`
- `.env.test`
- `.env.staging`
- `.env.production`

Environment variables always override values from env files.

### Debug mode

`DEBUG` controls FastAPI debug mode.

If `DEBUG` is not set:

- `local` and `test` default to `true`
- `staging` and `production` default to `false`

Debug mode is mainly for development (detailed exception pages and development diagnostics). It should stay off in staging/production.

### Example env file

See `.env.example` for all supported variables and placeholders.

### Database backend

The app is configured for PostgreSQL with async SQLAlchemy (`asyncpg` driver).
The SQLAlchemy URL is built from:

- `DB_DRIVER`
- `DB_HOST`
- `DB_PORT`
- `DB_USER`
- `DB_PASSWORD`
- `DB_BASE_NAME`

Defaults are `postgres/postgres/explore` on `localhost:5432`.
When `APP_ENV=test`, the app automatically uses `${DB_BASE_NAME}_test`.
Required PostgreSQL version is hardcoded in [`src/explore/db/config.py`](src/explore/db/config.py) as `REQUIRED_POSTGRES_VERSION`.

### Migrations (Alembic)

Schema migrations are managed with Alembic.

For a fresh local setup (after PostgreSQL is running and env vars are set), run:

`uv run alembic upgrade head`

This applies all migrations to the active environment database.
`APP_ENV` controls which DB is targeted:

- `APP_ENV=local` -> `${DB_BASE_NAME}` (default: `explore`)
- `APP_ENV=test` -> `${DB_BASE_NAME}_test` (default: `explore_test`)

Examples:

```bash
# local/dev DB
uv run alembic upgrade head

# test DB
APP_ENV=test uv run alembic upgrade head
```

When you change models and need a new migration:

```bash
uv run alembic revision --autogenerate -m "describe change"
uv run alembic upgrade head
```

Useful checks:

```bash
uv run alembic current
uv run alembic heads
uv run alembic history --verbose
```

### PostgreSQL prerequisites

Before running `uv run fastapi dev src/explore/app.py`, PostgreSQL must have:

- Admin database: `postgres` (used for bootstrap operations)
- A login role matching `DB_USER`
- Credentials matching `DB_PASSWORD`

Defaults if you do not override env vars:

- `DB_HOST=localhost`
- `DB_PORT=5432`
- `DB_USER=postgres`
- `DB_PASSWORD=postgres`
- `DB_BASE_NAME=explore`

With those defaults:

- local/dev app DB: `explore`
- test app DB: `explore_test`

In `local` and `test`, startup may create missing role/database and fix DB ownership.
In `staging` and `production`, startup is validation-only and fails if role/database are missing or ownership is wrong.

Recommended env files:

- `.env.local` for dev/local DB config
- `.env.test` for test DB config

Example local/test overrides:

```env
# .env.local
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_BASE_NAME=explore

# .env.test
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_BASE_NAME=explore
```

For Redis token storage, a key prefix is also derived from `REDIS_KEY_PREFIX_BASE`:

- non-test: `${REDIS_KEY_PREFIX_BASE}:`
- test: `${REDIS_KEY_PREFIX_BASE}_test:`

## Auth flow

This app uses bearer auth with Redis-backed tokens.

### 0. Prerequisites

Start PostgreSQL locally:

`docker run --rm --name explore-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:18.3`

Start Redis locally:

`docker run --rm -p 6379:6379 redis:7-alpine`

Start the API:

`uv run fastapi dev src/explore/app.py`

### 1. Register

```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"alice@example.com","password":"strongpass123"}'
```

Expected: `201 Created` and a user payload.

### 2. Unauthenticated access should fail

```bash
curl http://127.0.0.1:8000/whoami
```

Expected: `401 Unauthorized`.

### 3. Login

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=alice@example.com&password=strongpass123"
```

Expected response includes:

```json
{ "access_token": "<token>", "token_type": "bearer" }
```

Save token:

```bash
TOKEN="<paste_access_token_here>"
```

### 4. Call protected routes

Current user:

```bash
curl http://127.0.0.1:8000/whoami \
  -H "Authorization: Bearer $TOKEN"
```

FastAPI Users built-in profile:

```bash
curl http://127.0.0.1:8000/users/me \
  -H "Authorization: Bearer $TOKEN"
```

Expected: `200 OK` with user data (`verified_at` is typically `null` initially).

### 5. Logout

```bash
curl -X POST http://127.0.0.1:8000/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

Expected: `204 No Content`.

### 6. Confirm token is invalid after logout

```bash
curl http://127.0.0.1:8000/whoami \
  -H "Authorization: Bearer $TOKEN"
```

Expected: `401 Unauthorized`.

### 7. Email verification (current state)

Verification endpoints are available:

- `POST /auth/request-verify-token`
- `POST /auth/verify`

This project currently has no email delivery hook (`on_after_request_verify`) configured, so verification tokens are not sent anywhere yet. To fully test verify flow, add a custom `UserManager` callback (log token, print it, or send email) and then submit that token to `/auth/verify`.
