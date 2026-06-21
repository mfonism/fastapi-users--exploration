# 035: Complete Docs

## Task Metadata

| Field | Value |
|---|---|
| ID | 035 |
| Title | Complete docs |
| Parent epic | E7: API polish and docs |
| Sibling tasks | 034 |
| Blocking tasks | 034 |
| Blocked tasks | None |
| Time estimate | 45-60 minutes |
| Difficulty | Beginner |
| Parallelizable | Yes, branch E |
| Suggested labels | `docs`, `workflow`, `beginner` |
| Suggested commit | `docs: complete local workflow guide` |

## Rich Description

Update the README so a new student can install dependencies, start local
services, bootstrap databases, run migrations, run tests, and make quick API
checks.

## Learning Goal

Students learn that a project is not finished until someone else can run it.

## Files Created Or Modified

- `README.md`

## Exact Implementation Objective

Document prerequisites, optional Docker commands, first-time setup, daily local
workflow, formatting/linting, tests, configuration, database defaults, Alembic
commands, API quick checks, and future improvement ideas.

## Acceptance Criteria

- README lists Python, uv, PostgreSQL, and Redis prerequisites.
- README shows optional local Docker commands.
- README explains `.env` creation.
- README includes `uv sync`, `db-bootstrap`, pytest, and FastAPI dev commands.
- README explains local/test database naming.
- README explains Alembic model registry requirements.
- README includes quick curl checks for health and registration.

## Teaching Notes

Have students follow the README from a clean checkout if time allows. That is
the best documentation test.

