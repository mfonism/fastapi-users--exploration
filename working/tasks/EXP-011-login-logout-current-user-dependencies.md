# EXP-011: Build Login, Logout, And Current-User Dependencies

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
| Parent epic | EPIC-03: Core Authentication |
| Sibling issues | EXP-008, EXP-009, EXP-010 |
| Blocking issues | EXP-010 |
| Blocked issues | EXP-012 |
| Labels | `backend`, `auth`, `redis`, `tests` |
| Component | Sessions |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-011-login-logout-deps` |
| Suggested PR title | `EXP-011 Add login logout and current-user dependencies` |

## Context

The app needs a complete session lifecycle and reusable dependencies for
authenticated routes.

## Scope

- Add login/logout router composition.
- Require verified users for login.
- Set logout to return 204.
- Update `last_login_at` after successful login.
- Add current-user and current-user-token dependencies.
- Add optional current-user-token dependency for confirmation flows.

## Non-Goals

- No `/users/me` route yet.
- No profile update, delete, or deactivate route.

## Implementation Notes

- Deleted users must not be able to authenticate.
- Optional current-user-token dependency should return `None` for missing,
  invalid, or deleted users.
- Tests should confirm token revocation after logout.

## Acceptance Criteria

- Verified active users can log in.
- Unverified, deactivated, deleted, invalid-email, and bad-password login cases fail.
- Logout revokes the current token.
- Logout returns 204 with no body.
- `last_login_at` updates on successful login.
- Dependencies reject deleted users.

## Test Plan

- Run login tests.
- Run logout tests.
- Run dependency-covered endpoint tests after EXP-012 lands.

## Junior Engineer Guidance

Think of token auth as three steps: create token on login, attach token to
requests, remove token on logout.
