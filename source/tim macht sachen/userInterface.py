"""Modul für Ein- und Ausgabe über Terminal"""
import curses
from typing import List, Dict, Optional
from user import User
from password_manager import PasswordManager
from passwordGenerator import PasswordGenerator
from twoFactorAuth import TwoFactorAuth


class Interface:
    """
    Diese Klasse erstellt eine GUI für einen PasswordManager
    """
    def __init__(self) -> None:
        self.layer: int = 0
        self.stdscr: curses.window
        self._lastChooseRow: int = 1
        self.passwordgenerator: PasswordGenerator = PasswordGenerator(6)
        self.entryNumber:int
        self.height:int = -2

        self.chooseRow = 1
        self.lengthOfPage = 0
        self.key = ''
        self.currentUser = User(username="", master_password="")
        self.manager = PasswordManager(self.currentUser)

        self.typeMode = False
        self.userName = ""
        self.createPassword1 = ""
        self.createPassword2 = ""
        self.masterpassword = ""

        self.entry: Dict[str, str] = {
            "username": "username",
            "password": "Mein Passwort",
            "url": "irgenwie Google",
            "notes": "Leere Notiz",
            "category": "category Schwarzwaelderkirsch",
            "created_at": "Heute halt",
            "history": ["gestern","heute","morgen"]
        }

        self.plattform: List[str] = ["Netflix", "Instagram", "Kategorie 2", "MyLittlePony"]
        self.isCategory: List[bool] = [False, False, True, False]

        startPage: List[str] = ["Welcome to Password Manager", "Choose an Account", "Create an Account",  "Close this application"]
        createAccountPage: List[str] = ["Create your Account", "Type your Username", "", "Type your password", "",
                                         "Type your Password again", "", "Create Account", "Generate password"]
        loginAccountPage: List[str] = ["Log into your Account", "Type your Username", "", "Type your password", "", "LogIn"]
        currentAccountPage: List[str] = ["", "Create a new Entry"]
        newEntryPage: List[str] = ["New Entry", "Type your Name for the plattform", "", "Type the url", "", "Assign a category",
                                    "", "Type the password", "", "Might want to add a short Note?", "", "Save"]
        showPlattformPage: List[str] = ["Entry", "Name of the plattform", "", "url:", "", "category", "", "password", "", "note", "", "Save", "last edit", ""]
        self._allPages: List[List[str]] = [startPage, createAccountPage, loginAccountPage, currentAccountPage, newEntryPage, showPlattformPage]

    def showList(self, layer: int) -> int:
        """Gibt die Länge der ausgewählten Liste zurück und zeigt die Ausgewählte Liste im Terminal an"""
        self.layer = layer
        if self.stdscr is None:
            raise ValueError("_stdscr is not initialized.")
        self.stdscr.clear()
        currentPage = self._allPages[layer]
        self.stdscr.addstr(0, 0, currentPage[0])
        for i in range(1, len(currentPage)):
            if i == self.height:
                self.stdscr.addstr(0, 50, "Please extend your terminal in height")
                return i
            self.stdscr.addstr(i, 5, currentPage[i])
            
        self.stdscr.refresh()
        self._lastChooseRow = 1
        curses.curs_set(0)
        return i
    
    def showEntry(self, entry:int, create: bool, height: int) -> int:
        dataList = self._allPages[5]
        key:int
        if(not create):
            self.extractData(self.entry)
        for key, value in dataList.items():
            self.stdscr.addstr(key, 20, value)

            # Möglichkeit zur Modifikation des Eintrags
            if isinstance(value, list):
                # Wenn der Wert eine Liste ist
                for i, item in enumerate(value):
                    self.stdscr.addstr(key + i, 20, item)
        return key
                    
        


    def extractData(self, data: Dict[str, str]) -> None:
        """Fügt die Daten in der richtigen Liste hinzu"""
        dataList = self._allPages[5]
        dataList[2] = data["username"] #Wurde geändert
        dataList[4] = data["url"]
        dataList[6] = data["category"]
        dataList[8] = data["password"]
        dataList[10] = data["notes"]
        dataList.extend(data["history"])
        self._allPages[5] = dataList

    def openAccount(self, username: str, password: str) -> PasswordManager:
        currentUser = User(username=username, master_password=password)
        passwordManager = PasswordManager(currentUser)
        return passwordManager

    def handleEnter(self) ->bool:
        """Kümmert sich um die Eingabe der Enter Taste
        return Wert kann bei False andere Handle Taste aufrufen, Multikeyput"""
        if 4 >= self.layer >= 1 and not self.typeMode:  # Enter ohne Schreibmodus aktiviert
            if self.layer == 1 and self.chooseRow < 7:  # Account Erstelleingabe
                self.stdscr.keypad(False)
                self.typeMode = True
                return True
            elif self.layer == 1 and self.chooseRow == 7:  # Account erstellen
                self.stdscr.move(1, 30)
                self.stdscr.clrtoeol()
                if self.createPassword1 != self.createPassword2:  # Verifikation der Daten
                    self.stdscr.addstr(1, 30, "Passwords don't match")
                    return True
                elif self.userName == "":
                    self.stdscr.addstr(1, 30, "No Username given")
                    return True
                elif not self.passwordgenerator.containsEverything(self.createPassword1):
                    self.stdscr.addstr(1, 30, "Criteria not completed")
                    return True
                else:
                    self.stdscr.addstr(1, 30, "Account erstellt")
                    self.currentUser = User(username=self.userName, master_password=self.createPassword1)  # Account erstellt
                    self._allPages[3][0] = self.userName
                    self._allPages[3].extend(self.plattform)
                    self.lengthOfPage = self.showList(3)
                    return True
            elif self.layer == 1 and self.chooseRow == 8:
                self.createPassword1 = self.passwordgenerator.generate()
                self.createPassword2 = self.createPassword1
                self.stdscr.move(4, 4)
                self.stdscr.clrtoeol()
                self.stdscr.addstr(4, 4, self.createPassword2 + "  ")
                self.stdscr.move(6, 4)
                self.stdscr.clrtoeol()
                self.stdscr.addstr(6, 4, self.createPassword2 + "  ")
                return True
            elif self.layer == 2 and 0 < self.chooseRow < 5:  # Einloggen Eingabe
                self.stdscr.keypad(False)
                self.typeMode = True
                return True
            elif self.layer == 2 and self.chooseRow == 5:  # Account öffnen
                self.stdscr.addstr(1, 30, "Account öffnen")
                self.manager = self.openAccount(username=self.userName, password=self.masterpassword)
                return True
        elif 4 >= self.layer >= 1 and self.typeMode:  # Eingabemodus verlassen
            self.stdscr.keypad(True)
            self.typeMode = False
            return True
        return False
            

    def handleKeyRight(self)->bool:
        """Kümmert sich um Pfeiltaste Rechts Eingabe"""
        if self.layer == 0:  # Erste Page
            if self.chooseRow == 1:  # Einloggen
                self.lengthOfPage = self.showList(layer=2)
            elif self.chooseRow == 2:  # Account erstellen
                self.lengthOfPage = self.showList(layer=1)
            elif self.chooseRow == 3:  # Schließen Speichern der Daten Hier
                return True
            elif self.layer == 3:
                if self.chooseRow == 4:#Eintrag erstellen hier
                    print("Hier fehlt noch was")                    
        elif self.layer == 3 and self.lengthOfPage>= self.chooseRow >0:
            self.extractData(self.entry)
            self.lengthOfPage = self.showList(5) #Plattform anzeigen 
        elif self.layer == 5:
            if(self.lengthOfPage >=self.chooseRow > 0):
                self.entryNumber = 0
                self.showEntry(entry=self.entryNumber, create=False)
            
        return False
    def handleKeyLeft(self)->bool:
        """Kümmer sich um Pfeiltaste Links Eingabe"""
        if 3 > self.layer > 0:
            self.userName = ""
            self.lengthOfPage = self.showList(layer=0)  # Eine Seite zurück
        elif self.layer == 3:
            self.lengthOfPage = self.showList(layer=1)  # Eine Seite zurück
            # Hier auch noch Account schließen
        elif 5 <= self.layer >= 4:
            self.lengthOfPage = self.showList(layer=3)  # Eine Seite zurück
        else:
            return True  # Schließen auf der ersten Seite Speichern der Daten Hier
        return False

    def verifyPassword(self)->None:
        """Verifiziert sein Passwort auf Stärke, Benutzer Zeichensatz
            und Wie oft die ersten 5 Hashwerte gepawned wurden
            beim Account erstellen"""
        self.stdscr.addstr(5, 30, self.createPassword1)
        self.stdscr.addstr(6, 30, "Strength:")
        self.stdscr.move(6, 39)
        self.stdscr.clrtoeol()#Befehl zum restliochen Zeileninhalt löschen
        self.stdscr.addstr(6, 39, self.passwordgenerator.passwordSafety(self.createPassword1))
        self.stdscr.addstr(7, 30, "Criterias:")
        self.stdscr.addstr(7, 40, str(self.passwordgenerator.containsEverything(self.createPassword1)))

    def handleTypemode(self)->None:
        """"Kümmert sich um die Eingabe, Aufruf nur wenn Schreibmodus aktiviert ist"""
        checkPassword = False
        if  self.layer == 1:  # Account Erstelleingaben
            checkPassword = self.accountCreation()
        elif self.layer == 2:  # Login Eingabe
            if self.chooseRow in (1, 2):
                if self.key in( '\b','\x7f',curses.KEY_BACKSPACE):
                    self.userName = self.userName[:-1]
                else:
                    self.userName += self.key
                self.stdscr.addstr(2, 4, self.userName + "  ")
            elif self.chooseRow in (3, 4):
                if self.key in('\b','\x7f', curses.KEY_BACKSPACE) :
                    self.masterpassword = self.masterpassword[:-1]
                else:
                    self.masterpassword += self.key
                self.stdscr.addstr(4, 4, self.masterpassword + "  ")
        if checkPassword:
            self.verifyPassword()

    def accountCreation(self)->bool:
        """"Eingabe der Accountdaten"""
        checkPassword = False
        if self.chooseRow in (1, 2):  # Username eingabe
            if self.key in ('\b','\x7f',curses.KEY_BACKSPACE):
                self.userName = self.userName[:-1]
            elif len(self.key) == 1 and 32 <= ord(self.key) <= 126:
                self.userName += self.key
            self.stdscr.addstr(2, 4, self.userName + "  ")
        elif self.chooseRow in (3, 4):  # password1
            if self.key in('\b','\x7f',curses.KEY_BACKSPACE):
                self.createPassword1 = self.createPassword1[:-1]
                checkPassword = True
            elif len(self.key) == 1 and 32 <= ord(self.key) <= 126:
                self.createPassword1 += self.key
                checkPassword = True
            self.stdscr.addstr(4, 4, self.createPassword1 + "  ")
        elif self.chooseRow in (5, 6):  # Password 2
            if self.key in('\b','\x7f',curses.KEY_BACKSPACE) :
                self.createPassword2 = self.createPassword2[:-1]
            elif len(self.key) == 1 and 32 <= ord(self.key) <= 126:
                self.createPassword2 += self.key
            self.stdscr.addstr(6, 4, self.createPassword2 + "  ")
        return checkPassword


    def start(self) -> None:
        """Startet das GUI"""
        curses.wrapper(self.main)

    def main(self, stdscr: curses.window) -> None:
        """Wird von start aufgerufen, kümmert sich um die Reaktion auf Tastendrücke"""
        self.stdscr = stdscr
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        stdscr.clear()
        self.height, width = self.stdscr.getmaxyx()
        oldheight:int = -2
        while True:
            self.height, width = self.stdscr.getmaxyx()
            if(oldheight != self.height):
                self.lengthOfPage = self.showList(self.layer)
                if(self.layer == 5):
                    self.showEntry(self.entryNumber, False)
                elif(self.layer == 4):
                    self.showEntry(self.entrynumber, True)
            oldheight = self.height
            #self.chooseRow = self._lastChooseRow
            if self.chooseRow is None:
                self.chooseRow = 1
            self.key = self.stdscr.getkey()
            # self._stdscr.addstr(6, 0, key)
            if self.key in ('\n', '\r', curses.KEY_ENTER):  # Enter
                if( not self.handleEnter()):
                    self.handleKeyRight()
            elif self.key == "KEY_UP":  # Up
                self.chooseRow -= 1
            elif self.key == "KEY_DOWN":  # Down
                self.chooseRow += 1
            elif self.key == "KEY_LEFT":    # Left
                if self.handleKeyLeft():
                    break
            elif self.key == "KEY_RIGHT":  # Right
                if self.handleKeyRight():
                    break

            # Der Ganze Rest der Tastatur dadrunter
            elif self.typeMode:
                self.handleTypemode()

            if self.chooseRow > self.lengthOfPage - 1:
                self.chooseRow = 1
            elif self.chooseRow < 1:
                self.chooseRow = self.lengthOfPage - 1

            self.stdscr.addstr(self._lastChooseRow, 0, "    ")
            self.stdscr.addstr(self.chooseRow, 0, "--->")
           #self.stdscr.addstr(5, 0, str(self.layer))
            curses.curs_set(0)
            self._lastChooseRow = self.chooseRow
            self.stdscr.refresh()

        curses.nocbreak()
        #stdscr.keypad(False)
        curses.echo()
        

def main() -> None:
    interface = Interface()
    interface.start()


main()
