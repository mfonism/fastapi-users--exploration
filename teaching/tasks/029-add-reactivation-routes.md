# 029: Add Reactivation Routes

## Task Metadata

| Field | Value |
|---|---|
| ID | 029 |
| Title | Add reactivation routes |
| Parent epic | E5: Password and account recovery |
| Sibling tasks | 026, 027, 028 |
| Blocking tasks | 025, 028 |
| Blocked tasks | 034 |
| Time estimate | 45-60 minutes |
| Difficulty | Intermediate |
| Parallelizable | Yes, branch C |
| Suggested labels | `auth`, `reactivation`, `routes` |
| Suggested commit | `feat: add account reactivation endpoints` |

## Rich Description

Expose the reactivation service through two public endpoints: one to request a
reactivation email and one to confirm the token.

## Learning Goal

Students learn how to design public recovery endpoints that avoid leaking
whether an account exists.

## Files Created Or Modified

- `src/explore/auth/reactivation/routes.py`
- `src/explore/auth/routes.py`
- `tests/auth/views/test_request_reactivation.py`
- `tests/auth/views/test_confirm_reactivation.py`

## Exact Implementation Objective

Create `POST /auth/request-reactivation` returning 202 and
`POST /auth/reactivate` returning 204.

## Acceptance Criteria

- Requesting reactivation for an eligible deactivated user sends notification.
- Requesting reactivation for unknown, active, or deleted users still returns 202.
- Confirming a valid token clears `deactivated_at`.
- Reused, expired, stale, active-user, and deleted-user tokens are rejected.
- Empty success responses document 202 or 204 correctly.

## Teaching Notes

Make the response-code choice explicit: request accepted is 202 because the
email send is conceptually asynchronous.

