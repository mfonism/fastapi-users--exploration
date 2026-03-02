import unittest

from explore.db.config import is_postgres_server_version_compatible


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


if __name__ == "__main__":
    unittest.main()
