# EXP-013: Implement Deactivation And Soft Deletion

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
| Parent epic | EPIC-04: Account Self-Service |
| Sibling issues | EXP-012 |
| Blocking issues | EXP-012 |
| Blocked issues | EXP-015, EXP-017 |
| Labels | `backend`, `auth`, `users`, `security` |
| Component | Account lifecycle |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-013-account-lifecycle` |
| Suggested PR title | `EXP-013 Add deactivation and soft deletion` |

## Context

Users need account lifecycle controls. Deactivation blocks access while allowing
reactivation. Soft deletion marks an account deleted and revokes the current
session while preserving the database row.

## Scope

- Add `POST /auth/deactivate`.
- Add `DELETE /users/me`.
- Ensure deleted users are rejected from auth flows.
- Revoke current token after soft deletion.
- Add endpoint tests.

## Non-Goals

- No reactivation flow.
- No hard deletion.
- No admin account management.

## Implementation Notes

- Deactivation should set `is_active=False`.
- Soft deletion should set `is_deleted=True`.
- Soft deletion should logout the current token.
- Deleted-user login should map to bad credentials behavior.

## Acceptance Criteria

- Deactivated users cannot access protected endpoints.
- Deleted users cannot login or use protected endpoints.
- Delete endpoint returns 204 with no body.
- Deactivate endpoint returns 204 with no body.
- Current token is revoked after soft deletion.
- Tests cover deleted-user behavior in manager/dependencies.

## Test Plan

- Run deactivate tests.
- Run delete-current-user tests.
- Run login tests for deleted/deactivated users.
- Run verification/reset tests touched by deleted-user checks.

## Junior Engineer Guidance

Do not confuse deactivation and deletion. Deactivation is reversible.
Soft deletion is treated as final by auth flows in this app.
