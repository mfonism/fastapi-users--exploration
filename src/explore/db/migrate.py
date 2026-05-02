import argparse
import asyncio
import importlib
import os
import time

from alembic.config import Config

from alembic import command

from ..env import AppEnv

MigrationDirection = str


def parse_args(direction: MigrationDirection) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=f"{direction.title()} configured databases with Alembic.",
    )
    parser.add_argument(
        "--app-env",
        dest="app_envs",
        action="append",
        choices=[AppEnv.LOCAL.value, AppEnv.TEST.value],
        help=(
            "Apply only to the selected environment. "
            "Repeat to target multiple environments."
        ),
    )
    parser.add_argument(
        "--revision",
        default=None,
        help=(f"Alembic revision target. Defaults to '{default_revision(direction)}'."),
    )
    return parser.parse_args()


def alembic_command(direction: MigrationDirection):
    if direction == "upgrade":
        return command.upgrade
    if direction == "downgrade":
        return command.downgrade

    raise ValueError(f"Unsupported migration direction: {direction}")


def default_revision(direction: MigrationDirection) -> str:
    return "head" if direction == "upgrade" else "-1"


async def migrate_environment(
    app_env: AppEnv,
    direction: MigrationDirection,
    revision: str,
) -> float:
    os.environ["APP_ENV"] = app_env.value

    import explore.settings as settings_module

    settings_module = importlib.reload(settings_module)

    alembic_cfg = Config(settings_module.BASE_DIR / "alembic.ini")
    run_migration = alembic_command(direction)

    start = time.perf_counter()
    await asyncio.to_thread(run_migration, alembic_cfg, revision)
    end = time.perf_counter()

    return end - start


async def run_migrations(
    app_envs: list[AppEnv],
    direction: MigrationDirection,
    revision: str,
) -> None:
    seen: set[AppEnv] = set()

    for app_env in app_envs:
        if app_env in seen:
            continue

        elapsed = await migrate_environment(app_env, direction, revision)
        print(
            f"{app_env.value} database {direction}d to {revision} ✅ "
            f"(took {elapsed:.2f}s)"
        )
        seen.add(app_env)


def run(direction: MigrationDirection) -> None:
    args = parse_args(direction)
    app_envs = (
        [AppEnv(env) for env in args.app_envs]
        if args.app_envs
        else [AppEnv.LOCAL, AppEnv.TEST]
    )
    revision = args.revision or default_revision(direction)
    asyncio.run(run_migrations(app_envs, direction, revision))


def upgrade_main() -> None:
    run("upgrade")


def downgrade_main() -> None:
    run("downgrade")
