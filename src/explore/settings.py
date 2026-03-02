import os
from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from .config import AppEnv, normalize_app_env, resolve_env_files

BASE_DIR = Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    app_env: AppEnv = AppEnv.LOCAL
    debug: bool | None = None

    data_dir: Path | None = None
    core_db_url: str | None = None
    auth_redis_url: str = "redis://localhost:6379/0"

    reset_password_token_secret: SecretStr = SecretStr(
        "EXPLORE: RESET PASSWORD TOKEN SECRET"
    )
    verification_token_secret: SecretStr = SecretStr("EXPLORE: VERIFICATION TOKEN SECRET")

    model_config = SettingsConfigDict(
        env_file=None,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug_value(cls, value: object) -> bool | None:
        if value is None:
            return None

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            normalized = value.strip().lower()
            if normalized == "":
                return None
            if normalized in {"1", "true", "t", "yes", "y", "on", "debug", "dev"}:
                return True
            if normalized in {"0", "false", "f", "no", "n", "off", "release"}:
                return False

        raise ValueError("DEBUG must be a boolean-like value")

    @model_validator(mode="after")
    def finalize(self) -> "Settings":
        if self.debug is None:
            self.debug = self.app_env in {AppEnv.LOCAL, AppEnv.TEST}

        if self.data_dir is None:
            self.data_dir = BASE_DIR / ".data"
        self.data_dir.mkdir(exist_ok=True)

        if self.core_db_url is None:
            self.core_db_url = f"sqlite+aiosqlite:///{self.data_dir / 'db.sqlite'}"

        return self


@lru_cache
def get_settings() -> Settings:
    app_env = normalize_app_env(os.getenv("APP_ENV"))
    env_files = resolve_env_files(app_env, BASE_DIR)
    env_file_arg: str | tuple[str, ...] | None
    if not env_files:
        env_file_arg = None
    elif len(env_files) == 1:
        env_file_arg = str(env_files[0])
    else:
        env_file_arg = tuple(str(path) for path in env_files)

    return Settings(
        _env_file=env_file_arg,
        app_env=app_env,
    )
