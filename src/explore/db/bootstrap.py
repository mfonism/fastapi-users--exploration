import argparse
import asyncio
import importlib
import os
import time

from alembic.config import Config

from alembic import command

from ..env import AppEnv


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create and migrate the configured databases.",
    )
    parser.add_argument(
        "--app-env",
        dest="app_envs",
        action="append",
        choices=[AppEnv.LOCAL.value, AppEnv.TEST.value],
        help=(
            "Bootstrap only the selected environment. "
            "Repeat to bootstrap multiple environments."
        ),
    )
    return parser.parse_args()


async def bootstrap_environment(app_env: AppEnv) -> float:
    os.environ["APP_ENV"] = app_env.value

    import explore.db.config as db_config
    import explore.settings as settings_module

    settings_module = importlib.reload(settings_module)
    db_config = importlib.reload(db_config)

    alembic_cfg = Config(settings_module.BASE_DIR / "alembic.ini")

    start = time.perf_counter()
    await db_config.ensure_database()
    await asyncio.to_thread(command.upgrade, alembic_cfg, "head")
    end = time.perf_counter()

    return end - start


async def run_bootstrap(app_envs: list[AppEnv]) -> None:
    seen: set[AppEnv] = set()

    for app_env in app_envs:
        if app_env in seen:
            continue

        elapsed = await bootstrap_environment(app_env)
        print(
            f"{app_env.value} database is ready and migrated ✅ (took {elapsed:.2f}s)"
        )
        seen.add(app_env)


def main() -> None:
    args = parse_args()
    app_envs = (
        [AppEnv(env) for env in args.app_envs]
        if args.app_envs
        else [AppEnv.LOCAL, AppEnv.TEST]
    )
    asyncio.run(run_bootstrap(app_envs))
