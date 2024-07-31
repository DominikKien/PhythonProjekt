import curses
import os
accounts = ["Tim", "Justin", "Dominik"]
from userInterface import Interface
from account import Account

class main():
    def __init__(self) -> None:
        interface = Interface(accounts=accounts)
    def run(self) -> None:
        Interface.showResponse
    def loadAccounts(self) -> None:
        pass
    def createAccount(self) -> None:
        pass
    

newMain: main = main()
main.run
print("This one is on")

"""
### curses.beep() nicht gut, dass ich den Befehl gefunden habe
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
        #self._LoginPage = ["Choose an Account", "Create an Account", "Close this application"]
        self._topLimit = 1
        self._bottomLimit = 0
        

    def showResponse(self):
        print("I'm Alive")

    def getData(self, data: list):
        self._data = data

    def getMasterPassword(self):
        print("Master Password Eingabe\n")
        return input()
    
    def reactPage(self, keyinput:int)->None:
        self._chooseLayer = self._topLimit
        self._lastChooseLayer = self._chooseLayer
        self._stdscr.refresh()
        if(keyinput == 1):
            self._chooseLayer = self._chooseLayer - 1
        elif(keyinput == 2):
            self._chooseLayer = self._chooseLayer + 1


        if(self._chooseLayer >self._topLimit):
            self._chooseLayer = 1
        elif(self._chooseLayer <1):
            self._chooseLayer = self._bottomLimit
        self._stdscr.addstr(self._lastChooseLayer, 0, "    ")
        self._stdscr.addstr(self._chooseLayer, 0, "--->")
        
        self._lastChooseLayer = self._chooseLayer

    def loadPages(self) -> None:
        self._LoginPage = {"Choose an Account" :showAccounts() , "Create an Account" :createAccounts(), "Close this application" : closeOperation()}
    def actionPages(self) -> None:
        pages =[showFirstPage(), showSecondPage()]
        actionNumber = 5
        pages(self._layer(actionNumber))
        def showFirstPage(self, actionNumber:int) ->None:
            def showAccounts(self) ->None:
                self._accounts = []
                self._stdscr.addstr(0, 5, "List of the Accounts")
                with open("Accounts.csv", mode='r', newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                for row in reader:
                    account = Account( row['email'], row['phonenumber'])
                    self._accounts.append(account)
                    self._stdscr.addstr(row + 1, 5, account.email)
                self._topLimit = 1
                self._bottomLimit = len(self._accounts)
                if(not self._accounts):
                    self._stdscr.addstr( 1, 5, "No Accounts found")

            def createAccounts(self) ->None:
                with open("Accounts.csv", mode='w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = [ 'email', 'phonenumber']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                for account in self._accounts:
                    writer.writerow({
                        'email': account.email,
                        'phonenumber': account.phonenumber
                    })
            def closeOperation(self) -> None:
                pass
            
        def showSecondPage():
            pass

    def start(self):
        print("Starting the interface...")
        curses.wrapper(self.main)

    def main(self, stdscr):
        self._stdscr = stdscr
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.clear()
        self._stdscr = None
        self._stdscr.addstr(0, 0, "Welcome to Password Manager.")
        self.loadPages(self._chooseLayer)
        self._stdscr.refresh()
        while True:
            key = self.handleKeyPress()
            self.reactPage()
            if key == 5:
                break

        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()

    def handleKeyPress(self) -> int:
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
        
        return keypressed

def main():
    interface = Interface(accounts=accounts)
    interface.showResponse()
    interface.getData(data)
    interface.start()

#main()

"""