# 006: Add DB Session Helpers

## Task Metadata

| Field | Value |
|---|---|
| ID | 006 |
| Title | Add DB session helpers |
| Parent epic | E1: Configuration and database infrastructure |
| Sibling tasks | 004, 005, 007, 008, 009, 010, 011 |
| Blocking tasks | 005 |
| Blocked tasks | 007 |
| Time estimate | 45-60 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `database`, `sqlalchemy`, `async` |
| Suggested commit | `feat: configure async database sessions` |

## Rich Description

Add the async SQLAlchemy foundation: declarative base, engine creation,
sessionmaker creation, and a FastAPI-compatible session dependency.

## Learning Goal

Students learn the difference between engine, sessionmaker, session, and
dependency.

## Files Created Or Modified

- `src/explore/db/__init__.py`
- `src/explore/db/base.py`
- `src/explore/db/config.py`
- `pyproject.toml`
- `uv.lock`

## Exact Implementation Objective

Create `Base`, `create_engine`, `get_engine`, `create_async_session_maker`,
`get_async_session_maker`, and `get_async_session`.

## Acceptance Criteria

- `Base` extends SQLAlchemy `DeclarativeBase`.
- Engine uses `settings.core_db_url`.
- Cached getters avoid recreating engine/sessionmaker repeatedly.
- `get_async_session` yields an `AsyncSession`.
- No feature models are added in this task.

## Teaching Notes

Use a simple diagram: engine connects to DB, sessionmaker creates sessions,
sessions perform work.

