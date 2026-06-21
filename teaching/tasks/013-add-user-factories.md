# 013: Add User Factories

## Task Metadata

| Field | Value |
|---|---|
| ID | 013 |
| Title | Add user factories |
| Parent epic | E2: User domain model |
| Sibling tasks | 012, 014, 015 |
| Blocking tasks | 012 |
| Blocked tasks | 019 |
| Time estimate | 25-35 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `tests`, `factories`, `beginner` |
| Suggested commit | `test: add user factories` |

## Rich Description

Add reusable test builders for common user states. These factories keep later
tests short and make the account lifecycle easier to discuss.

## Learning Goal

Students learn how test data builders reduce repetition and make tests read
like scenarios.

## Files Created Or Modified

- `tests/__init__.py`
- `tests/factories/__init__.py`
- `tests/factories/user.py`
- `tests/factories/test_user.py`

## Exact Implementation Objective

Create helper functions such as `build_signed_up_user`,
`build_verified_user`, `build_plain_user`, `build_superuser`, and
`build_deleted_user`.

## Acceptance Criteria

- Each factory returns a `User` instance.
- Factories use deterministic timestamps.
- Callers can override any field.
- Factory tests verify the expected default state.

## Teaching Notes

Show one test before and after using a factory. The improvement should be
obvious.

