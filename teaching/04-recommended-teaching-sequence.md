# Recommended Teaching Sequence

This sequence rebuilds the project from zero. Each task is small enough to map
to one tutorial commit or one task-management card.

Detailed task cards live in [tasks](tasks).

## Full Sequence

| # | Title | Learning Goal | Files Created/Modified | Objective | Commit | Difficulty | Depends | Parallel |
|---:|---|---|---|---|---|---|---|---|
| 1 | Scaffold project | Python package layout | `.python-version`, `.gitignore`, `pyproject.toml`, `README.md`, `src/explore/__init__.py` | Create uv project metadata and importable package. | `chore: scaffold python package` | beginner | none | no |
| 2 | Add FastAPI health app | Minimal API | `src/explore/app.py`, `pyproject.toml`, `uv.lock` | Install FastAPI, create app, add `/health`. | `feat: add FastAPI health endpoint` | beginner | 1 | no |
| 3 | Add lint/format tooling | Quality loop | `pyproject.toml`, `.pre-commit-config.yaml` | Configure Ruff and pre-commit. | `chore: configure ruff and pre-commit` | beginner | 1 | no |
| 4 | Add environment model | Config basics | `src/explore/env.py` | Define environments, aliases, env-file resolution. | `feat: add app environment helpers` | beginner | 1 | no |
| 5 | Add settings | Pydantic settings | `src/explore/settings.py`, `.env.example`, `tests/test_settings.py` | Load DB, Redis, secrets, debug flags. | `feat: load settings from environment` | beginner | 4 | no |
| 6 | Add DB session helpers | Async SQLAlchemy | `src/explore/db/base.py`, `src/explore/db/config.py` | Create async engine/sessionmaker. | `feat: configure async database sessions` | intermediate | 5 | no |
| 7 | Initialize Alembic | Migrations | `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`, `src/explore/db/registry.py` | Connect Alembic to settings and metadata. | `chore: initialize alembic` | intermediate | 6 | no |
| 8 | Add DB commands | Developer workflow | `src/explore/db/bootstrap.py`, `src/explore/db/migrate.py`, `src/explore/console.py`, `pyproject.toml` | Add bootstrap, upgrade, downgrade commands. | `chore: add database management commands` | stretch | 7 | no |
| 9 | Guard migrations | Tooling safety | `scripts/check_empty_migrations.py`, `.pre-commit-config.yaml` | Fail on empty Alembic revisions. | `chore: guard against empty migrations` | intermediate | 7 | no |
| 10 | Add utilities | Shared helpers | `src/explore/utils/email.py`, `src/explore/utils/clock.py`, `tests/utils/test_email.py` | Normalize emails and centralize UTC time. | `feat: add email and clock utilities` | beginner | 5 | no |
| 11 | Add app errors | Error handling | `src/explore/exceptions.py`, `src/explore/auth/exceptions.py`, `src/explore/app.py` | Map app errors to JSON responses. | `feat: add API error handling` | beginner | 2 | no |
| 12 | Create user model | ORM modeling | `src/explore/auth/users/models.py`, `src/explore/db/registry.py`, first migration | Add base user table. | `feat: add user model and initial migration` | intermediate | 7 | no |
| 13 | Add user factories | Test data | `tests/factories/user.py`, `tests/factories/test_user.py` | Create reusable user builders. | `test: add user factories` | beginner | 12 | no |
| 14 | Add account-state fields | Domain modeling | `users/models.py`, migrations, `tests/auth/models/test_user.py` | Add timestamps and computed state properties. | `feat: model user account states` | intermediate | 10, 12 | no |
| 15 | Add user schemas | API contracts | `auth/users/schemas.py` | Define create/read/update schemas. | `feat: add user API schemas` | beginner | 14 | no |
| 16 | Add user manager | Library integration | `auth/users/manager.py`, `auth/notifications.py` | Connect SQLAlchemy user DB and manager hooks. | `feat: add user manager` | intermediate | 11, 15 | no |
| 17 | Add Redis auth backend | Token strategy | `auth/backends/redis.py`, `settings.py`, `.env.example` | Configure bearer transport and Redis strategy. | `feat: add Redis auth backend` | intermediate | 16 | no |
| 18 | Wire generated auth routers | Router composition | `auth/routes.py`, `app.py` | Add register, reset-password, verify routers. | `feat: wire generated auth routers` | intermediate | 17 | no |
| 19 | Test registration | Full feature test | `tests/auth/views/test_register.py` | Verify registration behavior and validation. | `test: cover user registration` | beginner | 13, 18 | no |
| 20 | Add verification flow | Token workflow | `manager.py`, `auth/routes.py`, verification tests | Request and confirm email verification. | `feat: add email verification workflow` | intermediate | 18, 19 | no |
| 21 | Add login/logout | Auth session lifecycle | `auth/sessions/routes.py`, `manager.py`, login/logout tests | Login verified users, revoke tokens, track login time. | `feat: add verified login and logout` | intermediate | 20 | no |
| 22 | Add current-user endpoint | Protected routes | `auth/dependencies.py`, `users/routes.py`, current-user tests | Implement authenticated `/users/me`. | `feat: add current user endpoint` | beginner | 21 | no |
| 23 | Add profile update | Request validation | `users/schemas.py`, `users/routes.py`, patch tests | Allow `full_name` updates only. | `feat: add current user profile updates` | beginner | 22 | yes |
| 24 | Add deactivation | Account lifecycle | `users/routes.py`, `models.py`, deactivate tests | Mark current user inactive. | `feat: add account deactivation` | beginner | 22 | yes |
| 25 | Add soft delete | Authorization edge cases | `users/routes.py`, `dependencies.py`, `manager.py`, `app.py`, delete tests | Soft delete user and revoke current session. | `feat: add soft deletion` | intermediate | 22 | yes |
| 26 | Add password reset | Generated flow customization | `manager.py`, `auth/routes.py`, password reset tests | Send and confirm reset-password tokens. | `feat: add password reset workflow` | intermediate | 21, 24, 25 | yes |
| 27 | Add change password | Custom command endpoint | `passwords/*`, change-password tests | Verify current password and set a new one. | `feat: add password change endpoint` | beginner | 22 | yes |
| 28 | Add reactivation service | JWT business rules | `reactivation/schemas.py`, `exceptions.py`, `service.py` | Generate and validate reactivation tokens. | `feat: add reactivation token service` | stretch | 24 | yes |
| 29 | Add reactivation routes | Public recovery flow | `reactivation/routes.py`, `auth/routes.py`, reactivation tests | Request and confirm reactivation. | `feat: add account reactivation endpoints` | intermediate | 25, 28 | yes |
| 30 | Add email-change model | Secondary resource | `email_changes/models.py`, migration, model tests | Store email-change token state. | `feat: add email change model` | intermediate | 14 | yes |
| 31 | Add email-change request service | Service-layer rules | `email_changes/service.py`, `exceptions.py` | Create request token and reject invalid new emails. | `feat: request email changes` | intermediate | 30 | yes |
| 32 | Add email-change request route | Authenticated command | `email_changes/routes.py`, `schemas.py`, request tests | Authenticated user requests new email. | `feat: add email change request endpoint` | beginner | 22, 31 | yes |
| 33 | Add email-change confirmation | Token confirmation | `email_changes/service.py`, `routes.py`, confirmation tests | Confirm token and update email safely. | `feat: confirm email changes` | stretch | 25, 32 | yes |
| 34 | Polish OpenAPI | API documentation | `tests/auth/views/test_openapi.py`, schemas/routes | Assert write-only password fields and empty responses. | `test: document auth OpenAPI responses` | beginner | 18, 27, 29, 33 | yes |
| 35 | Complete docs | Workshop runbook | `README.md` | Document setup, workflow, commands, and future plans. | `docs: complete local workflow guide` | beginner | all | yes |

## Suggested Commit Style

Use conventional-style commits:

- `chore:` for setup, tooling, and maintenance commands
- `feat:` for behavior students can observe
- `test:` for explicit test-focused commits
- `docs:` for workshop and local workflow documentation

Keep one learning goal per commit. If a task creates too much code for a live
segment, split it into "model", "route", "test", and "edge cases".

