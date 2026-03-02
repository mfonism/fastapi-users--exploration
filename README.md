# Explore

In which I explore `fastapi-users`

## Start server

`uv run fastapi dev src/explore/app.py`

## Testing

Run all tests:

`python -m unittest discover -s tests -p 'test_*.py' -q`

Run one test file:

`python -m unittest -q tests/test_settings.py`

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
- `DB_NAME`

Defaults are `postgres/postgres/explore` on `localhost:5432`.

## Auth flow

This app uses bearer auth with Redis-backed tokens.

### 0. Prerequisites

Start PostgreSQL locally:

`docker run --rm --name explore-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=explore -p 5432:5432 postgres:17`

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
