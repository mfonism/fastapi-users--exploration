# EPIC-02: Persistence And Test Infrastructure

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Status | Backlog |
| Priority | P1 |
| Milestone | Foundation |
| Labels | `backend`, `database`, `tests`, `migration` |
| Child issues | EXP-005, EXP-006, EXP-007 |
| Blocking epics | EPIC-01 |
| Blocked epics | EPIC-03 |

## Objective

Provide the async PostgreSQL persistence layer, Alembic migration flow, database
management commands, pytest fixtures, and SQLAlchemy-backed user model
foundation.

## Success Criteria

- Async SQLAlchemy sessions are available through FastAPI dependencies.
- Alembic can generate and apply migrations.
- Local and test databases can be bootstrapped.
- Tests run against isolated database transactions.
- The simple user shape from EPIC-01 is converted into a persisted model.
- User model state behavior is covered by tests.

## Notes For Junior Engineers

The DB infrastructure ticket is senior-owned. Student-facing persistence work
resumes when the user shape is converted into a SQLAlchemy model. Database work
has two parts: Python model code and migration files. Do not merge one without
the other.
