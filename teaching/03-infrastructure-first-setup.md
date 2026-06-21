# Infrastructure-First Setup

The first section of the workshop should make the project runnable, testable,
and easy to change before adding many features.

## Recommended Early Order

| Step | Why It Comes Early |
|---|---|
| Project scaffolding | Students need an importable package and repeatable commands. |
| FastAPI health endpoint | Gives immediate feedback that the app runs. |
| Ruff and pre-commit | Establishes formatting before many files exist. |
| Environment helpers | Prevents hardcoded local-only behavior. |
| Pydantic settings | Centralizes DB, Redis, and secret configuration. |
| Async DB helpers | Required before models, migrations, and tests. |
| Alembic setup | Teaches schema management before feature tables grow. |
| DB bootstrap commands | Reduces setup friction for local and test DBs. |
| Test fixtures | Gives students a safe feedback loop for endpoint work. |
| Basic smoke test | Confirms the full toolchain works. |

## Local Setup Script For Students

These commands should be in the student handout after the first few setup
tasks are complete:

```bash
uv sync
cp .env.example .env
uv run db-bootstrap
uv run pytest
uv run fastapi dev src/explore/app.py
```

Optional local services:

```bash
docker run --rm --name explore-postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 postgres:18.3
docker run --rm --name explore-redis -p 6379:6379 redis:7-alpine
```

## Files Created During Infrastructure Setup

| Task | Files |
|---|---|
| Scaffolding | `.python-version`, `.gitignore`, `pyproject.toml`, `README.md`, `src/explore/__init__.py` |
| Health app | `src/explore/app.py` |
| Tooling | `.pre-commit-config.yaml`, `pyproject.toml` |
| Environment | `src/explore/env.py`, `.env.example` |
| Settings | `src/explore/settings.py`, `tests/test_settings.py` |
| Database | `src/explore/db/base.py`, `src/explore/db/config.py` |
| Alembic | `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`, `src/explore/db/registry.py` |
| DB commands | `src/explore/db/bootstrap.py`, `src/explore/db/migrate.py`, `src/explore/console.py` |
| Migration guard | `scripts/check_empty_migrations.py`, `.pre-commit-config.yaml` |

## Smoke Test Goals

At the end of the infrastructure block, students should be able to:

- run `uv sync`
- run `uv run ruff check .`
- run `uv run ruff format .`
- start FastAPI locally
- call `/health`
- load settings from `.env`
- connect to PostgreSQL
- run Alembic against the configured DB
- run a minimal pytest test

## Teaching Advice

Keep the infrastructure block explicit but not too long. Beginners need to see
why each piece exists, but the workshop momentum should move toward features as
soon as the feedback loop works.

Good checkpoint question:

> If we change the DB name in `.env`, which object in code eventually sees that
> value?

Good simplification:

> Provide the DB bootstrap command as starter code if the group is new to
> PostgreSQL administration. Teach migrations separately from role/database
> ownership.

