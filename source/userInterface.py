# curses.beep() nicht gut, dass ich den Befehl gefunden habe
import curses
import csv
from account import Account

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
        self._stdscr = None
        loginPage = ["Choose an Account", "Create an Account", "Close this application"]
        actionLoginPage = [showAccounts(), createAccounts(), closepage()]
        def showAccounts(self) -> None:
            pass
        def createAccounts(self) -> None:
            pass
        def closepage(self) -> None:
            pass

        self._showPages = [loginPage]

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
        currentPage = self._showPages[self._layer]
        for i in range(len(currentPage)):
            self._stdscr.addstr(i + 1, 5, currentPage[i])
        self._stdscr.refresh()
        chooseRow = 1
        self._lastChooseRow = chooseRow

        self._accounts = [] # Accounts laden
        self._stdscr.addstr(0, 5, "List of the Accounts")
        with open("Accounts.csv", mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                account = Account( row['email'], row['phonenumber'])
                self._accounts.append(account)
                self._stdscr.addstr(row + 1, 5, account.email)
                if(not self._accounts):
                    self._stdscr.addstr( 1, 5, "No Accounts found")

        while True:
            chooseRow = self._lastChooseRow
            key = self.handleKeyPress()
            if(key == 1):
                chooseRow = chooseRow - 1
            elif(key == 2):
                chooseRow = chooseRow + 1
            elif(key == 3):
                pass
            elif(key == 4):
                if(self._layer == 0 and chooseRow == 1):#Account auswählen
                    pass      
            elif(key == 5): #Speichern der Daten Hier
                break

            if(chooseRow >len(currentPage)):
                chooseRow = 1
            elif(chooseRow <1):
                chooseRow = len(currentPage)
            self._stdscr.addstr(self._lastChooseRow, 0, "    ")
            self._stdscr.addstr(chooseRow, 0, "--->")
            self._lastChooseRow = chooseRow
        

        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()

    def handleKeyPress(self):
        keypressed = 0
        key = self._stdscr.getch()

        if key == curses.KEY_UP:
            curses.beep()
            keypressed = 1
            self._stdscr.addstr(5, 0, "Pfeiltaste oben gedrückt.   ")
        elif key == curses.KEY_DOWN:
            keypressed = 2
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
        return keypressed
    


    def createAccounts(self, email: str, phonenumber: str ) ->None:
        with open("Accounts.csv", mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [ 'email', 'phonenumber']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in self._accounts:
                writer.writerow({
                    'email': account.email,
                    'phonenumber': account.phonenumber
                    })

def main():
    interface = Interface(accounts=accounts)
    interface.showResponse()
    interface.getData(data)
    interface.start()

main()