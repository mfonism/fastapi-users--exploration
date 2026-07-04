# EXP-006: Persist Users With SQLAlchemy And Migrations

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
| Parent epic | EPIC-02: Persistence and Test Infrastructure |
| Sibling issues | EXP-005, EXP-007 |
| Blocking issues | EXP-004, EXP-005 |
| Blocked issues | EXP-007 |
| Labels | `backend`, `database`, `auth`, `migration`, `junior-friendly` |
| Component | User model |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-006-user-persistence` |
| Suggested PR title | `EXP-006 Persist users with SQLAlchemy` |

## Context

The app already has a simple user shape and database infrastructure. This task
connects those ideas by creating the first persisted domain model.

## Scope

- Convert the simple user shape into a SQLAlchemy `User` model.
- Add the user table fields needed by the target auth system.
- Register the model for Alembic discovery.
- Add a migration for the user table.
- Add tests that insert and fetch users through the async session.

## User Table Shape

| Group | Field | Type | Notes |
|---|---|---|---|
| Identity | `id` | UUID | Primary key; use the project UUID strategy. |
| Identity | `email` | string | Required, unique, indexed, normalized before storage. |
| Profile | `full_name` | string | Required. |
| Auth | `hashed_password` | string | Required once auth creation exists; never store raw passwords. |
| Verification | `email_verified_at` | timestamp with timezone, nullable | Drives `is_verified` later. |
| Activity | `deactivated_at` | timestamp with timezone, nullable | Drives `is_active` later. |
| Deletion | `deleted_at` | timestamp with timezone, nullable | Drives `is_deleted` later. |
| Privilege | `superuser_granted_at` | timestamp with timezone, nullable | Drives `is_superuser` later. |
| Compliance | `terms_accepted_at` | timestamp with timezone | Required for registration. |
| Login audit | `last_login_at` | timestamp with timezone, nullable | Updated by login hook later. |
| Audit | `created_at` | timestamp with timezone | Set on creation. |
| Audit | `updated_at` | timestamp with timezone | Updated on row change. |

## Non-Goals

- No HTTP routes.
- No `fastapi-users` manager yet.
- No Redis backend.
- No email-change table yet.
- No account-state property behavior beyond what is needed for mapping columns.

## Implementation Notes

- Email uniqueness must be enforced by the database.
- Store `hashed_password`, never raw passwords.
- Keep migrations reviewable and ordered.
- If the model registry misses this model, Alembic autogenerate may miss the
  table.

## Acceptance Criteria

- `user` table can be created by Alembic.
- User model imports in the model registry.
- Email uniqueness is enforced.
- Required fields are non-null where appropriate.
- Migration includes downgrade behavior.
- An async test can insert and fetch a user.

## Test Plan

- Run Alembic upgrade against the test database.
- Run model import smoke test.
- Run async insert/fetch tests.
- Run Ruff.

## Docs And Team Notes

- README should mention the first real migration workflow.
- If migration review conventions emerge, consider adding them to `AGENTS.md`.

## Junior Engineer Guidance

This is the first moment where Python model code and database schema must agree.
If you change one without the other, the app and database drift apart.
