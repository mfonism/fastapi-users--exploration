# 014: Add Account-State Fields

## Task Metadata

| Field | Value |
|---|---|
| ID | 014 |
| Title | Add account-state fields |
| Parent epic | E2: User domain model |
| Sibling tasks | 012, 013, 015 |
| Blocking tasks | 010, 012 |
| Blocked tasks | 015, 030 |
| Time estimate | 60-90 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `model`, `account-state`, `tests` |
| Suggested commit | `feat: model user account states` |

## Rich Description

Expand the user model from basic identity into a real account lifecycle model.
Use timestamps to represent verification, deactivation, deletion, superuser
granting, terms acceptance, last login, creation, and update times.

## Learning Goal

Students learn how computed properties can expose library-friendly booleans
while the database preserves useful audit timestamps.

## Files Created Or Modified

- `src/explore/auth/users/models.py`
- `tests/auth/models/test_user.py`
- Alembic revisions for new fields, database defaults, and `updated_at` behavior

## Exact Implementation Objective

Add timestamp columns and property setters for `is_active`, `is_deleted`,
`is_verified`, and `is_superuser`.

## Acceptance Criteria

- `is_active` maps to `deactivated_at is None`.
- `is_deleted` maps to `deleted_at is not None`.
- `is_verified` maps to `verified_at is not None`.
- `is_superuser` maps to `superuser_granted_at is not None`.
- Setting a boolean writes or clears the correct timestamp.
- Re-setting to the current state is a no-op.
- `__repr__` excludes password hashes.

## Teaching Notes

Use a state table. Students often mix up unverified, inactive, and deleted
users unless the states are made explicit.

