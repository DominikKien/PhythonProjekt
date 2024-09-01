import unittest
from unittest.mock import MagicMock, patch
import sys

sys.path.append('../')
from source.userInterface import Interface

class TestInterface(unittest.TestCase):

    def setUp(self) -> None:
        # Initialize Interface object
        self.interface = Interface()
        self.interface.stdscr = MagicMock()
        self.interface.stdscr.getmaxyx = MagicMock(return_value=(20, 80))
        self.interface.stdscr.getkey = MagicMock(return_value='KEY_UP')

    def test_showList(self) -> None:
        # Call the method under test
        self.interface.showList(layer=0)

        # Check that clear was called
        self.interface.stdscr.clear.assert_called_once()

        # Check that addstr was called
        self.interface.stdscr.addstr.assert_called()

    def test_showList_with_empty_stdscr(self) -> None:
        # Simulate an empty stdscr
        self.interface.stdscr = None
        with self.assertRaises(AttributeError):
            self.interface.showList(layer=0)

    def test_handleEnter_account_creation(self) -> None:
        # Simulate conditions for account creation
        self.interface.layer = 1
        self.interface.chooseRow = 7
        self.interface.createPassword1 = 'password123'
        self.interface.createPassword2 = 'password123'
        self.interface.userName = 'test_user'
        self.interface.passwordgenerator.containsEverything = MagicMock(return_value=True)
        self.interface.manager.newAccountValid = MagicMock(return_value=True)

        with patch('source.userInterface.User') as MockUser, patch('source.userInterface.PasswordManager') as MockPasswordManager:
            MockUser.return_value = MagicMock()
            MockPasswordManager.return_value = MagicMock()

            result = self.interface.handleEnter()
            self.assertTrue(result)
            MockUser.assert_called_with(username='test_user', masterPassword='password123')
            MockPasswordManager.assert_called_with(user=MockUser.return_value)

    def test_handleEnter_account_creation_fail(self) -> None:
        # Test for failed account creation
        self.interface.layer = 1
        self.interface.chooseRow = 7
        self.interface.createPassword1 = 'password123'
        self.interface.createPassword2 = 'password456'  # Passwords mismatch
        self.interface.userName = 'test_user'
        self.interface.passwordgenerator.containsEverything = MagicMock(return_value=True)

        result = self.interface.handleEnter()
        self.assertFalse(result)
        self.interface.stdscr.addstr.assert_called_with(1, 30, "Passwords don't match")

    def test_handleKeyRight(self) -> None:
        self.interface.layer = 0
        self.interface.chooseRow = 1
        with patch('source.userInterface.PasswordManager') as MockPasswordManager:
            MockPasswordManager.return_value = MagicMock()
            self.interface.handleKeyRight()
            self.interface.showList.assert_called_with(layer=2)

    def test_handleKeyLeft(self) -> None:
        self.interface.layer = 3
        self.interface.chooseRow = 1
        self.interface.handleKeyLeft()
        self.interface.showList.assert_called_with(layer=0)

    def test_importFile(self) -> None:
        with patch('builtins.open', unittest.mock.mock_open(read_data="data")) as mock_file:
            self.interface.importFile()
            mock_file.assert_called_with("../importExport/topSecret.json", 'rb')

    def test_exportFile(self) -> None:
        with patch('builtins.open', unittest.mock.mock_open(read_data="data")) as mock_file:
            self.interface.exportFile()
            mock_file.assert_called_with("passwords.json", 'wb')

    def test_verifyPassword(self) -> None:
        self.interface.passwordgenerator.passwordSafety = MagicMock(return_value="Strong")
        self.interface.passwordgenerator.containsEverything = MagicMock(return_value=True)
        self.interface.createPassword1 = "password123"
        self.interface.verifyPassword()
        self.interface.stdscr.addstr.assert_any_call(6, 79, "Strong")
        self.interface.stdscr.addstr.assert_any_call(7, 81, "True")

    def test_handleTypemode(self) -> None:
        # Implement a test for handleTypemode
        self.interface.layer = 1
        self.interface.chooseRow = 1
        self.interface.key = 'a'
        self.interface.handleTypemode()
        self.interface.stdscr.addstr.assert_called_with(2, 4, 'a  ')

if __name__ == '__main__':
    unittest.main()
