import pytest
from unittest.mock import MagicMock
from interface import Interface
from user import User
from passwordManager import PasswordManager
from passwordGenerator import PasswordGenerator

# Dummy-Setup für curses
@pytest.fixture
def mock_curses():
    curses = MagicMock()
    curses.window = MagicMock()
    curses.KEY_BACKSPACE = 127
    return curses

@pytest.fixture
def interface(mock_curses):
    interface = Interface()
    interface.stdscr = mock_curses.window
    interface.passwordgenerator = PasswordGenerator(6)
    interface.manager = MagicMock(spec=PasswordManager)
    interface.currentUser = MagicMock(spec=User)
    return interface

def test_show_list(interface, mock_curses):
    mock_curses.window.addstr = MagicMock()
    length = interface.showList(0)
    assert length > 0
    mock_curses.window.addstr.assert_called()  # Verifizieren, dass addstr aufgerufen wurde

def test_show_entry(interface, mock_curses):
    mock_curses.window.addstr = MagicMock()
    length = interface.showEntry(create=True, height=20)
    assert length > 0
    mock_curses.window.addstr.assert_called()

def test_extract_data(interface):
    data = {
        "name": "test_name",
        "url": "http://example.com",
        "category": "test_category",
        "password": "test_password",
        "notes": "test_notes",
        "created_at": "2024-09-01",
        "history": ["change1", "change2"]
    }
    result = interface.extractData(data)
    assert result[2] == "test_name"
    assert interface.entryName == "test_name"

def test_open_account(interface):
    user = User(username="test_user", masterPassword="test_password")
    manager = interface.openAccount("test_user", "test_password")
    assert manager.currentUser.username == user.username

def test_handle_enter(interface, mock_curses):
    interface.layer = 1
    interface.chooseRow = 7
    interface.createPassword1 = "password1"
    interface.createPassword2 = "password1"
    interface.userName = "test_user"
    interface.passwordgenerator.containsEverything = MagicMock(return_value=True)
    interface.manager.newAccountValid = MagicMock(return_value=True)
    result = interface.handleEnter()
    assert result is True
    mock_curses.window.addstr.assert_called()

def test_handle_key_right(interface, mock_curses):
    interface.layer = 0
    interface.chooseRow = 1
    interface.showList = MagicMock(return_value=5)
    result = interface.handleKeyRight()
    assert result is False
    interface.showList.assert_called()

def test_handle_key_left(interface):
    interface.layer = 2
    interface.showList = MagicMock(return_value=5)
    result = interface.handleKeyLeft()
    assert result is False
    interface.showList.assert_called()

def test_handle_typemode(interface, mock_curses):
    interface.layer = 1
    interface.chooseRow = 1
    interface.key = 'a'
    interface.typeMode = True
    interface.handleTypemode()
    assert interface.userName == 'a'
    mock_curses.window.addstr.assert_called()

def test_account_creation(interface, mock_curses):
    interface.layer = 1
    interface.chooseRow = 1
    interface.key = 'a'
    result = interface.accountCreation()
    assert result is False
    assert interface.userName == 'a'
    mock_curses.window.addstr.assert_called()

# Weitere Tests für alle Methoden der Interface Klasse
