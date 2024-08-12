# curses.beep() nicht gut, dass ich den Befehl gefunden habe
import curses
import csv
from user import User
from password_manager import PasswordManager
from passwordGenerator import PasswordGenerator

accounts = ["Choose an Account","Tim", "Justin", "Dominik"]



class Interface:    
    def __init__(self, accounts: list):
        print("I have been initialized")
        self._accounts = accounts
        self._layer = 0
        self._stdscr = None
        self.passwordgenerator = PasswordGenerator(6)
        
        
        startPage = ["Welcome to Password Manager","Choose an Account", "Create an Account", "Close this application"]                                          #0
        createAccountPage = ["Create your Account","Type your Username","","Type your password","","Type your Password again","","Create Account"]              #1
        LoginAccountPage = ["Log into your Account","Type your Username","","Type your password","","LogIn"]                                                    #2
        currentAccountPage = ["","Create a new Entry","Search per Name or URL for the plattform","","Search"]                                                   #3
        newEntryPage =["New Entry","Type your Name for the plattform","","Type the url","","Assign a category","","Type the password","", "might want to add a short Note?","","Save"] #4
        showPlattformPage =["Entry","Name of the plattform","","url:","","category","","password","", "Note","","Save","last edit",""]                          #5
        self._allPages = [startPage, createAccountPage, LoginAccountPage, currentAccountPage, newEntryPage, showPlattformPage]
    
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
    
    def openAccount(self, username:str, password:str) -> PasswordManager:
        currentUser = User(username=username, master_password=password)
        passwordManager = PasswordManager(currentUser)
        return passwordManager
    
    def getData(self, data: list):
        self._data = data

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
        userName =""
        createPassword1=""
        createPassword2=""
        masterpassword=""
        while True:
            chooseRow = self._lastChooseRow
            key = self._stdscr.getkey()
            #self._stdscr.addstr(6, 0, key)
            if(key == '\n' or key == '\r' or key == curses.KEY_ENTER ):#Enter
                if( 4>= self._layer >=1 and typeMode == False):#Enter ohne Schreibmodus aktiviert
                    if(self._layer == 1 and chooseRow < 7):#Account Erstelleeingabe
                        stdscr.keypad(False)
                        typeMode = True
                    elif(self._layer == 1 and chooseRow ==7):#Account erstellen
                        if(createPassword1 != createPassword2):
                            self._stdscr.addstr(1, 30, "Passwords dont match")
                        else:
                            lengthOfPage = self.showList(4)
                    elif(self._layer == 2 and 0<chooseRow<5):#Einloggen Eingabe
                        stdscr.keypad(False)
                        typeMode = True
                    elif(self._layer == 2 and chooseRow == 5):#Account öffnen
                        self._stdscr.addstr(1, 30, "Account öffnen")
                        manager = self.openAccount(username=userName, password=masterpassword)
                elif(4>= self._layer >=1 and typeMode == True): #Eingabemodus verlassen
                    stdscr.keypad(True)
                    typeMode = False
                else:
                    key = "KEY_RIGHT"
            elif(key == "KEY_UP"):#Up
                chooseRow = chooseRow - 1
            elif(key == "KEY_DOWN"):#Down
                chooseRow = chooseRow + 1
            elif(key == "KEY_LEFT"):#Left
                if 3 > self._layer >0:
                   userName =""
                   lengthOfPage = self.showList(layer= 0)#Eine Seite zurück
                elif(self._layer == 3):
                    lengthOfPage = self.showList(layer= 1)#Eine Seite zurück
                    #Hier auch noch Account schließen
                elif(5 <= self._layer >=4):
                    lengthOfPage = self.showList(layer= 3)#Eine Seite zurück
                else:
                    break#Schließen auf der ersten Seite Speichern der Daten Hier

            elif(key == "KEY_RIGHT"):#Right
                if(self._layer == 0):#Erste Page
                    if(chooseRow == 1):#Einloggen
                        lengthOfPage = self.showList(layer = 2)
                    elif(chooseRow == 2):#Account erstellen
                        lengthOfPage = self.showList(layer= 1)
                    elif(chooseRow == 3):#Schließen Speichern der Daten Hier
                        break
                elif(self._layer == 4):
                    continue

                #Der Ganze Rest der Tastatur dadrunter
            elif(typeMode == True and self._layer == 1):#Account Erstelleingaben
                if((chooseRow == 1 or chooseRow == 2) ):#Username eingabe
                    if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        userName = userName[:-1]
                    elif len(key) == 1 and 32 <= ord(key) <= 126:
                        userName = userName + key
                    self._stdscr.addstr(2, 4, userName + "  ")
                elif(chooseRow == 3 or chooseRow == 4):#password1
                    if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        createPassword1 = createPassword1[:-1]
                    elif len(key) == 1 and 32 <= ord(key) <= 126:
                        createPassword1 = createPassword1 + key
                    self._stdscr.addstr(4, 4, createPassword1+ "  ")
                elif(chooseRow == 5 or chooseRow == 6):#Password 2
                    if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        createPassword2 = createPassword2[:-1]
                    elif len(key) == 1 and 32 <= ord(key) <= 126:
                        createPassword2 = createPassword2 + key
                    self._stdscr.addstr(6, 4, createPassword2+ "  ")
            elif(typeMode == True and self._layer == 2):#Login Eingabe
                self._stdscr.addstr(6, 4, "Da sind mer")
                if(chooseRow == 1 or chooseRow == 2):
                    if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        userName = userName[:-1]
                    else:
                        userName = userName + key
                    self._stdscr.addstr(2, 4, userName+ "  ")
                elif(chooseRow == 3 or chooseRow == 4):
                    if(key == '\b' or key == '\x7f' or key == curses.KEY_BACKSPACE):
                        masterpassword = masterpassword[:-1]
                    else:
                        masterpassword = masterpassword + key
                self._stdscr.addstr(4, 4, masterpassword+ "  ")             
            
                    
              
            self._stdscr.refresh()
            if(chooseRow >lengthOfPage - 1):
                chooseRow = 1
            elif(chooseRow <1):
                chooseRow = lengthOfPage - 1

            if(self._layer ==4 or self._layer ==5):
                self._stdscr.addstr(6, 20, "Strength:")
                self._stdscr.addstr(6, 29, self.passwordgenerator.passwordSafety(createPassword1))
                self._stdscr.addstr(7, 20, "Criterias:")
                self._stdscr.addstr(7, 30, self.passwordgenerator.containsEverything(createPassword1))
            
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