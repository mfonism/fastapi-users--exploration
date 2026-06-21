# 011: Add App Errors

## Task Metadata

| Field | Value |
|---|---|
| ID | 011 |
| Title | Add app errors |
| Parent epic | E1: Configuration and database infrastructure |
| Sibling tasks | 004, 005, 006, 007, 008, 009, 010 |
| Blocking tasks | 002 |
| Blocked tasks | 016, 025, 027, 028, 031 |
| Time estimate | 25-35 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `errors`, `api`, `beginner` |
| Suggested commit | `feat: add API error handling` |

## Rich Description

Create a small app-specific exception hierarchy and register a FastAPI
exception handler that returns stable JSON error payloads.

## Learning Goal

Students learn how domain errors become HTTP responses without spreading
response-building code through every service.

## Files Created Or Modified

- `src/explore/exceptions.py`
- `src/explore/auth/exceptions.py`
- `src/explore/app.py`

## Exact Implementation Objective

Define `AppError`, `AppAPIError`, and an `AuthError` base. Register an exception
handler that returns `{"detail": exc.detail}` with the exception status code.

## Acceptance Criteria

- App-specific API errors share a common base class.
- FastAPI returns JSON for `AppAPIError`.
- Feature modules can subclass `AuthError`.
- No feature-specific errors are added yet.

## Teaching Notes

This task prepares for later services like password change, reactivation, and
email changes.

