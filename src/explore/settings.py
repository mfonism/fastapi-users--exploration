import os
from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL

from .config import AppEnv, normalize_app_env, resolve_env_files

BASE_DIR = Path(__file__).parent.parent.resolve()


class Settings(BaseSettings):
    app_env: AppEnv = AppEnv.LOCAL
    debug: bool | None = None

    db_driver: str = "postgresql+asyncpg"
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: SecretStr = SecretStr("postgres")
    db_base_name: str = "explore"

    auth_redis_url: str = "redis://localhost:6379/0"
    redis_key_prefix_base: str = "explore_auth_tokens"

    reset_password_token_secret: SecretStr = SecretStr(
        "EXPLORE: RESET PASSWORD TOKEN SECRET"
    )
    verification_token_secret: SecretStr = SecretStr(
        "EXPLORE: VERIFICATION TOKEN SECRET"
    )

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

        return self

    @property
    def database_name(self) -> str:
        if self.app_env == AppEnv.TEST:
            return f"{self.db_base_name}_test"
        return self.db_base_name

    @property
    def redis_key_prefix(self) -> str:
        if self.app_env == AppEnv.TEST:
            return f"{self.redis_key_prefix_base}_test:"
        return f"{self.redis_key_prefix_base}:"

    @property
    def core_db_url(self) -> URL:
        return URL.create(
            drivername=self.db_driver,
            username=self.db_user,
            password=self.db_password.get_secret_value(),
            host=self.db_host,
            port=self.db_port,
            database=self.database_name,
        )


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
