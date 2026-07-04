# EPIC-03: Core Authentication

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Status | Backlog |
| Priority | P1 |
| Milestone | Core Auth |
| Labels | `backend`, `auth`, `security` |
| Child issues | EXP-008, EXP-009, EXP-010, EXP-011 |
| Blocking epics | EPIC-02 |
| Blocked epics | EPIC-04 |

## Objective

Integrate `fastapi-users` with the local user model, Redis-backed bearer tokens,
registration, verification, login, logout, and current-user dependencies.

## Success Criteria

- Registration creates users with hashed passwords.
- Verification tokens can be requested and confirmed.
- Only verified active users can log in.
- Logout revokes Redis-backed tokens.
- Deleted users are consistently rejected.

## Notes For Junior Engineers

Most auth behavior comes from `fastapi-users`. Local code customizes it through
schemas, the user manager, dependencies, and the Redis backend.

