# 021: Add Login And Logout

## Task Metadata

| Field | Value |
|---|---|
| ID | 021 |
| Title | Add login and logout |
| Parent epic | E3: Authentication core |
| Sibling tasks | 016, 017, 018, 019, 020, 022 |
| Blocking tasks | 020 |
| Blocked tasks | 022, 026 |
| Time estimate | 60-75 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `auth`, `sessions`, `redis` |
| Suggested commit | `feat: add verified login and logout` |

## Rich Description

Add login/logout routes using the Redis auth backend. Require verified users to
login and make logout revoke the access token.

## Learning Goal

Students learn the session lifecycle: issue a token, use the token, revoke the
token.

## Files Created Or Modified

- `src/explore/auth/sessions/__init__.py`
- `src/explore/auth/sessions/routes.py`
- `src/explore/auth/routes.py`
- `src/explore/auth/users/manager.py`
- `tests/auth/views/test_login.py`
- `tests/auth/views/test_logout.py`

## Exact Implementation Objective

Include the generated auth router with `requires_verification=True`, adjust the
logout route to return 204, and ensure login updates `last_login_at`.

## Acceptance Criteria

- Verified users can log in with email and password.
- Emails are normalized during login.
- Invalid emails and bad credentials are rejected.
- Unverified, deleted, and deactivated users cannot log in.
- Logout revokes the token.
- Logout returns 204 with no response content.
- Login updates `last_login_at`.

## Teaching Notes

Ask students why logout needs Redis in this design.

