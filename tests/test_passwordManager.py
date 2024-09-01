#pylint: disable=C
import unittest
from unittest.mock import MagicMock
import sys
sys.path.append('../')
from source.encryption import Encryption
from source.storage import Storage
from source.user import User
from source.passwordManager import PasswordManager

class TestPasswordManager(unittest.TestCase):

    def setUp(self) -> None:
        self.mock_user = User(username='testuser', masterPassword='testpass')
        self.mock_storage = MagicMock(Storage)
        self.mock_encryption = MagicMock(Encryption)
        self.manager = PasswordManager(user=self.mock_user, storageFile='test.json')
        self.manager.storage = self.mock_storage
        self.manager.encryption = self.mock_encryption

    def test_existingAccountValid(self) -> None:
        # Setup
        self.manager.getEntry = MagicMock(return_value={"password": "verify"})
        # Test
        self.assertTrue(self.manager.existingAccountValid())

    def test_newAccountValid(self) -> None:
        # Setup
        self.manager.getAllEntries = MagicMock(return_value=[])
        # Test
        self.assertTrue(self.manager.newAccountValid())
        self.manager.getAllEntries = MagicMock(return_value=["verify"])
        self.assertFalse(self.manager.newAccountValid())

    def test_addEntry(self) -> None:
        # Setup
        self.manager.getAllEntries = MagicMock(return_value=[])
        self.manager.encryption.encrypt = MagicMock(side_effect=lambda x: f"encrypted_{x}")
        # Test
        result = self.manager.addEntry("name", "password", "url", "notes", "category")
        self.assertTrue(result)
        self.manager.storage.addPassword.assert_called_once_with(
            username='testuser',
            name='name',
            password='encrypted_password',
            url='encrypted_url',
            notes='encrypted_notes',
            category='encrypted_category',
            datetime=MagicMock()  # Ensure datetime is properly mocked
        )

    def test_getEntry(self) -> None:
        # Setup
        self.manager.storage.getEntry = MagicMock(return_value={
            "password": "encrypted_password",
            "created_at": "encrypted_date",
            "url": "encrypted_url",
            "notes": "encrypted_notes",
            "category": "encrypted_category",
            "history": ["encrypted_history"]
        })
        self.manager.encryption.decrypt = MagicMock(side_effect=lambda x: x.replace("encrypted_", ""))
        # Test
        entry = self.manager.getEntry("name")
        self.assertEqual(entry['password'], 'password')
        self.assertEqual(entry['created_at'], 'date')
        self.assertEqual(entry['url'], 'url')
        self.assertEqual(entry['notes'], 'notes')
        self.assertEqual(entry['category'], 'category')
        self.assertEqual(entry['history'], ['history'])

    def test_updateEntry(self) -> None:
        # Setup
        self.manager.encryption.encrypt = MagicMock(return_value="encrypted_new_password")
        # Test
        self.manager.updateEntry("name", "new_password")
        self.manager.storage.updatePassword.assert_called_once_with(
            username='testuser',
            name='name',
            newPassword='encrypted_new_password'
        )

    def test_deleteEntry(self) -> None:
        # Test
        self.manager.deleteEntry("name")
        self.manager.storage.deletePassword.assert_called_once_with(
            username='testuser',
            name='name'
        )

    def test_getAllEntries(self) -> None:
        # Setup
        self.manager.storage.getAllEntryes = MagicMock(return_value=["entry1", "entry2"])
        # Test
        entries = self.manager.getAllEntries()
        self.assertEqual(entries, ["entry1", "entry2"])

    def test_getAllEntriesByUrl(self) -> None:
        # Setup
        self.manager.getAllEntries = MagicMock(return_value=["entry1"])
        self.manager.getEntry = MagicMock(return_value={"url": "http://example.com"})
        # Test
        entries = self.manager.getAllEntriesByUrl("example.com")
        self.assertEqual(entries, ["entry1"])

    def test_getAllEntriesByName(self) -> None:
        # Setup
        self.manager.getAllEntries = MagicMock(return_value=["entry1"])
        self.manager.getEntry = MagicMock(return_value={"name": "test_name"})
        # Test
        entries = self.manager.getAllEntriesByName("test_name")
        self.assertEqual(entries, ["entry1"])

if __name__ == '__main__':
    unittest.main()