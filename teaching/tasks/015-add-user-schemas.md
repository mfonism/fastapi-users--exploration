# 015: Add User Schemas

## Task Metadata

| Field | Value |
|---|---|
| ID | 015 |
| Title | Add user schemas |
| Parent epic | E2: User domain model |
| Sibling tasks | 012, 013, 014 |
| Blocking tasks | 014 |
| Blocked tasks | 016 |
| Time estimate | 35-45 minutes |
| Difficulty | Beginner |
| Parallelizable | No |
| Suggested labels | `schemas`, `pydantic`, `api` |
| Suggested commit | `feat: add user API schemas` |

## Rich Description

Define the public request and response schemas for users. These schemas decide
what clients can send and which internal fields are exposed.

## Learning Goal

Students learn that API schemas are contracts and should not blindly mirror the
database model.

## Files Created Or Modified

- `src/explore/auth/users/schemas.py`

## Exact Implementation Objective

Add `UserCreate`, `UserRead`, `CurrentUserRead`, and `CurrentUserUpdate`.
Normalize email on creation and allow only `full_name` in current-user updates.

## Acceptance Criteria

- `UserCreate` requires `email`, `full_name`, `password`, and `terms_accepted_at`.
- Password is marked `writeOnly` in OpenAPI metadata.
- `UserCreate.create_update_dict()` normalizes email.
- `CurrentUserUpdate` forbids unknown fields.
- Response schemas use `from_attributes=True` where ORM objects are returned.

## Teaching Notes

Ask which fields should be visible to the user and which are internal. This
sets up later OpenAPI tests.

