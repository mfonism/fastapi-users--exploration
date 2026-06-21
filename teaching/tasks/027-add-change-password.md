# 027: Add Change Password

## Task Metadata

| Field | Value |
|---|---|
| ID | 027 |
| Title | Add change password |
| Parent epic | E5: Password and account recovery |
| Sibling tasks | 026, 028, 029 |
| Blocking tasks | 011, 022 |
| Blocked tasks | 034 |
| Time estimate | 45-60 minutes |
| Difficulty | Beginner |
| Parallelizable | Yes, branch B |
| Suggested labels | `auth`, `passwords`, `service-layer` |
| Suggested commit | `feat: add password change endpoint` |

## Rich Description

Add a custom authenticated endpoint for changing the current user's password
when they know their current password.

## Learning Goal

Students learn the route/schema/service/exception pattern used by later custom
features.

## Files Created Or Modified

- `src/explore/auth/passwords/__init__.py`
- `src/explore/auth/passwords/schemas.py`
- `src/explore/auth/passwords/exceptions.py`
- `src/explore/auth/passwords/service.py`
- `src/explore/auth/passwords/routes.py`
- `src/explore/auth/routes.py`
- `tests/auth/views/test_change_password.py`

## Exact Implementation Objective

Create `POST /auth/change-password`, verify the current password, update the
password through `UserManager`, and return 204.

## Acceptance Criteria

- `PasswordChange` contains `current_password` and `new_password`.
- Both password fields are marked `writeOnly`.
- Wrong current password raises `CHANGE_PASSWORD_BAD_PASSWORD`.
- Correct current password updates the hash.
- Response status is 204 with no body.

## Teaching Notes

Compare this custom flow to generated reset-password routes. Students should
see why some features are library-provided and others are app-specific.

