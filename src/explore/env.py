from enum import StrEnum
from pathlib import Path


class AppEnv(StrEnum):
    LOCAL = "local"
    TEST = "test"
    STAGING = "staging"
    PRODUCTION = "production"


APP_ENV_ALIASES: dict[str, AppEnv] = {
    "local": AppEnv.LOCAL,
    "dev": AppEnv.LOCAL,
    "development": AppEnv.LOCAL,
    "test": AppEnv.TEST,
    "testing": AppEnv.TEST,
    "staging": AppEnv.STAGING,
    "stage": AppEnv.STAGING,
    "prod": AppEnv.PRODUCTION,
    "production": AppEnv.PRODUCTION,
}

APP_ENV_FILE_SUFFIX: dict[AppEnv, str] = {
    AppEnv.LOCAL: "local",
    AppEnv.TEST: "test",
    AppEnv.STAGING: "staging",
    AppEnv.PRODUCTION: "production",
}


def normalize_app_env(value: str | None) -> AppEnv:
    if value is None:
        return AppEnv.LOCAL

    normalized = value.strip().lower()
    try:
        return APP_ENV_ALIASES[normalized]
    except KeyError as exc:
        valid = ", ".join(sorted(APP_ENV_ALIASES.keys()))
        raise ValueError(f"Unsupported APP_ENV '{value}'. Use one of: {valid}") from exc


def resolve_env_files(app_env: AppEnv, base_dir: Path) -> tuple[Path, ...]:
    shared_file = base_dir / ".env"
    env_file = base_dir / f".env.{APP_ENV_FILE_SUFFIX[app_env]}"
    return tuple(path for path in (shared_file, env_file) if path.exists())
