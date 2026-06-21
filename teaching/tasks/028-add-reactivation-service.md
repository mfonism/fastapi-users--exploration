# 028: Add Reactivation Service

## Task Metadata

| Field | Value |
|---|---|
| ID | 028 |
| Title | Add reactivation service |
| Parent epic | E5: Password and account recovery |
| Sibling tasks | 026, 027, 029 |
| Blocking tasks | 011, 024 |
| Blocked tasks | 029 |
| Time estimate | 60-90 minutes |
| Difficulty | Stretch |
| Parallelizable | Yes, branch C |
| Suggested labels | `auth`, `reactivation`, `tokens`, `stretch` |
| Suggested commit | `feat: add reactivation token service` |

## Rich Description

Add the service logic for requesting and confirming account reactivation. The
token should include user ID and the current `deactivated_at` timestamp so old
tokens stop working after state changes.

## Learning Goal

Students learn how token claims can bind a recovery action to a specific user
state.

## Files Created Or Modified

- `src/explore/auth/reactivation/__init__.py`
- `src/explore/auth/reactivation/schemas.py`
- `src/explore/auth/reactivation/exceptions.py`
- `src/explore/auth/reactivation/service.py`
- `src/explore/auth/notifications.py`

## Exact Implementation Objective

Create `request_reactivation` and `confirm_reactivation` service functions
using JWT generation/decoding and a dedicated token audience.

## Acceptance Criteria

- Active users do not receive reactivation tokens.
- Deleted users do not receive reactivation tokens.
- Deactivated users receive a token containing `sub`, `deactivated_at`, and `aud`.
- Invalid, expired, malformed, unknown-user, active-user, deleted-user, and stale tokens are rejected.
- Successful confirmation sets `is_active=True`.

## Teaching Notes

This is security-sensitive. Give students a failing-test matrix before they
write implementation code.

