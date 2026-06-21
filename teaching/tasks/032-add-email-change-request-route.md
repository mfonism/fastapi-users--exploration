# 032: Add Email-Change Request Route

## Task Metadata

| Field | Value |
|---|---|
| ID | 032 |
| Title | Add email-change request route |
| Parent epic | E6: Email-change workflow |
| Sibling tasks | 030, 031, 033 |
| Blocking tasks | 022, 031 |
| Blocked tasks | 033 |
| Time estimate | 45-60 minutes |
| Difficulty | Beginner |
| Parallelizable | Yes, branch D |
| Suggested labels | `routes`, `email-change`, `auth` |
| Suggested commit | `feat: add email change request endpoint` |

## Rich Description

Expose the email-change request service as an authenticated endpoint and send
the raw token through the notification placeholder.

## Learning Goal

Students learn how to combine authenticated dependencies, service calls, and
side-effect placeholders in a route.

## Files Created Or Modified

- `src/explore/auth/email_changes/schemas.py`
- `src/explore/auth/email_changes/routes.py`
- `src/explore/auth/routes.py`
- `src/explore/auth/notifications.py`
- `tests/auth/views/test_request_email_change.py`

## Exact Implementation Objective

Create `POST /auth/request-email-change` with `EmailChangeRequest`, current-user
dependency, DB session dependency, and notification call.

## Acceptance Criteria

- Authenticated users can request a new email.
- Request stores a `UserEmailChange` row.
- Notification receives new email, current user's name, and raw token.
- Same-email and taken-email cases return stable error details.
- Older unresolved requests are cancelled.
- Response status is 204 with no body.

## Teaching Notes

Ask students why the notification is sent to the new email, not the old email.

