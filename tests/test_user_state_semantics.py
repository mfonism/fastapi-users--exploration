import unittest
from datetime import datetime, timezone

from explore.auth.models import User


class TestUserStateSemantics(unittest.TestCase):
    def test_deactivated_at_drives_is_active(self) -> None:
        user = User(email="active@example.com", hashed_password="hash")
        self.assertTrue(user.is_active)
        self.assertIsNone(user.deactivated_at)

        user.is_active = False
        self.assertFalse(user.is_active)
        self.assertIsNotNone(user.deactivated_at)

        user.is_active = True
        self.assertTrue(user.is_active)
        self.assertIsNone(user.deactivated_at)

    def test_verified_at_drives_is_verified(self) -> None:
        user = User(email="verified@example.com", hashed_password="hash")
        self.assertFalse(user.is_verified)
        self.assertIsNone(user.verified_at)

        user.is_verified = True
        self.assertTrue(user.is_verified)
        self.assertIsNotNone(user.verified_at)

        user.is_verified = False
        self.assertFalse(user.is_verified)
        self.assertIsNone(user.verified_at)

    def test_superuser_granted_at_drives_is_superuser(self) -> None:
        user = User(email="super@example.com", hashed_password="hash")
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.superuser_granted_at)

        user.is_superuser = True
        self.assertTrue(user.is_superuser)
        self.assertIsNotNone(user.superuser_granted_at)

        user.is_superuser = False
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.superuser_granted_at)

    def test_terms_accepted_at_is_timestamp(self) -> None:
        user = User(email="terms@example.com", hashed_password="hash")
        self.assertIsNone(user.terms_accepted_at)

        accepted_at = datetime.now(timezone.utc)
        user.terms_accepted_at = accepted_at
        self.assertEqual(user.terms_accepted_at, accepted_at)

    def test_deleted_at_is_timestamp(self) -> None:
        user = User(email="deleted@example.com", hashed_password="hash")
        self.assertIsNone(user.deleted_at)

        deleted_at = datetime.now(timezone.utc)
        user.deleted_at = deleted_at
        self.assertEqual(user.deleted_at, deleted_at)


if __name__ == "__main__":
    unittest.main()
