# EXP-012: Implement Current-User Profile Endpoints

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P1 |
| Estimate | 3 points |
| Level | Junior |
| Parent epic | EPIC-04: Account Self-Service |
| Sibling issues | EXP-013 |
| Blocking issues | EXP-011 |
| Blocked issues | EXP-013, EXP-014 |
| Labels | `backend`, `api`, `users`, `junior-friendly` |
| Component | Users |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-012-current-user-profile` |
| Suggested PR title | `EXP-012 Add current-user profile endpoints` |

## Context

Authenticated users need to read their own public profile and update allowed
profile fields.

## Scope

- Add `GET /users/me`.
- Add `PATCH /users/me`.
- Add response schema for current user.
- Add update schema that only allows `full_name`.
- Add endpoint tests.

## Non-Goals

- No admin user lookup.
- No email change in this ticket.
- No account deletion or deactivation.

## Implementation Notes

- Use current-user dependency; never accept a user ID in the path.
- Use response models to hide internal fields.
- Forbid unknown update fields.

## Acceptance Criteria

- Unauthenticated requests to `/users/me` return 401.
- Authenticated users receive their public current-user payload.
- Users can update `full_name`.
- Attempts to update account-state fields are rejected.
- Internal fields are not returned.

## Test Plan

- Run current-user tests.
- Run profile update tests.
- Confirm OpenAPI shows expected schemas.

## Junior Engineer Guidance

The current user comes from the token, not from the request body. This is an
important authorization rule.
