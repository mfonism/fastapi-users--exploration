# EXP-015: Implement Account Reactivation Workflow

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
| Parent epic | EPIC-05: Recovery and Reactivation |
| Sibling issues | EXP-014 |
| Blocking issues | EXP-013 |
| Blocked issues | EXP-018 |
| Labels | `backend`, `auth`, `reactivation`, `security` |
| Component | Reactivation |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-015-reactivation` |
| Suggested PR title | `EXP-015 Add account reactivation workflow` |

## Context

Deactivated users need a recovery path that does not reveal whether an email
belongs to an account and does not allow stale tokens.

## Scope

- Add reactivation request schema and confirm schema.
- Add reactivation token service.
- Add reactivation routes.
- Add notification placeholder.
- Add tests for request and confirmation flows.

## Non-Goals

- No password reset changes unless needed for deactivated-user behavior.
- No real email provider.

## Implementation Notes

- Token should include user ID, `deactivated_at`, and a dedicated audience.
- Confirm should reject tokens if the user's current `deactivated_at` no longer
  matches the token.
- Request endpoint should return 202 for unknown, active, deleted, and eligible
  users to avoid account enumeration.

## Acceptance Criteria

- Eligible deactivated users receive reactivation notification.
- Unknown, active, and deleted users do not leak state.
- Valid token clears `deactivated_at`.
- Invalid, expired, reused, stale, active-user, and deleted-user tokens fail.
- Request route returns 202 with no body.
- Confirm route returns 204 with no body.

## Test Plan

- Run request-reactivation tests.
- Run confirm-reactivation tests.
- Run login tests to confirm reactivated users can authenticate when verified.

## Junior Engineer Guidance

The `deactivated_at` claim is what makes old tokens stale. Do not remove it
unless the product decision changes.
