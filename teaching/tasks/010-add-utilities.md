# 010: Add Utilities

## Task Metadata

| Field | Value |
|---|---|
| ID | 010 |
| Title | Add utilities |
| Parent epic | E1: Configuration and database infrastructure |
| Sibling tasks | 004, 005, 006, 007, 008, 009, 011 |
| Blocking tasks | 005 |
| Blocked tasks | 014 |
| Time estimate | 25-35 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `utilities`, `tests`, `beginner` |
| Suggested commit | `feat: add email and clock utilities` |

## Rich Description

Add small shared helpers for email normalization and current UTC time.

## Learning Goal

Students learn why small helpers make tests deterministic and keep repeated
logic out of routes and models.

## Files Created Or Modified

- `src/explore/utils/__init__.py`
- `src/explore/utils/email.py`
- `src/explore/utils/clock.py`
- `tests/utils/__init__.py`
- `tests/utils/test_email.py`

## Exact Implementation Objective

Implement `normalize_email(email: str) -> str` using `email-validator` and
`utcnow() -> datetime` using timezone-aware UTC datetimes.

## Acceptance Criteria

- Email normalization strips whitespace.
- Unicode domain examples normalize to ASCII form.
- Invalid emails raise `EmailNotValidError`.
- `utcnow` returns timezone-aware UTC datetimes.

## Teaching Notes

The clock helper exists mainly for tests. Point out how patching one helper is
cleaner than patching `datetime.now` everywhere.

