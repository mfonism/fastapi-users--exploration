# 007: Initialize Alembic

## Task Metadata

| Field | Value |
|---|---|
| ID | 007 |
| Title | Initialize Alembic |
| Parent epic | E1: Configuration and database infrastructure |
| Sibling tasks | 004, 005, 006, 008, 009, 010, 011 |
| Blocking tasks | 006 |
| Blocked tasks | 008, 009, 012 |
| Time estimate | 45-60 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `database`, `alembic`, `migrations` |
| Suggested commit | `chore: initialize alembic` |

## Rich Description

Set up Alembic so database schema changes can be represented as versioned
migration files.

## Learning Goal

Students learn that model code and actual database schema are connected through
migrations, but they are not the same thing.

## Files Created Or Modified

- `alembic.ini`
- `alembic/env.py`
- `alembic/script.py.mako`
- `alembic/README`
- `src/explore/db/registry.py`

## Exact Implementation Objective

Configure Alembic to read the app database URL from `settings.core_db_url` and
to use `Base.metadata` after importing model registry.

## Acceptance Criteria

- Alembic environment imports `explore.db.registry`.
- `target_metadata` points to `Base.metadata`.
- Online migrations use async SQLAlchemy engine configuration.
- Offline migrations use the rendered app database URL.
- `uv run alembic current` can run against a prepared database.

## Teaching Notes

Emphasize the future rule: every new SQLAlchemy model must be imported in the
registry or autogenerate can miss it.

