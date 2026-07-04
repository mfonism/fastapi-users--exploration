# EXP-008: Implement User Schemas And FastAPI Users Manager

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
| Sibling issues | EXP-009, EXP-010, EXP-011 |
| Blocking issues | EXP-007 |
| Blocked issues | EXP-009 |
| Labels | `backend`, `auth`, `schemas`, `security` |
| Component | Auth manager |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-008-user-manager` |
| Suggested PR title | `EXP-008 Add user schemas and manager hooks` |

## Context

`fastapi-users` needs app-specific schemas and a user manager to connect the
SQLAlchemy model with auth library behavior.

## Scope

- Add user create/read/current-user/update schemas.
- Normalize emails during user creation and lookup.
- Add `UserManager`.
- Add notification placeholders.
- Reject deleted users from sensitive manager flows.
- Add login hook to track `last_login_at`.

## Non-Goals

- No Redis backend.
- No routes wired yet.
- No real email provider.

## Implementation Notes

- Password fields should be marked `writeOnly`.
- Current-user update schema should forbid unknown fields.
- Manager secrets should come from settings.
- Invalid email login should not leak timing behavior.

## Acceptance Criteria

- Schemas expose only intended fields.
- Email normalization applies on create and lookup.
- Manager integrates with `SQLAlchemyUserDatabase`.
- Registration requests verification.
- Password reset and verification notification hooks call placeholders.
- Deleted users are rejected consistently.

## Test Plan

- Unit test schema normalization if useful.
- Manager behavior will be covered in downstream endpoint tests.
- Run Ruff.

## Junior Engineer Guidance

Read `fastapi-users` examples for manager hooks, but keep app-specific decisions
inside this project's manager.
