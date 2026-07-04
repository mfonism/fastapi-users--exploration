# EXP-005: Set Up Async Database, Alembic, Commands, And Test Harness

## Linear Metadata

| Field | Value |
|---|---|
| Team | Backend |
| Project | Explore Auth API |
| Issue type | Story |
| Status | Backlog |
| Priority | P1 |
| Estimate | 8 points |
| Level | Senior |
| Parent epic | EPIC-02: Persistence and Test Infrastructure |
| Sibling issues | EXP-006, EXP-007 |
| Blocking issues | EXP-003, EXP-004 |
| Blocked issues | EXP-006, EXP-018 |
| Labels | `backend`, `database`, `migration`, `tests`, `senior-owned` |
| Component | Database infrastructure |
| Target start | TBD |
| Target due | TBD |
| Suggested branch | `feature/exp-005-db-infrastructure` |
| Suggested PR title | `EXP-005 Set up async database infrastructure` |

## Context

Database setup is too concept-heavy for early student work. This senior-owned
ticket creates the infrastructure that later student tickets will use.

The goal is to prove the database plumbing, not to introduce feature
persistence.

## Scope

- Configure typed settings and `.env` file loading.
- Support separate app environments:
  - `local`
  - `local_testing`
  - `staging`
  - `production`
- Configure SQLAlchemy async engine/session helpers.
- Add FastAPI async session dependency.
- Initialize Alembic.
- Connect Alembic to shared SQLAlchemy metadata.
- Add database commands:
  - `db-upgrade`
  - `db-downgrade`
- Add migration guard for empty migrations.
- Add async pytest database fixtures and dependency override pattern.

## Constraints

- Do not turn the user shape from EXP-004 into a SQLAlchemy model.
- Do not add a user table.
- Do not add feature tables.
- Alembic should be wired to shared metadata, but the metadata may be empty for
  now.
- This ticket should prove infrastructure, not domain persistence.

## Non-Goals

- No user persistence model.
- No auth endpoint implementation.
- No Redis setup.
- No password helper fixture yet unless needed by the test harness skeleton.

## Implementation Notes

- `get_async_session` should yield an `AsyncSession`.
- Alembic should import a model registry before reading `Base.metadata`.
- Database URLs should come from settings.
- Test fixtures should set the test environment before importing app modules.
- Use transaction rollback to isolate DB tests.
- Use `httpx.ASGITransport` for API tests if endpoint tests need app calls.

## Acceptance Criteria

- App code can create an async engine from settings.
- App code can create an async session.
- Alembic can run `current` against a prepared database.
- `db-upgrade` and `db-downgrade` commands work.
- Empty Alembic migrations fail the migration guard.
- The async test harness can open and roll back a transaction.
- No application tables are created yet.

## Test Plan

- Run settings tests.
- Run `uv run alembic current` against a prepared local/test database.
- Run `uv run db-upgrade --app-env local_testing`.
- Run `uv run db-downgrade --app-env local_testing --revision -1` only if a
  migration exists.
- Run a minimal async DB fixture smoke test.
- Run the migration guard.

## Docs And Team Notes

- README should explain environment names and database commands.
- If DB command usage becomes repetitive, consider extracting it into a local
  guide or Codex skill later.

## Junior Engineer Guidance

You may not own this ticket, but you should understand the boundary: this sets
up the road. The next ticket drives on it by creating the first real table.
