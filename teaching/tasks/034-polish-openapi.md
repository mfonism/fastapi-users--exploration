# 034: Polish OpenAPI

## Task Metadata

| Field | Value |
|---|---|
| ID | 034 |
| Title | Polish OpenAPI |
| Parent epic | E7: API polish and docs |
| Sibling tasks | 035 |
| Blocking tasks | 018, 027, 029, 033 |
| Blocked tasks | 035 |
| Time estimate | 30-45 minutes |
| Difficulty | Beginner |
| Parallelizable | Yes, branch E |
| Suggested labels | `openapi`, `docs`, `tests` |
| Suggested commit | `test: document auth OpenAPI responses` |

## Rich Description

Add tests that lock in important API documentation details: password fields are
write-only and command endpoints document empty success responses correctly.

## Learning Goal

Students learn that OpenAPI output is part of the public API contract and can
be tested.

## Files Created Or Modified

- `tests/auth/views/test_openapi.py`
- route files as needed for response status metadata
- schema files as needed for `writeOnly`

## Exact Implementation Objective

Assert OpenAPI schema properties and response codes for password fields,
logout, change-password, deactivate, reactivate, delete user, and request
reactivation.

## Acceptance Criteria

- `UserCreate.password` is write-only.
- `PasswordChange.current_password` is write-only.
- `PasswordChange.new_password` is write-only.
- 204 command endpoints document 204 and no 200 content.
- Request reactivation documents 202 and no 200 content.

## Teaching Notes

Treat this as polish after behavior works. Students should first care about
runtime behavior, then documented behavior.

