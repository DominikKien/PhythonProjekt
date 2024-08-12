# curses.beep() nicht gut, dass ich den Befehl gefunden habe
import curses
import csv
from user import User
from password_manager import PasswordManager

accounts = ["Choose an Account","Tim", "Justin", "Dominik"]



class Interface:
    def showList(self, layer:int) -> int:
        self._layer = layer
        self._stdscr.clear()
        currentPage = self._allPages[layer]
        length = len(currentPage)
        self._stdscr.addstr(0, 0, currentPage[0])
        for i in range(1, length):
            self._stdscr.addstr(i, 5, currentPage[i])
        self._stdscr.refresh()
        self._lastChooseRow = 1
        curses.curs_set(0)
        return length
    
    def showPlattformInfo(self, plattforms: list, offset:int) -> int:
        length = len(plattforms)
        for i in range(length):
            self._stdscr.addstr(i, offset, plattforms[i])
        self._stdscr.refresh()
        return length
            
    def openAccount(number:int) -> None:
        pass
    def __init__(self, accounts: list):
        print("I have been initialized")
        self._accounts = accounts
        self._layer = 0
        self._stdscr = None
        
        startPage = ["Welcome to Password Manager","Choose an Account", "Create an Account", "Close this application"]
        createAccountPage = ["Create your Account","Type your email","","Type your phonenumber","","Type your Password","","Create Account"]
        inputAccountPage = ["Input your Password for","","LogIn"]
        self._plattformPage = [["Error occured"],[self.createInfo]]
        self._allPages = [startPage, accounts, createAccountPage, inputAccountPage]
    
    
    def createInfo(self) -> list:
        password = "123212"
        note =""
        return [password, note]
    def noPlattform(self) ->bool:
        return False

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

        
        lengthOfPage = self.showList(layer = 0)
        typeMode = False
        email =""
        phonenumber=""
        password=""
        masterpassword=""
        controllpassword="MeineFresse"
        while True:
            chooseRow = self._lastChooseRow
            key = self._stdscr.getkey()
            #self._stdscr.addstr(6, 0, key)
            if(key == '\n' or key == '\r' or key == curses.KEY_ENTER ):#Enter
                if( 4>= self._layer >=2 and typeMode == False):#Eingabe Modus aktivieren
                    if(self._layer == 2 and chooseRow <= 7):
                        stdscr.keypad(False)
                        typeMode = True
                    elif(self._layer == 3 and 0<chooseRow<2):
                        stdscr.keypad(False)
                        typeMode = True
                        
                    elif(self._layer == 3 and chooseRow == 2):
                        if(masterpassword == controllpassword):
                            self._platform = [["Plattformen","Kategeorie Das da","Plattform1","Plattform2","Kategorie2","Plattform3"],
                                          [self.noPlattform(),self.noPlattform(), self.createInfo(), self.createInfo(), self.noPlattform,self.createInfo()]]
                            self.showPlattformInfo(self._platform[0], 4) 
                            lengthOfPage = len(self._platform[0])
                        else:
                            masterpassword =""
                elif(self._layer == 2 and typeMode == False and chooseRow ==7):#Account erstellen
                    self._stdscr.addstr(9, 0, email)
                    self._stdscr.addstr(10, 0, phonenumber)
                    self._stdscr.addstr(11, 0, password)
                elif(self._layer == 4 and typeMode == False):#Plattform auswählen
                    continue
                elif(4>= self._layer >=2 and typeMode == True): #Eingabemodus verlassen
                    stdscr.keypad(True)
                    typeMode = False
                
                
                        
                self._stdscr.addstr(lengthOfPage, 0, "Enter")
            elif(key == "KEY_UP"):#Up
                chooseRow = chooseRow - 1
            elif(key == "KEY_DOWN"):#Down
                chooseRow = chooseRow + 1
            elif(key == "KEY_LEFT"):#Left
                if 3 > self._layer >0:
                   lengthOfPage = self.showList(layer= 0)#Eine Seite zurück oder
                elif(self._layer == 3):
                    lengthOfPage = self.showList(layer= 1)#Eine Seite zurück oder
                else:
                    break#Schließen auf der ersten Seite Speichern der Daten Hier
            elif(key == "KEY_RIGHT"):#Right
                if(self._layer == 0):#Erste Page
                    if(chooseRow == 1):#Accounts zeigen
                        lengthOfPage = self.showList(layer = 1)
                    elif(chooseRow == 2):#Account erstellen
                        lengthOfPage = self.showList(layer= 2)
                    elif(chooseRow == 3):#Schließen Speichern der Daten Hier
                        break
                elif(self._layer == 1):#Account Auswählen
                    lengthOfPage = self.showList(layer = 3)
                elif(self._layer == 4):
                    if(self._platform[chooseRow] != False):
                        plattformInfo = self._platform[1][chooseRow]
                        self.showPlattform(plattformInfo, offset = 20 )#Zeige Ausgewählte PlatformInfo
                    else:
                        continue #Hier dann so Meldung, möchtest du eine neue Kategeorie einfügen oder einen Plattform verschieben

                    #AccountAuswahl mit Account Choose   
                #Der Ganze Rest der Tastatur dadrunter  
            elif(typeMode == True and self._layer == 2):#Account Erstelleingaben
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
                else:
                    self._stdscr.addstr(8, 0, "Here could be your Error Message for not knowing which specification have not been reached")
            elif(typeMode == True and self._layer == 3):#Master Passwort Eingabe
                if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        masterpassword = masterpassword[:-1]
                else:
                        masterpassword = masterpassword + key
                self._stdscr.addstr(1, 4, masterpassword+ "  ")
                
            
            self._stdscr.refresh()

            
                      
        
            if(chooseRow >lengthOfPage - 1):
                chooseRow = 1
            elif(chooseRow <1):
                chooseRow = lengthOfPage - 1
            
            self._stdscr.addstr(self._lastChooseRow, 0, "    ")
            self._stdscr.addstr(chooseRow, 0, "--->")
            curses.curs_set(0)
            self._lastChooseRow = chooseRow
        

        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
    


    
                
                

def main():
    interface = Interface(accounts=accounts)
    interface.start()
    ich = User("HI", "Ibins")
    passworman = PasswordManager(user=ich)
    print(passworman)

    

main()