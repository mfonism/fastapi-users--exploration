# 020: Add Verification Flow

## Task Metadata

| Field | Value |
|---|---|
| ID | 020 |
| Title | Add verification flow |
| Parent epic | E3: Authentication core |
| Sibling tasks | 016, 017, 018, 019, 021, 022 |
| Blocking tasks | 018, 019 |
| Blocked tasks | 021 |
| Time estimate | 60-75 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `auth`, `verification`, `tokens` |
| Suggested commit | `feat: add email verification workflow` |

## Rich Description

Complete the email verification flow by testing verification-token requests and
token confirmation behavior.

## Learning Goal

Students learn token-based state transitions and how to make an operation
idempotent for already verified users.

## Files Created Or Modified

- `src/explore/auth/users/manager.py`
- `tests/auth/views/test_request_verify_token.py`
- `tests/auth/views/test_verify.py`

## Exact Implementation Objective

Ensure verification requests call the notification placeholder and verification
sets `verified_at`. Deleted users should not receive valid verification flows.

## Acceptance Criteria

- Requesting a verification token sends a notification for eligible users.
- Confirming a valid token marks the user verified.
- Verifying an already verified user returns the user instead of failing.
- Expired or invalid tokens are rejected.
- Deleted users cannot verify or request verification.

## Teaching Notes

Show the difference between "request token" and "confirm token". They are
separate endpoints and separate user actions.

