# 022: Add Current-User Endpoint

## Task Metadata

| Field | Value |
|---|---|
| ID | 022 |
| Title | Add current-user endpoint |
| Parent epic | E3: Authentication core |
| Sibling tasks | 016, 017, 018, 019, 020, 021 |
| Blocking tasks | 021 |
| Blocked tasks | 023, 024, 025, 027, 032 |
| Time estimate | 45-60 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `auth`, `users`, `protected-route` |
| Suggested commit | `feat: add current user endpoint` |

## Rich Description

Create the first custom protected route: `GET /users/me`. This route returns
the authenticated user using the current-user dependency.

## Learning Goal

Students learn how route dependencies enforce authentication before route code
runs.

## Files Created Or Modified

- `src/explore/auth/dependencies.py`
- `src/explore/auth/users/routes.py`
- `src/explore/auth/routes.py`
- `tests/auth/views/test_get_current_user.py`

## Exact Implementation Objective

Create current-user dependencies for active, verified users and expose
`GET /users/me` with the `CurrentUserRead` response model.

## Acceptance Criteria

- Unauthenticated requests return 401.
- Authenticated verified users receive their public current-user payload.
- Deleted users are rejected even if token authentication succeeds.
- Internal user fields are hidden.
- Route is named `users:current_user`.

## Teaching Notes

This task is the safe split point for parallel student work.

