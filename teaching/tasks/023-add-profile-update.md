# 023: Add Profile Update

## Task Metadata

| Field | Value |
|---|---|
| ID | 023 |
| Title | Add profile update |
| Parent epic | E4: Account management |
| Sibling tasks | 024, 025 |
| Blocking tasks | 022 |
| Blocked tasks | None |
| Time estimate | 35-45 minutes |
| Difficulty | Beginner |
| Parallelizable | Yes, branch A |
| Suggested labels | `users`, `profile`, `beginner` |
| Suggested commit | `feat: add current user profile updates` |

## Rich Description

Allow authenticated users to update their own `full_name` while preventing them
from changing account-state fields.

## Learning Goal

Students learn how update schemas protect sensitive fields.

## Files Created Or Modified

- `src/explore/auth/users/schemas.py`
- `src/explore/auth/users/routes.py`
- `tests/auth/views/test_patch_current_user.py`

## Exact Implementation Objective

Add `PATCH /users/me` using `CurrentUserUpdate` and `UserManager._update`.

## Acceptance Criteria

- Authenticated users can update `full_name`.
- Response returns the updated current-user payload.
- Unknown fields are rejected.
- Account-state fields such as `is_superuser`, `is_active`, and `deleted_at` are rejected.
- Route is named `users:patch_current_user`.

## Teaching Notes

Have students try sending a forbidden field in the request body and predict the
response.

