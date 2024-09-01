import unittest
from unittest.mock import MagicMock, patch
import sys
sys.path.append('../')
from source.userInterface import Interface

class TestInterface(unittest.TestCase):
    def setUp(self) ->None:
        # Initialisieren des Interface-Objekts
        self.interface = Interface()
        self.interface.stdscr = MagicMock()
        self.interface.stdscr.getmaxyx = MagicMock(return_value=(20, 80))
        self.interface.stdscr.getkey = MagicMock(return_value='KEY_UP')

    def test_showList(self)->None:
        self.interface.stdscr.clear = MagicMock()
        self.interface.showList(layer=0)
        self.interface.stdscr.addstr.assert_called()

    def test_showList_with_empty_stdscr(self)->None:
        self.interface.stdscr = None
        with self.assertRaises(ValueError):
            self.interface.showList(layer=0)

    def test_handleEnter_account_creation(self)->None:
        # Simulieren der Bedingungen für Account-Erstellung
        self.interface.layer = 1
        self.interface.chooseRow = 7
        self.interface.createPassword1 = 'password123'
        self.interface.createPassword2 = 'password123'
        self.interface.userName = 'test_user'
        self.interface.passwordgenerator.containsEverything = MagicMock(return_value=True)
        self.interface.manager.newAccountValid = MagicMock(return_value=True)
        
        with patch('interface.User') as MockUser, patch('interface.PasswordManager') as MockPasswordManager:
            MockUser.return_value = MagicMock()
            MockPasswordManager.return_value = MagicMock()
            
            result = self.interface.handleEnter()
            self.assertTrue(result)
            MockUser.assert_called_with(username='test_user', masterPassword='password123')
            MockPasswordManager.assert_called_with(user=MockUser.return_value)

    def test_handleEnter_account_creation_fail(self) ->None:
        # Test für fehlgeschlagene Account-Erstellung
        self.interface.layer = 1
        self.interface.chooseRow = 7
        self.interface.createPassword1 = 'password123'
        self.interface.createPassword2 = 'password456'  # Passwords mismatch
        self.interface.userName = 'test_user'
        self.interface.passwordgenerator.containsEverything = MagicMock(return_value=True)
        
        result = self.interface.handleEnter()
        self.assertTrue(result)
        self.interface.stdscr.addstr.assert_called_with(1, 30, "Passwords don't match")

    def test_handleKeyRight(self)->None:
        self.interface.layer = 0
        self.interface.chooseRow = 1
        with patch('interface.PasswordManager') as MockPasswordManager:
            MockPasswordManager.return_value = MagicMock()
            self.interface.handleKeyRight()
            self.interface.showList.assert_called_with(layer=2)

    def test_handleKeyLeft(self)->None:
        self.interface.layer = 3
        self.interface.chooseRow = 1
        self.interface.handleKeyLeft()
        self.interface.showList.assert_called_with(layer=0)

    def test_importFile(self)->None:
        with patch('builtins.open', unittest.mock.mock_open(read_data="data")) as mock_file:
            self.interface.importFile()
            mock_file.assert_called_with("../importExport/topSecret.json", 'rb')

    def test_exportFile(self)->None:
        with patch('builtins.open', unittest.mock.mock_open(read_data="data")) as mock_file:
            self.interface.exportFile()
            mock_file.assert_called_with("passwords.json", 'rb')

    def test_verifyPassword(self)->None:
        self.interface.passwordgenerator.passwordSafety = MagicMock(return_value="Strong")
        self.interface.passwordgenerator.containsEverything = MagicMock(return_value=True)
        self.interface.createPassword1 = "password123"
        self.interface.verifyPassword()
        self.interface.stdscr.addstr.assert_any_call(6, 79, "Strong")
        self.interface.stdscr.addstr.assert_any_call(7, 81, "True")

    def test_handleTypemode(self)->None:
        # Implementieren eines Tests für handleTypemode (kann je nach Bedarf erweitert werden)
        self.interface.layer = 1
        self.interface.chooseRow = 1
        self.interface.key = 'a'
        self.interface.handleTypemode()
        self.interface.stdscr.addstr.assert_called_with(2, 4, 'a  ')

if __name__ == '__main__':
    unittest.main()
