# EPIC-04: Account Self-Service

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Status | Backlog |
| Priority | P1 |
| Milestone | Account Management |
| Labels | `backend`, `users`, `auth` |
| Child issues | EXP-012, EXP-013 |
| Blocking epics | EPIC-03 |
| Blocked epics | EPIC-05, EPIC-06 |

## Objective

Allow authenticated users to inspect and manage their own account without
exposing privileged or internal fields.

## Success Criteria

- `/users/me` returns the authenticated user.
- Users can update allowed profile fields.
- Users can deactivate accounts.
- Users can soft delete accounts.
- Deactivated and deleted users lose access appropriately.

## Notes For Junior Engineers

Never trust a request body to identify the user. These routes should operate on
the authenticated user from dependencies.

