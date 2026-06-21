# 026: Add Password Reset

## Task Metadata

| Field | Value |
|---|---|
| ID | 026 |
| Title | Add password reset |
| Parent epic | E5: Password and account recovery |
| Sibling tasks | 027, 028, 029 |
| Blocking tasks | 021, 024, 025 |
| Blocked tasks | None |
| Time estimate | 60-75 minutes |
| Difficulty | Intermediate |
| Parallelizable | Yes, branch B |
| Suggested labels | `auth`, `passwords`, `recovery` |
| Suggested commit | `feat: add password reset workflow` |

## Rich Description

Use the generated reset-password router and local manager hooks to support
forgot-password and reset-password behavior.

## Learning Goal

Students learn the difference between public recovery flows and authenticated
account-management flows.

## Files Created Or Modified

- `src/explore/auth/routes.py`
- `src/explore/auth/users/manager.py`
- `src/explore/auth/notifications.py`
- `tests/auth/views/test_forgot_password.py`
- `tests/auth/views/test_reset_password.py`

## Exact Implementation Objective

Ensure forgot-password sends a notification placeholder and reset-password
updates the stored password hash for valid tokens.

## Acceptance Criteria

- Forgot-password accepts known user emails without returning user details.
- Reset-password updates the password hash.
- Reused, expired, and invalid tokens are rejected.
- Deleted users cannot reset passwords.
- Deactivated users cannot be reactivated by password reset.
- Notification function receives recipient email, name, and token.

## Teaching Notes

Emphasize non-enumeration: public recovery endpoints should not reveal whether
an email belongs to an account.

