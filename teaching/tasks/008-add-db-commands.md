# 008: Add DB Commands

## Task Metadata

| Field | Value |
|---|---|
| ID | 008 |
| Title | Add DB commands |
| Parent epic | E1: Configuration and database infrastructure |
| Sibling tasks | 004, 005, 006, 007, 009, 010, 011 |
| Blocking tasks | 007 |
| Blocked tasks | None |
| Time estimate | 60-90 minutes |
| Difficulty | Stretch |
| Parallelizable | No |
| Suggested labels | `database`, `cli`, `stretch` |
| Suggested commit | `chore: add database management commands` |

## Rich Description

Add command-line helpers to create and migrate the local and test databases.
This makes setup repeatable for students and avoids manual Alembic command
sequences.

## Learning Goal

Students learn how project scripts can wrap common operational tasks.

## Files Created Or Modified

- `src/explore/db/bootstrap.py`
- `src/explore/db/migrate.py`
- `src/explore/console.py`
- `src/explore/db/config.py`
- `pyproject.toml`

## Exact Implementation Objective

Expose `db-bootstrap`, `db-upgrade`, and `db-downgrade` project scripts. The
bootstrap command should prepare local and test DBs by default, with an
`--app-env` option for selecting one or more environments.

## Acceptance Criteria

- `uv run db-bootstrap` targets local and test DBs by default.
- `uv run db-bootstrap --app-env test` targets only the test DB.
- `uv run db-upgrade` applies Alembic migrations.
- `uv run db-downgrade --revision -1` can downgrade.
- Commands reload settings after changing `APP_ENV`.

## Teaching Notes

This is useful but operationally dense. In a beginner workshop, provide this as
starter code and explain only the command surface.

