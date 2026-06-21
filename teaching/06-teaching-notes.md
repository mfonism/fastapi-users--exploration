# Teaching Notes

## Setup And Tooling

Explain verbally:

- why the project uses a `src/` package layout
- why uv owns dependency installation and command execution
- why `.env.example` is committed but `.env` is ignored
- how Ruff and pre-commit keep style conversations out of code review

Common beginner mistakes:

- forgetting to run `uv sync`
- committing `.env`
- running `python` directly instead of `uv run python`
- importing app modules before setting `APP_ENV=test` in tests

Checkpoint questions:

- What file makes `explore` importable?
- Where would you add a new dependency?
- Why do we want a health endpoint before auth exists?

Optional stretch:

- add GitHub Actions for `uv sync`, Ruff, and pytest

## Settings And Database

Explain verbally:

- settings are values that can change between environments
- ORM models describe Python objects, migrations describe DB changes
- async sessions are passed through dependencies instead of global variables
- Alembic must import all models before reading `Base.metadata`

Common beginner mistakes:

- hardcoding DB URLs
- forgetting to import new models in `db/registry.py`
- creating a model without a migration
- running tests before bootstrapping the test database

Checkpoint questions:

- What is the test database called when `DB_BASE_NAME=explore`?
- Why does `get_async_session` yield instead of return?
- What is the difference between `Base.metadata` and an Alembic revision file?

Optional stretch:

- add one intentionally broken migration and practice rollback

## User Model And Account State

Explain verbally:

- account state is stored as timestamps, not plain booleans
- computed properties like `is_active` translate timestamps into library-friendly booleans
- setters centralize state-transition timing
- `__repr__` must avoid sensitive data like password hashes

Common beginner mistakes:

- storing raw passwords
- returning internal state fields from public schemas
- changing timestamps directly in route handlers
- confusing deleted, deactivated, and unverified states

Checkpoint questions:

- What does `is_active=False` actually write to the database?
- Why might `deleted_at` be better than deleting the row?
- Which fields should never appear in API responses?

Optional stretch:

- extract repeated timestamp-state patterns into SQLAlchemy mixins

## fastapi-users Integration

Explain verbally:

- `fastapi-users` provides generated routers and manager extension points
- schemas define what the API accepts and returns
- `UserManager` hooks are where app-specific side effects happen
- Redis stores session tokens for logout/revocation

Common beginner mistakes:

- trying to edit library-generated route internals
- not normalizing email before lookup
- forgetting that login requires verified users in this app
- mocking the wrong notification function in tests

Checkpoint questions:

- Which file defines the Redis token lifetime?
- Which method sends verification after registration?
- Why does invalid email during login still hash the submitted password?

Optional stretch:

- add a second auth backend and compare behavior

## Protected Routes

Explain verbally:

- dependencies can enforce authentication before route code runs
- response models protect internal fields
- update schemas should forbid fields users are not allowed to change

Common beginner mistakes:

- trusting request bodies to identify the current user
- allowing users to update `is_superuser` or `deleted_at`
- returning SQLAlchemy objects without response-model thought

Checkpoint questions:

- Why does `/users/me` not accept a user ID?
- What happens if a deleted user presents a still-valid token?
- Where is `full_name` update validation enforced?

Optional stretch:

- add an admin-only route and compare current-user dependencies

## Password And Recovery Workflows

Explain verbally:

- password reset is public but token-protected
- password change is authenticated and current-password-protected
- generated router flows and custom route flows can coexist

Common beginner mistakes:

- leaking whether an email exists
- forgetting `writeOnly` on password fields
- updating a password without verifying the old one

Checkpoint questions:

- Why does change-password require authentication but reset-password does not?
- What response should the API return for an accepted empty command?
- Where is the password hash created?

Optional stretch:

- add password strength validation and tests

## Reactivation And Email Change

Explain verbally:

- reactivation tokens include state so old tokens become stale
- email-change tokens are stored hashed, not raw
- request endpoints should avoid user enumeration
- confirmation endpoints need expiry, cancellation, reuse, and race checks

Common beginner mistakes:

- storing raw confirmation tokens
- forgetting expiry checks
- not cancelling older email-change requests
- confirming email change for deleted or inactive users

Checkpoint questions:

- Why does a reactivation token include `deactivated_at`?
- What makes an email-change token unusable?
- Why should requesting reactivation always return 202?

Optional stretch:

- wire a real email provider behind `notifications.py`

## Tests

Explain verbally:

- unit-like model tests are faster and simpler than endpoint tests
- endpoint tests exercise dependency wiring and response contracts
- the async client can call the app in-process
- transaction fixtures isolate database state between tests

Common beginner mistakes:

- not awaiting async client calls
- forgetting to flush before reading generated IDs
- sharing mutable client headers across tests unintentionally
- not clearing dependency overrides

Checkpoint questions:

- Which fixture creates an authenticated request?
- Why do tests patch notification functions?
- What does the nested transaction fixture protect?

Optional stretch:

- add coverage measurement and require coverage for new tasks

