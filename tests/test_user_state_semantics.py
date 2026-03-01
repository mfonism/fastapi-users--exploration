import unittest

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


if __name__ == "__main__":
    unittest.main()
