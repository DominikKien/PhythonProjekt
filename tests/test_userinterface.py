#pylint: disable=C
import unittest
import curses
from unittest.mock import patch, Mock
import sys

# Den Pfad anpassen, falls notwendig
sys.path.append('../')
from source.userInterface import Interface


class TestInterface(unittest.TestCase):

    @staticmethod
    @patch('curses.wrapper')
    def test_start(mock_wrapper: Mock) -> None:
        interface = Interface()
        mock_wrapper.return_value = None
        interface.start()
        mock_wrapper.assert_called_once()

    @staticmethod
    @patch('curses.initscr')
    @patch('curses.noecho')
    @patch('curses.cbreak')
    @patch('curses.endwin')
    def test_main(mock_initscr: Mock) -> None:
        stdscr = mock_initscr.return_value
        stdscr.getkey.side_effect = ['\n', '\r', 'KEY_LEFT', 'KEY_RIGHT',
                                      'KEY_UP', 'KEY_DOWN', 'q']

        interface = Interface()
        interface.main(stdscr)
        stdscr.keypad.assert_called_with(True)

    def test_showList(self) -> None:
        interface = Interface()
        stdscr = curses.initscr()
        interface.stdscr = stdscr
        length = interface.showList(layer=0)
        self.assertEqual(length, len(interface.allPages[0]))

    def test_extractData(self) -> None:
        interface = Interface()
        data = {
            "username": "user1",
            "password": "pass1",
            "url": "http://example.com",
            "notes": "note",
            "category": "category1",
            "created_at": "Heute",
            "history": ["gestern", "heute", "morgen"]
        }
        interface.extractData(data)
        self.assertEqual(interface.allPages[5][2], "user1")

    @patch('curses.initscr')
    def test_handleEnter(self, mock_initscr: Mock) -> None:
        stdscr = mock_initscr.return_value
        interface = Interface()
        interface.stdscr = stdscr
        interface.layer = 1
        interface.chooseRow = 7
        interface.createPassword1 = "pass1"
        interface.createPassword2 = "pass1"
        interface.userName = "user1"
        interface.handleEnter()
        self.assertIsNotNone(interface.currentUser)
        self.assertEqual(interface.currentUser.username, "user1")


if __name__ == '__main__':
    unittest.main()
