# 012: Create User Model

## Task Metadata

| Field | Value |
|---|---|
| ID | 012 |
| Title | Create user model |
| Parent epic | E2: User domain model |
| Sibling tasks | 013, 014, 015 |
| Blocking tasks | 007 |
| Blocked tasks | 013, 014 |
| Time estimate | 45-60 minutes |
| Difficulty | Intermediate |
| Parallelizable | No |
| Suggested labels | `model`, `database`, `migration` |
| Suggested commit | `feat: add user model and initial migration` |

## Rich Description

Create the first application table: users. Start with the core identity and
authentication fields needed by `fastapi-users`.

## Learning Goal

Students learn how a SQLAlchemy model maps to a database table and why the
password field stores a hash instead of the raw password.

## Files Created Or Modified

- `src/explore/auth/__init__.py`
- `src/explore/auth/users/__init__.py`
- `src/explore/auth/users/models.py`
- `src/explore/db/registry.py`
- `alembic/versions/<revision>_initial_schema.py`

## Exact Implementation Objective

Define a `User` SQLAlchemy model with UUID primary key, unique indexed email,
full name, hashed password, and initial audit timestamps.

## Acceptance Criteria

- `User.__tablename__` is `"user"`.
- Email is unique, indexed, and limited to 320 characters.
- `hashed_password` is present and not nullable.
- The model is imported in `db/registry.py`.
- An Alembic migration creates the table and email index.

## Teaching Notes

Before writing the migration, ask students what would happen if the model file
existed but the database table did not.

