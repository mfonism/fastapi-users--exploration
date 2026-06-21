# 024: Add Deactivation

## Task Metadata

| Field | Value |
|---|---|
| ID | 024 |
| Title | Add deactivation |
| Parent epic | E4: Account management |
| Sibling tasks | 023, 025 |
| Blocking tasks | 022 |
| Blocked tasks | 026, 028 |
| Time estimate | 35-45 minutes |
| Difficulty | Beginner |
| Parallelizable | Yes, branch A |
| Suggested labels | `auth`, `account-state`, `beginner` |
| Suggested commit | `feat: add account deactivation` |

## Rich Description

Add an authenticated command endpoint that deactivates the current user by
setting `is_active` to false.

## Learning Goal

Students learn how a route can perform a state transition and return an empty
success response.

## Files Created Or Modified

- `src/explore/auth/users/routes.py`
- `tests/auth/views/test_deactivate.py`

## Exact Implementation Objective

Create `POST /auth/deactivate`, update the current user through the manager,
and return 204.

## Acceptance Criteria

- Authenticated verified users can deactivate their account.
- Deactivation writes `deactivated_at`.
- The deactivated user can no longer access `/users/me`.
- Response status is 204 with no body.
- Route is named `auth:deactivate`.

## Teaching Notes

Connect this to the earlier timestamp-backed `is_active` property.

