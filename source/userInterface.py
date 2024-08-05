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
        self._lastChooseRow = 1
        curses.curs_set(0)
        return len(currentPage)
    def addString(self, previousText:str) ->str:
        pass
    def showAccounts(self) -> None:
        pass
    def openAccount(number:int) -> None:
        pass
    def __init__(self, accounts: list):
        print("I have been initialized")
        self._accounts = accounts
        self._layer = 0
        self._stdscr = None
        createAccountPage = ["Type your email","","Type your phonenumber","","Type your Password","","Create Account"]
        loginPage = ["Choose an Account", "Create an Account", "Close this application"]
        self._headings = ["Welcome to Password Manager", "Choose an Account", "Create an Account"]
        actionLoginPage = [self.showAccounts(),self.showResponse]
        self._allPages = [loginPage, accounts, createAccountPage]
    

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
        typeMode = False
        email =""
        phonenumber=""
        password=""
        while True:
            chooseRow = self._lastChooseRow
            key = self._stdscr.getkey()
            #self._stdscr.addstr(6, 0, key)
            if(key == '\n' or key == '\r' or key == curses.KEY_ENTER):#Enter
                if(self._layer == 2 and typeMode == False and chooseRow <7):#Eingabe Modus für Account erstellen
                    stdscr.keypad(False)
                    typeMode = True
                elif(self._layer == 2 and typeMode == True): #Eingabemodus verlassen
                    stdscr.keypad(True)
                    typeMode = False
                elif(self._layer == 2 and typeMode == False and chooseRow ==7):#Account erstellen
                    pass
                        
                self._stdscr.addstr(lengthOfPage, 0, "Enter")
            elif(key == "KEY_UP"):#Up
                chooseRow = chooseRow - 1
            elif(key == "KEY_DOWN"):#Down
                chooseRow = chooseRow + 1
            elif(key == "KEY_LEFT"):#Left
                if self._layer >0:
                   lengthOfPage = self.showList(layer= self._layer - 1, heading= self._headings[self._layer - 1])#Eine Seite zurück oder
                else:
                    break#Schließen auf der ersten Seite Speichern der Daten Hier
            elif(key == "KEY_RIGHT"):#Right
                if(self._layer == 0):#Erste Page
                    if(chooseRow == 1):#Accounts zeigen
                        lengthOfPage = self.showList(layer = 1,heading=self._headings[1])
                    elif(chooseRow == 2):#Account erstellen
                        lengthOfPage = self.showList(layer= 2, heading= self._headings[2])
                    elif(chooseRow == 3):#Schließen Speichern der Daten Hier
                        break
            elif(typeMode == True):
                if((chooseRow == 1 or chooseRow == 2) ):#Email Eingabe
                    if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        email = email[:-1]
                    elif len(key) == 1 and 32 <= ord(key) <= 126:
                        email = email + key
                    self._stdscr.addstr(2, 4, email + "  ")
                elif(chooseRow == 3 or chooseRow == 4):#Telefonummer
                    if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        phonenumber = phonenumber[:-1]
                    elif len(key) == 1 and 32 <= ord(key) <= 126:
                        phonenumber = phonenumber + key
                    self._stdscr.addstr(4, 4, phonenumber+ "  ")
                elif(chooseRow == 5 or chooseRow == 6):#Passwort
                    if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        password = password[:-1]
                    elif len(key) == 1 and 32 <= ord(key) <= 126:
                        password = password + key
                    self._stdscr.addstr(6, 4, password+ "  ")

            
                      
        
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
    


    
                
                

def main():
    interface = Interface(accounts=accounts)
    #interface.showResponse()
    interface.getData(data)
    interface.start()

    

main()