# 016: Add User Manager

## Task Metadata

| Field | Value |
|---|---|
| ID | 016 |
| Title | Add user manager |
| Parent epic | E3: Authentication core |
| Sibling tasks | 017, 018, 019, 020, 021, 022 |
| Blocking tasks | 011, 015 |
| Blocked tasks | 017, 018 |
| Time estimate | 60-75 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `auth`, `fastapi-users`, `manager` |
| Suggested commit | `feat: add user manager` |

## Rich Description

Create the bridge between this app's `User` model and `fastapi-users`. This is
where app-specific behavior hooks into registration, verification, reset
password, login, and deleted-user checks.

## Learning Goal

Students learn how a third-party auth library can be customized without
rewriting its core behavior.

## Files Created Or Modified

- `src/explore/auth/users/manager.py`
- `src/explore/auth/notifications.py`
- `src/explore/auth/exceptions.py`

## Exact Implementation Objective

Implement `get_user_db`, `UserManager`, and `get_user_manager`. Add placeholder
notification functions for verification and password reset.

## Acceptance Criteria

- `UserManager` extends `UUIDIDMixin` and `BaseUserManager`.
- Manager uses configured reset and verification token secrets.
- Email lookup and authentication normalize email.
- Deleted users are rejected from protected auth flows.
- Registration requests verification.
- Login updates `last_login_at`.
- Notification functions are async placeholders.

## Teaching Notes

Call out the hooks by name. Students should leave knowing which methods the
library calls and which ones the app overrides.

