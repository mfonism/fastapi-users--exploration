# 025: Add Soft Delete

## Task Metadata

| Field | Value |
|---|---|
| ID | 025 |
| Title | Add soft delete |
| Parent epic | E4: Account management |
| Sibling tasks | 023, 024 |
| Blocking tasks | 011, 022 |
| Blocked tasks | 026, 029, 033 |
| Time estimate | 60-75 minutes |
| Difficulty | Intermediate |
| Parallelizable | Yes, branch A |
| Suggested labels | `users`, `soft-delete`, `auth` |
| Suggested commit | `feat: add soft deletion` |

## Rich Description

Add account deletion as a soft-delete operation. The user row remains in the
database, but `deleted_at` is set and the current session is revoked.

## Learning Goal

Students learn why some systems keep deleted rows and how auth checks must
respect that state.

## Files Created Or Modified

- `src/explore/auth/users/routes.py`
- `src/explore/auth/dependencies.py`
- `src/explore/auth/users/manager.py`
- `src/explore/auth/exceptions.py`
- `src/explore/app.py`
- `tests/auth/views/test_delete_current_user.py`

## Exact Implementation Objective

Create `DELETE /users/me`, set `is_deleted=True`, revoke the current Redis
token, and ensure deleted users cannot authenticate or use protected routes.

## Acceptance Criteria

- Authenticated users can soft delete their own account.
- `deleted_at` is written.
- The current token is revoked.
- Deleted users receive bad-credentials-style login errors.
- Deleted users cannot verify, reset password, or use current-user routes.
- Response status is 204 with no body.

## Teaching Notes

This is a good place to discuss user privacy, audit trails, and the difference
between product behavior and physical deletion.

