import unittest

from sqlalchemy.engine import URL

from explore.config import AppEnv
from explore.db.config import (
    is_local_or_test_env,
    is_postgres_server_version_compatible,
)


class TestDbConfig(unittest.TestCase):
    def test_postgres_version_compatible_for_matching_major_minor(self) -> None:
        self.assertTrue(is_postgres_server_version_compatible("18.3", "18.3"))
        self.assertTrue(
            is_postgres_server_version_compatible(
                "PostgreSQL 18.3 (Debian 18.3-1.pgdg)",
                "18.3",
            )
        )
        self.assertTrue(is_postgres_server_version_compatible("18.3.2", "18.3"))

    def test_postgres_version_incompatible_for_non_matching_major_minor(self) -> None:
        self.assertFalse(is_postgres_server_version_compatible("18.2", "18.3"))
        self.assertFalse(is_postgres_server_version_compatible("17.9", "18.3"))

    def test_postgres_version_incompatible_for_unparseable_input(self) -> None:
        self.assertFalse(is_postgres_server_version_compatible("release", "18.3"))
        self.assertFalse(is_postgres_server_version_compatible("18.3", "release"))
        self.assertFalse(is_postgres_server_version_compatible("18.3", "18"))

    def test_role_ownership_management_is_limited_to_local_and_test(self) -> None:
        self.assertTrue(is_local_or_test_env(AppEnv.LOCAL))
        self.assertTrue(is_local_or_test_env(AppEnv.TEST))
        self.assertFalse(is_local_or_test_env(AppEnv.STAGING))
        self.assertFalse(is_local_or_test_env(AppEnv.PRODUCTION))

    def test_admin_db_url_uses_plain_postgresql_driver_for_psycopg(self) -> None:
        # override settings object in module to control values
        from types import SimpleNamespace

        fake = SimpleNamespace(
            db_user="user+name",
            db_password=SimpleNamespace(get_secret_value=lambda: "p@ss word"),
            db_driver="postgresql+asyncpg",
            db_host="host",
            db_port=5432,
        )
        # assign into config module
        import explore.db.config as cfg

        cfg.settings = fake
        url = cfg.get_admin_db_url()
        self.assertIsInstance(url, URL)
        self.assertEqual(url.drivername, "postgresql")
        self.assertEqual(url.username, "user+name")
        self.assertEqual(url.password, "p@ss word")
        self.assertEqual(url.host, "host")
        self.assertEqual(url.port, 5432)
        self.assertEqual(url.database, "postgres")

    def test_engine_and_session_maker_are_cached(self) -> None:
        import explore.db.config as cfg

        e1 = cfg.get_engine()
        e2 = cfg.get_engine()
        self.assertIs(e1, e2)
        m1 = cfg.get_async_session_maker()
        m2 = cfg.get_async_session_maker()
        self.assertIs(m1, m2)


if __name__ == "__main__":
    unittest.main()
