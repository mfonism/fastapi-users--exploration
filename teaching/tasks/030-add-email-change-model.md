# 030: Add Email-Change Model

## Task Metadata

| Field | Value |
|---|---|
| ID | 030 |
| Title | Add email-change model |
| Parent epic | E6: Email-change workflow |
| Sibling tasks | 031, 032, 033 |
| Blocking tasks | 014 |
| Blocked tasks | 031 |
| Time estimate | 60-75 minutes |
| Difficulty | Intermediate |
| Parallelizable | Yes, branch D |
| Suggested labels | `model`, `email-change`, `migration` |
| Suggested commit | `feat: add email change model` |

## Rich Description

Add a separate table to track pending email-change requests. The table stores
old email, new email, hashed token, expiry, confirmation, cancellation, and
creation time.

## Learning Goal

Students learn when a workflow deserves its own model instead of extra columns
on the user table.

## Files Created Or Modified

- `src/explore/auth/email_changes/__init__.py`
- `src/explore/auth/email_changes/models.py`
- `src/explore/db/registry.py`
- `tests/auth/models/test_user_email_change.py`
- Alembic revision for `user_email_change`

## Exact Implementation Objective

Create `UserEmailChange`, token generation/hash helpers, and model methods
`is_usable`, `confirm`, and `cancel`.

## Acceptance Criteria

- Raw email-change tokens are never stored.
- Token hashes are unique and indexed.
- `user_id` references `user.id` with cascade delete.
- `is_usable` returns false when expired, confirmed, or cancelled.
- `confirm` writes `confirmed_at` once.
- `cancel` writes `cancelled_at` once.
- Model helper tests cover token and state behavior.

## Teaching Notes

Use this as the main example for "workflow state as a table".

