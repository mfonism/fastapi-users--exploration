# EXP-004: Define Simple User Shape Without Persistence

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P1 |
| Estimate | 2 points |
| Level | Junior |
| Parent epic | EPIC-01: Foundation and First App Concepts |
| Sibling issues | EXP-001, EXP-002, EXP-003 |
| Blocking issues | EXP-001, EXP-002 |
| Blocked issues | EXP-006 |
| Labels | `backend`, `users`, `schemas`, `junior-friendly` |
| Component | User shape |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-004-user-shape` |
| Suggested PR title | `EXP-004 Define simple user shape` |

## Context

Before persistence exists, students should define what a user looks like in the
application. This introduces a domain concept without also asking them to learn
async SQLAlchemy, UUIDs, PostgreSQL, and Alembic.

## Scope

- Add a simple app-level user shape.
- Include user-facing fields only:
  - `email`
  - `full_name`
- Add tests for valid and invalid user data.

## Non-Goals

- No database.
- No SQLAlchemy.
- No Alembic migration.
- No UUID/id field.
- No username unless the product later decides it needs one.
- No password or authentication behavior.

## Implementation Notes

- A Pydantic model/schema is enough for this stage.
- Use email validation if available in the project dependencies.
- Keep this shape easy to replace or extend when persistence is introduced.

## Acceptance Criteria

- A valid user shape can be created.
- `email` is required and validated.
- `full_name` is required.
- Tests explain the expected shape clearly.

## Test Plan

- Run the user-shape tests.
- Run the existing health endpoint test.

## Docs And Team Notes

- README may mention that the project now has its first domain concept.
- Do not document database setup yet; that arrives in the next ticket.

## Junior Engineer Guidance

This is not the database user model yet. Think of it as answering: "What does
the app mean when it says user?" Persistence comes later.
