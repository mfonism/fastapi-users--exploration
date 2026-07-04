# EXP-014: Implement Password Reset And Password Change

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P1 |
| Estimate | 5 points |
| Level | Intermediate |
| Parent epic | EPIC-05: Recovery and Reactivation |
| Sibling issues | EXP-015 |
| Blocking issues | EXP-012 |
| Blocked issues | EXP-018 |
| Labels | `backend`, `auth`, `passwords`, `security` |
| Component | Passwords |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-014-password-workflows` |
| Suggested PR title | `EXP-014 Add password reset and change workflows` |

## Context

The service supports two password workflows: public reset through tokens and
authenticated change using the current password.

## Scope

- Ensure generated forgot-password and reset-password routes behave correctly.
- Add custom `POST /auth/change-password`.
- Add password-change schema, service, route, and error.
- Add tests for both workflows.

## Non-Goals

- No password strength policy beyond library behavior.
- No real email provider.
- No account reactivation.

## Implementation Notes

- Password-change route requires current active verified user.
- Wrong current password should return stable error detail.
- Password fields should be write-only in schemas.
- Deleted and deactivated users must not use reset flows.

## Acceptance Criteria

- Forgot-password calls notification placeholder without leaking user existence.
- Valid reset token updates the password hash.
- Reused, expired, and invalid reset tokens are rejected.
- Change-password verifies the current password.
- Wrong current password returns `CHANGE_PASSWORD_BAD_PASSWORD`.
- Successful password change returns 204 with no body.

## Test Plan

- Run forgot-password tests.
- Run reset-password tests.
- Run change-password tests.
- Run OpenAPI password write-only checks after EXP-018.

## Junior Engineer Guidance

Reset-password is for users who cannot log in. Change-password is for users who
are already authenticated.
