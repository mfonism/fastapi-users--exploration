import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pydantic import SecretStr

from explore.config import AppEnv, normalize_app_env, resolve_env_files
from explore.settings import Settings


class TestSettings(unittest.TestCase):
    def test_normalize_app_env_aliases(self) -> None:
        self.assertEqual(normalize_app_env("dev"), AppEnv.LOCAL)
        self.assertEqual(normalize_app_env("testing"), AppEnv.TEST)
        self.assertEqual(normalize_app_env("stage"), AppEnv.STAGING)
        self.assertEqual(normalize_app_env("prod"), AppEnv.PRODUCTION)

    def test_resolve_env_files_prefers_shared_then_specific(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            (base_dir / ".env").write_text("DEBUG=false\n", encoding="utf-8")
            (base_dir / ".env.staging").write_text("DEBUG=true\n", encoding="utf-8")

            env_files = resolve_env_files(AppEnv.STAGING, base_dir)
            self.assertEqual(
                env_files,
                (base_dir / ".env", base_dir / ".env.staging"),
            )

    def test_debug_default_depends_on_environment(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            local_settings = Settings(app_env=AppEnv.LOCAL)
            staging_settings = Settings(app_env=AppEnv.STAGING)

            self.assertTrue(local_settings.debug)
            self.assertFalse(staging_settings.debug)

    def test_environment_variables_override_env_files(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            base_dir = Path(temp_dir)
            env_file = base_dir / ".env.local"
            env_file.write_text(
                "AUTH_REDIS_URL=redis://localhost:6379/1\n",
                encoding="utf-8",
            )

            with patch.dict(
                os.environ,
                {
                    "AUTH_REDIS_URL": "redis://localhost:6379/7",
                },
                clear=False,
            ):
                settings = Settings(
                    _env_file=str(env_file),
                    app_env=AppEnv.LOCAL,
                )

            self.assertEqual(settings.auth_redis_url, "redis://localhost:6379/7")

    def test_database_url_is_built_from_parts(self) -> None:
        settings = Settings(
            db_driver="postgresql+asyncpg",
            db_host="db.internal",
            db_port=5433,
            db_user="app_user",
            db_password=SecretStr("s3cret"),
            db_name="explore_app",
        )
        self.assertEqual(
            settings.core_db_url,
            "postgresql+asyncpg://app_user:s3cret@db.internal:5433/explore_app",
        )


if __name__ == "__main__":
    unittest.main()
