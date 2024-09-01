#pylint: disable=C
import unittest
import os
import json
from storage import Storage  # type: ignore

class TestStorage(unittest.TestCase):

    def setUp(self) -> None:
        self.test_file = 'test_storage.json'
        with open(self.test_file, 'w', encoding="utf-8") as file:
            json.dump({}, file)
        self.storage = Storage(self.test_file)

    def tearDown(self) -> None:
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_loadData_empty_file(self) -> None:
        self.assertEqual(self.storage.data, {})

    def test_addPassword(self) -> None:
        self.storage.addPassword(
            username="testuser",
            name="example",
            password="password123",
            url="http://example.com",
            notes="test note",
            category="email",
            datetime="2023-09-01T12:00:00"
        )
        self.assertIn("testuser", self.storage.data)
        self.assertEqual(len(self.storage.data["testuser"]), 1)

    def test_getEntry(self) -> None:
        self.storage.addPassword(
            username="testuser",
            name="example",
            password="password123",
            url="http://example.com",
            notes="test note",
            category="email",
            datetime="2023-09-01T12:00:00"
        )
        entry = self.storage.getEntry("testuser", "example")
        self.assertEqual(entry["name"], "example")
        self.assertEqual(entry["password"], "password123")

    def test_getAllEntries(self) -> None:
        self.storage.addPassword(
            username="testuser",
            name="example1",
            password="password123",
            url="http://example.com",
            notes="test note",
            category="email",
            datetime="2023-09-01T12:00:00"
        )
        self.storage.addPassword(
            username="testuser",
            name="example2",
            password="password456",
            url="http://example2.com",
            notes="another note",
            category="social",
            datetime="2023-09-02T12:00:00"
        )
        entries = self.storage.getAllEntryes("testuser")
        self.assertEqual(entries, ["example1", "example2"])

    def test_updatePassword(self) -> None:
        self.storage.addPassword(
            username="testuser",
            name="example",
            password="password123",
            url="http://example.com",
            notes="test note",
            category="email",
            datetime="2023-09-01T12:00:00"
        )
        self.storage.updatePassword("testuser", "example", "newpassword123")
        entry = self.storage.getEntry("testuser", "example")
        self.assertEqual(entry["password"], "newpassword123")
        self.assertEqual(entry["history"], ["password123"])

    def test_deletePassword(self) -> None:
        self.storage.addPassword(
            username="testuser",
            name="example",
            password="password123",
            url="http://example.com",
            notes="test note",
            category="email",
            datetime="2023-09-01T12:00:00"
        )
        self.storage.deletePassword("testuser", "example")
        entry = self.storage.getEntry("testuser", "example")
        self.assertEqual(entry, {})

if __name__ == '__main__':
    unittest.main()
