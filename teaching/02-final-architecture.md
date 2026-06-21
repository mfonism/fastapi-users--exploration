# Final Architecture

## Folder Overview

```text
.
├── alembic/
│   ├── env.py
│   └── versions/
├── scripts/
│   └── check_empty_migrations.py
├── src/
│   └── explore/
│       ├── app.py
│       ├── env.py
│       ├── settings.py
│       ├── exceptions.py
│       ├── db/
│       ├── utils/
│       └── auth/
└── tests/
    ├── conftest.py
    ├── factories/
    ├── utils/
    └── auth/
```

## Application Entry Point

`src/explore/app.py` owns the FastAPI application object. It:

- creates the app
- runs database startup checks in lifespan
- includes the auth router
- maps app-specific exceptions to JSON responses
- exposes `/health`

## Configuration

Configuration is split into two layers:

| File | Responsibility |
|---|---|
| `src/explore/env.py` | Defines supported app environments and env-file resolution. |
| `src/explore/settings.py` | Reads settings, derives DB names, builds DB URLs, and derives Redis key prefixes. |
| `.env.example` | Documents local variables students copy into `.env`. |

The app supports `local`, `test`, `staging`, and `production`, with aliases like
`dev`, `testing`, `stage`, and `prod`.

## Database Layer

| File | Responsibility |
|---|---|
| `src/explore/db/base.py` | Declarative SQLAlchemy base class. |
| `src/explore/db/config.py` | Async engine, sessionmaker, database bootstrap checks, PostgreSQL version check. |
| `src/explore/db/registry.py` | Imports all models so Alembic sees them. |
| `src/explore/db/bootstrap.py` | CLI command to create and migrate local/test DBs. |
| `src/explore/db/migrate.py` | CLI commands for upgrade and downgrade. |
| `alembic/env.py` | Connects Alembic to app settings and model metadata. |

## Auth Modules

```text
auth/
├── routes.py
├── dependencies.py
├── exceptions.py
├── notifications.py
├── backends/
│   └── redis.py
├── users/
│   ├── models.py
│   ├── schemas.py
│   ├── manager.py
│   └── routes.py
├── sessions/
│   └── routes.py
├── passwords/
│   ├── schemas.py
│   ├── service.py
│   ├── exceptions.py
│   └── routes.py
├── reactivation/
│   ├── schemas.py
│   ├── service.py
│   ├── exceptions.py
│   └── routes.py
└── email_changes/
    ├── models.py
    ├── schemas.py
    ├── service.py
    ├── exceptions.py
    └── routes.py
```

The pattern is intentionally repeatable:

1. `schemas.py` defines request/response shapes.
2. `models.py` defines persisted state when a feature needs its own table.
3. `service.py` contains business rules.
4. `routes.py` handles HTTP concerns and dependencies.
5. `exceptions.py` defines stable API error codes.

## Main Request Flow

```text
HTTP request
  -> FastAPI app
  -> auth router
  -> route function
  -> dependency resolution
       -> async DB session
       -> current user/token, when required
       -> UserManager, when required
  -> service or manager method
  -> SQLAlchemy model mutation/query
  -> PostgreSQL and/or Redis
  -> response model or empty 204/202 response
```

## Example: Protected Current User Flow

```text
GET /users/me
  -> users.routes.get_current_user
  -> current_user dependency
  -> fastapi-users validates bearer token
  -> Redis strategy loads token state
  -> database loads user
  -> dependency rejects inactive, unverified, or deleted users
  -> route returns CurrentUserRead
```

## Example: Email Change Flow

```text
POST /auth/request-email-change
  -> current_user dependency
  -> request_email_change service
  -> normalize new email
  -> reject same/taken email
  -> cancel unresolved requests
  -> create UserEmailChange with hashed token
  -> send notification placeholder

POST /auth/confirm-email-change
  -> hash submitted token
  -> load matching UserEmailChange
  -> reject expired, cancelled, confirmed, deleted, inactive, or taken email
  -> update user email
  -> mark user verified at confirmation time
  -> logout matching current session if present
```

