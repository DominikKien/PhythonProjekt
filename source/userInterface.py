# curses.beep() nicht gut, dass ich den Befehl gefunden habe
import curses
import csv
#from account import Account

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
    """"
    def loadAccounts(self) -> None:
        self._accounts = [] # Accounts laden
        with open("source/Accounts.csv", mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                account = Account( row['email'], row['phonenumber'])
                self._accounts.append(account)
                self._stdscr.addstr(row + 1, 5, account.email)
                if(not self._accounts):

    def createAccounts(self, email: str, phonenumber: str ) ->None:
        print("I ran once")
        with open("source/Accounts.csv", mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [ 'email', 'phonenumber']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for account in self._accounts:
                writer.writerow({
                    'email': account.email,
                    'phonenumber': account.phonenumber
                    })
                    self._stdscr.addstr( 1, 5, "No Accounts found")"""""
    def showList(self, layer:int, heading:str) -> int:
        self._layer = layer
        self._stdscr.clear()
        self._stdscr.addstr(0, 0, heading)
        currentPage = self._allPages[layer]
        for i in range(len(currentPage)):
            self._stdscr.addstr(i + 1, 5, currentPage[i])
        self._stdscr.refresh()
        chooseRow = 0
        self._lastChooseRow = 1
        curses.curs_set(0)
        return len(currentPage)
    def showAccounts(self) -> None:
        pass
    def closepage(self) -> int:
        return 5
    def openAccount(number:int) -> None:
        pass
    def __init__(self, accounts: list):
        print("I have been initialized")
        self._accounts = accounts
        self._layer = 0
        self._stdscr = None
        self._email = ""
        self._phonenumber = ""

        loginPage = ["Choose an Account", "Create an Account", "Close this application"]
        self._headings = ["Welcome to Password Manager", "Choose an Account", "Create an Account"]
        actionLoginPage = [self.showAccounts(),self.showResponse, self.closepage()]
        #actionLoginPage = [self.showAccounts(),self.createAccounts(self._email, self._phonenumber), self.closepage()]
        self._allPages = [loginPage, accounts]
    

    def showResponse(self): 
        curses.beep()

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

        
        lengthOfPage = self.showList(layer = 0, heading = self._headings[0])
        while True:
            chooseRow = self._lastChooseRow
            key = self.handleKeyPress()
            if(key == 1):#Up
                chooseRow = chooseRow - 1
            elif(key == 2):#Down
                chooseRow = chooseRow + 1
            elif(key == 3 and self._layer >0):#Left
                self.showList(layer= self._layer - 1, heading= self._headings[self._layer - 1])
            elif(key == 4):#Rigtht
                if(self._layer == 0):#Erste Page
                    if(chooseRow == 1):#Accounts zeigen
                        self.showList(layer = 1,heading=self._headings[1])
                    elif(chooseRow == 2):
                        pass
                    elif(chooseRow == 3):
                        key = self.closepage()
                      
            if(key == 5): #Speichern der Daten Hier
                break
            if(chooseRow >lengthOfPage):
                chooseRow = 1
            elif(chooseRow <1):
                chooseRow = lengthOfPage
            self._stdscr.addstr(self._lastChooseRow, 0, "    ")
            self._stdscr.addstr(chooseRow, 0, "--->")
            curses.curs_set(0)
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
    


    
                
                

def main():
    interface = Interface(accounts=accounts)
    #interface.showResponse()
    interface.getData(data)
    interface.start()

    

main()