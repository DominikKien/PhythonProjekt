#pylint: disable=C
import unittest
from hashlib import sha256
from user import User  # Anpassen auf den tatsächlichen Pfad


class TestUser(unittest.TestCase):
    def setUp(self) -> None:
        self.user = User(username="testuser", masterPassword="securepassword123")

    def test_init(self) -> None:
        expected_hash = sha256("securepassword123".encode()).hexdigest()
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.masterPasswordHash, expected_hash)

    def test_hashPassword(self) -> None:
        hashed_password = self.user.hashPassword("mypassword")
        expected_hash = sha256("mypassword".encode()).hexdigest()
        self.assertEqual(hashed_password, expected_hash)

    def test_setUsername(self) -> None:
        self.user.setUsername("newuser")
        self.assertEqual(self.user.username, "newuser")


if __name__ == '__main__':
    unittest.main()
