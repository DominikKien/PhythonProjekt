#pylint: disable=C
import unittest
from unittest.mock import MagicMock
import sys
sys.path.append('../')
from source.passwordManager import PasswordManager  # Anpassen auf den tatsächlichen Pfad
from source.storage import Storage
from source.encryption import Encryption
from source.user import User


class TestPasswordManager(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_user = User(username="testuser", masterPassword="hashed_password")
        self.mock_encryption = MagicMock(Encryption)
        self.mock_storage = MagicMock(Storage)
        self.password_manager = PasswordManager(self.mock_user, storageFile='test_passwords.json')
        self.password_manager.encryption = self.mock_encryption
        self.password_manager.storage = self.mock_storage

    def test_existingAccountValid(self) -> None:
        self.mock_storage.getEntry.return_value = {"password": "verify"}
        self.assertTrue(self.password_manager.existingAccountValid())

        self.mock_storage.getEntry.return_value = {"password": "wrong"}
        self.assertFalse(self.password_manager.existingAccountValid())

    def test_newAccountValid(self) -> None:
        self.mock_storage.getAllEntryes.return_value = []
        self.mock_encryption.encrypt.return_value = "encrypted"
        self.assertTrue(self.password_manager.newAccountValid())

        self.mock_storage.getAllEntryes.return_value = ["existing"]
        self.assertFalse(self.password_manager.newAccountValid())

    def test_addEntry(self) -> None:
        self.mock_storage.getAllEntryes.return_value = []
        self.assertTrue(self.password_manager.addEntry(
            name="example", password="password123", url="http://example.com", notes="note", category="email"
        ))
        self.mock_encryption.encrypt.assert_called_with("password123")

        # Entry exists, expect False
        self.mock_storage.getAllEntryes.return_value = ["example"]
        self.assertFalse(self.password_manager.addEntry(
            name="example", password="password123", url="http://example.com"
        ))

    def test_getEntry(self) -> None:
        encrypted_data = {
            "name": "example",
            "password": "encrypted_password",
            "url": "encrypted_url",
            "notes": "encrypted_notes",
            "category": "encrypted_category",
            "created_at": "encrypted_created_at",
            "history": ["encrypted_old_password"]
        }
        self.mock_storage.getEntry.return_value = encrypted_data
        self.mock_encryption.decrypt.side_effect = [
            "password123", "2023-09-01T12:00:00", "http://example.com", "test note", "email", "old_password"
        ]
        
        entry = self.password_manager.getEntry("example")
        self.assertEqual(entry['password'], "password123")
        self.assertEqual(entry['created_at'], "2023-09-01T12:00:00")
        self.assertEqual(entry['url'], "http://example.com")

    def test_updateEntry(self) -> None:
        self.mock_encryption.encrypt.return_value = "encrypted_new_password"
        self.password_manager.updateEntry(name="example", newPassword="newpassword123")
        self.mock_storage.updatePassword.assert_called_with(
            username="testuser", name="example", newPassword="encrypted_new_password"
        )

    def test_deleteEntry(self) -> None:
        self.password_manager.deleteEntry(name="example")
        self.mock_storage.deletePassword.assert_called_with(username="testuser", name="example")

    def test_getAllEntryes(self) -> None:
        self.mock_storage.getAllEntryes.return_value = ["entry1", "entry2"]
        entries = self.password_manager.getAllEntryes()
        self.assertEqual(entries, ["entry1", "entry2"])


if __name__ == '__main__':
    unittest.main()
