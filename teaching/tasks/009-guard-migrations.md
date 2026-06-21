# 009: Guard Migrations

## Task Metadata

| Field | Value |
|---|---|
| ID | 009 |
| Title | Guard migrations |
| Parent epic | E1: Configuration and database infrastructure |
| Sibling tasks | 004, 005, 006, 007, 008, 010, 011 |
| Blocking tasks | 003, 007 |
| Blocked tasks | None |
| Time estimate | 30-45 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `tooling`, `alembic`, `quality` |
| Suggested commit | `chore: guard against empty migrations` |

## Rich Description

Add a small static check that fails when an Alembic migration has no operation
inside `upgrade()` or `downgrade()`.

## Learning Goal

Students learn that tooling can encode project-specific safety rules.

## Files Created Or Modified

- `scripts/check_empty_migrations.py`
- `.pre-commit-config.yaml`

## Exact Implementation Objective

Parse migration files with `ast` and detect whether `op.<operation>()` calls
exist inside both migration functions.

## Acceptance Criteria

- The script exits 0 when migrations contain Alembic operations.
- The script exits 1 and prints useful failures when a migration is empty.
- Pre-commit runs the script before Ruff hooks.
- The implementation uses Python AST parsing, not fragile text matching.

## Teaching Notes

This is a nice stretch example of using the standard library to inspect code.

