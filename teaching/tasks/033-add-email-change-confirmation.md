# 033: Add Email-Change Confirmation

## Task Metadata

| Field | Value |
|---|---|
| ID | 033 |
| Title | Add email-change confirmation |
| Parent epic | E6: Email-change workflow |
| Sibling tasks | 030, 031, 032 |
| Blocking tasks | 025, 032 |
| Blocked tasks | 034 |
| Time estimate | 90-120 minutes |
| Difficulty | Stretch |
| Parallelizable | Yes, branch D |
| Suggested labels | `email-change`, `tokens`, `stretch` |
| Suggested commit | `feat: confirm email changes` |

## Rich Description

Complete the email-change workflow. Confirmation should validate a token,
reject unusable states, update the user's email, mark the change confirmed, and
logout the matching current session if the user is authenticated.

## Learning Goal

Students learn how confirmation flows handle expiry, reuse, cancellation,
authorization edge cases, and database uniqueness races.

## Files Created Or Modified

- `src/explore/auth/email_changes/service.py`
- `src/explore/auth/email_changes/routes.py`
- `src/explore/auth/email_changes/schemas.py`
- `tests/auth/views/test_confirm_email_change.py`

## Exact Implementation Objective

Create `confirm_email_change` service logic and
`POST /auth/confirm-email-change` route.

## Acceptance Criteria

- Unknown tokens raise `EMAIL_CHANGE_BAD_TOKEN`.
- Expired, reused, and cancelled tokens are rejected.
- Deleted or deactivated users cannot confirm changes.
- Taken emails are rejected before update.
- DB uniqueness violations during update become `EMAIL_CHANGE_EMAIL_TAKEN`.
- Successful confirmation updates `user.email`.
- Successful confirmation sets `user.verified_at` to confirmation time.
- Matching current session is logged out.
- Unrelated current sessions remain valid.

## Teaching Notes

This is the most complex feature. Split it into model lookup, usability checks,
user checks, update, and session logout.

