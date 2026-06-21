# 019: Test Registration

## Task Metadata

| Field | Value |
|---|---|
| ID | 019 |
| Title | Test registration |
| Parent epic | E3: Authentication core |
| Sibling tasks | 016, 017, 018, 020, 021, 022 |
| Blocking tasks | 013, 018 |
| Blocked tasks | 020 |
| Time estimate | 45-60 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `tests`, `registration`, `auth` |
| Suggested commit | `test: cover user registration` |

## Rich Description

Add endpoint tests for registration so students see the first full vertical
slice: request payload, schema validation, manager hooks, database write, and
response payload.

## Learning Goal

Students learn how endpoint tests verify behavior across several layers at
once.

## Files Created Or Modified

- `tests/conftest.py`
- `tests/auth/views/__init__.py`
- `tests/auth/views/assertions.py`
- `tests/auth/views/test_register.py`

## Exact Implementation Objective

Create async test fixtures for app requests and write registration tests for
success, email normalization, duplicate email rejection, validation errors, and
verification notification calls.

## Acceptance Criteria

- Registration creates a DB user.
- Password is hashed and not stored raw.
- Internal user fields are hidden from response payloads.
- Email is normalized before storage.
- Duplicate normalized emails are rejected.
- Invalid payloads return 422.
- Verification notification placeholder is called after successful register.

## Teaching Notes

This is the first good place to introduce `httpx.ASGITransport` and dependency
overrides.

