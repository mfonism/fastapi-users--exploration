# EXP-017: Implement Email-Change Confirmation Workflow

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P2 |
| Estimate | 8 points |
| Level | Advanced |
| Parent epic | EPIC-06: Email Change Workflow |
| Sibling issues | EXP-016 |
| Blocking issues | EXP-013, EXP-016 |
| Blocked issues | EXP-018 |
| Labels | `backend`, `auth`, `email-change`, `security`, `stretch` |
| Component | Email change |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-017-email-change-confirm` |
| Suggested PR title | `EXP-017 Add email change confirmation workflow` |

## Context

Email-change confirmation is security-sensitive. The service must reject bad
tokens, expired requests, reused requests, cancelled requests, deleted users,
deactivated users, and emails taken during confirmation.

## Scope

- Add confirmation schema.
- Add confirmation service.
- Add confirmation route.
- Update user email and verification timestamp on success.
- Logout matching current session after successful confirmation.
- Add comprehensive endpoint tests.

## Non-Goals

- No email-change request creation changes unless tests reveal a bug.
- No multi-factor verification.
- No real email provider.

## Implementation Notes

- Look up request by token hash.
- Use model `is_usable()` and `confirm()` helpers.
- Check user exists and is active/not deleted.
- Check new email is not taken before update.
- Convert user email unique constraint races into `EMAIL_CHANGE_EMAIL_TAKEN`.
- Optional current-user token should only be logged out when it belongs to the
  same user.

## Acceptance Criteria

- Valid token updates `user.email`.
- Successful confirmation sets `user.verified_at`.
- Unknown, expired, reused, and cancelled tokens fail.
- Deleted and deactivated users fail.
- Taken email cases fail cleanly.
- Matching current session is revoked.
- Unrelated current session remains valid.
- Successful route returns 204 with no body.

## Test Plan

- Run confirm-email-change endpoint tests.
- Run request-email-change tests to ensure no regression.
- Run login/logout tests for session behavior.

## Junior Engineer Guidance

This ticket is intentionally large. If you get stuck, split the work into:
token lookup, usability checks, user checks, update, and session logout.
