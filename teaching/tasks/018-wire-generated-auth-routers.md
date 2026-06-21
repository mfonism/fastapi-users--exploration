# 018: Wire Generated Auth Routers

## Task Metadata

| Field | Value |
|---|---|
| ID | 018 |
| Title | Wire generated auth routers |
| Parent epic | E3: Authentication core |
| Sibling tasks | 016, 017, 019, 020, 021, 022 |
| Blocking tasks | 016, 017 |
| Blocked tasks | 019, 020, 034 |
| Time estimate | 45-60 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `auth`, `routing`, `fastapi-users` |
| Suggested commit | `feat: wire generated auth routers` |

## Rich Description

Create the central auth router and include the generated registration,
reset-password, and verification routers from `fastapi-users`.

## Learning Goal

Students learn router composition and how a library can provide API routes that
are still configured by local schemas and managers.

## Files Created Or Modified

- `src/explore/auth/dependencies.py`
- `src/explore/auth/routes.py`
- `src/explore/app.py`

## Exact Implementation Objective

Instantiate `FastAPIUsers` and include generated routers under `/auth`. Mount
the auth router in the main app.

## Acceptance Criteria

- `fastapi_users` is configured with `get_user_manager` and the Redis backend.
- Registration router uses `CurrentUserRead` and `UserCreate`.
- Reset-password router is included under `/auth`.
- Verification router uses `CurrentUserRead`.
- `app.include_router(auth_router)` is present.

## Teaching Notes

Use OpenAPI docs to show routes that appeared because of library wiring.

