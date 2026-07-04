# EXP-016: Implement Email-Change Request Workflow

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P2 |
| Estimate | 5 points |
| Level | Intermediate |
| Parent epic | EPIC-06: Email Change Workflow |
| Sibling issues | EXP-017 |
| Blocking issues | EXP-012 |
| Blocked issues | EXP-017 |
| Labels | `backend`, `auth`, `email-change`, `database` |
| Component | Email change |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-016-email-change-request` |
| Suggested PR title | `EXP-016 Add email change request workflow` |

## Context

Changing an email address requires a pending request, a confirmation token, and
validation that the new email is allowed.

## Scope

- Add `UserEmailChange` model and migration.
- Add token generation and hash helpers.
- Add request service.
- Add request route.
- Add notification placeholder.
- Add model and request endpoint tests.

## Non-Goals

- No confirmation route yet.
- No real email provider.
- No session invalidation yet.

## Implementation Notes

- Store token hashes, not raw tokens.
- Cancel unresolved previous requests for the same user.
- Reject same email and already-used email.
- Normalize new email before comparison and storage.

## Acceptance Criteria

- Email-change table is created by migration.
- Token helper returns random raw tokens.
- Hash helper is deterministic and does not expose raw token.
- Request creates pending email-change row with expiry.
- Same-email and taken-email cases return stable errors.
- Notification receives raw token and new email address.

## Test Plan

- Run email-change model tests.
- Run request-email-change endpoint tests.
- Run Alembic upgrade for the new table.

## Junior Engineer Guidance

Think of this ticket as "create a pending request." Do not update the user's
email until the confirmation ticket.
