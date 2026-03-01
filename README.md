# Explore

In which I explore `fastapi-users`

## Start server

`uv run fastapi dev src/explore/app.py`

## Auth flow

This app uses bearer auth with Redis-backed tokens.

### 0. Prerequisites

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

Expected: `200 OK` with user data (`is_verified` is typically `false` initially).

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
