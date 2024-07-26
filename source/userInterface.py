# curses.beep() nicht gut, dass ich den Befehl gefunden habe
import curses

accounts = ["Tim", "Justin", "Dominik"]

data = [
    {
        "category": "category1",
        "plattform": "Netflix",
        "password": "HAHAHA1234_Ü",
        "note 1": "Das Password ist falsch"
    },
    {
        "category": "category1",
        "plattform": "LeagueOfLegends",
        "password": "Kinderpasswort!!_.ÄÖ",
        "note 1": "Das Password ist falsch"
    }
]

class Interface:
    def __init__(self, accounts: list):
        print("I have been initialized")
        self._accounts = accounts
        self._layer = 0
        self._LoginPage = ["Choose an Account", "Create an Account", "Close this application"]
        self._stdscr = None

    def showResponse(self):
        print("I'm Alive")

    def getData(self, data: list):
        self._data = data

    def getMasterPassword(self):
        print("Master Password Eingabe\n")
        return input()

    def start(self):
        print("Starting the interface...")
        curses.wrapper(self.main)

    def main(self, stdscr):
        self._stdscr = stdscr
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.clear()

        self._stdscr.addstr(0, 0, "Welcome to Password Manager.")
        for i in range(len(self._LoginPage)):
            self._stdscr.addstr(i + 1, 5, self._LoginPage[i])
        self._stdscr.refresh()
        self._chooseLayer = 1
        self._lastChooseLayer = self._chooseLayer
        while True:
            key = self.handleKeyPress()
            if key == 5:
                break

        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()

    def handleKeyPress(self):
        keypressed = 0
        key = self._stdscr.getch()

        if key == curses.KEY_UP:
            curses.beep()
            keypressed = 1
            self._chooseLayer = self._chooseLayer - 1
            self._stdscr.addstr(5, 0, "Pfeiltaste oben gedrückt.   ")
        elif key == curses.KEY_DOWN:
            keypressed = 2
            self._chooseLayer = self._chooseLayer + 1
            self._stdscr.addstr(5, 0, "Pfeiltaste unten gedrückt.  ")
        elif key == curses.KEY_LEFT:
            keypressed = 3
            self._stdscr.addstr(5, 0, "Pfeiltaste links gedrückt.  ")
        elif key == curses.KEY_RIGHT:
            keypressed = 4
            self._stdscr.addstr(5, 0, "Pfeiltaste rechts gedrückt. ")
        elif key == ord('q'):
            keypressed = 5
            self._stdscr.addstr(5, 0, "Q gedrückt.  ")
        
        self._stdscr.refresh()
        if(self._chooseLayer >len(self._LoginPage)):
            self._chooseLayer = 1
        elif(self._chooseLayer <1):
            self._chooseLayer = len(self._LoginPage)
        self._stdscr.addstr(self._lastChooseLayer, 0, "    ")
        self._stdscr.addstr(self._chooseLayer, 0, "--->")
        
        self._lastChooseLayer = self._chooseLayer

        

        return keypressed

def main():
    interface = Interface(accounts=accounts)
    interface.showResponse()
    interface.getData(data)
    interface.start()

main()


    