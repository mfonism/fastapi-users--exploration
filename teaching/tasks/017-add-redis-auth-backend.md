# 017: Add Redis Auth Backend

## Task Metadata

| Field | Value |
|---|---|
| ID | 017 |
| Title | Add Redis auth backend |
| Parent epic | E3: Authentication core |
| Sibling tasks | 016, 018, 019, 020, 021, 022 |
| Blocking tasks | 016 |
| Blocked tasks | 018 |
| Time estimate | 35-45 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `auth`, `redis`, `tokens` |
| Suggested commit | `feat: add Redis auth backend` |

## Rich Description

Configure bearer-token authentication backed by Redis. This gives the app a
session store that can revoke tokens on logout.

## Learning Goal

Students learn why token storage strategy affects logout behavior.

## Files Created Or Modified

- `src/explore/auth/backends/__init__.py`
- `src/explore/auth/backends/redis.py`
- `src/explore/settings.py`
- `.env.example`
- `pyproject.toml`
- `uv.lock`

## Exact Implementation Objective

Create a `BearerTransport`, Redis strategy factory, and `AuthenticationBackend`
using values from settings.

## Acceptance Criteria

- `AUTH_REDIS_URL` is documented in `.env.example`.
- Redis key prefix changes in test environment.
- `tokenUrl` is `auth/login`.
- Token lifetime is 3600 seconds.
- Backend name is `redis`.

## Teaching Notes

Draw the difference between a self-contained token and a stored token. This app
uses stored tokens so logout can revoke access.

