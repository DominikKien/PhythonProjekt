import unittest
import curses
from unittest.mock import patch
from io import StringIO
from userInterface import Interface 

class TestInterface(unittest.TestCase):

    @patch('curses.wrapper')
    def test_start(self, mock_wrapper):
        interface = Interface()
        mock_wrapper.return_value = None
        interface.start()
        mock_wrapper.assert_called_once()

    @patch('curses.initscr')
    @patch('curses.noecho')
    @patch('curses.cbreak')
    @patch('curses.endwin')
    def test_main(self, mock_initscr, mock_noecho, mock_cbreak, mock_endwin):
        stdscr = mock_initscr.return_value
        stdscr.getkey.side_effect = ['\n', '\r', 'KEY_LEFT', 'KEY_RIGHT', 'KEY_UP', 'KEY_DOWN', 'q']
        
        interface = Interface()
        interface.main(stdscr)
        stdscr.keypad.assert_called_with(True)

    def test_showList(self):
        interface = Interface()
        stdscr = curses.initscr()
        interface.stdscr = stdscr
        length = interface.showList(layer=0)
        self.assertEqual(length, len(interface._allPages[0]))

    def test_extractData(self):
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
        self.assertEqual(interface._allPages[5][2], "user1")

    @patch('curses.initscr')
    def test_handleEnter(self, mock_initscr):
        stdscr = mock_initscr.return_value
        interface = Interface()
        interface.stdscr = stdscr
        interface.layer = 1
        interface.chooseRow = 7
        interface.createPassword1 = "pass1"
        interface.createPassword2 = "pass1"
        interface.userName = "user1"
        interface.handleEnter()
        self.assertEqual(interface.currentUser.username, "user1")

if __name__ == '__main__':
    unittest.main()
