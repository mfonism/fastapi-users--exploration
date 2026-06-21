# 005: Add Settings

## Task Metadata

| Field | Value |
|---|---|
| ID | 005 |
| Title | Add settings |
| Parent epic | E1: Configuration and database infrastructure |
| Sibling tasks | 004, 006, 007, 008, 009, 010, 011 |
| Blocking tasks | 004 |
| Blocked tasks | 006, 010 |
| Time estimate | 40-50 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `config`, `pydantic`, `tests` |
| Suggested commit | `feat: load settings from environment` |

## Rich Description

Add typed settings with defaults for local development and clear environment
variables for database, Redis, and auth secrets.

## Learning Goal

Students learn how environment variables become typed Python values and how
derived settings reduce repeated logic.

## Files Created Or Modified

- `src/explore/settings.py`
- `.env.example`
- `tests/test_settings.py`
- `pyproject.toml`
- `uv.lock`

## Exact Implementation Objective

Use `pydantic-settings` to create `Settings`, load env files based on `APP_ENV`,
derive local/test database names, and derive Redis key prefixes.

## Acceptance Criteria

- `.env.example` documents all supported values.
- `Settings(app_env=AppEnv.TEST).database_name` ends with `_test`.
- `debug` defaults to true for local/test and false otherwise.
- Boolean-like strings such as `true`, `false`, `on`, and `off` parse correctly.
- Tests cover `db_echo` and debug defaults.

## Teaching Notes

Make a table on the board: input env var, Python field, derived property, final
consumer.

