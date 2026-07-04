# Task Index

These task files are written for a professional task-management tool such as
Linear, but the order is intentionally student-friendly. The roadmap introduces
one idea at a time, keeps senior-heavy infrastructure isolated, and uses later
tickets to fold in work that would be too much too early.

## Tasks

| ID | Title | Epic | Level | Priority | Estimate | Blocks |
|---|---|---|---|---|---:|---|
| EXP-001 | Initialize packaged project | EPIC-01 | Junior | P1 | 1 | EXP-002, EXP-003, EXP-004 |
| EXP-002 | Add health endpoint and first test | EPIC-01 | Junior | P1 | 2 | EXP-003, EXP-004 |
| EXP-003 | Configure Python tooling and local developer workflow | EPIC-01 | Junior | P1 | 2 | EXP-005, EXP-018 |
| EXP-004 | Define simple user shape without persistence | EPIC-01 | Junior | P1 | 2 | EXP-006 |
| EXP-005 | Set up async database, Alembic, commands, and test harness | EPIC-02 | Senior | P1 | 8 | EXP-006, EXP-018 |
| EXP-006 | Persist users with SQLAlchemy and migrations | EPIC-02 | Intermediate | P1 | 5 | EXP-007 |
| EXP-007 | Add user account-state behavior and factories | EPIC-02 | Junior | P1 | 3 | EXP-008 |
| EXP-008 | Implement user schemas and FastAPI Users manager | EPIC-03 | Intermediate | P1 | 5 | EXP-009 |
| EXP-009 | Configure Redis auth backend and generated auth routers | EPIC-03 | Intermediate | P1 | 5 | EXP-010 |
| EXP-010 | Build registration and verification flows | EPIC-03 | Intermediate | P1 | 5 | EXP-011 |
| EXP-011 | Build login, logout, and current-user dependencies | EPIC-03 | Intermediate | P1 | 5 | EXP-012 |
| EXP-012 | Implement current-user profile endpoints | EPIC-04 | Junior | P1 | 3 | EXP-013, EXP-014 |
| EXP-013 | Implement deactivation and soft deletion | EPIC-04 | Intermediate | P1 | 5 | EXP-015, EXP-017 |
| EXP-014 | Implement password reset and password change | EPIC-05 | Intermediate | P1 | 5 | EXP-018 |
| EXP-015 | Implement account reactivation workflow | EPIC-05 | Intermediate | P2 | 5 | EXP-018 |
| EXP-016 | Implement email-change request workflow | EPIC-06 | Intermediate | P2 | 5 | EXP-017 |
| EXP-017 | Implement email-change confirmation workflow | EPIC-06 | Advanced | P2 | 8 | EXP-018 |
| EXP-018 | Finalize OpenAPI contract, README, and release checks | EPIC-07 | Junior | P1 | 3 | None |

## Import Notes

Each task file contains:

- Linear metadata
- context
- scope
- non-goals
- implementation notes
- acceptance criteria
- test plan
- rollout/docs notes
- junior engineer guidance

## Deferred Work Tracking

When a ticket intentionally avoids something, that work should appear in a
future ticket. Examples:

- `EXP-004` defines the user shape but does not persist it; `EXP-006` handles
  persistence.
- `EXP-005` wires empty Alembic metadata but does not create feature tables;
  `EXP-006` creates the user table.
- Auth-specific password and token behavior waits until EPIC-03.
